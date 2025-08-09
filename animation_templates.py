"""
Animation Templates Library
Contains reusable JavaScript/HTML templates for different types of scientific explanations
"""

class AnimationTemplates:
    
    @staticmethod
    def solar_system_advanced() -> str:
        return '''
        // Enhanced Solar System Animation with Seasons
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, 800/600, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(800, 600);
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        document.getElementById('animation-container').appendChild(renderer.domElement);

        // Lighting setup
        const ambientLight = new THREE.AmbientLight(0x404040, 0.4);
        scene.add(ambientLight);
        
        const sunLight = new THREE.PointLight(0xffffff, 1, 100);
        sunLight.position.set(0, 0, 0);
        sunLight.castShadow = true;
        scene.add(sunLight);

        // Create Sun
        const sunGeometry = new THREE.SphereGeometry(1, 32, 32);
        const sunMaterial = new THREE.MeshBasicMaterial({{ 
            color: 0xffff00,
            emissive: 0xffaa00,
            emissiveIntensity: 0.3
        }});
        const sun = new THREE.Mesh(sunGeometry, sunMaterial);
        scene.add(sun);

        // Create Earth with texture
        const earthGeometry = new THREE.SphereGeometry(0.4, 32, 32);
        const earthMaterial = new THREE.MeshLambertMaterial({{ 
            color: 0x4169e1,
            transparent: true,
            opacity: 0.9
        }});
        const earth = new THREE.Mesh(earthGeometry, earthMaterial);
        earth.rotation.z = {earth_tilt} * Math.PI / 180;
        earth.castShadow = true;
        earth.receiveShadow = true;
        scene.add(earth);

        // Add orbit path
        const orbitGeometry = new THREE.RingGeometry({orbit_radius} - 0.05, {orbit_radius} + 0.05, 64);
        const orbitMaterial = new THREE.MeshBasicMaterial({{ 
            color: 0xffffff, 
            side: THREE.DoubleSide,
            transparent: true,
            opacity: 0.3
        }});
        const orbitRing = new THREE.Mesh(orbitGeometry, orbitMaterial);
        orbitRing.rotation.x = -Math.PI / 2;
        scene.add(orbitRing);

        // Animation variables
        let angle = 0;
        let earthRotation = 0;
        const orbitRadius = {orbit_radius};
        const animationSpeed = {animation_speed};
        
        // Seasonal position markers
        const seasons = ['Spring', 'Summer', 'Fall', 'Winter'];
        const seasonAngles = [0, Math.PI/2, Math.PI, 3*Math.PI/2];

        function animate() {{
            requestAnimationFrame(animate);
            
            // Earth orbital motion
            angle += animationSpeed;
            earth.position.x = Math.cos(angle) * orbitRadius;
            earth.position.z = Math.sin(angle) * orbitRadius;
            
            // Earth rotation on axis
            earthRotation += 0.05;
            earth.rotation.y = earthRotation;
            
            // Update camera to follow orbit
            camera.position.x = Math.cos(angle - Math.PI/4) * 8;
            camera.position.z = Math.sin(angle - Math.PI/4) * 8;
            camera.position.y = 3;
            camera.lookAt(0, 0, 0);
            
            renderer.render(scene, camera);
        }}

        // Initialize camera
        camera.position.set(6, 3, 6);
        camera.lookAt(0, 0, 0);
        
        // Add controls info
        const info = document.createElement('div');
        info.innerHTML = 'Earth rotates around Sun showing axial tilt causing seasons';
        info.style.position = 'absolute';
        info.style.top = '10px';
        info.style.left = '10px';
        info.style.color = 'white';
        info.style.background = 'rgba(0,0,0,0.7)';
        info.style.padding = '10px';
        document.getElementById('animation-container').appendChild(info);
        
        // Auto-start animation when page loads
        window.addEventListener('load', () => {{
            animate();
        }});
        
        // Also start immediately in case load event already fired
        animate();
        '''

    @staticmethod
    def photosynthesis_process() -> str:
        return '''
        // SVG-based Photosynthesis Animation
        const svg = d3.select("#animation-container")
            .append("svg")
            .attr("width", 800)
            .attr("height", 600)
            .style("background", "linear-gradient(to bottom, #87CEEB 0%, #98FB98 100%)");

        // Plant structure
        const plant = svg.append("g").attr("class", "plant");
        
        // Stem
        plant.append("rect")
            .attr("x", 390)
            .attr("y", 300)
            .attr("width", 20)
            .attr("height", 250)
            .attr("fill", "#228B22");

        // Leaves
        const leafData = [
            {{x: 350, y: 320, rotation: -30}},
            {{x: 430, y: 340, rotation: 30}},
            {{x: 340, y: 380, rotation: -45}},
            {{x: 440, y: 400, rotation: 45}}
        ];

        leafData.forEach((d, i) => {{
            plant.append("ellipse")
                .attr("cx", d.x)
                .attr("cy", d.y)
                .attr("rx", 40)
                .attr("ry", 20)
                .attr("fill", "#32CD32")
                .attr("transform", `rotate(${{d.rotation}} ${{d.x}} ${{d.y}})`);
        }});

        // Roots
        const rootPaths = [
            "M400,550 Q350,570 320,590",
            "M400,550 Q450,570 480,590",
            "M400,550 Q380,580 360,600",
            "M400,550 Q420,580 440,600"
        ];

        rootPaths.forEach(path => {{
            svg.append("path")
                .attr("d", path)
                .attr("stroke", "#8B4513")
                .attr("stroke-width", 3)
                .attr("fill", "none");
        }});

        // Sun
        const sun = svg.append("g").attr("class", "sun");
        sun.append("circle")
            .attr("cx", 700)
            .attr("cy", 100)
            .attr("r", 50)
            .attr("fill", "#FFD700");

        // Sun rays
        for(let i = 0; i < 8; i++) {{
            const angle = (i * 45) * Math.PI / 180;
            const x1 = 700 + Math.cos(angle) * 60;
            const y1 = 100 + Math.sin(angle) * 60;
            const x2 = 700 + Math.cos(angle) * 80;
            const y2 = 100 + Math.sin(angle) * 80;
            
            sun.append("line")
                .attr("x1", x1).attr("y1", y1)
                .attr("x2", x2).attr("y2", y2)
                .attr("stroke", "#FFD700")
                .attr("stroke-width", 3);
        }}

        // Animate sunlight particles
        function animateSunlight() {{
            const particles = svg.selectAll(".light-particle")
                .data(d3.range(20));

            particles.enter()
                .append("circle")
                .attr("class", "light-particle")
                .attr("r", 2)
                .attr("fill", "#FFFF00")
                .attr("cx", 700)
                .attr("cy", 100)
                .transition()
                .duration(2000)
                .ease(d3.easeLinear)
                .attr("cx", d => 400 + Math.random() * 100 - 50)
                .attr("cy", d => 350 + Math.random() * 100 - 50)
                .attr("opacity", 0)
                .remove();

            setTimeout(animateSunlight, 500);
        }}

        // Animate CO2 absorption
        function animateCO2() {{
            const co2 = svg.selectAll(".co2")
                .data(d3.range(10));

            co2.enter()
                .append("text")
                .attr("class", "co2")
                .text("CO₂")
                .attr("x", d => 200 + Math.random() * 100)
                .attr("y", d => 200 + Math.random() * 200)
                .attr("fill", "#666")
                .attr("font-size", "12px")
                .transition()
                .duration(3000)
                .attr("x", 400)
                .attr("y", 350)
                .attr("opacity", 0)
                .remove();

            setTimeout(animateCO2, 1000);
        }}

        // Animate O2 production
        function animateO2() {{
            const o2 = svg.selectAll(".o2")
                .data(d3.range(5));

            o2.enter()
                .append("text")
                .attr("class", "o2")
                .text("O₂")
                .attr("x", 400)
                .attr("y", 350)
                .attr("fill", "#0000FF")
                .attr("font-size", "12px")
                .transition()
                .duration(2000)
                .attr("x", d => 400 + Math.random() * 200 - 100)
                .attr("y", d => 200 + Math.random() * 100)
                .attr("opacity", 0)
                .remove();

            setTimeout(animateO2, 1500);
        }}

        // Add equation
        svg.append("text")
            .attr("x", 50)
            .attr("y", 50)
            .attr("fill", "black")
            .attr("font-size", "16px")
            .attr("font-weight", "bold")
            .text("6CO₂ + 6H₂O + light energy → C₆H₁₂O₆ + 6O₂");

        // Auto-start animations when page loads
        window.addEventListener('load', () => {{
            animateSunlight();
            animateCO2();
            animateO2();
        }});
        
        // Also start immediately in case load event already fired
        animateSunlight();
        animateCO2();
        animateO2();
        '''

    @staticmethod
    def electric_circuit() -> str:
        return '''
        // Canvas-based Electric Circuit Animation
        const canvas = document.createElement('canvas');
        canvas.width = 800;
        canvas.height = 600;
        canvas.style.border = '1px solid #ccc';
        document.getElementById('animation-container').appendChild(canvas);
        
        const ctx = canvas.getContext('2d');
        
        // Circuit components
        const battery = {{ x: 100, y: 300, width: 60, height: 40 }};
        const resistor = {{ x: 400, y: 200, width: 80, height: 20 }};
        const led = {{ x: 600, y: 300, radius: 15 }};
        
        // Wire paths
        const wirePaths = [
            [{{x: 160, y: 280}}, {{x: 400, y: 280}}, {{x: 400, y: 210}}], // Top wire
            [{{x: 480, y: 210}}, {{x: 600, y: 210}}, {{x: 600, y: 285}}], // Right wire
            [{{x: 600, y: 315}}, {{x: 600, y: 400}}, {{x: 160, y: 400}}, {{x: 160, y: 320}}] // Bottom wire
        ];
        
        // Electron particles
        let electrons = [];
        const electronSpeed = 2;
        
        function createElectrons() {{
            // Create electrons along the wire path
            for(let pathIndex = 0; pathIndex < wirePaths.length; pathIndex++) {{
                const path = wirePaths[pathIndex];
                for(let i = 0; i < path.length - 1; i++) {{
                    for(let j = 0; j < 3; j++) {{
                        const progress = j / 3;
                        const x = path[i].x + (path[i + 1].x - path[i].x) * progress;
                        const y = path[i].y + (path[i + 1].y - path[i].y) * progress;
                        electrons.push({{
                            x: x,
                            y: y,
                            pathIndex: pathIndex,
                            segmentIndex: i,
                            segmentProgress: progress
                        }});
                    }}
                }}
            }}
        }}
        
        function drawBattery() {{
            ctx.fillStyle = '#333';
            ctx.fillRect(battery.x, battery.y, battery.width, battery.height);
            
            // Positive terminal
            ctx.fillStyle = '#ff0000';
            ctx.fillRect(battery.x + battery.width - 5, battery.y + 10, 5, 20);
            
            // Negative terminal
            ctx.fillStyle = '#000000';
            ctx.fillRect(battery.x, battery.y + 10, 5, 20);
            
            // Labels
            ctx.fillStyle = 'white';
            ctx.font = '20px Arial';
            ctx.fillText('+', battery.x + battery.width - 15, battery.y + 25);
            ctx.fillText('-', battery.x + 10, battery.y + 25);
        }}
        
        function drawResistor() {{
            ctx.strokeStyle = '#8B4513';
            ctx.lineWidth = 4;
            ctx.beginPath();
            // Zigzag pattern for resistor
            const startX = resistor.x;
            const endX = resistor.x + resistor.width;
            const y = resistor.y + resistor.height / 2;
            const segments = 6;
            const segmentWidth = resistor.width / segments;
            
            ctx.moveTo(startX, y);
            for(let i = 0; i < segments; i++) {{
                const x = startX + i * segmentWidth;
                const nextX = x + segmentWidth;
                const zigY = y + (i % 2 === 0 ? -10 : 10);
                ctx.lineTo(x + segmentWidth/2, zigY);
                ctx.lineTo(nextX, y);
            }}
            ctx.stroke();
            
            // Resistor label
            ctx.fillStyle = 'black';
            ctx.font = '12px Arial';
            ctx.fillText('R', resistor.x + resistor.width/2 - 5, resistor.y - 5);
        }}
        
        function drawLED() {{
            // LED body
            ctx.fillStyle = electrons.some(e => e.pathIndex === 2) ? '#00ff00' : '#666';
            ctx.beginPath();
            ctx.arc(led.x, led.y, led.radius, 0, 2 * Math.PI);
            ctx.fill();
            
            // LED glow effect when current flows
            if(electrons.some(e => e.pathIndex === 2)) {{
                ctx.shadowBlur = 20;
                ctx.shadowColor = '#00ff00';
                ctx.beginPath();
                ctx.arc(led.x, led.y, led.radius * 0.8, 0, 2 * Math.PI);
                ctx.fill();
                ctx.shadowBlur = 0;
            }}
            
            // LED label
            ctx.fillStyle = 'black';
            ctx.font = '12px Arial';
            ctx.fillText('LED', led.x - 15, led.y - 25);
        }}
        
        function drawWires() {{
            ctx.strokeStyle = '#333';
            ctx.lineWidth = 3;
            
            wirePaths.forEach(path => {{
                ctx.beginPath();
                ctx.moveTo(path[0].x, path[0].y);
                for(let i = 1; i < path.length; i++) {{
                    ctx.lineTo(path[i].x, path[i].y);
                }}
                ctx.stroke();
            }});
        }}
        
        function drawElectrons() {{
            ctx.fillStyle = '#0066ff';
            electrons.forEach(electron => {{
                ctx.beginPath();
                ctx.arc(electron.x, electron.y, 3, 0, 2 * Math.PI);
                ctx.fill();
                
                // Electron trail
                ctx.fillStyle = 'rgba(0, 102, 255, 0.3)';
                ctx.beginPath();
                ctx.arc(electron.x - 5, electron.y, 2, 0, 2 * Math.PI);
                ctx.fill();
                ctx.fillStyle = '#0066ff';
            }});
        }}
        
        function updateElectrons() {{
            electrons.forEach(electron => {{
                const path = wirePaths[electron.pathIndex];
                if(!path) return;
                
                electron.segmentProgress += electronSpeed / 100;
                
                if(electron.segmentProgress >= 1) {{
                    electron.segmentIndex++;
                    electron.segmentProgress = 0;
                    
                    if(electron.segmentIndex >= path.length - 1) {{
                        electron.pathIndex = (electron.pathIndex + 1) % wirePaths.length;
                        electron.segmentIndex = 0;
                    }}
                }}
                
                const currentPath = wirePaths[electron.pathIndex];
                if(currentPath && electron.segmentIndex < currentPath.length - 1) {{
                    const start = currentPath[electron.segmentIndex];
                    const end = currentPath[electron.segmentIndex + 1];
                    electron.x = start.x + (end.x - start.x) * electron.segmentProgress;
                    electron.y = start.y + (end.y - start.y) * electron.segmentProgress;
                }}
            }});
        }}
        
        function animate() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            drawWires();
            drawBattery();
            drawResistor();
            drawLED();
            drawElectrons();
            
            updateElectrons();
            
            requestAnimationFrame(animate);
        }}
        
        // Add circuit description
        const description = document.createElement('div');
        description.innerHTML = 'Electric current flows from positive to negative terminal through the circuit';
        description.style.marginTop = '10px';
        description.style.fontFamily = 'Arial, sans-serif';
        document.getElementById('animation-container').appendChild(description);
        
        // Auto-start animation when page loads
        window.addEventListener('load', () => {{
            createElectrons();
            animate();
        }});
        
        // Also start immediately in case load event already fired
        createElectrons();
        animate();
        '''

    @staticmethod
    def wave_interference() -> str:
        return '''
        // Canvas-based Wave Interference Animation
        const canvas = document.createElement('canvas');
        canvas.width = 800;
        canvas.height = 600;
        document.getElementById('animation-container').appendChild(canvas);
        
        const ctx = canvas.getContext('2d');
        
        let time = 0;
        const wave1Source = {{ x: 200, y: 300 }};
        const wave2Source = {{ x: 600, y: 300 }};
        const frequency1 = 0.02;
        const frequency2 = 0.02;
        const amplitude1 = 50;
        const amplitude2 = 50;
        
        function drawWave(sourceX, sourceY, frequency, amplitude, color, time) {{
            ctx.strokeStyle = color;
            ctx.lineWidth = 2;
            
            // Draw concentric circles representing wave fronts
            for(let r = 10; r < 400; r += 20) {{
                const waveHeight = amplitude * Math.sin(frequency * (r - time * 100));
                const alpha = Math.max(0, 1 - r / 400);
                
                ctx.globalAlpha = alpha;
                ctx.beginPath();
                ctx.arc(sourceX, sourceY, r + waveHeight, 0, 2 * Math.PI);
                ctx.stroke();
            }}
            ctx.globalAlpha = 1;
        }}
        
        function drawInterference() {{
            const imageData = ctx.createImageData(canvas.width, canvas.height);
            const data = imageData.data;
            
            for(let x = 0; x < canvas.width; x++) {{
                for(let y = 0; y < canvas.height; y++) {{
                    const distance1 = Math.sqrt(Math.pow(x - wave1Source.x, 2) + Math.pow(y - wave1Source.y, 2));
                    const distance2 = Math.sqrt(Math.pow(x - wave2Source.x, 2) + Math.pow(y - wave2Source.y, 2));
                    
                    const wave1 = amplitude1 * Math.sin(frequency1 * (distance1 - time * 100));
                    const wave2 = amplitude2 * Math.sin(frequency2 * (distance2 - time * 100));
                    const interference = wave1 + wave2;
                    
                    const intensity = Math.abs(interference) / (amplitude1 + amplitude2);
                    const color = interference > 0 ? [255, 100, 100] : [100, 100, 255];
                    
                    const index = (y * canvas.width + x) * 4;
                    data[index] = color[0] * intensity;     // Red
                    data[index + 1] = color[1] * intensity; // Green
                    data[index + 2] = color[2] * intensity; // Blue
                    data[index + 3] = 255 * intensity * 0.3; // Alpha
                }}
            }}
            
            ctx.putImageData(imageData, 0, 0);
        }}
        
        function animate() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            drawInterference();
            
            // Draw wave sources
            ctx.fillStyle = '#ff0000';
            ctx.beginPath();
            ctx.arc(wave1Source.x, wave1Source.y, 8, 0, 2 * Math.PI);
            ctx.fill();
            
            ctx.fillStyle = '#0000ff';
            ctx.beginPath();
            ctx.arc(wave2Source.x, wave2Source.y, 8, 0, 2 * Math.PI);
            ctx.fill();
            
            time += 0.02;
            requestAnimationFrame(animate);
        }}
        
        // Auto-start animation when page loads
        window.addEventListener('load', () => {{
            animate();
        }});
        
        // Also start immediately in case load event already fired
        animate();
        '''