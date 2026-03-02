---
name: pixel-art-creator
description: >
  Creates authentic pixel art graphics for 2D game development, including sprites, tilesets, animations, and UI elements.
  Useful for designing game assets, creating sprite sheets, building tilesets for procedural generation, animating characters, or designing game interfaces for pixel art games like roguelikes.
user-invocable: true
version: 1.0.0
license: MIT
---

## **Agent Skill: Pixel Art Creator**

### **Input Schema**
```yaml
type: object
properties:
  asset_type:
    type: string
    enum: [sprite, tileset, animation, ui_element]
    description: The type of pixel art asset to create.
  theme:
    type: string
    description: The visual theme or style (e.g., fantasy, sci-fi, retro, dungeon).
    default: fantasy
  resolution:
    type: string
    enum: [8x8, 16x16, 32x32, 64x64]
    description: The resolution of each tile or sprite.
    default: 16x16
  color_palette:
    type: string
    description: A description of the color palette (e.g., "16-bit retro," "monochrome," "vibrant fantasy").
    default: 16-bit retro
  description:
    type: string
    description: A detailed description of the asset (e.g., "a knight sprite with sword and shield, idle animation").
  output_format:
    type: string
    enum: [png, gif, json, sprite_sheet]
    description: The format of the output file.
    default: png
  num_frames:
    type: integer
    description: The number of animation frames (for animations).
    default: 4
  transparency:
    type: boolean
    description: Whether the output should support transparency.
    default: true
required:
  - asset_type
  - description
```

---

### **Output Schema**
```yaml
type: object
properties:
  asset:
    type: string
    format: binary
    description: The generated pixel art asset (image or sprite sheet).
  metadata:
    type: object
    description: Metadata about the generated asset.
    properties:
      asset_type:
        type: string
        description: The type of asset created.
      resolution:
        type: string
        description: The resolution of the asset.
      color_palette:
        type: string
        description: The color palette used.
      frames:
        type: integer
        description: The number of frames (for animations).
      theme:
        type: string
        description: The visual theme of the asset.
      timestamp:
        type: string
        format: date-time
        description: When the asset was created.
```

---

### **Examples**

#### **Example 1: Generate a Sprite**
**Input:**
```json
{
  "asset_type": "sprite",
  "theme": "fantasy",
  "resolution": "16x16",
  "color_palette": "16-bit retro",
  "description": "A knight sprite with sword and shield, facing right, idle pose.",
  "output_format": "png",
  "transparency": true
}
```

**Output:**
```json
{
  "asset": "[binary png data]",
  "metadata": {
    "asset_type": "sprite",
    "resolution": "16x16",
    "color_palette": "16-bit retro",
    "theme": "fantasy",
    "timestamp": "2026-02-28T12:00:00Z"
  }
}
```

---

#### **Example 2: Generate a Tileset**
**Input:**
```json
{
  "asset_type": "tileset",
  "theme": "dungeon",
  "resolution": "16x16",
  "color_palette": "dark fantasy",
  "description": "A dungeon tileset with walls, floors, doors, and traps.",
  "output_format": "png",
  "transparency": true
}
```

**Output:**
```json
{
  "asset": "[binary png data]",
  "metadata": {
    "asset_type": "tileset",
    "resolution": "16x16",
    "color_palette": "dark fantasy",
    "theme": "dungeon",
    "timestamp": "2026-02-28T12:05:00Z"
  }
}
```

---

#### **Example 3: Generate an Animation**
**Input:**
```json
{
  "asset_type": "animation",
  "theme": "retro",
  "resolution": "32x32",
  "color_palette": "monochrome",
  "description": "A walking animation for a robot character, 4 frames.",
  "output_format": "gif",
  "num_frames": 4,
  "transparency": true
}
```

**Output:**
```json
{
  "asset": "[binary gif data]",
  "metadata": {
    "asset_type": "animation",
    "resolution": "32x32",
    "color_palette": "monochrome",
    "frames": 4,
    "theme": "retro",
    "timestamp": "2026-02-28T12:10:00Z"
  }
}
```

---

### **Execution Logic (Pseudocode)**
```python
def pixel_art_creator(input):
    # Parse input
    asset_type = input["asset_type"]
    theme = input.get("theme", "fantasy")
    resolution = input.get("resolution", "16x16")
    color_palette = input.get("color_palette", "16-bit retro")
    description = input["description"]
    output_format = input.get("output_format", "png")
    num_frames = input.get("num_frames", 4)
    transparency = input.get("transparency", True)

    # Generate pixel art (placeholder for actual generation logic)
    if asset_type == "sprite":
        asset = generate_sprite(theme, resolution, color_palette, description, transparency)
    elif asset_type == "tileset":
        asset = generate_tileset(theme, resolution, color_palette, description, transparency)
    elif asset_type == "animation":
        asset = generate_animation(theme, resolution, color_palette, description, num_frames, transparency)
    elif asset_type == "ui_element":
        asset = generate_ui_element(theme, resolution, color_palette, description, transparency)

    # Create metadata
    metadata = {
        "asset_type": asset_type,
        "resolution": resolution,
        "color_palette": color_palette,
        "theme": theme,
        "timestamp": datetime.now().isoformat(),
    }
    if asset_type == "animation":
        metadata["frames"] = num_frames

    # Return output
    return {
        "asset": asset,
        "metadata": metadata,
    }

# Placeholder functions
def generate_sprite(theme, resolution, color_palette, description, transparency):
    # Use a pixel art generation library or API
    # Example: Use Aseprite API, Piskel, or a custom pixel art generator
    pass

def generate_tileset(theme, resolution, color_palette, description, transparency):
    pass

def generate_animation(theme, resolution, color_palette, description, num_frames, transparency):
    pass

def generate_ui_element(theme, resolution, color_palette, description, transparency):
    pass
```

---

### **Dependencies**
- **Pixel Art Generation:**
  - [Aseprite](https://www.aseprite.org/) (via CLI or API)
  - [Piskel](https://www.piskelapp.com/) (open-source pixel art tool)
  - [Python Imaging Library (Pillow)](https://pillow.readthedocs.io/) for image manipulation
- **Animation:**
  - Pillow for GIF creation
  - [Pyxel](https://github.com/kitao/pyxel) for retro pixel art and animations
- **Color Palettes:**
  - [Lospec Palette List](https://lospec.com/palette-list)
  - Custom palette generation scripts

---

### **Error Handling**
- **Invalid Input:** Return an error if `asset_type` or `resolution` is invalid.
- **Generation Failure:** Retry or return a placeholder asset if generation fails.
- **Unsupported Format:** Default to PNG if the requested format is unsupported.

---

### **Notes**
- For actual pixel art generation, you can integrate with tools like **Aseprite**, **Piskel**, or use **Python libraries** (e.g., Pillow, Pyxel) to create and manipulate pixel art programmatically.
- For more advanced features (e.g., animation), consider using **sprite sheet generators** or **GIF creation tools**.
- This skill is designed to be modular, so you can replace the placeholder generation functions with actual implementations or API calls.

---

### **Usage Example in an Agent Workflow**
```yaml
- use: pixel_art_creator
  with:
    asset_type: "tileset"
    theme: "dungeon"
    resolution: "16x16"
    color_palette: "dark fantasy"
    description: "A dungeon tileset with walls, floors, doors, and traps."
    output_format: "png"
  next:
    - if: success
      then:
        - save_asset_to_disk
        - notify_user
    - if: error
      then:
        - log_error
        - retry_or_fallback
```

---

This skill provides a flexible and reusable way to generate pixel art assets for your game development pipeline.