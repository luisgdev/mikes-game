#!/usr/bin/env python3
"""Main game loop for Mike's Journey Home - Runner Game."""

import pygame
import sys
import os

def load_sprite(path: str, scale: float = 1.0) -> pygame.Surface:
    """Load and scale a sprite image."""
    try:
        sprite = pygame.image.load(path)
        if scale != 1.0:
            size = (int(sprite.get_width() * scale), int(sprite.get_height() * scale))
            sprite = pygame.transform.scale(sprite, size)
        return sprite.convert_alpha()
    except pygame.error as e:
        print(f"Error loading sprite {path}: {e}")
        # Create a fallback surface
        surface = pygame.Surface((32, 32), pygame.SRCALPHA)
        surface.fill((255, 0, 255, 128))  # Magenta with transparency
        return surface

class Ground:
    """Class to handle the scrolling ground with dirt and grass layers."""
    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.scroll_speed = 4
        self.scroll_position = 0
        
        # Load ground tiles
        sprite_dir = os.path.join(os.path.dirname(__file__), "..", "sprites")
        
        # Try to load generated grass, fallback to default
        grass_path = os.path.join(sprite_dir, "generated", "grass_16x16.png")
        if not os.path.exists(grass_path):
            grass_path = os.path.join(sprite_dir, "floor", "grass_tile.png")
        
        dirt_path = os.path.join(sprite_dir, "floor", "ground_tile.png")
        
        self.grass_tile = load_sprite(grass_path, scale=2.0)
        self.dirt_tile = load_sprite(dirt_path, scale=2.0)
        
        # Ground dimensions
        self.tile_width = self.grass_tile.get_width()
        self.tile_height = self.grass_tile.get_height()
        self.ground_height = 4  # 4 tiles high
        
    def update(self):
        """Update scroll position."""
        self.scroll_position += self.scroll_speed
        
        # Reset position when we've scrolled a full screen width
        if self.scroll_position > self.tile_width:
            self.scroll_position = 0
    
    def draw(self, screen: pygame.Surface):
        """Draw the scrolling ground."""
        # Draw dirt base (3 tiles high)
        for y in range(3):
            self._draw_layer(screen, self.dirt_tile, y)
        
        # Draw grass top layer (1 tile high)
        self._draw_layer(screen, self.grass_tile, 3)
    
    def _draw_layer(self, screen: pygame.Surface, tile: pygame.Surface, layer: int):
        """Draw a single layer of tiles."""
        # Calculate y position for this layer
        y_pos = self.screen_height - (self.ground_height - layer) * self.tile_height
        
        # Draw tiles with scrolling effect
        for x in range(-1, (self.screen_width // self.tile_width) + 2):
            # Calculate x position with scrolling
            x_pos = (x * self.tile_width) - (self.scroll_position % self.tile_width)
            
            # Draw tile
            screen.blit(tile, (x_pos, y_pos))
            
            # Draw second copy for seamless scrolling
            screen.blit(tile, (x_pos + self.tile_width, y_pos))
    
    def get_top_position(self) -> int:
        """Get the y position of the top of the ground."""
        return self.screen_height - self.ground_height * self.tile_height

class Mike:
    """Class to handle Mike's character with animations."""
    
    def __init__(self, screen_width: int, screen_height: int, ground_top: int, grass_tile_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.ground_top = ground_top
        self.grass_tile_height = grass_tile_height
        
        # Load Mike's sprites
        sprite_dir = os.path.join(os.path.dirname(__file__), "..", "sprites", "characters", "mike")
        
        # Load walking animation frames (GIF)
        try:
            walking_gif = pygame.image.load(os.path.join(sprite_dir, "cat-walking.gif"))
            # Convert GIF to frames (simple approach - split the GIF)
            self.walking_frames = []
            # For simplicity, we'll use the whole GIF as one frame for now
            # In a real game, you'd extract individual frames
            self.walking_frames.append(pygame.transform.scale(walking_gif, (
                int(walking_gif.get_width() * 0.4),
                int(walking_gif.get_height() * 0.4)
            )))
        except:
            # Fallback - create a simple walking animation
            self.walking_frames = []
            for i in range(2):
                surface = pygame.Surface((60, 80), pygame.SRCALPHA)
                pygame.draw.circle(surface, (255, 100, 0), (30, 40), 20)  # Orange cat
                pygame.draw.rect(surface, (0, 0, 0), (25, 60, 10, 20))  # Legs
                if i == 1:
                    pygame.draw.rect(surface, (0, 0, 0), (35, 60, 10, 20))  # Second leg position
                self.walking_frames.append(surface)
        
        # Load sitting sprite
        self.sitting_sprite = load_sprite(os.path.join(sprite_dir, "cat-stoped.gif"), scale=0.4)
        
        # Position and state
        self.x = screen_width // 4
        # Position Mike in the middle of the grass zone
        self.y = ground_top - self.sitting_sprite.get_height() + (grass_tile_height // 4)
        
        self.current_sprite = self.sitting_sprite
        self.is_walking = False
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.1  # Faster animation
        
        # Journey state
        self.journey_started = False
        self.journey_completed = False
        self.energy = 100  # Energy percentage
        self.goal_position = screen_width * 3  # Goal is 3 screens away
        
    def update(self, space_pressed: bool, dt: float, ground: 'Ground'):
        """Update Mike's state."""
        # Start journey with SPACE (only if not already started or completed)
        if space_pressed and not self.journey_started and not self.journey_completed:
            self.journey_started = True
            self.is_walking = True
            if self.walking_frames:
                self.current_sprite = self.walking_frames[0]
        
        # Once journey started, keep walking until goal or energy depletion
        if self.journey_started and not self.journey_completed:
            # Move Mike forward automatically
            self.x += ground.scroll_speed
            
            # Animation
            self.animation_timer += dt
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.animation_frame = (self.animation_frame + 1) % len(self.walking_frames)
                self.current_sprite = self.walking_frames[self.animation_frame]
            
            # Check if reached goal
            if self.x >= self.goal_position:
                self.journey_completed = True
                self.is_walking = False
                self.current_sprite = self.sitting_sprite
            
            # Check if energy depleted (for future obstacle collisions)
            if self.energy <= 0:
                self.journey_completed = True
                self.is_walking = False
                self.current_sprite = self.sitting_sprite
        
        # Update ground scroll speed based on journey state
        if self.journey_started and not self.journey_completed:
            ground.scroll_speed = 6  # Faster scrolling when walking
        else:
            ground.scroll_speed = 2  # Slower scrolling when sitting
    

    
    def draw(self, screen: pygame.Surface):
        """Draw Mike on the screen."""
        screen.blit(self.current_sprite, (self.x, self.y))

def main():
    """Initialize Pygame and set up the main game loop."""
    # Initialize Pygame
    pygame.init()
    
    # Set up the display
    screen_width = 1280
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Mike's Journey Home - Runner")
    
    # Colors
    WHITE = (255, 255, 255)
    BLUE = (135, 206, 235)  # Sky blue
    
    # Create ground
    ground = Ground(screen_width, screen_height)
    ground_top = ground.get_top_position()
    
    # Create Mike
    mike = Mike(screen_width, screen_height, ground_top, ground.tile_height)
    
    # Game state
    running = True
    space_pressed = False
    
    # Main game loop
    clock = pygame.time.Clock()
    
    while running:
        # Calculate delta time for smooth animations
        dt = clock.tick(60) / 1000.0  # Convert to seconds
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    space_pressed = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    space_pressed = False
        
        # Update game objects
        ground.update()
        mike.update(space_pressed, dt, ground)
        
        # Fill the screen with sky color
        screen.fill(BLUE)
        
        # Draw game objects
        ground.draw(screen)
        mike.draw(screen)
        
        # Draw instructions and status
        font = pygame.font.Font(None, 36)
        
        if not mike.journey_started and not mike.journey_completed:
            instruction = font.render("Press SPACE to start journey!", True, (255, 255, 255))
            instruction_rect = instruction.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(instruction, instruction_rect)
        elif mike.journey_completed:
            completion_text = font.render("Journey Completed! 🎉", True, (255, 215, 0))
            completion_rect = completion_text.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(completion_text, completion_rect)
        
        # Draw energy bar (top left)
        energy_text = font.render(f"Energy: {mike.energy}%", True, (255, 255, 255))
        screen.blit(energy_text, (20, 20))
        
        # Draw distance progress
        distance = min(100, (mike.x / mike.goal_position) * 100)
        distance_text = font.render(f"Progress: {int(distance)}%", True, (255, 255, 255))
        screen.blit(distance_text, (20, 60))
        
        # Update the display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(60)
    
    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()