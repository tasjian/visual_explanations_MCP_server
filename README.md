# 🎬 Visual Explanation MCP Server

An **MCP (Model Control Protocol) server** that creates **animated visual explanations** for scientific and educational concepts. Ask a question like *"Why does the Earth have seasons?"* and get both a text explanation and an interactive animation showing the Earth's orbit and axial tilt.

## 🌟 Features

- **AI-Powered Explanations**: Uses OpenAI GPT or Anthropic Claude to generate detailed explanations
- **Structured Animation Instructions**: AI generates JSON instructions for creating visualizations  
- **Multiple Animation Types**: 3D (Three.js), 2D SVG (D3.js), and Canvas-based animations
- **Interactive Demo**: Built-in web interface for testing
- **Educational Focus**: Optimized for science, physics, chemistry, and biology concepts

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js (for frontend dependencies, optional)

### Installation

```bash
# Clone or download the project
cd vis_ex_MCP

# Install Python dependencies
pip install -r requirements.txt

# Set API key (optional - will use mock responses without it)
export OPENAI_API_KEY="your-openai-key"
# OR
export ANTHROPIC_API_KEY="your-anthropic-key"

# Start the server
python run_server.py
```

### Usage

1. **Web Demo**: Open http://localhost:8000/demo
2. **API Endpoint**: POST to http://localhost:8000/query
3. **API Documentation**: http://localhost:8000/docs

## 📚 Supported Topics

The system works best with visual scientific concepts:

### 🌍 Astronomy & Physics
- **Earth's seasons** - Shows orbital mechanics and axial tilt
- **Wave interference** - Demonstrates constructive/destructive interference
- **Planetary motion** - Orbital dynamics and gravitational effects

### 🔬 Biology & Chemistry  
- **Photosynthesis** - Shows light energy conversion and molecular processes
- **Cell division** - Mitosis and meiosis animations
- **Chemical reactions** - Molecular interactions and bond formation

### ⚡ Engineering & Technology
- **Electric circuits** - Current flow and component behavior
- **Mechanical systems** - Gears, levers, and force transmission
- **Signal processing** - Waveforms and filtering

## 🎯 Example Queries

Try these questions in the demo:

```
"Why does the Earth have seasons?"
"How does photosynthesis work?"
"What happens in an electric circuit?"
"How do waves interfere with each other?"
"Why do objects fall at the same rate?"
```

## 🔧 API Reference

### POST /query

Request body:
```json
{
  "content": "Why does the Earth have seasons?"
}
```

Response:
```json
{
  "text_response": "The Earth has seasons because...",
  "animation_instructions": {
    "scene_type": "solar_system",
    "actors": ["earth", "sun"],
    "parameters": {
      "earth_tilt": 23.5,
      "orbit_radius": 4,
      "animation_speed": 0.015
    },
    "timeline": [...],
    "annotations": [...]
  },
  "html_animation": "<iframe>...</iframe>"
}
```

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Query    │───▶│   MCP Server     │───▶│  LLM Provider   │
│ "Why seasons?"  │    │  (FastAPI)       │    │ (OpenAI/Claude) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │ Animation        │
                       │ Compiler         │
                       └──────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │ HTML + JS        │
                       │ Animation        │
                       └──────────────────┘
```

### Core Components

1. **MCP Server** (`mcp_server.py`) - FastAPI server handling requests
2. **LLM Integration** (`llm_integration.py`) - Connects to AI providers
3. **Animation Compiler** - Converts instructions to JavaScript
4. **Template Library** (`animation_templates.py`) - Reusable animation code

## 🎨 Animation Types

### 3D Animations (Three.js)
- Solar systems and planetary motion
- Molecular structures
- Mechanical systems

### 2D Vector (D3.js/SVG)  
- Biological processes
- Flow diagrams
- Statistical visualizations

### Canvas-based
- Wave phenomena  
- Particle systems
- Circuit diagrams

## 🔧 Configuration

### Environment Variables

```bash
# Required for real LLM responses
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Server settings (optional)
MCP_PORT=8000
MCP_HOST=localhost
```

### Template Customization

Add new animation templates in `animation_templates.py`:

```python
@staticmethod  
def my_custom_animation() -> str:
    return '''
    // Your JavaScript animation code here
    const scene = new THREE.Scene();
    // ... 
    '''
```

## 🧪 Development

### Project Structure

```
vis_ex_MCP/
├── mcp_server.py           # Main FastAPI server
├── llm_integration.py      # LLM provider connections
├── animation_templates.py  # JavaScript templates
├── requirements.txt        # Python dependencies  
├── run_server.py          # Startup script
└── README.md              # This file
```

### Adding New Animation Types

1. Create template in `animation_templates.py`
2. Add scene type to LLM prompt in `llm_integration.py`
3. Update compiler in `mcp_server.py`
4. Test with demo interface

### Testing

```bash
# Start development server with auto-reload
python run_server.py

# Test API endpoint
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"content": "Why does the Earth have seasons?"}'
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your animation template or improvement  
4. Test with the demo interface
5. Submit a pull request

## 📄 License

MIT License - feel free to use and modify for educational purposes.

## 🎯 Future Enhancements

- [ ] Voice narration with text-to-speech
- [ ] Interactive controls (sliders, buttons)
- [ ] Mobile-responsive animations
- [ ] More science topics (chemistry, advanced physics)
- [ ] Integration with educational platforms
- [ ] Real-time collaborative viewing

---

**Built with ❤️ for education and visual learning**