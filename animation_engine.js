/**
 * Universal Animation Engine
 * Parses structured JSON and creates animations dynamically
 */

class AnimationEngine {
    constructor(containerId, canvasId) {
        this.containerId = containerId;
        this.canvasId = canvasId;
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.actors = {};
        this.animations = [];
        this.currentTime = 0;
        this.isPlaying = false;
        this.loop = true;
        this.duration = 10;
    }

    // Initialize the 3D scene
    initScene(width = 800, height = 600) {
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(75, width/height, 0.1, 1000);
        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.renderer.setSize(width, height);
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        
        const container = document.getElementById(this.containerId);
        if (container) {
            container.appendChild(this.renderer.domElement);
        }

        // Default lighting
        const ambientLight = new THREE.AmbientLight(0x404040, 0.4);
        this.scene.add(ambientLight);
        
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.6);
        directionalLight.position.set(5, 5, 5);
        directionalLight.castShadow = true;
        this.scene.add(directionalLight);
    }

    // Create actor from JSON definition
    createActor(actorDef) {
        let mesh;
        const { id, type, radius = 1, color = '#ffffff', position = [0,0,0] } = actorDef;

        switch (type) {
            case 'sphere':
                const sphereGeometry = new THREE.SphereGeometry(radius, 32, 32);
                const sphereMaterial = new THREE.MeshLambertMaterial({ 
                    color: color,
                    transparent: actorDef.opacity < 1,
                    opacity: actorDef.opacity || 1
                });
                
                if (actorDef.emissive) {
                    sphereMaterial.emissive = new THREE.Color(actorDef.emissive);
                    sphereMaterial.emissiveIntensity = 0.3;
                }
                
                mesh = new THREE.Mesh(sphereGeometry, sphereMaterial);
                break;

            case 'cube':
                const cubeGeometry = new THREE.BoxGeometry(radius, radius, radius);
                const cubeMaterial = new THREE.MeshLambertMaterial({ color: color });
                mesh = new THREE.Mesh(cubeGeometry, cubeMaterial);
                break;

            case 'cylinder':
                const cylGeometry = new THREE.CylinderGeometry(radius, radius, actorDef.height || 2);
                const cylMaterial = new THREE.MeshLambertMaterial({ color: color });
                mesh = new THREE.Mesh(cylGeometry, cylMaterial);
                break;

            case 'plane':
                const planeGeometry = new THREE.PlaneGeometry(actorDef.width || 2, actorDef.height || 2);
                const planeMaterial = new THREE.MeshLambertMaterial({ color: color });
                mesh = new THREE.Mesh(planeGeometry, planeMaterial);
                break;

            case 'line':
                const points = actorDef.points || [[0,0,0], [1,1,1]];
                const lineGeometry = new THREE.BufferGeometry().setFromPoints(
                    points.map(p => new THREE.Vector3(...p))
                );
                const lineMaterial = new THREE.LineBasicMaterial({ color: color });
                mesh = new THREE.Line(lineGeometry, lineMaterial);
                break;

            case 'particle_system':
                mesh = this.createParticleSystem(actorDef);
                break;

            default:
                console.warn(`Unknown actor type: ${type}`);
                mesh = new THREE.Object3D(); // Empty object
        }

        mesh.position.set(...position);
        if (actorDef.rotation) {
            mesh.rotation.set(...actorDef.rotation.map(r => r * Math.PI / 180));
        }
        if (actorDef.scale) {
            mesh.scale.set(...actorDef.scale);
        }

        // Store additional properties
        mesh.userData = { ...actorDef };
        
        this.scene.add(mesh);
        this.actors[id] = mesh;
        
        return mesh;
    }

    createParticleSystem(actorDef) {
        const count = actorDef.count || 100;
        const geometry = new THREE.BufferGeometry();
        const positions = new Float32Array(count * 3);
        const colors = new Float32Array(count * 3);
        
        const color = new THREE.Color(actorDef.color);
        
        for (let i = 0; i < count; i++) {
            positions[i * 3] = (Math.random() - 0.5) * 10;
            positions[i * 3 + 1] = (Math.random() - 0.5) * 10;
            positions[i * 3 + 2] = (Math.random() - 0.5) * 10;
            
            colors[i * 3] = color.r;
            colors[i * 3 + 1] = color.g;
            colors[i * 3 + 2] = color.b;
        }
        
        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
        
        const material = new THREE.PointsMaterial({
            size: actorDef.particle_size || 0.1,
            vertexColors: true
        });
        
        return new THREE.Points(geometry, material);
    }

    // Load animation from JSON
    loadAnimation(animationData) {
        this.duration = animationData.duration || 10;
        this.loop = animationData.loop !== false;
        
        // Create actors
        animationData.actors.forEach(actorDef => {
            this.createActor(actorDef);
        });

        // Set up camera
        if (animationData.camera) {
            const cam = animationData.camera;
            this.camera.position.set(...cam.position);
            this.camera.lookAt(...cam.target);
            this.camera.fov = cam.fov || 75;
            this.camera.updateProjectionMatrix();
        } else {
            this.camera.position.set(5, 5, 5);
            this.camera.lookAt(0, 0, 0);
        }

        // Process timeline events
        this.animations = animationData.timeline || [];
        
        // Store annotations
        this.annotations = animationData.annotations || [];
        
        return this;
    }

    // Update animation at given time
    updateAnimation(time) {
        this.currentTime = time;
        
        // Process timeline events
        this.animations.forEach(event => {
            if (time >= event.time && time <= (event.time + (event.duration || 1))) {
                const progress = (time - event.time) / (event.duration || 1);
                const easedProgress = this.applyEasing(progress, event.easing || 'linear');
                
                // Apply properties to actors
                Object.entries(event.properties).forEach(([key, value]) => {
                    this.applyProperty(key, value, easedProgress);
                });
            }
        });
        
        // Handle special cases like orbits
        this.updateOrbits(time);
        this.updateParticleSystems(time);
    }

    applyProperty(key, value, progress) {
        const [actorId, property] = key.split('_');
        const actor = this.actors[actorId];
        
        if (!actor) return;
        
        switch (property) {
            case 'orbit':
                const angle = value * progress * Math.PI / 180;
                const radius = actor.userData.orbit_radius || 3;
                actor.position.x = Math.cos(angle) * radius;
                actor.position.z = Math.sin(angle) * radius;
                break;
                
            case 'rotation':
                actor.rotation.y = value * progress * Math.PI / 180;
                break;
                
            case 'position':
                if (Array.isArray(value)) {
                    actor.position.set(...value.map(v => v * progress));
                }
                break;
        }
    }

    updateOrbits(time) {
        Object.values(this.actors).forEach(actor => {
            const userData = actor.userData;
            if (userData.orbit_radius && userData.orbit_speed) {
                const angle = time * userData.orbit_speed;
                actor.position.x = Math.cos(angle) * userData.orbit_radius;
                actor.position.z = Math.sin(angle) * userData.orbit_radius;
            }
        });
    }

    updateParticleSystems(time) {
        // Update particle positions, flows, etc.
        // Implementation depends on specific particle behaviors
    }

    applyEasing(t, type) {
        switch (type) {
            case 'ease-in': return t * t;
            case 'ease-out': return t * (2 - t);
            case 'ease-in-out': return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
            default: return t; // linear
        }
    }

    // Animation playback
    play() {
        this.isPlaying = true;
        this.animate();
    }

    pause() {
        this.isPlaying = false;
    }

    animate() {
        if (!this.isPlaying) return;
        
        requestAnimationFrame(() => this.animate());
        
        // Update time
        this.currentTime += 0.016; // ~60fps
        
        if (this.currentTime > this.duration) {
            if (this.loop) {
                this.currentTime = 0;
            } else {
                this.pause();
                return;
            }
        }
        
        this.updateAnimation(this.currentTime);
        this.updateAnnotations(this.currentTime);
        this.renderer.render(this.scene, this.camera);
    }

    updateAnnotations(time) {
        // Show/hide annotations based on current time
        this.annotations.forEach((annotation, index) => {
            const annotationEl = document.getElementById(`annotation-${index}`);
            if (annotationEl) {
                const showTime = annotation.time;
                const hideTime = showTime + (annotation.duration || 3);
                
                if (time >= showTime && time <= hideTime) {
                    annotationEl.style.display = 'block';
                    annotationEl.style.opacity = Math.min(1, (time - showTime) * 2);
                } else {
                    annotationEl.style.display = 'none';
                }
            }
        });
    }

    // Create annotation elements
    createAnnotationElements() {
        const container = document.getElementById(this.containerId);
        this.annotations.forEach((annotation, index) => {
            const el = document.createElement('div');
            el.id = `annotation-${index}`;
            el.className = 'animation-annotation';
            el.textContent = annotation.text;
            el.style.cssText = `
                position: absolute;
                background: rgba(0,0,0,0.8);
                color: white;
                padding: 10px;
                border-radius: 5px;
                display: none;
                z-index: 100;
                ${annotation.position ? 
                    `top: ${annotation.position[1]}px; left: ${annotation.position[0]}px;` : 
                    `bottom: 20px; left: 20px;`}
            `;
            container.appendChild(el);
        });
    }
}

// Global function to create animation from JSON
function createAnimationFromJSON(animationData, containerId = 'animation-container') {
    const engine = new AnimationEngine(containerId);
    engine.initScene();
    engine.loadAnimation(animationData);
    engine.createAnnotationElements();
    
    // Auto-start
    setTimeout(() => {
        engine.play();
    }, 100);
    
    return engine;
}