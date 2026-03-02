#!/usr/bin/env python3
"""
Demo script to display mock sprites in a Pygame window (no LLM calls).
"""

import pygame
import sys
from typing import List, Tuple


def create_mock_tile(color: Tuple[int, int, int], size: int = 16) -> pygame.Surface:
    """Create a mock tile surface with a solid color."""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    surface.fill(color)
    return surface


def main() -> None:
    """Main function to display mock tiles in a Pygame window."""
    # Initialize Pygame
    pygame.init()
    
    # Create mock tiles
    tile_types = ["grass", "water", "dirt", "stone"]
    colors = [
        (34, 139, 34),    # Grass green
        (65, 105, 225),   # Water blue
        (139, 69, 19),    # Dirt brown
        (128, 128, 128),  # Stone gray
    ]
    size = 16
    
    tiles = []
    for color in colors[:2]:  # Use only 2 tiles for demo
        tile = create_mock_tile(color, size)
        tiles.append(tile)
    
    # Set up the display
    screen_width = 400
    screen_height = 200
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Mock Tiles Demo")
    
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
