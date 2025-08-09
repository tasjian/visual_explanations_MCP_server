"""
Animation Schema Definition
Defines the structured JSON format for animation instructions
"""

from pydantic import BaseModel
from typing import List, Dict, Any, Optional, Union
from enum import Enum

class SceneType(str, Enum):
    SOLAR_SYSTEM = "solar_system"
    PHOTOSYNTHESIS = "photosynthesis"
    CIRCUIT = "circuit"
    WAVE_INTERFERENCE = "wave_interference"
    MOLECULAR = "molecular"
    CUSTOM = "custom"

class ActorType(str, Enum):
    SPHERE = "sphere"
    CUBE = "cube"
    PLANE = "plane"
    CYLINDER = "cylinder"
    PARTICLE_SYSTEM = "particle_system"
    LINE = "line"
    TEXT = "text"

class Actor(BaseModel):
    id: str
    type: ActorType
    radius: Optional[float] = None
    color: str = "#ffffff"
    position: List[float] = [0, 0, 0]
    rotation: List[float] = [0, 0, 0]
    scale: List[float] = [1, 1, 1]
    
    # Physics properties
    mass: Optional[float] = None
    velocity: Optional[List[float]] = None
    
    # Specific properties for different types
    tilt: Optional[float] = None
    orbit_radius: Optional[float] = None
    emissive: Optional[str] = None
    opacity: Optional[float] = 1.0
    
    # Text-specific
    text_content: Optional[str] = None
    font_size: Optional[float] = None

class TimelineEvent(BaseModel):
    time: float
    properties: Dict[str, Any]
    duration: Optional[float] = 1.0
    easing: str = "linear"  # linear, ease-in, ease-out, ease-in-out

class Annotation(BaseModel):
    time: float
    text: str
    position: Optional[List[float]] = None
    duration: Optional[float] = 3.0
    style: Optional[Dict[str, str]] = None

class CameraSettings(BaseModel):
    position: List[float] = [0, 0, 10]
    target: List[float] = [0, 0, 0]
    fov: float = 75
    follow_actor: Optional[str] = None

class AnimationInstructions(BaseModel):
    scene: SceneType
    actors: List[Actor]
    timeline: List[TimelineEvent]
    annotations: List[Annotation]
    camera: Optional[CameraSettings] = None
    duration: float = 10.0
    loop: bool = True
    
class AnimationResponse(BaseModel):
    text: str
    animation_instructions: AnimationInstructions

# Example schemas for different scene types
SCENE_SCHEMAS = {
    SceneType.SOLAR_SYSTEM: {
        "typical_actors": ["sun", "earth", "moon", "orbit_path"],
        "common_properties": ["orbit_radius", "tilt", "rotation_speed", "orbit_speed"],
        "example": {
            "scene": "solar_system",
            "actors": [
                {
                    "id": "sun",
                    "type": "sphere",
                    "radius": 1.0,
                    "color": "#ffff00",
                    "emissive": "#ffaa00",
                    "position": [0, 0, 0]
                },
                {
                    "id": "earth",
                    "type": "sphere", 
                    "radius": 0.3,
                    "color": "#4169e1",
                    "tilt": 23.5,
                    "orbit_radius": 3.0,
                    "position": [3, 0, 0]
                }
            ]
        }
    },
    
    SceneType.PHOTOSYNTHESIS: {
        "typical_actors": ["plant", "sun", "co2_particles", "o2_particles", "h2o_particles"],
        "common_properties": ["particle_count", "flow_rate", "reaction_rate"],
        "example": {
            "scene": "photosynthesis",
            "actors": [
                {
                    "id": "plant",
                    "type": "custom",
                    "color": "#228b22",
                    "position": [0, 0, 0]
                },
                {
                    "id": "co2_particles",
                    "type": "particle_system",
                    "color": "#666666",
                    "count": 50
                }
            ]
        }
    },
    
    SceneType.CIRCUIT: {
        "typical_actors": ["battery", "resistor", "led", "wire", "electrons"],
        "common_properties": ["voltage", "current", "resistance", "electron_speed"],
        "example": {
            "scene": "circuit",
            "actors": [
                {
                    "id": "battery",
                    "type": "cube",
                    "color": "#333333",
                    "position": [-2, 0, 0]
                },
                {
                    "id": "electrons",
                    "type": "particle_system",
                    "color": "#0066ff",
                    "count": 20
                }
            ]
        }
    }
}