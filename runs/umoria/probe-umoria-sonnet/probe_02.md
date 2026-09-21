# Umoria Architecture Overview

I have some knowledge of Umoria (also written as "Moria"), one of the classic early roguelikes derived from the same lineage as Rogue, developed originally at UC Berkeley in the 1980s by Robert Alan Koeneke and Jimmey Wayne Todd. I'll describe what I know, but I want to flag upfront that my familiarity with the specific internal architecture is moderate rather than deep—I have general knowledge of its structure but may not have precise details about every module, especially regarding more recent refactored versions (like the GitHub revival project that ported it to C++).

## General Architectural Characteristics

**Language and Era**: Original Umoria was written in C, following the coding conventions typical of early-to-mid 1980s Unix software—lots of global state, minimal abstraction, and terse function names constrained by early compiler limitations.

**Monolithic, Global-State Design**: Like most games of its generation, Umoria relies heavily on large global arrays and structs to represent:
- The dungeon level (a 2D grid of tile/feature data)
- The player character struct (stats, inventory, position, conditions)
- Monster records (an array of active monster instances)
- Item/object definitions (a master template list plus instantiated objects)

**File/Module Breakdown** (roughly, from what I recall of the source tree):
- Files split by *game subsystem* rather than by object-oriented class boundaries—e.g., separate files for spells, combat/melee, monster AI/movement, dungeon generation, object generation, save/load, and terminal I/O.
- A terminal abstraction layer (curses-based, or a custom "term.c"-style wrapper) to isolate screen-drawing calls from game logic, since it needed to support various Unix terminal types.

**Data-Driven Content**: Monsters, items, and spells are defined via arrays of structs (often initialized from external text data files in later versions) rather than hard-coded logic per-entity, which was a notable design choice for extensibility given the era.

**Save Game System**: A binary serialization approach dumping struct contents directly to disk, which made the format fragile to compiler/platform changes—typical of the period.

**Turn-Based Game Loop**: A central dispatch loop reading player input, resolving one game "turn," updating monster AI/movement, and refreshing display—standard for turn-based roguelikes.

## Caveats

I don't have confident, detailed knowledge of:
- Exact filenames and their specific responsibilities in the original source tree
- The specific differences introduced by the open-source revival/modernization (the version maintained on GitHub since the 2010s, which I believe modernized it to C++ with better separation of concerns)
- Precise data structure layouts or function signatures

If you're working from a specific version of the source (original Berkeley release vs. the modern C++ revival), let me know which, and I can reason more carefully about what's likely true—but I'd rather not fabricate specifics I'm not sure of.
