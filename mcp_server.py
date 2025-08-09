from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import json
import asyncio
import os
from datetime import datetime
import uvicorn

from animation_templates import AnimationTemplates
from llm_integration import generate_llm_response, LLMProvider

app = FastAPI(title="Visual Explanation MCP Server", version="1.0.0")

class Query(BaseModel):
    content: str
    
class AnimationInstructions(BaseModel):
    scene_type: str
    actors: List[str]
    parameters: Dict[str, Any]
    timeline: List[Dict[str, Any]]
    annotations: List[Dict[str, str]]
    
class MCPResponse(BaseModel):
    text_response: str
    animation_instructions: Optional[AnimationInstructions] = None
    html_animation: Optional[str] = None

class AnimationCompiler:
    """Converts structured animation instructions to JavaScript code"""
    
    def __init__(self):
        self.templates = AnimationTemplates()
    
    def _load_templates(self) -> Dict[str, str]:
        return {
            "solar_system": self.templates.solar_system_advanced(),
            "photosynthesis": self.templates.photosynthesis_process(),
            "circuit": self.templates.electric_circuit(),
            "wave_interference": self.templates.wave_interference()
        }
    
    
    def compile_animation(self, instructions: AnimationInstructions) -> str:
        """Convert animation instructions to HTML with embedded JavaScript"""
        
        template_map = self._load_templates()
        template = template_map.get(instructions.scene_type, self._default_template())
        
        # Fill template parameters
        if instructions.scene_type == "solar_system":
            params = instructions.parameters
            template = template.format(
                earth_tilt=params.get("earth_tilt", 23.5),
                orbit_radius=params.get("orbit_radius", 3),
                animation_speed=params.get("animation_speed", 0.01)
            )
        
        # Create complete HTML
        html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Visual Explanation</title>
            <style>
                body {{ margin: 0; padding: 20px; font-family: Arial, sans-serif; }}
                #animation-container {{ border: 1px solid #ccc; }}
                .annotations {{ margin-top: 20px; }}
                .annotation {{ 
                    padding: 10px; 
                    margin: 5px 0; 
                    background: #f0f0f0; 
                    border-radius: 5px; 
                }}
            </style>
            <script src="https://cdn.jsdelivr.net/npm/three@0.152.2/build/three.min.js"></script>
            <script src="https://d3js.org/d3.v7.min.js"></script>
        </head>
        <body>
            <div id="animation-container"></div>
            <canvas id="animation-canvas"></canvas>
            <div class="annotations">
                {"".join(f'<div class="annotation">{ann["text"]}</div>' for ann in instructions.annotations)}
            </div>
            <script>
                {template}
            </script>
        </body>
        </html>
        '''
        
        return html
    
    def _default_template(self) -> str:
        return '''
        document.getElementById('animation-container').innerHTML = 
            '<p>Animation template not found for this scene type.</p>';
        '''

# Initialize animation compiler
compiler = AnimationCompiler()

# Use the imported LLM integration function

@app.post("/query", response_model=MCPResponse)
async def query_mcp(req: Query):
    """Main MCP endpoint for processing queries"""
    
    # Generate LLM response with animation instructions
    llm_response = await generate_llm_response(req.content, LLMProvider.OPENAI)
    
    response = MCPResponse(text_response=llm_response["text"])
    
    # If animation instructions are provided, compile them
    if llm_response.get("animation_instructions"):
        instructions = AnimationInstructions(**llm_response["animation_instructions"])
        response.animation_instructions = instructions
        response.html_animation = compiler.compile_animation(instructions)
    
    return response

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
            textarea { width: 100%; height: 100px; }
            button { padding: 10px 20px; background: #007cba; color: white; border: none; cursor: pointer; }
            .response-text { background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 10px 0; }
            iframe { width: 100%; height: 600px; border: 1px solid #ccc; }
        </style>
    </head>
    <body>
        <h1>Visual Explanation MCP Server Demo</h1>
        <div class="container">
            <div class="input-panel">
                <h3>Ask a Question</h3>
                <textarea id="query" placeholder="Try: Why does the Earth have seasons?">Why does the Earth have seasons?</textarea>
                <br><br>
                <button onclick="sendQuery()">Generate Explanation</button>
            </div>
            <div class="output-panel">
                <h3>Response</h3>
                <div id="text-response" class="response-text"></div>
                <div id="animation-container"></div>
            </div>
        </div>

        <script>
            async function sendQuery() {
                const query = document.getElementById('query').value;
                const response = await fetch('/query', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ content: query })
                });
                
                const data = await response.json();
                document.getElementById('text-response').textContent = data.text_response;
                
                if (data.html_animation) {
                    document.getElementById('animation-container').innerHTML = 
                        '<iframe srcdoc="' + data.html_animation.replace(/"/g, '&quot;') + '"></iframe>';
                }
            }
        </script>
    </body>
    </html>
    '''
    
    return html_content

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)