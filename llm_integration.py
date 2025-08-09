"""
LLM Integration Module
Handles communication with various LLM providers (OpenAI, Anthropic, etc.)
and prompt engineering for generating structured animation instructions
"""

import json
import os
from typing import Dict, Any, Optional, List
import asyncio
from dataclasses import dataclass
from enum import Enum
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LLMProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic" 
    HUGGINGFACE = "huggingface"
    LOCAL = "local"

@dataclass
class AnimationInstruction:
    scene_type: str
    actors: List[str]
    parameters: Dict[str, Any]
    timeline: List[Dict[str, Any]]
    annotations: List[Dict[str, str]]

class LLMIntegrator:
    def __init__(self, provider: LLMProvider = LLMProvider.OPENAI):
        self.provider = provider
        self.api_key = os.getenv(f"{provider.value.upper()}_API_KEY")
        self._setup_client()
    
    def _setup_client(self):
        """Initialize the appropriate LLM client"""
        if self.provider == LLMProvider.OPENAI:
            try:
                import openai
                self.client = openai.OpenAI(api_key=self.api_key)
            except ImportError:
                raise ImportError("OpenAI package not installed. Run: pip install openai")
        
        elif self.provider == LLMProvider.ANTHROPIC:
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=self.api_key)
            except ImportError:
                raise ImportError("Anthropic package not installed. Run: pip install anthropic")
    
    def _get_system_prompt(self) -> str:
        return '''You are an expert at creating educational animations for scientific concepts. 
        Given a question, you must respond with both a clear text explanation and structured JSON instructions for creating an animated visualization.

        Your response must be valid JSON in this exact format:
        {
            "text": "Clear explanation of the concept...",
            "animation_instructions": {
                "scene_type": "solar_system|photosynthesis|circuit|wave_interference|molecular|custom",
                "actors": ["list", "of", "objects", "in", "scene"],
                "parameters": {
                    "key_parameter": value,
                    "another_parameter": value
                },
                "timeline": [
                    {"time": 0, "action": "description", "parameters": {}},
                    {"time": 1, "action": "description", "parameters": {}}
                ],
                "annotations": [
                    {"time": 0, "text": "Explanation of what happens at this moment"},
                    {"time": 1, "text": "Next explanation"}
                ]
            }
        }

        Scene types and their typical parameters:
        - solar_system: earth_tilt, orbit_radius, animation_speed, show_seasons
        - photosynthesis: plant_type, light_intensity, co2_flow, o2_production
        - circuit: voltage, resistance, current_flow, component_types
        - wave_interference: frequency1, frequency2, amplitude1, amplitude2, wave_type
        - molecular: molecule_type, reaction_type, temperature, pressure
        
        Always include realistic parameter values and detailed timeline with annotations.'''

    def _create_prompt(self, query: str) -> str:
        return f"""Question: {query}

        Please provide both a text explanation and animation instructions for this scientific concept. 
        Focus on the key visual elements that would help someone understand the concept better.
        
        Make sure your response is valid JSON matching the required format."""

    async def generate_response(self, query: str) -> Dict[str, Any]:
        """Generate LLM response with structured animation instructions"""
        
        if self.provider == LLMProvider.OPENAI:
            return await self._openai_response(query)
        elif self.provider == LLMProvider.ANTHROPIC:
            return await self._anthropic_response(query)
        else:
            return await self._mock_response(query)

    async def _openai_response(self, query: str) -> Dict[str, Any]:
        """Generate response using OpenAI API"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": self._create_prompt(query)}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return await self._mock_response(query)

    async def _anthropic_response(self, query: str) -> Dict[str, Any]:
        """Generate response using Anthropic API"""
        try:
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=2000,
                system=self._get_system_prompt(),
                messages=[
                    {"role": "user", "content": self._create_prompt(query)}
                ]
            )
            
            content = response.content[0].text
            return json.loads(content)
            
        except Exception as e:
            print(f"Anthropic API error: {e}")
            return await self._mock_response(query)

    async def _mock_response(self, query: str) -> Dict[str, Any]:
        """Generate mock response based on query patterns"""
        
        query_lower = query.lower()
        
        # Solar system / seasons
        if any(word in query_lower for word in ['season', 'earth', 'sun', 'orbit', 'tilt']):
            return {
                "text": "The Earth has seasons because its rotational axis is tilted 23.5 degrees relative to its orbital plane around the Sun. This tilt means that as Earth orbits the Sun throughout the year, different parts of the planet receive varying amounts of direct sunlight. When the Northern Hemisphere is tilted toward the Sun, it experiences summer with longer days and more direct sunlight, while the Southern Hemisphere experiences winter. Six months later, the situation reverses.",
                "animation_instructions": {
                    "scene_type": "solar_system",
                    "actors": ["earth", "sun", "orbit_path"],
                    "parameters": {
                        "earth_tilt": 23.5,
                        "orbit_radius": 4,
                        "animation_speed": 0.015,
                        "show_seasons": True,
                        "earth_rotation_speed": 0.05
                    },
                    "timeline": [
                        {"time": 0, "action": "start_orbit", "earth_position": "summer_solstice"},
                        {"time": 1, "action": "continue_orbit", "earth_position": "autumn_equinox"},
                        {"time": 2, "action": "continue_orbit", "earth_position": "winter_solstice"},
                        {"time": 3, "action": "continue_orbit", "earth_position": "spring_equinox"}
                    ],
                    "annotations": [
                        {"time": 0, "text": "Summer: Northern hemisphere tilted toward Sun"},
                        {"time": 1, "text": "Autumn: Equal day/night length"},
                        {"time": 2, "text": "Winter: Northern hemisphere tilted away from Sun"},
                        {"time": 3, "text": "Spring: Equal day/night length again"}
                    ]
                }
            }
        
        # Photosynthesis
        elif any(word in query_lower for word in ['photosynthesis', 'plant', 'chlorophyll', 'oxygen', 'carbon dioxide']):
            return {
                "text": "Photosynthesis is the process by which plants convert light energy, carbon dioxide, and water into glucose and oxygen. This occurs primarily in the leaves, where chlorophyll captures sunlight. The chemical equation is: 6CO₂ + 6H₂O + light energy → C₆H₁₂O₆ + 6O₂. This process is essential for life on Earth as it produces the oxygen we breathe and forms the base of most food chains.",
                "animation_instructions": {
                    "scene_type": "photosynthesis",
                    "actors": ["plant", "sun", "co2_molecules", "h2o_molecules", "o2_molecules", "glucose"],
                    "parameters": {
                        "plant_type": "generic_plant",
                        "light_intensity": 80,
                        "co2_flow_rate": 10,
                        "o2_production_rate": 6,
                        "animation_duration": 10
                    },
                    "timeline": [
                        {"time": 0, "action": "sunlight_hits_leaves", "intensity": 100},
                        {"time": 1, "action": "co2_enters_stomata", "rate": 10},
                        {"time": 2, "action": "water_absorbed_by_roots", "rate": 8},
                        {"time": 3, "action": "glucose_production", "amount": 1},
                        {"time": 4, "action": "oxygen_release", "amount": 6}
                    ],
                    "annotations": [
                        {"time": 0, "text": "Sunlight provides energy for the process"},
                        {"time": 1, "text": "CO₂ enters through leaf pores (stomata)"},
                        {"time": 2, "text": "Water travels from roots to leaves"},
                        {"time": 3, "text": "Glucose (sugar) is produced for plant energy"},
                        {"time": 4, "text": "Oxygen is released as a byproduct"}
                    ]
                }
            }
        
        # Electric circuits
        elif any(word in query_lower for word in ['circuit', 'electric', 'current', 'voltage', 'resistance', 'electron']):
            return {
                "text": "An electric circuit is a closed path through which electric current can flow. Current consists of moving electrons that flow from the negative terminal of a power source (like a battery) through the circuit components and back to the positive terminal. The flow of current is governed by Ohm's Law: V = I × R, where voltage (V) equals current (I) times resistance (R).",
                "animation_instructions": {
                    "scene_type": "circuit",
                    "actors": ["battery", "resistor", "led", "wires", "electrons"],
                    "parameters": {
                        "voltage": 9,
                        "resistance": 470,
                        "current": 0.019,
                        "electron_speed": 2,
                        "show_electron_flow": True
                    },
                    "timeline": [
                        {"time": 0, "action": "electrons_leave_battery", "current": 0.019},
                        {"time": 1, "action": "electrons_through_resistor", "voltage_drop": 8.9},
                        {"time": 2, "action": "electrons_power_led", "brightness": 100},
                        {"time": 3, "action": "electrons_return_battery", "circuit_complete": True}
                    ],
                    "annotations": [
                        {"time": 0, "text": "Electrons flow from battery's negative terminal"},
                        {"time": 1, "text": "Resistor limits current flow, voltage drops"},
                        {"time": 2, "text": "LED converts electrical energy to light"},
                        {"time": 3, "text": "Electrons complete the circuit back to battery"}
                    ]
                }
            }
        
        # Wave interference
        elif any(word in query_lower for word in ['wave', 'interference', 'frequency', 'amplitude', 'oscillation']):
            return {
                "text": "Wave interference occurs when two or more waves meet and combine. When wave peaks align (constructive interference), they create larger amplitudes. When peaks meet troughs (destructive interference), they can cancel out. This principle explains many phenomena including sound acoustics, light patterns, and water wave behavior.",
                "animation_instructions": {
                    "scene_type": "wave_interference",
                    "actors": ["wave_source_1", "wave_source_2", "interference_pattern"],
                    "parameters": {
                        "frequency1": 0.02,
                        "frequency2": 0.02,
                        "amplitude1": 50,
                        "amplitude2": 50,
                        "wave_speed": 100,
                        "medium": "water"
                    },
                    "timeline": [
                        {"time": 0, "action": "generate_waves", "sources": 2},
                        {"time": 1, "action": "waves_propagate", "distance": 100},
                        {"time": 2, "action": "constructive_interference", "amplitude": 100},
                        {"time": 3, "action": "destructive_interference", "amplitude": 0}
                    ],
                    "annotations": [
                        {"time": 0, "text": "Two wave sources generate identical waves"},
                        {"time": 1, "text": "Waves spread outward in concentric circles"},
                        {"time": 2, "text": "Constructive interference: waves add together"},
                        {"time": 3, "text": "Destructive interference: waves cancel out"}
                    ]
                }
            }
        
        # Default response
        else:
            return {
                "text": f"This is an explanation for: {query}. The system would analyze this topic and provide relevant scientific information with appropriate visualizations.",
                "animation_instructions": {
                    "scene_type": "custom",
                    "actors": ["generic_object"],
                    "parameters": {
                        "animation_type": "basic",
                        "duration": 5
                    },
                    "timeline": [
                        {"time": 0, "action": "initialize", "state": "start"},
                        {"time": 1, "action": "demonstrate", "state": "active"}
                    ],
                    "annotations": [
                        {"time": 0, "text": "Starting demonstration"},
                        {"time": 1, "text": "Showing key concepts"}
                    ]
                }
            }

    def validate_animation_instructions(self, instructions: Dict[str, Any]) -> bool:
        """Validate that animation instructions have required fields"""
        required_fields = ['scene_type', 'actors', 'parameters', 'timeline', 'annotations']
        return all(field in instructions for field in required_fields)

# Convenience function for easy import
async def generate_llm_response(query: str, provider: LLMProvider = LLMProvider.OPENAI) -> Dict[str, Any]:
    """Convenience function to generate LLM response"""
    integrator = LLMIntegrator(provider)
    return await integrator.generate_response(query)