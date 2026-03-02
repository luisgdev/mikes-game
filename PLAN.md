# Mike’s Journey Home
- **Genre:** 2D 8-bit Endless Runner / Platformer
- **Inspiration:** Flappy Bird + T-Rex Dinosaur Game
- **Main Character:** Mike, an orange cat
- **Objective:** Navigate through procedurally generated levels, avoid traps, collect power-ups, and reach Paris.

---

## **1. Project Overview**
- **Core Stack:** Pygame, Mistral AI (Ministral/Large), `mistralai` Python SDK
- **Procedural Generation:** Mistral AI generates level layouts, obstacle/collectible placement, and climate.
- **Visual Style:** 8-bit pixel art, SVG/PNG sprites, parallax scrolling.
- **Gameplay:** Side-scrolling platformer with jumping mechanics.

---

## **2. Technical Architecture**

### **2.1 Core Components**
| Component         | Technology/Tool          | Description                                                          |
|-------------------|--------------------------|----------------------------------------------------------------------|
| Game Engine       | Pygame                   | Handles rendering, input, game loop, and collision detection.        |
| AI/Procedural Gen | Mistral AI + `mistralai` | Generates level layouts, obstacle/collectible placement and climate. |
| Asset Management  | Custom sprite loader     | Loads and renders SVG/PNG sprites.                                   |
| Energy System     | Pygame + Custom Class    | Tracks Mike’s energy (5 max) renders energy bar, handles collisions. |

---

### **2.2 File Structure**
```
mikes_journey/
├── assets/
│   ├── sprites/
│   │   ├── characters/
│   │   ├── locations/
│   │   ├── floor/
│   │   ├── collectibles/
│   │   ├── energy.svg
│   │   └── ...
│   └── sounds/
├── src/
│   ├── main.py              # Main game loop and entry point
│   ├── level.py             # Level generation and management
│   ├── player.py            # Mike’s logic and animations
│   ├── energy.py            # Energy system logic
│   ├── obstacles.py         # Obstacle and enemy logic
│   ├── collectibles.py      # Collectible and power-up logic
│   ├── ai_procedural.py     # Mistral AI integration for procedural generation
│   └── utils.py             # Helper functions (e.g., SVG loading)
├── PLAN.md
└── README.md
```

---

## **3. Implementation Plan**

### **3.1 Setup & Dependencies**
- Install Pygame: `uv add pygame`
- Install Mistral AI SDK: `uv add mistralai`
- Install SVG renderer: `uv add cairosvg`

---

### **3.2 Step-by-Step Development**

#### **Step 1: Initialize Pygame Project**
- Set up the basic Pygame window and game loop using `uv run main.py`.
- Load and render a placeholder sprite for Mike.

#### **Step 2: Implement Mike’s Movement**
- Add jumping and walking animations using provided GIFs.
- Implement basic collision detection with the ground.

#### **Step 3: Energy System**
- Create the `EnergySystem` class (see code above).
- Render the energy bar at the top of the screen.
- Implement logic for losing energy on collision.

#### **Step 4: Mistral AI Integration**
- Set up the `mistralai` client.
- Design prompts for level generation (e.g., obstacles, collectibles, checkpoints).
- Parse Mistral’s output and dynamically build levels in Pygame.

#### **Step 5: Procedural Level Generation**
- For each level (Tokyo, NYC, Paris), generate:
  - Obstacle placement
  - Collectible placement
  - Checkpoints
  - Climate and daylight
- Use Mistral AI to suggest new sprites or level themes.

#### **Step 6: Obstacles & Collectibles**
- Implement obstacle and collectible classes.
- Add logic for Mike to interact with collectibles (e.g., gain power-ups).

#### **Step 7: Climate & Daylight Effects**
- Use Mistral AI to generate climate/lighting conditions.
- Apply visual effects in Pygame (e.g., rain, fog, night tint).

#### **Step 8: Timer & Scoreboard**
- Implement a timer to track the time taken to complete each level.
- Create a scoreboard that ranks players based on the smallest amount of seconds taken to reach the goal.

#### **Step 9: UI & Polish**
- Add a start screen, game over screen, and level transition screens.
- Implement sound effects for collecting items, losing energy, and level completion.

#### **Step 10: Testing & Debugging**
- Test each level for playability and balance.
- Debug collision detection, energy loss logic, and timer functionality.

#### **Step 11: Deployment**
- Package the game for distribution (e.g., PyInstaller).
- Write a README with instructions for running the game.

---

## **4. Key Features**
- **Procedural Levels:** Unique layouts for each playthrough.
- **Energy System:** Visual feedback for collisions.
- **AI-Driven Design:** Mistral AI generates level content dynamically.
- **Scalable:** Easy to add new cities, obstacles, or mechanics.

---

## **5. Risks & Mitigations**
| Risk                               | Mitigation                                                             |
|------------------------------------|------------------------------------------------------------------------|
| Mistral AI output is inconsistent  | Validate and post-process AI output before using it in-game.           |
| SVG rendering is slow              | Pre-render SVGs to PNGs during development.                            |
| Collision detection is buggy       | Use Pygame’s `Rect` and `spritecollide` for robust collision handling. |
| Game becomes too hard/easy         | Balance energy, obstacle density, and collectibles via playtesting.    |

---

## **6. Timeline (Example)**
| Task                          | Estimated Time |
|-------------------------------|----------------|
| Setup & Basic Pygame Loop     | 2 hours        |
| Mike’s Movement & Animations  | 4 hours        |
| Energy System                 | 2 hours        |
| Mistral AI Integration        | 4 hours        |
| Procedural Level Generation   | 6 hours        |
| Obstacles & Collectibles      | 4 hours        |
| Climate & UI Polish           | 4 hours        |
| Timer & Scoreboard             | 3 hours        |
| Testing & Debugging           | 4 hours        |
| Deployment & Documentation    | 2 hours        |

---

## **7. Open Questions**
- Should Mike have a “super jump” power-up?

---


### **Next Steps**
1. **Review the plan** for completeness and feasibility.
2. **Prioritize tasks** based on your timeline and resources.
3. **Start with the core loop** (Pygame setup, Mike’s movement, energy system).
