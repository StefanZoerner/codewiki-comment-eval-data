# monster_cpp Module Documentation

## Introduction

The `monster_cpp` module handles all monster-related functionality in the game, including monster movement, combat, AI behavior, death handling, and interaction with the player character. This module is essential for creating dynamic and challenging gameplay experiences through intelligent monster behavior.

## Architecture Overview

```mermaid
graph TD
    A[monster_cpp] --> B[Monster Management]
    A --> C[Combat System]
    A --> D[AI Behavior]
    A --> E[Death Handling]
    A --> F[Visibility System]
    
    B --> B1[Monster Creation]
    B --> B2[Monster Movement]
    B --> B3[Monster Update]
    
    C --> C1[Attack Processing]
    C --> C2[Damage Calculation]
    C --> C3[Spell Casting]
    
    D --> D1[Movement Logic]
    D --> D2[Decision Making]
    D --> D3[Pathfinding]
    
    E --> E1[Death Effects]
    E --> E2[Item Dropping]
    E --> E3[Experience Gain]
    
    F --> F1[Visibility Check]
    F --> F2[Lighting Updates]
```

## Core Components

### Monster Data Structures

The module works with several key data structures:

- **Monster_t**: Represents individual monsters with properties like position, health, and state
- **Creature_t**: Defines monster types with attributes like movement patterns, attacks, and defenses
- **Recall_t**: Stores player knowledge about monsters for character recall
- **Tile_t**: Represents dungeon tiles that contain monsters and items

### Key Functions

#### Visibility Management

```mermaid
flowchart LR
    A[monsterUpdateVisibility] --> B[Check Distance]
    A --> C[Check Light Conditions]
    A --> D[Check Player Status]
    B --> E{Visible?}
    C --> E
    D --> E
    E -- Yes --> F[Update Lit State]
    E -- No --> G[Clear Lit State]
```

The visibility system determines whether monsters are visible to the player based on lighting conditions, player status, and monster properties. It uses the `monsterIsVisible()` function to check if a monster should be displayed on screen.

#### Combat System

```mermaid
flowchart TD
    A[monsterAttackPlayer] --> B[Process Attacks]
    B --> C[Check Attack Hits]
    C --> D{Hit Successful?}
    D -- Yes --> E[Apply Damage]
    D -- No --> F[Miss Message]
    E --> G[Handle Special Effects]
    G --> H[Update Creature Recall]
    H --> I[Check Death]
```

The combat system processes monster attacks against the player, handling hit detection, damage calculation, and special attack effects. It includes functions for:

- `executeAttackOnPlayer()`: Processes specific attack types and applies effects
- `monsterPrintAttackDescription()`: Displays attack messages
- `monsterConfuseOnAttack()`: Handles confusion effects from attacks

#### Monster Movement AI

```mermaid
flowchart TD
    A[monsterMove] --> B[Check Conditions]
    B --> C{Confused?}
    C -- Yes --> D[Confused Movement]
    C -- No --> E{Can Cast Spell?}
    E -- Yes --> F[Cast Spell]
    E -- No --> G[Normal Movement]
    G --> H[Choose Direction]
    H --> I[Execute Move]
```

The AI system controls monster movement through various strategies:

- **Confusion handling** (`monsterMoveConfused`)
- **Spell casting** (`monsterCastSpell`)
- **Normal movement** (`monsterMoveNormally`)
- **Random movement** (`monsterMoveRandomly`)
- **Special behaviors** (`monsterMultiplyCritter`, `monsterMoveOutOfWall`)

#### Death and Experience Handling

```mermaid
flowchart TD
    A[monsterTakeHit] --> B[Calculate Damage]
    B --> C{Monster Dead?}
    C -- Yes --> D[Handle Death]
    C -- No --> E[Continue Fighting]
    D --> F[Drop Items]
    D --> G[Gain Experience]
    D --> H[Update Recall]
```

When monsters are defeated, they trigger the death sequence which handles:

- Item dropping based on monster flags
- Experience gain for the player
- Memory updates for creature recall
- Special win conditions

## Component Interactions

```mermaid
flowchart LR
    A[Player] -->|Input| B[Game Loop]
    B --> C[monsterUpdateVisibility]
    B --> D[updateMonsters]
    D --> E[monsterMove]
    D --> F[monsterAttackPlayer]
    E --> G[makeMove]
    G --> H[monsterAllowedToMove]
    H --> I[dungeonMoveCreatureRecord]
    F --> J[executeAttackOnPlayer]
    J --> K[playerTakesHit]
    K --> L[character_death_check]
    L --> M[game_over_check]
```

## Data Flow

1. **Player Input Processing**: Game loop calls `updateMonsters()` to process all active monsters
2. **Visibility Updates**: `monsterUpdateVisibility()` checks if monsters should be visible
3. **Movement Execution**: `monsterMove()` determines how each monster should act
4. **Combat Resolution**: `monsterAttackPlayer()` handles attacks against the player
5. **Damage Application**: `executeAttackOnPlayer()` applies specific damage effects
6. **State Updates**: Monster health, status, and memory are updated throughout the process

## Dependencies

This module depends on several other system components:

- [headers.h](headers.md): Contains global definitions and includes
- [player_cpp](player_cpp.md): Player character management and combat
- [dungeon_cpp](dungeon_cpp.md): Dungeon layout and tile management
- [items_cpp](items_cpp.md): Item handling and treasure generation
- [spells_cpp](spells_cpp.md): Spell casting mechanics
- [config_cpp](config_cpp.md): Configuration constants and settings

## Configuration Constants

The module uses various configuration constants defined in the config system:

- `MON_MAX_SIGHT`: Maximum sight range for monsters
- `MON_MAX_LEVELS`: Maximum monster level for calculations
- `MON_MULTIPLY_ADJUST`: Adjustment factor for monster multiplication
- Various movement and attack flags from the config namespace

## Performance Considerations

The monster processing system is designed to handle multiple monsters efficiently:

- Uses optimized movement algorithms
- Implements early termination for non-interactive monsters
- Minimizes redundant visibility checks
- Processes monsters in reverse order to avoid index issues during deletion

## Error Handling

The module implements robust error handling for edge cases:

- Checks for valid monster IDs before operations
- Validates coordinates before movement
- Handles dead monsters gracefully
- Ensures proper cleanup when monsters are removed

## Security Considerations

The module follows security best practices:

- Bounds checking for array accesses
- Validation of monster IDs and positions
- Proper handling of player input and state changes
- Prevention of buffer overflows in string operations
