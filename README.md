# SantientPHP (SPH) Game Engine & 2D Platformer

<p align="center">
  <img src="assets/icon.png" width="180" height="180" alt="Bigfoot Game Engine Icon" />
  <br />
  <strong>A lightweight, high-performance 2D game engine built entirely in SantientPHP (SPH 0.1)</strong>
  <br />
  <em>Zero external runtime dependencies &bull; 60 FPS locked &bull; Native Win32 &bull; 128-bit SIMD Vector Acceleration</em>
</p>

---

## Overview

The **SantientPHP Game Engine** is a native, hardware-accelerated 2D platforming and level-creation framework built from the ground up to showcase the systems programming and GUI capabilities of **SantientPHP (SPH 0.1)**. 

The engine compiles to a single, standalone Windows native executable (`bin/game.exe`, ~496 KB) with an embedded application icon and **zero third-party DLL dependencies** (linking only standard Windows system libraries `kernel32`, `user32`, `gdi32`, `winmm`, and `opengl32`).

---

## Key Features

| Feature | Description |
| :--- | :--- |
| **Playable Character (Bigfoot)** | Imposing 24×32 Sasquatch protagonist derived from vector artwork with 4 animated frames (Idle, Walk 1, Walk 2, Jump), Patterson-Gimlin stride, calibrated $14\times28$ hitbox, and dynamic squash & stretch. |
| **Autonomous Procedural Level Generator** | Intelligent PCG system that continuously synthesizes endless new levels ($N \to \infty$) with guaranteed jump-arc reachability ($h_{\text{max}} = 69.8\text{px}$, $d_{\text{max}} = 105.7\text{px}$), 4 rotating biomes, procedural seeds, auto-placed springs & checkpoints, and recurring Boss Arenas every 5 stages. |
| **4-Channel Chiptune Synthesizer** | Lock-free software sound mixer running on a dedicated thread using Windows' built-in `winmm.dll` (`waveOutOpen`/`waveOutWrite` at 44.1 kHz 16-bit PCM) with Square, Triangle, Sawtooth, and White Noise waves, pitch envelopes, and level-specific BGM tracks. |
| **SIMD 2D Dynamic Lighting** | Dark ambient lightmap pass in subterranean and volcanic biomes where Bigfoot's lantern, checkpoints, and torches emit radial glow computed 4 pixels at a time via SSE2 intrinsics (`sph_canvas_apply_lighting_simd`). |
| **Window & Rendering Engine** | Native Win32 window management (`sph_gui_window_*`), non-blocking message pump, aspect-ratio scaling fullscreen, and dual rendering: **Tier-2 SIMD Framebuffer Canvas** (`sph_canvas_*`, Bresenham lines, midpoint circles, 5x7 bitmap font rasterizer) + **Hardware OpenGL 2D Pipeline** (`sph_gl_*`). |
| **Platformer Juice** | 0.12s jump buffering, coyote time, 40-60ms hit-stop, decaying camera screen shake (`shake_intensity *= 0.85`), dynamic squash & stretch ($1.30\times$ / $0.70\times$), and reactive particle bursts. |
| **Reactive Enemy AI** | Multi-state FSM (Patrol &rarr; Alert &rarr; Chase) with `!` alert indicators, swoop chaser drones, predictive lead-time turrets, and the multi-phase Sky Knight boss. |
| **Dynamic World Mechanics** | Moving platforms with smooth velocity inheritance, crumbling blocks with 3s respawn timers, and checkpoint banners. |
| **Interactive Level Editor** | 4-bit bitmask auto-tiling, Ctrl+Z / Ctrl+Y undo/redo ring buffer, brush palette (1-9), disk serialization, and `F5` instant playtest from mouse cursor. |
| **Embedded Executable Icon** | Multi-resolution icon (`.ico`) embedded into resource ID 1 via `windres` and `sph.toml`, appearing in Windows File Explorer, taskbar, and window titlebar. |

---

## Autonomous Level Generator & Biomes

Once the hand-crafted trilogy is conquered, the engine switches to the **Autonomous Procedural Level Generator (PCG)**:

```
LVL 1: GREENFIELD MEADOWS          | Hand-Crafted Introduction
LVL 2: SPIKEFALL CAVERN            | Hand-Crafted Subterranean Spikes & SIMD Lighting
LVL 3: CASTLE OF THE SKY           | Hand-Crafted High Castle Ascent
LVL 4: SUNKEN VAULT [SEED #5094]   | PCG Synthesized Biome 3
LVL 5: OBSIDIAN CHASM [BOSS ARENA] | PCG Boss Battle: Sky Knight Arena
LVL 6: CRYSTAL CITADEL [SEED #932] | PCG Synthesized Biome 1
LVL 7: SHADOW CHASM [SEED #8851]   | PCG Synthesized Biome 2
...
LVL N: ...                         | Endless unique stages
```

### Rotating Biomes:
1. **Emerald Forest** (Biome 0): Daylight ambient, grass & dirt tiles, Ch. 1 lively chiptune track.
2. **Crystal Cavern** (Biome 1): Subterranean brick, crumbling bridges, hazard pits, and SIMD radial lantern glow.
3. **Sky Citadel** (Biome 2): High wind stone towers and chasms with Ch. 3 melody.
4. **Volcanic Vault** (Biome 3): Obsidian masonry, hazard trenches, fiery glow lighting, and Ch. 4 boss battle rush soundtrack.

### Reachability Physics:
* Gravity $g = 980 \text{ px/s}^2$, jump impulse $v = -370 \text{ px/s} \implies h_{\text{max}} = 69.8 \text{ px}$ (4.36 tiles), $d_{\text{max}} = 105.7 \text{ px}$ (6.6 tiles).
* Gaps wider than 3 tiles automatically receive **Moving Platforms** or **Crumbling Stepping Stones**.
* Platform ascents $\ge 3$ tiles automatically spawn **Super Spring Pads**.

---

## Controls

### Gameplay Mode
| Key | Action |
| :--- | :--- |
| **A / D** or **Left / Right** | Walk Left / Right |
| **Space / W / Up** | Jump (variable height, buffered, with coyote time) |
| **Tab / E** | Toggle Interactive Level Editor |
| **F5** | Playtest from Mouse Cursor |
| **F11** | Toggle Fullscreen (Aspect-ratio scaled) |
| **M** | Toggle Chiptune Synthesizer Mute |
| **R** | Restart / Reset Current Level |
| **Enter** | Advance to Next Stage upon Stage Clear |

### Level Editor Mode
| Key / Mouse | Action |
| :--- | :--- |
| **Left Click** | Paint selected brush tile onto grid |
| **Right Click** | Erase tile (Air) |
| **Keys 1 - 7** | Tile Brush: Grass (1), Dirt (2), Stone (3), Coin (4), Spikes (5), Spring (6), Flag (7) |
| **Keys 8 - 9** | Mechanics Brush: Crumbling Block (8), Checkpoint (9) |
| **Ctrl + Z** | Undo last tile change |
| **Ctrl + Y** | Redo last tile change |
| **S / L** | Save / Load level to `custom_level.dat` |

---

## Project Structure

```text
game/
├── assets/
│   ├── icon.ico               # Multi-resolution native Windows application icon (16x16 to 256x256)
│   └── icon.png               # High-resolution 256x256 master icon
├── bin/
│   └── game.exe               # Compiled standalone native executable with embedded icon (~496 KB)
├── lib/
│   ├── libsph_gui.a           # Precompiled native GUI runtime library
│   ├── libsph_runtime.a       # Aggregate SantientPHP runtime library
│   └── libsph_core.a          # Core runtime static library
├── src/
│   ├── engine/
│   │   ├── types.sph          # Primitives, Generics (Pair<T, U>), Vec2f, Rect, Color, String helpers
│   │   ├── simd_math.sph      # 128-bit SIMD vector acceleration (f32x4, i32x4, SSE/AVX detection)
│   │   ├── window.sph         # Win32 native window, DPI, client rect, message pump
│   │   ├── canvas.sph         # 32-bit RGBA SIMD canvas, primitives, 5x7 bitmap font rasterizer
│   │   ├── gl_render.sph      # Hardware OpenGL 2D pipeline (ortho projection, batch quads)
│   │   ├── texture.sph        # Procedural sprite atlas generator, memory management, blitter
│   │   ├── animation.sph      # Frame-based animation clips, state machine, atlas mapping
│   │   ├── collision.sph      # AABB intersection, spatial hash grid, SIMD batch box testing
│   │   ├── physics.sph        # Euler kinematics, gravity, drag, platformer controller, particles
│   │   ├── input.sph          # Direct GetAsyncKeyState polling, key edge detection, mouse coordinates
│   │   ├── audio.sph          # 4-channel threaded chiptune synth mixer (winmm.dll waveOut)
│   │   ├── ecs.sph            # Entity-Component-System definitions, FSM AI, archetypes
│   │   ├── scene.sph          # Scene state machine (Title, Gameplay, Editor, Victory, GameOver)
│   │   └── editor.sph         # Interactive level editor (auto-tiling, undo/redo, cursor playtest)
│   ├── game/
│   │   ├── levels.sph         # Hand-crafted trilogy + Autonomous Procedural Level Generator
│   │   └── platformer.sph     # Complete 2D platformer gameplay, camera, HUD, parallax background
│   └── main.sph               # Engine initialization, 60 FPS event loop, telemetry overlay, shutdown
├── stdlib/                    # SantientPHP Standard Library modules
├── build.ps1                  # PowerShell build and automation script
├── sph.toml                   # Compiler manifest configuration
└── README.md                  # Comprehensive engine and game documentation
```

---

## Build & Run

### Prerequisites
- **SantientPHP Compiler (`sphc`)**: SPH 0.1 compiler with Native GUI Subsystem support.
- **MinGW-w64 GCC**: GCC 14+ / 15+ toolchain (provides Win32, GDI, and OpenGL libraries).

### Using the Build Script (`build.ps1`)
```powershell
# 1. Semantic check only:
powershell -ExecutionPolicy Bypass -File .\build.ps1 -CheckOnly

# 2. Compile optimized release build with embedded icon:
powershell -ExecutionPolicy Bypass -File .\build.ps1 -Release

# 3. Build and launch game:
powershell -ExecutionPolicy Bypass -File .\build.ps1 -Run
```

### Direct Compiler Command (`sphc`)
```powershell
sphc build src/main.sph --gui -O3 -o bin/game.exe
.\bin\game.exe
```

---

## Systems Tested

- **128-bit SIMD Vector Acceleration**: Hardware SSE/AVX CPU feature detection (`Simd::has_sse()`, `Simd::has_avx()`), vector types (`f32x4`, `i32x4`), Euler step vectors, distance squared, bounding box clamp, and SSE2-accelerated canvas memset/blit/lighting.
- **Hardware OpenGL**: Context creation (`sph_gl_context_create`), double buffer swapping (`sph_gl_swap_buffers`), orthographic matrix projection (`glOrtho`), and hardware viewport management.
- **Native GUI Subsystem**: Win32 window creation, non-blocking message pump (`sph_gui_pump_events`), and native system dialogs (`sph_gui_messagebox`).
- **Memory Management & Pointers**: Manual allocation and deallocation (`sph_alloc`, `sph_free`), raw pointers (`*void`, `*i32`, `*i64`), `unsafe` blocks, and SantientPHP's borrow checker.
- **Value Structs & Generics**: Strongly typed structs for vectors, geometry, entity components, animations, and game state. Generic container instantiation (`Pair<T, U>`).
- **Event Loops**: Rock-solid 60 FPS non-blocking game loop with microsecond-accurate delta time calculation via Win32 `QueryPerformanceCounter`.

---

## License

This project is licensed under the MIT License.
