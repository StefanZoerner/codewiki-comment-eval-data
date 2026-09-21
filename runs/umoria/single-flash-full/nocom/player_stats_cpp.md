# player_stats_cpp Module Documentation

## Overview

The `player_stats_cpp` module handles all player statistics calculations and modifications within the game engine. This module manages character attributes, experience levels, hit points calculation, attack mechanics, and various stat adjustments that affect gameplay balance and character progression.

## Architecture

```mermaid
graph TD
    A[player_stats.cpp] --> B[Player Stats Management]
    A --> C[Experience Level System]
    A --> D[Hit Points Calculation]
    A --> E[Attack Mechanics]
    A --> F[Stat Adjustment Systems]
    A --> G[Character Attribute Management]
    
    B --> H[playerInitializeBaseExperienceLevels]
    B --> I[playerCalculateHitPoints]
    B --> J[playerAttackBlows]
    B --> K[playerStatAdjustmentWisdomIntelligence]
    B --> L[playerStatAdjustmentCharisma]
    B --> M[playerStatAdjustmentConstitution]
    B --> N[playerSetAndUseStat]
    B --> O[playerStatRandomIncrease]
    B --> P[playerStatRandomDecrease]
    B --> Q[playerStatRestore]
    B --> R[playerStatBoost]
    B --> S[playerToHitAdjustment]
    B --> T[playerArmorClassAdjustment]
    B --> U[playerDisarmAdjustment]
    B --> V[playerDamageAdjustment]
```

## Core Components

### Experience Level System

The module initializes base experience levels required for each character level through `playerInitializeBaseExperienceLevels()`. This function sets up a predefined array of experience values that determine when players advance to higher levels.

### Hit Points Calculation

`playerCalculateHitPoints()` calculates a player's maximum hit points based on:
- Base HP levels from class configuration
- Constitution modifier
- Heroic status bonuses
- Current HP proportion maintenance during level changes

### Attack Mechanics

The attack system includes several functions:
- `playerAttackBlows()`: Determines number of attacks per round based on strength and dexterity
- `playerToHitAdjustment()`: Calculates bonus to hit probability
- `playerArmorClassAdjustment()`: Computes armor class modifier
- `playerDisarmAdjustment()`: Handles disarm success chance
- `playerDamageAdjustment()`: Modifies damage output

### Stat Adjustment Systems

Multiple functions handle different aspects of player statistics:
- **Wisdom/Intelligence Adjustment**: `playerStatAdjustmentWisdomIntelligence()`
- **Charisma Adjustment**: `playerStatAdjustmentCharisma()`
- **Constitution Adjustment**: `playerStatAdjustmentConstitution()`
- **Stat Modification**: `playerModifyStat()` (internal helper)
- **Stat Application**: `playerSetAndUseStat()`

### Character Attribute Management

The module provides comprehensive stat management including:
- Random stat increases/decreases (`playerStatRandomIncrease()`, `playerStatRandomDecrease()`)
- Stat restoration (`playerStatRestore()`)
- Stat boosting (`playerStatBoost()`)

## Data Flow

```mermaid
flowchart LR
    A[Game Engine] --> B[playerInitializeBaseExperienceLevels]
    B --> C[Experience Table]
    A --> D[playerCalculateHitPoints]
    D --> E[HP Calculation]
    E --> F[HP Update]
    A --> G[playerAttackBlows]
    G --> H[Attack Calculation]
    A --> I[playerStatAdjustmentWisdomIntelligence]
    I --> J[Stat Modifier]
    A --> K[playerStatAdjustmentCharisma]
    K --> L[Charisma Modifier]
    A --> M[playerStatAdjustmentConstitution]
    M --> N[Constitution Modifier]
    A --> O[playerSetAndUseStat]
    O --> P[Stat Application]
    O --> Q[Stat Recalculation]
    A --> R[playerStatRandomIncrease]
    R --> S[Stat Increase]
    A --> T[playerStatRandomDecrease]
    T --> U[Stat Decrease]
    A --> V[playerStatRestore]
    V --> W[Stat Restoration]
    A --> X[playerStatBoost]
    X --> Y[Stat Boosting]
    A --> Z[playerToHitAdjustment]
    Z --> AA[To-Hit Modifier]
    A --> AB[playerArmorClassAdjustment]
    AB --> AC[Armor Class Modifier]
    A --> AD[playerDisarmAdjustment]
    AD --> AE[Disarm Modifier]
    A --> AF[playerDamageAdjustment]
    AF --> AG[Damage Modifier]
```

## Component Interactions

```mermaid
graph TB
    subgraph "Player Stats Management"
        A[playerInitializeBaseExperienceLevels]
        B[playerCalculateHitPoints]
        C[playerAttackBlows]
        D[playerSetAndUseStat]
        E[playerStatRandomIncrease]
        F[playerStatRandomDecrease]
        G[playerStatRestore]
        H[playerStatBoost]
    end
    
    subgraph "Stat Adjustment Functions"
        I[playerStatAdjustmentWisdomIntelligence]
        J[playerStatAdjustmentCharisma]
        K[playerStatAdjustmentConstitution]
        L[playerToHitAdjustment]
        M[playerArmorClassAdjustment]
        N[playerDisarmAdjustment]
        O[playerDamageAdjustment]
    end
    
    A --> D
    B --> D
    C --> D
    D --> I
    D --> J
    D --> K
    D --> L
    D --> M
    D --> N
    D --> O
    E --> D
    F --> D
    G --> D
    H --> D
```

## Integration Points

This module integrates with:
- [game_config](game_config.md): Accesses configuration data for class-specific spell systems
- [character_system](character_system.md): Manages character state and attributes
- [combat_system](combat_system.md): Uses attack and defense modifiers
- [level_system](level_system.md): Works with experience and level progression
- [spell_system](spell_system.md): Handles spell casting based on intelligence/wisdom stats

## Key Constants and Configuration

The module references several configuration constants:
- `PLAYER_MAX_LEVEL`: Maximum player level cap
- `PlayerAttr` enum: Defines attribute types (STR, DEX, INT, etc.)
- `blows_table[]`: Attack frequency table based on strength/dexterity combinations
- Status flags from `config::player::status`: Heroic status indicators

## Process Flows

### Stat Modification Process

```mermaid
sequenceDiagram
    participant Player
    participant StatsModule
    participant GameEngine
    
    Player->>StatsModule: Request stat change
    StatsModule->>StatsModule: Apply modification
    StatsModule->>StatsModule: Validate limits
    StatsModule->>StatsModule: Calculate new stat value
    StatsModule->>StatsModule: Update used stat
    StatsModule->>GameEngine: Notify stat change
    GameEngine->>Player: Update UI
```

### Level Progression Flow

```mermaid
sequenceDiagram
    participant Player
    participant StatsModule
    participant GameEngine
    
    Player->>GameEngine: Gain experience
    GameEngine->>StatsModule: Check level up
    StatsModule->>StatsModule: Calculate new level
    StatsModule->>StatsModule: Update experience
    StatsModule->>StatsModule: Recalculate hit points
    StatsModule->>StatsModule: Update stats
    StatsModule->>GameEngine: Notify level change
    GameEngine->>Player: Display level up message
```

## Dependencies

This module depends on:
- `headers.h`: Includes necessary definitions and global variables
- Global `py` structure: Contains player data and state
- Configuration arrays like `classes[]` and `blows_table[]`
- Random number generation functions
- Display functions for character stats

## Notes

The module implements complex stat calculations that directly impact gameplay balance. All stat modifications are carefully bounded to prevent extreme values while maintaining meaningful progression. The system supports both direct stat manipulation and random stat fluctuations for character development variety.
