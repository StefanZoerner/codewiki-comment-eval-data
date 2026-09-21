# Spells Module Documentation

## Introduction

The `spells_h` module defines the core spell system for the game, including spell definitions, spell casting functions, and related utilities. This module provides the foundation for magical abilities within the game world, handling everything from basic spell mechanics to complex area effects and creature manipulation.

## Architecture Overview

```mermaid
graph TD
    A[Spells Module] --> B[Spell Definitions]
    A --> C[Spell Casting Functions]
    A --> D[Spell Utility Functions]
    A --> E[Spell Data Structures]
    
    B --> B1[Spell_t Structure]
    B --> B2[MagicSpellFlags Enum]
    B --> B3[magic_spells Array]
    B --> B4[spell_names Array]
    
    C --> C1[castSpellGetId Function]
    C --> C2[Spell Casting Logic]
    
    D --> D1[Spell Detection Functions]
    D --> D2[Spell Area Effects]
    D --> D3[Spell Manipulation Functions]
    
    E --> E1[Coord_t Type]
    E --> E2[Spell Constants]
```

## Core Components

### Spell Data Structures

The module defines several key data structures:

**MagicSpellFlags Enum**
```c
enum MagicSpellFlags {
    MagicMissile,
    Lightning,
    PoisonGas,
    Acid,
    Frost,
    Fire,
    HolyOrb,
};
```
This enum defines the different types of spells available in the game system.

**Spell_t Structure**
```c
typedef struct {
    uint8_t level_required;
    uint8_t mana_required;
    uint8_t failure_chance;
    uint8_t exp_gain_for_learning;
} Spell_t;
```
Each spell has metadata including required level, mana cost, failure chance, and experience gained for learning.

### Spell Arrays

**magic_spells Array**
```c
extern Spell_t magic_spells[PLAYER_MAX_CLASSES - 1][31];
```
This two-dimensional array stores spell data organized by player class and spell index.

**spell_names Array**
```c
extern const char *spell_names[62];
```
Contains string names for all available spells.

## Spell Categories

### Spell Casting Functions

The module includes functions for casting various types of spells:

```mermaid
graph LR
    A[Spell Casting] --> B[Direct Targeting]
    A --> C[Area Effects]
    A --> D[Creature Manipulation]
    A --> E[Player Effects]
    A --> F[Environmental Changes]
    
    B --> B1[spellFireBolt]
    B --> B2[spellFireBall]
    B --> B3[spellBreath]
    B --> B4[spellChangeMonsterHitPoints]
    
    C --> C1[spellLightArea]
    C --> C2[spellDarkenArea]
    C --> C3[spellStarlite]
    C --> C4[spellDestroyArea]
    
    D --> D1[spellConfuseMonster]
    D --> D2[spellSleepMonster]
    D --> D3[spellPolymorphMonster]
    D --> D4[spellTeleportAwayMonster]
    
    E --> E1[spellChangePlayerHitPoints]
    E --> E2[spellRestorePlayerLevels]
    E --> E3[spellLoseSTR]
    E --> E4[spellLoseEXP]
    
    F --> F1[spellEarthquake]
    F --> F2[spellCreateFood]
    F --> F3[spellWardingGlyph]
```

### Spell Utility Functions

Utility functions provide supporting capabilities for spell operations:

```mermaid
graph TD
    A[Spell Utilities] --> B[Detection Spells]
    A --> C[Mapping Functions]
    A --> D[Identification]
    A --> E[Area Manipulation]
    A --> F[Object Manipulation]
    A --> G[Status Effects]
    
    B --> B1[spellDetectTreasureWithinVicinity]
    B --> B2[spellDetectObjectsWithinVicinity]
    B --> B3[spellDetectTrapsWithinVicinity]
    B --> B4[spellDetectSecretDoorssWithinVicinity]
    
    C --> C1[spellMapCurrentArea]
    C --> C2[spellLightLine]
    
    D --> D1[spellIdentifyItem]
    D --> D2[spellDispelCreature]
    
    E --> E1[spellLightArea]
    E --> E2[spellDarkenArea]
    E --> E3[spellDestroyArea]
    
    F --> F1[spellRechargeItem]
    F --> F2[spellEnchantItem]
    F --> F3[spellRemoveCurseFromAllWornItems]
    
    G --> G1[spellSlowPoison]
    G --> G2[spellSleepAllMonsters]
    G --> G3[spellSpeedAllMonsters]
```

## Integration Points

This module integrates with several other core systems:

- **[player_h.md](player_h.md)**: Uses spell data for player character abilities
- **[monster_h.md](monster_h.md)**: Interacts with monster behavior through spell effects
- **[map_h.md](map_h.md)**: Works with coordinate systems for area effects
- **[item_h.md](item_h.md)**: Manages item enchantment and recharging spells
- **[game_logic_h.md](game_logic_h.md)**: Provides spell casting logic for game events

## Data Flow

```mermaid
sequenceDiagram
    participant Player
    participant Spells
    participant GameLogic
    
    Player->>Spells: castSpellGetId()
    Spells->>Spells: Validate spell parameters
    Spells->>GameLogic: Execute spell effect
    GameLogic->>Spells: Return spell result
    Spells->>Player: Provide feedback
```

## Process Flows

### Spell Casting Process

1. Player selects spell from menu
2. `castSpellGetId()` validates selection and parameters
3. Spell data retrieved from `magic_spells` array
4. Spell execution function called with appropriate parameters
5. Game state updated based on spell effects
6. Feedback provided to player

### Spell Effect Application

```mermaid
graph TD
    A[Spell Cast] --> B[Parameter Validation]
    B --> C[Mana Check]
    C --> D[Level Check]
    D --> E[Failure Chance Roll]
    E --> F{Success?}
    F -->|Yes| G[Execute Spell Effect]
    F -->|No| H[Spell Failure]
    G --> I[Update Game State]
    I --> J[Provide Feedback]
    H --> K[Provide Failure Feedback]
```

## Dependencies

This module depends on:
- **[coord_h.md](coord_h.md)**: For coordinate-based spell effects
- **[player_h.md](player_h.md)**: For player-specific spell data
- **[monster_h.md](monster_h.md)**: For monster manipulation spells
- **[item_h.md](item_h.md)**: For item-related spells

## Usage Examples

Basic spell casting would involve:
1. Calling `castSpellGetId()` to get spell parameters
2. Using the returned spell ID to call specific spell functions
3. Passing appropriate coordinates and parameters
4. Handling return values for success/failure states

## Notes

The spell system uses a fixed-size array structure for efficient access to spell data. The module assumes proper initialization of spell data arrays before use, and relies on external systems for validation of spell parameters and player state management.
