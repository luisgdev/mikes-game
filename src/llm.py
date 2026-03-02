"""LLM module for AI-powered procedural content generation."""

from mistralai import Mistral
from mistralai.models import UserMessage
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
import os
import re
import json


@dataclass
class LLMConfig:
    """Configuration for LLM generator."""
    api_key: str = None
    model: str = "mistral-small-latest"
    temperature: float = 0.7
    max_tokens: int = 1000


class LLMGenerator:
    """Handles all LLM interactions for procedural content generation."""
    
    def __init__(self, config: LLMConfig = None):
        """Initialize the Mistral AI client.
        
        Args:
            config: LLMConfig dataclass. If None, will load from config.toml.
        """
        if config is None:
            # Load config from file
            try:
                from src.config import AppConfig
                app_config = AppConfig.load()
                api_key = app_config.mistral_api_key
                if not api_key:
                    raise ValueError("Mistral API key not set in config")
            except ImportError:
                raise ImportError("Config module not found")
            except ValueError as e:
                raise ValueError(f"Configuration error: {e}")
            
            config = LLMConfig(api_key=api_key)
        
        self.config = config
        self.client = Mistral(api_key=self.config.api_key)
        
    def generate_level_layout(self, city: str, difficulty: str = "medium") -> Dict[str, Any]:
        """Generate a level layout for a specific city.
        
        Args:
            city: The city name (e.g., "Tokyo", "Paris")
            difficulty: Difficulty level (easy, medium, hard)
            
        Returns:
            Dictionary containing level layout information
        """
        prompt = f"""Generate a level layout for Mike's Journey Home game.
        City: {city}
        Difficulty: {difficulty}
        
        Provide a JSON response with the following structure:
        {{
          "obstacles": [
            {{"type": "spike", "position": 100, "frequency": 5}},
            {{"type": "enemy", "position": 200, "frequency": 3}}
          ],
          "collectibles": [
            {{"type": "power-up", "position": 150, "frequency": 2}},
            {{"type": "energy", "position": 300, "frequency": 1}}
          ],
          "checkpoints": [100, 300, 500],
          "climate": "sunny",
          "daylight": "day"
        }}
        
        Be creative but keep it balanced for the difficulty level.
        Return only valid JSON, no markdown formatting."""
        
        return self._generate_json_response(prompt)
        
    def generate_obstacle_placement(self, level_length: int, difficulty: str) -> List[Dict[str, Any]]:
        """Generate obstacle placement for a level.
        
        Args:
            level_length: Length of the level in units
            difficulty: Difficulty level
            
        Returns:
            List of obstacle dictionaries with type, position, and properties
        """
        prompt = f"""Generate obstacle placement for a level of length {level_length}.
        Difficulty: {difficulty}
        
        Provide a JSON array of obstacles with:
        - type: obstacle type (spike, enemy, pit, etc.)
        - position: x coordinate
        - properties: any additional properties
        
        Make it challenging but fair for {difficulty} difficulty."""
        
        return self._generate_json_response(prompt)
        
    def generate_collectible_placement(self, level_length: int) -> List[Dict[str, Any]]:
        """Generate collectible placement for a level.
        
        Args:
            level_length: Length of the level in units
            
        Returns:
            List of collectible dictionaries with type, position, and properties
        """
        prompt = f"""Generate collectible placement for a level of length {level_length}.
        
        Provide a JSON array of collectibles with:
        - type: collectible type (power-up, energy, book, etc.)
        - position: x coordinate
        - properties: any additional properties
        
        Include a good mix of helpful items."""
        
        return self._generate_json_response(prompt)
        
    def generate_climate_effects(self, city: str) -> Dict[str, Any]:
        """Generate climate effects for a city.
        
        Args:
            city: The city name
            
        Returns:
            Dictionary containing climate information
        """
        prompt = f"""Generate climate effects for {city} in Mike's Journey Home.
        
        Provide a JSON response with:
        - weather: current weather condition
        - effects: visual effects to apply
        - intensity: severity level (1-10)
        
        Be creative but appropriate for {city}."""
        
        return self._generate_json_response(prompt)
        
    def _generate_json_response(self, prompt: str) -> Any:
        """Generate a JSON response from the LLM.
        
        Args:
            prompt: The prompt to send to the LLM
            
        Returns:
            Parsed JSON response
        """
        chat_response = self.client.chat.complete(
            model=self.config.model,
            messages=[UserMessage(content=prompt)]
        )
        
        # Extract and parse the JSON content
        response_content = chat_response.choices[0].message.content
        
        # Simple JSON parsing - in production you'd want more robust error handling

        try:
            return json.loads(response_content)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown if present

            json_match = re.search(r'```json\s*([\s\S]*?)\s*```', response_content)
            if json_match:
                return json.loads(json_match.group(1))
            raise ValueError(f"Could not parse JSON from LLM response: {response_content}")

    def generate_rgba_tile(self, tile_type: str, prompt: str | None = None, size: int = 8) -> List[List[Tuple[int, int, int, int]]]:
        """Generate an RGBA tile array for a specific tile type.
        
        Args:
            tile_type: Type of tile (grass, water, dirt, etc.)
            size: Size of tile in pixels (default 8x8)
            prompt: Optional System prompt
            
        Returns:
            2D list of RGBA tuples
        """
        if not prompt:
            prompt = f"""Generate an {size}x{size} RGBA pixel array for a {tile_type} tile.
            
            Use appropriate colors for {tile_type}:
            - Grass: shades of green (e.g., (34, 139, 34, 255))
            - Water: shades of blue (e.g., (65, 105, 225, 255))
            - Dirt: shades of brown (e.g., (139, 69, 19, 255))
            - Stone: shades of gray (e.g., (128, 128, 128, 255))
            
            Return as a Python list of lists of RGBA tuples.
            Example format for 2x2:
            [
                [(34, 139, 34, 255), (46, 139, 87, 255)],
                [(34, 139, 34, 255), (139, 69, 19, 255)]
            ]
            
            Return ONLY the Python list, no additional text or markdown formatting."""
        
        response = self._generate_text_response(prompt)
        return self._parse_rgba_array(response)

    def _generate_text_response(self, prompt: str) -> str:
        """Generate a text response from the LLM.
        
        Args:
            prompt: The prompt to send to the LLM
            
        Returns:
            Raw text response
        """
        chat_response = self.client.chat.complete(
            model=self.config.model,
            messages=[UserMessage(content=prompt)]
        )
        return chat_response.choices[0].message.content

    @staticmethod
    def _parse_rgba_array(text: str) -> List[List[Tuple[int, int, int, int]]]:
        """Parse RGBA array from text response.
        
        Args:
            text: Raw text from LLM
            
        Returns:
            2D list of RGBA tuples
        """
        try:
            # Handle case where LLM returns a list object directly
            if isinstance(text, list):
                array = text
            else:
                # Extract Python list from text
                match = re.search(r'\[.*\]', text, re.DOTALL)
                if not match:
                    raise ValueError("No Python list found in response")
                
                # Parse the list
                array = eval(match.group(0), {'__builtins__': None}, {})
            
            # Validate structure and convert RGB to RGBA
            for row in array:
                for pixel in row:
                    if len(pixel) == 3:
                        # Convert RGB to RGBA by adding alpha channel
                        pixel = list(pixel) + [255]
                    elif len(pixel) != 4 or not all(0 <= c <= 255 for c in pixel):
                        raise ValueError(f"Invalid RGBA pixel: {pixel}")
            
            return array
        except Exception as e:
            raise ValueError(f"Failed to parse RGBA array: {e}")


# Example usage
if __name__ == "__main__":
    # This would require a valid API key
    generator = LLMGenerator()
    level = generator.generate_level_layout("Tokyo", "medium")
    print(level)
    print("LLM module ready. Add your Mistral API key to use.")