"""
Generate small RGBA pixel arrays using an LLM, convert to PNG with Pillow,
and save for use in Pygame.
"""

import json
import re
import numpy as np
from PIL import Image
from typing import List, Tuple

# Mock LLM response (replace with actual LLM call in production)
def mock_llm_generate(prompt: str) -> str:
    """Mock LLM response for testing. Replace with real LLM integration."""
    # Generate a simple 8x8 tile based on tile_type
    if "grass" in prompt.lower():
        base_green = (34, 139, 34, 255)
        variant_green = (46, 139, 87, 255)
        dirt = (139, 69, 19, 255)
        pixels = [
            [base_green if (i + j) % 2 == 0 else variant_green for j in range(8)]
            for i in range(8)
        ]
        # Add some dirt patches
        for i in range(8):
            for j in range(8):
                if i > 5 and j > 5:
                    pixels[i][j] = dirt
    elif "water" in prompt.lower():
        base_blue = (65, 105, 225, 255)
        light_blue = (100, 149, 237, 255)
        dark_blue = (70, 130, 180, 255)
        pixels = [
            [base_blue if (i + j) % 3 == 0 else light_blue for j in range(8)]
            for i in range(8)
        ]
        # Add some darker patches
        for i in range(8):
            for j in range(8):
                if i % 3 == 0 and j % 3 == 0:
                    pixels[i][j] = dark_blue
    elif "dirt" in prompt.lower():
        base_brown = (139, 69, 19, 255)
        light_brown = (160, 82, 45, 255)
        pixels = [
            [base_brown if (i + j) % 2 == 0 else light_brown for j in range(8)]
            for i in range(8)
        ]
    elif "stone" in prompt.lower():
        gray = (128, 128, 128, 255)
        dark_gray = (64, 64, 64, 255)
        pixels = [
            [gray if (i + j) % 2 == 0 else dark_gray for j in range(8)]
            for i in range(8)
        ]
    else:
        # Default: checkerboard pattern
        pixels = [
            [(255, 0, 0, 255) if (i + j) % 2 == 0 else (0, 0, 0, 255) for j in range(8)]
            for i in range(8)
        ]
    return json.dumps(pixels)

def parse_rgba_array(llm_output: str) -> List[List[Tuple[int, int, int, int]]]:
    """Parse LLM output into a 2D list of RGBA tuples."""
    try:
        # Extract Python list using regex
        match = re.search(r'\[.*\]', llm_output, re.DOTALL)
        if not match:
            raise ValueError("No Python list found in LLM output.")

        # Eval is safe here because we control the LLM output format
        array = eval(match.group(0), {'__builtins__': None}, {})

        # Validate RGBA tuples
        for row in array:
            for pixel in row:
                if len(pixel) != 4 or not all(0 <= c <= 255 for c in pixel):
                    raise ValueError(f"Invalid RGBA pixel: {pixel}")
        return array
    except Exception as e:
        raise ValueError(f"Failed to parse LLM output: {e}")

def save_as_png(pixels: List[List[Tuple[int, int, int, int]]], filepath: str) -> None:
    """Convert RGBA array to PNG and save."""
    array = np.array(pixels, dtype='uint8')
    img = Image.fromarray(array, 'RGBA')
    img.save(filepath)
    print(f"Saved: {filepath}")

def generate_tile(tile_type: str, size: Tuple[int, int] = (8, 8)) -> str:
    """Generate a tile of given type and size, save as PNG."""
    prompt = f"""
    Generate a {size[0]}x{size[1]} RGBA pixel array for a {tile_type} tile.
    Use colors appropriate for {tile_type} (e.g., green for grass, blue for water).
    Output as a Python list of lists of RGBA tuples (0-255).
    Example format:
    [
        [(255, 0, 0, 255), (0, 255, 0, 255)],
        [(0, 0, 255, 255), (255, 255, 0, 255)]
    ]
    """
    # Replace with actual LLM call in production
    llm_output = mock_llm_generate(prompt)
    pixels = parse_rgba_array(llm_output)

    # Ensure output matches requested size
    if len(pixels) != size[0] or any(len(row) != size[1] for row in pixels):
        raise ValueError(f"Generated tile size mismatch. Expected {size}, got {len(pixels)}x{len(pixels[0])}")

    filepath = f"sprites/generated/{tile_type}_{size[0]}x{size[1]}.png"
    save_as_png(pixels, filepath)
    return filepath

if __name__ == "__main__":
    # Example usage
    import os
    os.makedirs("sprites/generated", exist_ok=True)

    tiles = ["grass", "water", "dirt", "stone"]
    for tile in tiles:
        generate_tile(tile, size=(8, 8))