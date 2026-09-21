# Umoria Architecture Overview

I have some knowledge of this project, though my familiarity is moderate rather than deep, so I'll describe what I know with appropriate caveats.

**Umoria** is one of the classic early roguelikes (derived from the original Moria, developed at UC Berkeley in the mid-1980s by Robert Alan Koeneke and Jimmey Wayne Todd, later maintained by others). It's written in C and is a direct ancestor/relative of Angband.

## General Characteristics

The codebase reflects its 1980s origins:
- **Procedural C**, not object-oriented — this predates widespread OOP conventions in game design.
- Heavy use of **global state** and global arrays for game data (monsters, items, dungeon levels, player stats).
- Data-driven design via **external data files** that define monster templates, item templates, dungeon vaults, and spell lists, parsed into fixed-size C structs/arrays at startup or compile time.
- Split roughly along functional/domain lines rather than layered architecture (no strict separation of "engine" vs "game logic" vs "UI").

## Rough Module Breakdown (as I recall it)

- **Dungeon generation** — algorithms for generating levels, rooms, corridors, and placing vaults/features.
- **Monster handling** — monster memory (recall), AI/movement routines, spawning tables.
- **Item/object system** — item generation, identification, enchantment, inventory management.
- **Player systems** — character creation, races/classes, stats, experience, spellcasting.
- **Command interpreter** — a main loop reading keystrokes and dispatching to action functions (movement, combat, item use, etc.), typical of terminal-based roguelikes.
- **Display/terminal layer** — abstracted somewhat through curses (or a custom terminal abstraction) to support multiple platforms (DOS, Unix, etc.), since Moria/Umoria supported several systems historically.
- **Save/load (persistence)** — serializing the large global game state to a save file, notoriously version-fragile in old roguelikes like this.

## Honest Caveat

I don't have detailed, file-by-file knowledge of the current Umoria source tree (e.g., exact filenames, current maintainers' refactoring choices, or the specific state of the modernized C++ port that exists on GitHub today). If you're working with a specific version — especially the more recent C++ modernization efforts — I'd be guessing at specifics like exact class structures, namespaces, or build system details rather than recalling them reliably. If you can tell me which version/repo you're looking at, or paste specific code, I can give you a more precise and trustworthy answer.
