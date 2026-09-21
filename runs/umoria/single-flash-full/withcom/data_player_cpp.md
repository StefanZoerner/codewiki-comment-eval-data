# data_player_cpp Module Documentation

## Introduction

The `data_player_cpp` module serves as the central repository for all player character-related data structures and constants used throughout the game system. This module defines the fundamental characteristics, abilities, and progression systems for player characters including class definitions, racial attributes, background information, and spell systems.

This module provides the foundational data that drives character creation, advancement, and gameplay mechanics. It contains arrays and structures that define how players progress through different classes, races, and skill levels within the game world.

## Architecture Overview

```mermaid
graph TD
    A[data_player_cpp] --> B[Class Definitions]
    A --> C[Race Attributes]
    A --> D[Background Data]
    A --> E[Spell Systems]
    A --> F[Character Provisions]
    
    B --> B1[Class Rank Titles]
    B --> B2[Class Statistics]
    B --> B3[Level Adjustments]
    B --> B4[Spell Lists]
    
    C --> C1[Racial Base Stats]
    C --> C2[Racial Modifiers]
    C --> C3[Racial Characteristics]
    
    D --> D1[Background Descriptions]
    D --> D2[Background Effects]
    
    E --> E1[Spell Names]
    E --> E2[Spell Properties]
    
    F --> F1[Starting Equipment]
```

## Core Data Structures

### Class Rank Titles System

The module implements a comprehensive class ranking system that defines titles earned at various levels across different character classes:

```mermaid
graph LR
    subgraph Class_Rank_Titles
        A[Warrior Titles]
        B[Mage Titles]
        C[Priest Titles]
        D[Rogue Titles]
        E[Ranger Titles]
        F[Paladin Titles]
        
        A --> A1["Rookie"-"Lord Noble"]
        B --> B1["Novice"-"Wizard Lord"]
        C --> C1["Believer"-"Noble Priest"]
        D --> D1["Vagabond"-"Guildsmaster"]
        E --> E1["Runner (1st)"-"Ranger Lord"]
        F --> F1["Gallant"-"High Lord"]
    end
```

Each class has its own progression path with specific titles that reflect character development and achievement within that class system.

### Race Attribute System

The race system defines the fundamental physical and statistical characteristics of different character races:

```mermaid
graph TD
    A[Race Attributes] --> B[Human]
    A --> C[Half-Elf]
    A --> D[Elf]
    A --> E[Halfling]
    A --> F[Gnome]
    A --> G[Dwarf]
    A --> H[Half-Orc]
    A --> I[Half-Troll]
    
    B --> B1[STR:0, INT:0, WIS:0, DEX:0, CON:0, CHR:0]
    B --> B2[Ages:14, Heights:72, Weights:66]
    B --> B3[Special:0, Stealth:0, Infra:100, Exp:100]
    
    C --> C1[STR:-1, INT:1, WIS:0, DEX:1, CON:-1, CHR:1]
    C --> C2[Ages:24, Heights:66, Weights:62]
    C --> C3[Special:2, Stealth:6, Infra:100, Exp:110]
    
    D --> D1[STR:-1, INT:2, WIS:1, DEX:1, CON:-2, CHR:1]
    D --> D2[Ages:75, Heights:60, Weights:54]
    D --> D3[Special:5, Stealth:8, Infra:80, Exp:120]
```

Each race includes:
- **Base statistics** (Strength, Intelligence, Wisdom, Dexterity, Constitution, Charisma)
- **Age ranges** and **physical characteristics** (heights and weights)
- **Special abilities** and **combat modifiers**
- **Infravision** capabilities and **experience multipliers**

### Background Information System

The background system provides detailed character origin stories and social positioning:

```mermaid
graph TD
    A[Background System] --> B[Social Status]
    A --> C[Familial Position]
    A --> D[Racial Heritage]
    A --> E[Occupational Path]
    
    B --> B1[Serf, Yeoman, Townsman, Guildsman, Knight, Noble, Royal]
    C --> C1[Illegitimate, Acknowledged, First Child, Only Child]
    D --> D1[Elves, Halflings, Gnomes, Dwarves, Orcs, Trolls]
    E --> E1[Warrior, Mage, Priest, Rogue, Ranger, Prince, King, Various Professions]
```

Background data includes:
- **Social class descriptions**
- **Family position indicators**
- **Heritage information**
- **Occupational influences**

### Class Definition System

The core class definitions establish the fundamental characteristics and abilities of each playable class:

```mermaid
graph TD
    A[Class Definitions] --> B[Warrior]
    A --> C[Mage]
    A --> D[Priest]
    A --> E[Rogue]
    A --> F[Ranger]
    A --> G[Paladin]
    
    B --> B1[HP:9, BTH:70, Save:18, Spell:None]
    B --> B2[Dis:25, Stealth:1, FOS:38]
    C --> C1[HP:0, BTH:34, Save:36, Spell:Mage]
    C --> C2[Dis:30, Stealth:2, FOS:20]
    D --> D1[HP:2, BTH:48, Save:30, Spell:PRIEST]
    D --> D2[Dis:25, Stealth:2, FOS:32]
```

Each class definition includes:
- **Hit points per level**
- **Combat statistics** (base to hit, saving throws)
- **Skill modifiers** (disarm, stealth, find traps)
- **Spellcasting capabilities**
- **Experience requirements**

### Spell System Integration

The spell system provides magical capabilities organized by class:

```mermaid
graph TD
    A[Spell System] --> B[Mage Spells]
    A --> C[Priest Spells]
    A --> D[Rogue Spells]
    A --> E[Ranger Spells]
    A --> F[Paladin Spells]
    
    B --> B1[31 Spells Total]
    C --> C1[31 Spells Total]
    D --> D1[31 Spells Total]
    E --> E1[31 Spells Total]
    F --> F1[31 Spells Total]
    
    B --> B2[Names: Magic Missile, Detect Monsters, Phase Door...]
    C --> C2[Names: Detect Evil, Cure Light Wounds, Bless...]
```

### Character Provision System

The starting equipment system ensures new characters begin with appropriate gear:

```mermaid
graph TD
    A[Starting Equipment] --> B[Warrior]
    A --> C[Mage]
    A --> D[Priest]
    A --> E[Rogue]
    A --> F[Ranger]
    A --> G[Paladin]
    
    B --> B1[Food Ration, Torch, Cloak, Stiletto, Leather Armor]
    C --> C1[Food Ration, Torch, Cloak, Stiletto, Beginners-Magick]
    D --> D1[Food Ration, Torch, Cloak, Stiletto, Beginners Handbook]
    E --> E1[Food Ration, Torch, Cloak, Stiletto, Beginners-Magick]
    F --> F1[Food Ration, Torch, Cloak, Stiletto, Beginners-Magick]
    G --> G1[Food Ration, Torch, Cloak, Stiletto, Beginners Handbook]
```

## Component Interactions

```mermaid
flowchart LR
    A[Player Creation] --> B[Class Selection]
    A --> C[Race Selection]
    A --> D[Background Selection]
    
    B --> E[Class Stats]
    C --> E
    D --> E
    
    E --> F[Level Progression]
    F --> G[Rank Title Assignment]
    F --> H[Spell Acquisition]
    F --> I[Stat Improvements]
    
    G --> J[Character Display]
    H --> J
    I --> J
    
    J --> K[Gameplay Mechanics]
```

## Data Flow and Usage

The data in `data_player_cpp` flows through the system as follows:

1. **Initialization**: During game startup, all character data is loaded into memory
2. **Character Creation**: Players select race, class, and background which determines initial stats
3. **Progression**: As players level up, rank titles and abilities are updated from the defined arrays
4. **Combat**: Class-specific combat modifiers and spell systems are accessed during gameplay
5. **Display**: Character information is rendered using the stored titles and attributes

## Integration Points

This module integrates with several other system components:

- **[game_character.md](game_character.md)**: Provides character management interfaces that utilize these data structures
- **[player_stats.md](player_stats.md)**: Uses race and class data for stat calculations
- **[spell_system.md](spell_system.md)**: Accesses spell lists and spell properties
- **[character_progression.md](character_progression.md)**: Implements level advancement using class rank titles

## Constants and Limits

The module defines several important constants that govern character behavior:

- `PLAYER_MAX_CLASSES`: Maximum number of playable classes (6)
- `PLAYER_MAX_LEVEL`: Maximum character level (40)
- `PLAYER_MAX_RACES`: Number of available races (8)
- `PLAYER_MAX_BACKGROUNDS`: Number of background options (100+)
- `CLASS_MAX_LEVEL_ADJUST`: Maximum level adjustments per class

## Future Considerations

When extending this module, consider:
1. Adding new classes or races while maintaining compatibility
2. Implementing dynamic title generation for custom classes
3. Supporting modded content through extensible data structures
4. Optimizing memory usage for large datasets
5. Providing clear documentation for external modders

This module forms the foundation for all player character interactions in the game system and requires careful maintenance to ensure consistent gameplay balance.
