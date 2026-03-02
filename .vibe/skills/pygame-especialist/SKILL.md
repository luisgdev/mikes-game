---
name: pygame-2d-game-creator
description: >
  Creates 2D games using Pygame, following object-oriented programming (OOP) and clean code practices.
  This skill can generate game prototypes, levels, or full games with modular and reusable components.
  Useful for rapid prototyping, educational purposes, or as a foundation for more complex game projects.
user-invocable: true
version: 1.0.0
license: MIT
---

## **Agent Skill: Pygame 2D Game Creator**

## **Input Schema**
```yaml
type: object
properties:
  game_type:
    type: string
    enum: [platformer, roguelike, puzzle, arcade, rpg]
    description: The type of game to create.
    default: platformer
  game_title:
    type: string
    description: The title of the game.
    default: My Pygame Adventure
  screen_width:
    type: integer
    description: The width of the game window.
    default: 800
  screen_height:
    type: integer
    description: The height of the game window.
    default: 600
  player_character:
    type: object
    description: Configuration for the player character.
    properties:
      sprite:
        type: string
        description: Path to the player sprite image or description for procedural generation.
        default: player.png
      speed:
        type: integer
        description: Movement speed of the player.
        default: 5
      jump_height:
        type: integer
        description: Jump height of the player (for platformers).
        default: 10
  levels:
    type: array
    description: List of levels to generate.
    items:
      type: object
      properties:
        layout:
          type: string
          description: Path to a level layout file (e.g., JSON or CSV) or a procedural generation description.
          default: level1.json
        theme:
          type: string
          description: Visual theme of the level (e.g., forest, dungeon, space).
          default: forest
        enemies:
          type: array
          description: List of enemies in the level.
          items:
            type: object
            properties:
              sprite:
                type: string
                description: Path to the enemy sprite.
                default: enemy.png
              speed:
                type: integer
                description: Movement speed of the enemy.
                default: 2
              health:
                type: integer
                description: Health points of the enemy.
                default: 10
  ui_elements:
    type: array
    description: List of UI elements to include (e.g., score, health bar).
    items:
      type: object
      properties:
        type:
          type: string
          enum: [score, health_bar, inventory, menu]
          description: Type of UI element.
        position:
          type: string
          description: Position of the UI element (e.g., top-left, bottom-right).
          default: top-left
  use_llm:
    type: boolean
    description: Whether to use an LLM for procedural content generation (e.g., level layouts, quests).
    default: false
  clean_code:
    type: boolean
    description: Enforce clean code practices (e.g., type hints, docstrings, modular design).
    default: true
required:
  - game_type
  - game_title
```

---

## **Output Schema**
```yaml
type: object
properties:
  game_files:
    type: object
    description: Generated game files and assets.
    properties:
      main_script:
        type: string
        format: binary
        description: The main Python script for the game.
      assets:
        type: array
        description: List of generated or referenced asset files.
        items:
          type: object
          properties:
            path:
              type: string
              description: Path to the asset file.
            type:
              type: string
              description: Type of asset (e.g., sprite, tileset, sound).
      level_files:
        type: array
        description: List of generated level files.
        items:
          type: object
          properties:
            path:
              type: string
              description: Path to the level file.
            theme:
              type: string
              description: Theme of the level.
  metadata:
    type: object
    description: Metadata about the generated game.
    properties:
      game_type:
        type: string
        description: The type of game created.
      game_title:
        type: string
        description: The title of the game.
      screen_resolution:
        type: string
        description: The resolution of the game window.
      levels:
        type: integer
        description: The number of levels generated.
      timestamp:
        type: string
        format: date-time
        description: When the game was created.
      clean_code:
        type: boolean
        description: Whether clean code practices were enforced.
      llm_used:
        type: boolean
        description: Whether an LLM was used for procedural generation.
```

---

## **Examples**

---

### **Example 1: Generate a Platformer Game**
**Input:**
```json
{
  "game_type": "platformer",
  "game_title": "Forest Adventure",
  "screen_width": 800,
  "screen_height": 600,
  "player_character": {
    "sprite": "player.png",
    "speed": 5,
    "jump_height": 10
  },
  "levels": [
    {
      "layout": "level1.json",
      "theme": "forest",
      "enemies": [
        {
          "sprite": "goblin.png",
          "speed": 2,
          "health": 10
        }
      ]
    }
  ],
  "ui_elements": [
    {
      "type": "score",
      "position": "top-left"
    },
    {
      "type": "health_bar",
      "position": "top-right"
    }
  ],
  "use_llm": false,
  "clean_code": true
}
```

**Output:**
```json
{
  "game_files": {
    "main_script": "[binary Python script data]",
    "assets": [
      {"path": "player.png", "type": "sprite"},
      {"path": "goblin.png", "type": "sprite"},
      {"path": "forest_tileset.png", "type": "tileset"}
    ],
    "level_files": [
      {"path": "level1.json", "theme": "forest"}
    ]
  },
  "metadata": {
    "game_type": "platformer",
    "game_title": "Forest Adventure",
    "screen_resolution": "800x600",
    "levels": 1,
    "timestamp": "2026-02-28T12:00:00Z",
    "clean_code": true,
    "llm_used": false
  }
}
```

---

### **Example 2: Generate a Roguelike Game**
**Input:**
```json
{
  "game_type": "roguelike",
  "game_title": "Dungeon Crawler",
  "screen_width": 1024,
  "screen_height": 768,
  "player_character": {
    "sprite": "hero.png",
    "speed": 4,
    "jump_height": 8
  },
  "levels": [
    {
      "layout": "procedural_dungeon",
      "theme": "dungeon",
      "enemies": [
        {
          "sprite": "skeleton.png",
          "speed": 1,
          "health": 15
        },
        {
          "sprite": "bat.png",
          "speed": 3,
          "health": 5
        }
      ]
    }
  ],
  "ui_elements": [
    {
      "type": "health_bar",
      "position": "top-right"
    },
    {
      "type": "inventory",
      "position": "bottom-right"
    }
  ],
  "use_llm": true,
  "clean_code": true
}
```

**Output:**
```json
{
  "game_files": {
    "main_script": "[binary Python script data]",
    "assets": [
      {"path": "hero.png", "type": "sprite"},
      {"path": "skeleton.png", "type": "sprite"},
      {"path": "bat.png", "type": "sprite"},
      {"path": "dungeon_tileset.png", "type": "tileset"}
    ],
    "level_files": [
      {"path": "dungeon_level1.json", "theme": "dungeon"}
    ]
  },
  "metadata": {
    "game_type": "roguelike",
    "game_title": "Dungeon Crawler",
    "screen_resolution": "1024x768",
    "levels": 1,
    "timestamp": "2026-02-28T12:05:00Z",
    "clean_code": true,
    "llm_used": true
  }
}
```

---

## **Execution Logic (Pseudocode)**
```python
def pygame_2d_game_creator(input):
    # Parse input
    game_type = input["game_type"]
    game_title = input["game_title"]
    screen_width = input.get("screen_width", 800)
    screen_height = input.get("screen_height", 600)
    player_config = input.get("player_character", {})
    levels = input.get("levels", [])
    ui_elements = input.get("ui_elements", [])
    use_llm = input.get("use_llm", False)
    clean_code = input.get("clean_code", True)

    # Generate game structure
    game_files = {}
    assets = []
    level_files = []

    # Generate main script
    main_script = generate_main_script(
        game_type=game_type,
        game_title=game_title,
        screen_width=screen_width,
        screen_height=screen_height,
        player_config=player_config,
        levels=levels,
        ui_elements=ui_elements,
        clean_code=clean_code,
    )
    game_files["main_script"] = main_script

    # Generate assets and levels
    for level in levels:
        level_layout = level.get("layout", "")
        theme = level.get("theme", "forest")
        enemies = level.get("enemies", [])

        # Generate level file (procedural or from template)
        if use_llm and level_layout == "procedural_dungeon":
            level_file = generate_procedural_level(theme, enemies)
        else:
            level_file = load_or_generate_level(level_layout, theme, enemies)

        level_files.append({
            "path": level_file["path"],
            "theme": theme,
        })

        # Collect assets
        for enemy in enemies:
            assets.append({
                "path": enemy["sprite"],
                "type": "sprite",
            })
        assets.append({
            "path": f"{theme}_tileset.png",
            "type": "tileset",
        })

    # Add player sprite
    assets.append({
        "path": player_config["sprite"],
        "type": "sprite",
    })

    # Create metadata
    metadata = {
        "game_type": game_type,
        "game_title": game_title,
        "screen_resolution": f"{screen_width}x{screen_height}",
        "levels": len(levels),
        "timestamp": datetime.now().isoformat(),
        "clean_code": clean_code,
        "llm_used": use_llm,
    }

    # Return output
    return {
        "game_files": {
            "main_script": main_script,
            "assets": assets,
            "level_files": level_files,
        },
        "metadata": metadata,
    }

# Placeholder functions
def generate_main_script(game_type, game_title, screen_width, screen_height, player_config, levels, ui_elements, clean_code):
    # Generate Python script using OOP and clean code practices
    script = f"""# {game_title} - A {game_type} game created with Pygame
import pygame
import sys
from typing import List, Dict, Optional

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = {screen_width}
SCREEN_HEIGHT = {screen_height}
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("{game_title}")
CLOCK = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game states
class GameState:
    def __init__(self):
        self.running = True
        self.score = 0

# Player class
class Player:
    def __init__(self, x: int, y: int, sprite: str, speed: int, jump_height: int):
        self.x = x
        self.y = y
        self.sprite = pygame.image.load(sprite)
        self.speed = speed
        self.jump_height = jump_height
        self.health = 100

    def move(self, dx: int, dy: int):
        self.x += dx * self.speed
        self.y += dy * self.speed

    def draw(self, surface):
        surface.blit(self.sprite, (self.x, self.y))

# Enemy class
class Enemy:
    def __init__(self, x: int, y: int, sprite: str, speed: int, health: int):
        self.x = x
        self.y = y
        self.sprite = pygame.image.load(sprite)
        self.speed = speed
        self.health = health

    def move(self, dx: int, dy: int):
        self.x += dx * self.speed
        self.y += dy * self.speed

    def draw(self, surface):
        surface.blit(self.sprite, (self.x, self.y))

# Level class
class Level:
    def __init__(self, layout: str, theme: str, enemies: List[Dict]):
        self.layout = layout
        self.theme = theme
        self.enemies = [Enemy(e["x"], e["y"], e["sprite"], e["speed"], e["health"]) for e in enemies]

    def draw(self, surface):
        # Draw level layout and enemies
        pass

# UI classes
class UIElement:
    def __init__(self, element_type: str, position: str):
        self.type = element_type
        self.position = position

    def draw(self, surface, game_state):
        # Draw UI element based on type and position
        pass

# Main game class
class Game:
    def __init__(self):
        self.state = GameState()
        self.player = Player(100, 100, "{player_config['sprite']}", {player_config['speed']}, {player_config['jump_height']})
        self.levels = [Level(l["layout"], l["theme"], l["enemies"]) for l in {levels}]
        self.current_level = 0
        self.ui_elements = [UIElement(ui["type"], ui["position"]) for ui in {ui_elements}]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state.running = False

    def update(self):
        # Update game state, player, enemies, etc.
        pass

    def draw(self):
        SCREEN.fill(BLACK)
        self.levels[self.current_level].draw(SCREEN)
        self.player.draw(SCREEN)
        for ui in self.ui_elements:
            ui.draw(SCREEN, self.state)
        pygame.display.flip()

    def run(self):
        while self.state.running:
            self.handle_events()
            self.update()
            self.draw()
            CLOCK.tick(FPS)
        pygame.quit()
        sys.exit()

# Run the game
if __name__ == "__main__":
    game = Game()
    game.run()
"""
    return script.encode("utf-8")

def generate_procedural_level(theme, enemies):
    # Use LLM or procedural generation to create a level
    pass

def load_or_generate_level(layout, theme, enemies):
    # Load from file or generate a level
    pass
```

---

## **Dependencies**
- **Pygame:** For game development and rendering.
- **Optional LLM Integration:** For procedural content generation (e.g., level layouts, quests).
- **Type Hints and Clean Code Tools:** `mypy`, `pylint`, or `flake8` for code quality.

---

## **Error Handling**
- **Invalid Game Type:** Return an error if `game_type` is not supported.
- **Missing Assets:** Fall back to placeholder assets or generate simple shapes.
- **LLM Failure:** Use predefined templates if LLM generation fails.

---

## **Clean Code Practices Enforced**
- **Modular Design:** Separate classes for `Player`, `Enemy`, `Level`, and `UIElement`.
- **Type Hints:** Use Python type hints for better code clarity.
- **Docstrings:** Include docstrings for all classes and methods.
- **Constants:** Use constants for screen dimensions, colors, etc.
- **Separation of Concerns:** Keep game logic, rendering, and input handling separate.

---

## **Usage Example in an Agent Workflow**
```yaml
- use: pygame_2d_game_creator
  with:
    game_type: "platformer"
    game_title: "Forest Adventure"
    screen_width: 800
    screen_height: 600
    player_character:
      sprite: "player.png"
      speed: 5
      jump_height: 10
    levels:
      - layout: "level1.json"
        theme: "forest"
        enemies:
          - sprite: "goblin.png"
            speed: 2
            health: 10
    ui_elements:
      - type: "score"
        position: "top-left"
      - type: "health_bar"
        position: "top-right"
    use_llm: false
    clean_code: true
  next:
    - if: success
      then:
        - save_game_files
        - notify_user
    - if: error
      then:
        - log_error
        - retry_or_fallback
```

---

## **Notes**
- This skill generates a **modular**, **object-oriented**, and **clean** Pygame project, making it easy to extend or modify.
- For procedural content, you can integrate with an LLM (e.g., Mistral API) to generate levels, quests, or dialogue.
- The generated code is ready for further development, testing, and deployment.

