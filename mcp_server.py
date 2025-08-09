from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import json
import asyncio
import os
from datetime import datetime
import uvicorn
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from animation_schema import AnimationInstructions, AnimationResponse
from llm_integration import generate_llm_response, LLMProvider

app = FastAPI(title="Visual Explanation MCP Server", version="2.0.0")

class Query(BaseModel):
    content: str
    
class MCPResponse(BaseModel):
    text_response: str
    animation_instructions: Optional[AnimationInstructions] = None
    html_animation: Optional[str] = None

class AnimationCompiler:
    """Converts structured JSON animation instructions to HTML with universal animation engine"""
    
    def compile_animation(self, instructions: AnimationInstructions) -> str:
        """Convert animation instructions to HTML with embedded JavaScript"""
        
        # Convert instructions to JSON for the animation engine
        animation_json = instructions.model_dump_json()
        
        # Create complete HTML with universal animation engine
        html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Visual Explanation</title>
            <style>
                body {{ margin: 0; padding: 20px; font-family: Arial, sans-serif; }}
                #animation-container {{ 
                    position: relative;
                    border: 1px solid #ccc; 
                    width: 800px;
                    height: 600px;
                    background: #f8f8f8;
                }}
                .animation-annotation {{
                    position: absolute;
                    background: rgba(0,0,0,0.8);
                    color: white;
                    padding: 10px;
                    border-radius: 5px;
                    font-size: 14px;
                    max-width: 300px;
                    z-index: 100;
                }}
                .controls {{
                    margin-top: 10px;
                }}
                .controls button {{
                    margin-right: 10px;
                    padding: 8px 16px;
                    background: #007cba;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 14px;
                }}
                .controls button:hover {{
                    background: #005a8b;
                }}
                .info {{
                    margin-top: 10px;
                    padding: 10px;
                    background: #e3f2fd;
                    border-radius: 4px;
                    font-size: 14px;
                }}
            </style>
            <script src="https://cdn.jsdelivr.net/npm/three@0.152.2/build/three.min.js"></script>
        </head>
        <body>
            <div id="animation-container">
                <div style="padding: 20px; text-align: center;">
                    <p>Loading animation...</p>
                </div>
            </div>
            <div class="controls">
                <button onclick="window.animationEngine && window.animationEngine.play()">▶ Play</button>
                <button onclick="window.animationEngine && window.animationEngine.pause()">⏸ Pause</button>
                <button onclick="restartAnimation()">🔄 Restart</button>
            </div>
            <div class="info">
                🎬 Interactive Animation • Scene: {instructions.scene} • Duration: {instructions.duration}s
            </div>
            
            <script>
                // Universal Animation Engine (embedded)
                {self._get_animation_engine_code()}
                
                // Animation data from AI
                const animationData = {animation_json};
                
                function restartAnimation() {{
                    if (window.animationEngine) {{
                        window.animationEngine.currentTime = 0;
                        window.animationEngine.play();
                    }}
                }}
                
                // Initialize and start animation
                function initializeAnimation() {{
                    try {{
                        window.animationEngine = createAnimationFromJSON(animationData, 'animation-container');
                        console.log('Animation initialized successfully');
                    }} catch (error) {{
                        console.error('Animation initialization failed:', error);
                        document.getElementById('animation-container').innerHTML = 
                            '<div style="padding: 20px; text-align: center; color: #666;">Animation could not be loaded. Please refresh to try again.</div>';
                    }}
                }}
                
                // Start when ready
                document.addEventListener('DOMContentLoaded', initializeAnimation);
                
                if (document.readyState !== 'loading') {{
                    initializeAnimation();
                }}
            </script>
        </body>
        </html>
        '''
        
        return html
    
    def _get_animation_engine_code(self) -> str:
        """Load the animation engine JavaScript code"""
        try:
            with open('animation_engine.js', 'r') as f:
                return f.read()
        except FileNotFoundError:
            return self._get_fallback_animation_engine()
    
    def _get_fallback_animation_engine(self) -> str:
        """Minimal animation engine fallback"""
        return '''
        function createAnimationFromJSON(data, containerId) {
            console.log('Using fallback animation engine');
            const container = document.getElementById(containerId);
            
            // Create basic Three.js scene
            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(75, 800/600, 0.1, 1000);
            const renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(800, 600);
            container.innerHTML = '';
            container.appendChild(renderer.domElement);
            
            // Basic lighting
            const light = new THREE.AmbientLight(0x404040);
            scene.add(light);
            const dirLight = new THREE.DirectionalLight(0xffffff, 0.5);
            dirLight.position.set(5, 5, 5);
            scene.add(dirLight);
            
            // Create basic actors
            const actors = {};
            data.actors.forEach(actor => {
                let mesh;
                if (actor.type === 'sphere') {
                    const geo = new THREE.SphereGeometry(actor.radius || 0.5, 16, 16);
                    const mat = new THREE.MeshLambertMaterial({ color: actor.color || '#ffffff' });
                    mesh = new THREE.Mesh(geo, mat);
                } else {
                    const geo = new THREE.BoxGeometry(1, 1, 1);
                    const mat = new THREE.MeshLambertMaterial({ color: actor.color || '#ffffff' });
                    mesh = new THREE.Mesh(geo, mat);
                }
                mesh.position.set(...(actor.position || [0, 0, 0]));
                scene.add(mesh);
                actors[actor.id] = mesh;
            });
            
            camera.position.set(5, 5, 5);
            camera.lookAt(0, 0, 0);
            
            // Simple animation loop
            let time = 0;
            function animate() {
                requestAnimationFrame(animate);
                time += 0.016;
                
                // Basic orbit for solar system
                if (data.scene === 'solar_system' && actors.earth) {
                    actors.earth.position.x = Math.cos(time) * 3;
                    actors.earth.position.z = Math.sin(time) * 3;
                    actors.earth.rotation.y += 0.05;
                }
                
                renderer.render(scene, camera);
            }
            
            return {
                play: animate,
                pause: () => {},
                currentTime: 0
            };
        }
        '''

# Initialize animation compiler
compiler = AnimationCompiler()

@app.post("/query", response_model=MCPResponse)
async def query_mcp(req: Query):
    """Main MCP endpoint for processing queries"""
    
    # Generate LLM response with animation instructions
    # Use Anthropic since we have the API key configured
    llm_response = await generate_llm_response(req.content, LLMProvider.ANTHROPIC)
    
    response = MCPResponse(text_response=llm_response["text"])
    
    # If animation instructions are provided, compile them
    if llm_response.get("animation_instructions"):
        try:
            instructions = AnimationInstructions(**llm_response["animation_instructions"])
            response.animation_instructions = instructions
            response.html_animation = compiler.compile_animation(instructions)
        except Exception as e:
            print(f"Animation compilation error: {e}")
            # Fallback to text-only response
            pass
    
    return response

@app.get("/system-prompt")
async def get_system_prompt():
    """Display the system prompt used for generating animations"""
    from llm_integration import LLMIntegrator, LLMProvider
    integrator = LLMIntegrator(LLMProvider.ANTHROPIC)
    return {
        "system_prompt": integrator._get_system_prompt(),
        "user_prompt_template": integrator._create_prompt("EXAMPLE_QUERY"),
        "description": "This is the system prompt that guides Claude to generate structured animation instructions"
    }

@app.get("/demo", response_class=HTMLResponse)
async def demo():
    """Demo page for testing the MCP server"""
    
    html_content = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Visual Explanation MCP Demo</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }
            .container { display: flex; gap: 20px; }
            .input-panel { flex: 1; }
            .output-panel { flex: 2; }
            textarea { width: 100%; height: 100px; font-size: 14px; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }
            button { padding: 12px 24px; background: #007cba; color: white; border: none; cursor: pointer; border-radius: 4px; font-size: 16px; }
            button:hover { background: #005a8b; }
            button:disabled { background: #ccc; cursor: not-allowed; }
            .response-text { background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 10px 0; line-height: 1.6; }
            iframe { width: 100%; height: 650px; border: 1px solid #ccc; border-radius: 4px; }
            .header-link { color: #007cba; text-decoration: none; font-weight: bold; }
            .header-link:hover { text-decoration: underline; }
            .examples { margin-top: 15px; }
            .example { 
                background: #e3f2fd; 
                padding: 8px 12px; 
                margin: 5px 0; 
                border-radius: 4px; 
                cursor: pointer; 
                font-size: 14px;
                transition: background 0.2s;
            }
            .example:hover { background: #bbdefb; }
        </style>
    </head>
    <body>
        <h1>🎬 Visual Explanation MCP Server</h1>
        <div style="margin-bottom: 20px; text-align: center;">
            <a href="/system-prompt" target="_blank" class="header-link">
                🤖 View System Prompt Used for AI Generation
            </a>
        </div>
        <div class="container">
            <div class="input-panel">
                <h3>Ask a Science Question</h3>
                <textarea id="query" placeholder="Try: Why does the Earth have seasons?">Why does the Earth have seasons?</textarea>
                <br><br>
                <button onclick="sendQuery()">Generate Explanation</button>
                
                <div class="examples">
                    <strong>Example Questions:</strong>
                    <div class="example" onclick="setQuery(this.textContent)">Why does the Earth have seasons?</div>
                    <div class="example" onclick="setQuery(this.textContent)">How does photosynthesis work?</div>
                    <div class="example" onclick="setQuery(this.textContent)">What happens in an electric circuit?</div>
                    <div class="example" onclick="setQuery(this.textContent)">How do waves interfere with each other?</div>
                    <div class="example" onclick="setQuery(this.textContent)">Why do objects fall at the same rate?</div>
                </div>
            </div>
            <div class="output-panel">
                <h3>AI Response & Animation</h3>
                <div id="text-response" class="response-text">Ask a question to see the AI-generated explanation and interactive animation!</div>
                <div id="animation-container"></div>
            </div>
        </div>

        <script>
            function setQuery(text) {
                document.getElementById('query').value = text;
            }
        
            async function sendQuery() {
                const button = document.querySelector('button');
                const query = document.getElementById('query').value;
                const textResponse = document.getElementById('text-response');
                const animationContainer = document.getElementById('animation-container');
                
                // Show loading state
                button.disabled = true;
                button.textContent = 'Generating...';
                textResponse.innerHTML = '🤔 <strong>Thinking...</strong><br>Generating explanation and animation instructions...';
                animationContainer.innerHTML = '';
                
                try {
                    const response = await fetch('/query', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ content: query })
                    });
                    
                    if (!response.ok) {
                        throw new Error(`Server error: ${response.status}`);
                    }
                    
                    const data = await response.json();
                    textResponse.innerHTML = `<strong>Explanation:</strong><br>${data.text_response}`;
                    
                    if (data.html_animation) {
                        const iframe = document.createElement('iframe');
                        iframe.srcdoc = data.html_animation;
                        iframe.style.width = '100%';
                        iframe.style.height = '650px';
                        iframe.style.border = '1px solid #ccc';
                        iframe.style.borderRadius = '4px';
                        iframe.onload = function() {
                            console.log('Animation loaded successfully');
                        };
                        animationContainer.innerHTML = '';
                        animationContainer.appendChild(iframe);
                    } else {
                        animationContainer.innerHTML = '<p style="color: #666; padding: 20px; text-align: center;">No animation available for this query.</p>';
                    }
                    
                } catch (error) {
                    console.error('Error:', error);
                    textResponse.innerHTML = `❌ <strong>Error:</strong> ${error.message}`;
                    animationContainer.innerHTML = '<p style="color: #ff0000; padding: 20px; text-align: center;">Failed to generate animation.</p>';
                    
                } finally {
                    // Reset button state
                    button.disabled = false;
                    button.textContent = 'Generate Explanation';
                }
            }
            
            // Allow Enter key to submit
            document.getElementById('query').addEventListener('keypress', function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendQuery();
                }
            });
        </script>
    </body>
    </html>
    '''
    
    return html_content

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)