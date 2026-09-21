# Umoria Architecture Overview

I have some knowledge of Umoria (also known as "Moria"), the classic roguelike dungeon crawler originally written by Robert Alan Koeneke and Jimmey Wayne Todd, with later ports and cleanup work (notably by David Grabiner and others maintaining the open-source releases). However, I want to be upfront: my knowledge of the specific internal architecture is limited, and I don't want to overstate precision on details like exact function names, file organization in specific versions, or line-level structure.

## What I Can Describe with Reasonable Confidence

**General era and style:** Umoria originated in the mid-1980s, written in C, and follows the coding conventions typical of that period—heavy use of global state, large monolithic source files, and minimal abstraction layers compared to modern game architecture. It was a direct ancestor/sibling to the Angband codebase, and the two share significant conceptual and structural DNA (Angband was originally a fork of Moria).

**High-level structural themes I recall:**
- **Global game state**: Player stats, dungeon level data, and monster/item arrays are typically held in large global structs/arrays rather than passed around or encapsulated.
- **Separation by game subsystem**: Source files are generally split by concern—dungeon generation, monster AI, combat resolution, item/inventory handling, spellcasting, and the command interpreter loop.
- **Terminal-based I/O layer**: Because it's a curses-style text interface, there's typically an abstraction layer (often via curses/termcap or a custom wrapper) isolating screen-drawing code from game logic, to support portability across Unix terminal types.
- **Save file handling**: A serialization module handles reading/writing the compact binary save format, which was historically a source of portability bugs (endianness, struct packing) across architectures.
- **Command-driven main loop**: Like most roguelikes of that generation, there's a central loop reading a keypress, dispatching to a large switch/dispatch table of command handlers, then updating monster turns and screen state.

## What I'm Not Confident About

I don't have reliable, specific knowledge of:
- The exact modern file layout (e.g., how the CMake-based open-source revival by Chris Rasch/UMoria maintainers organized `src/` in recent releases)
- Specific struct definitions or naming conventions used in the actual codebase
- How much the maintained open-source version (post-1990s releases) refactored the original 1990 source versus preserving it as-is

If you're working with a specific version of the source (e.g., the GitHub `dungeon/umoria` restoration), I'd recommend treating my answer as a general orientation rather than a precise map, and I'm happy to reason through actual source files or specific modules if you share them or point me to particular ones you're curious about.
