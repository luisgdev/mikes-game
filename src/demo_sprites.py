#!/usr/bin/env python3
"""
Demo script to generate sprites using LLM and display them in a Pygame window.
"""

import pygame
import sys
from typing import List, Tuple

# Local imports
from src.llm import LLMGenerator
from src.generate_tile import save_as_png


def generate_and_save_tiles(tile_types: List[str], size: int = 16) -> None:
    """Generate tiles using LLM and save them as PNG files."""
    generator = LLMGenerator()
    
    for tile_type in tile_types[:2]:  # Generate only 2 tiles for demo
        tile = generator.generate_rgba_tile(tile_type, size=size)
        filepath = f"sprites/generated/{tile_type}_{size}x{size}.png"
        save_as_png(tile, filepath)
        print(f"Generated and saved {tile_type} tile to {filepath}")


def load_tile(filepath: str) -> pygame.Surface:
    """Load a tile image and return it as a Pygame surface."""
    try:
        surface = pygame.image.load(filepath)
        return surface.convert_alpha()
    except pygame.error as e:
        print(f"Error loading {filepath}: {e}")
        return pygame.Surface((16, 16))


def main() -> None:
    """Main function to generate tiles and display them in a Pygame window."""
    # Initialize Pygame
    pygame.init()
    
    # Generate and save tiles
    tile_types = ["grass", "water", "dirt", "stone"]
    size = 16
    generate_and_save_tiles(tile_types, size)
    
    # Load generated tiles (only the first 2 for demo)
    tiles = []
    for tile_type in tile_types[:2]:
        filepath = f"sprites/generated/{tile_type}_{size}x{size}.png"
        tile_surface = load_tile(filepath)
        tiles.append(tile_surface)
    
    # Set up the display
    screen_width = 400
    screen_height = 200
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("LLM-Generated Tiles Demo")
    
    # Main game loop
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Clear the screen
        screen.fill((0, 0, 0))
        
        # Display tiles
        for i, tile in enumerate(tiles):
            x = 50 + i * (size + 20)
            y = 50
            screen.blit(tile, (x, y))
            
            # Draw tile name
            font = pygame.font.Font(None, 24)
            text = font.render(tile_types[i], True, (255, 255, 255))
            screen.blit(text, (x, y + size + 10))
        
        # Update the display
        pygame.display.flip()
        clock.tick(60)
    
    # Quit Pygame
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
