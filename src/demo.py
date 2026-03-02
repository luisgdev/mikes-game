"""Demo: Generate pixel art using LLM and display it."""

from PIL import Image
import json
from typing import List
from src.llm import LLMGenerator
from src.config import AppConfig

# Load configuration
config = AppConfig.load()

# Example JSON pixel data (from LLM output)
SIZE = 16

def generate_pixel_art(description: str = "orange cat facing left") -> List[List[List[int]]]:
    """Generate a 16x16 pixel art sprite using LLM."""
    # Read the pixel art prompt
    with open("src/pixel-art-prompt.md", "r") as f:
        prompt_template = f.read()
    
    # Replace the description placeholder
    prompt = prompt_template.replace("[orange cat facing left]", description)
    
    # Use LLM to generate the pixel art
    generator = LLMGenerator()
    
    # Generate the response
    response_text = generator.generate_rgba_tile(prompt=prompt, tile_type=description)
    
    # Parse the JSON response
    try:
        # Handle case where LLM returns a list object directly
        if isinstance(response_text, list):
            pixel_data = response_text
        else:
            # Remove markdown code block formatting if present
            if response_text.startswith("```json"):
                response_text = response_text[7:].strip()
            if response_text.endswith("```"):
                response_text = response_text[:-3].strip()
            
            pixel_data = json.loads(response_text)
        
        # Validate the structure
        if len(pixel_data) != 16 or any(len(row) != 16 for row in pixel_data):
            raise ValueError("Generated pixel data is not 16x16")
            
        return pixel_data
    except json.JSONDecodeError as e:
        print(f"Failed to parse LLM response: {e}")
        print(f"Response was: {response_text}")
        # Fallback to default data
        return []


if __name__ == "__main__":
    # Generate pixel art using LLM
    data = generate_pixel_art("bright star in the sky")

    size = len(data)
    print(f"Length of data: {size}")
    print(f"Length of rows: {[len(row) for row in data]}")
    # Create image
    img = Image.new('RGB', (size, size))
    pixels = img.load()

    for y in range(size):
        for x in range(size):
            pixels[x, y] = tuple(data[y][x])

    img.save('star-sky.png')
