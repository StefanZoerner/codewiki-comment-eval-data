# Umoria Architecture Overview

Umoria is a classic dungeon-crawling roguelike, originally derived from Moria (created at UC Berkeley) and later released as open source by Robert Alan Koeneke and James E. Wilson. It's written in C, and its architecture reflects its era (late 1980s) and its Unix/curses heritage. Here's what I know about its structure:

## Core Design Characteristics

**Procedural, not object-oriented**: Being written in C, the codebase relies on global state, structs, and procedural functions rather than any OOP abstraction. Most game state lives in large global structures rather than being passed around cleanly.

**Monolithic global game state**: There's typically a central "player" struct holding character stats, inventory, position, etc., and a "dungeon" or "cave" representation (often a 2D array of tile/feature structs) representing the current level. Because the whole game operates on a single level in memory at a time, level generation, monster placement, and rendering all reference this shared global grid.

## Major Subsystems

1. **Dungeon generation** — Procedural level generation code that carves rooms, corridors, and vaults, then populates them with monsters, items, and traps according to depth-based tables.

2. **Monster AI/movement** — A monster list/array with per-monster state (hp, position, memory of the player) updated each turn in a fairly simple, deterministic loop (no complex FOV/pathing—closer to line-of-sight and Manhattan-distance chasing).

3. **Combat and command interpretation** — A dispatch loop reads a keypress and calls a handler function; combat resolution (to-hit, damage, criticals) is table-driven based on class/race/equipment.

4. **Items/inventory system** — Item templates in static tables (often loaded from data files like the "misc" or scoring files) describing weapons, armor, potions, scrolls, etc., with instances holding modifiers (enchantment, curses).

5. **Display/UI layer** — Built on curses (or a term-io abstraction layer) to draw the map, status line, and messages. Umoria historically has a `term.c` or similar abstraction to isolate terminal-specific code, since it targeted multiple Unix terminal types.

6. **Save/load system** — Custom binary serialization of the global game state structures directly to disk, which is notoriously version-fragile (a common trait of that era's C save systems).

## Honest Caveat

I know Umoria's general architecture at a conceptual level (its lineage from Moria, its influence on Angband, and typical patterns of the code), but I do **not** have detailed, reliable knowledge of the actual current file layout, specific function names, or exact struct definitions in the modern GitHub repository (openmoria/umoria or similar). If you need precise details—specific filenames, function signatures, or the exact module breakdown—I'd be guessing rather than recalling verified facts, and I'd recommend checking the actual source tree.
