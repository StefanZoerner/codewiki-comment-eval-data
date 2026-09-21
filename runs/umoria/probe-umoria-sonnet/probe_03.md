# Umoria Architecture Overview

Umoria (the precursor to Moria and ancestor of Angband) is a classic C roguelike from the late 1980s/early 1990s. I have knowledge of its general structure, though I'll note upfront that my familiarity is stronger with its conceptual design than with exact file-by-file specifics of any particular version, since the codebase has had multiple releases over decades (original VMS/Unix version, later ports, and the more recent open-source revival).

## General Structure

**Language & Era**: Written in C, originally for VMS and Unix systems (1983-1990s), reflecting programming idioms of that period—lots of global state, fixed-size arrays, and file-based data rather than dynamic structures.

**Core Subsystems** (conceptually):

1. **Game State / Globals** – A large, heavily shared global state holds the player character, dungeon level, monster list, and object list. Most functions operate on this shared mutable state rather than passing objects around, which is typical of the era's C style.

2. **Dungeon Generation** – Level generation code builds room-and-corridor mazes using algorithmic room placement, corridor digging (often via a simple pathfinding/tunneling algorithm), and door/trap/treasure placement. Levels are stored as a 2D grid of tile types.

3. **Monster System** – Monsters are defined via static data tables (name, stats, abilities, symbol) and instantiated into a live monster list per level. AI is fairly simple: movement toward the player, basic attack routines, and special abilities triggered by flags.

4. **Object/Item System** – Items also use static template tables (weapon types, armor types, potions, scrolls, etc.) with instances carrying variable data (enchantment bonuses, charges, identification status). Inventory management, equipping, and stacking logic sit here.

5. **Command Interpreter** – A main loop reads a keypress, dispatches to a large switch/lookup table of command handlers (movement, combat, spellcasting, item use, etc.).

6. **Combat & Magic** – Formulas for to-hit, damage, spell effects are typically centralized in combat.c/spells.c-style files, operating on the global player/monster structures.

7. **Display Layer** – Terminal rendering via curses (or a custom terminal abstraction) draws the map, status line, and messages. This is usually isolated somewhat from game logic to support different terminal backends.

8. **Save/Load** – Binary serialization of the game state to a save file, notoriously version-fragile in old-school roguelikes.

## Characteristic Traits

- **Data-driven content**: monsters and items defined in tables/arrays compiled into the binary (or read from data files in some versions), making it moddable at the data level without engine changes.
- **Monolithic globals**: unlike modern designs, there's minimal encapsulation—most "objects" are structs accessed globally.
- **Direct lineage to Angband**: Angband's early codebase was literally a fork of Umoria, extended with classes, races, and more content, so Umoria's architecture is essentially a simpler, smaller ancestor of Angband's.

## Caveat

I don't have reliable, precise knowledge of the exact current file layout, function names, or module boundaries in the modern maintained Umoria repository (e.g., on GitHub) — that project has been refactored over time (including a shift toward more modern C++ in recent releases). If you need accurate specifics about *today's* source tree (file names, class structure, build system), I'd be guessing rather than reporting known facts, so it would be best to check the repository directly for that level of detail.
