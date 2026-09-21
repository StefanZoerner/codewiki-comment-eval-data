# player_bash_cpp Module Documentation

## Brief Introduction

The `player_bash_cpp` module implements the player's ability to bash doors, chests, and creatures in the game. This functionality allows players to break down closed doors, destroy chests, and attack creatures through bash actions. The module handles the complex logic of determining success rates, calculating damage, and managing the consequences of successful or failed bashing attempts.

## Module Overview

This module contains the core implementation for the player bash action, which is a fundamental combat and exploration mechanic in the game. It interfaces with various game systems including player statistics, inventory management, creature handling, and dungeon generation.

### Key Features

- **Door Bashing**: Players can bash closed doors, potentially opening them or breaking them
- **Chest Destruction**: Players can destroy chests, with potential for loot destruction or lock breaking
- **Creature Attacks**: Players can bash attacking creatures directly
- **Success Calculation**: Complex probability calculations based on player attributes
- **Damage System**: Damage calculation incorporating weapon weight, strength, and level
- **Status Effects**: Paralysis and stun effects from failed bashes

## Architecture and Component Relationships

```mermaid
graph TD
    A[player_bash()] --> B[playerBashPosition()]
    A --> C[playerBashClosedDoor()]
    A --> D[playerBashClosedChest()]
    A --> E[playerBashAttack()]
    B --> E
    C --> F[dungeonLiteSpot()]
    C --> G[playerMove()]
    E --> H[playerTestBeingHit()]
    E --> I[monsterTakeHit()]
    E --> J[playerWeaponCriticalBlow()]
    E --> K[displayCharacterExperience()]
    
    subgraph Game Systems
        H --> L[PlayerStats]
        H --> M[MonsterStats]
        H --> N[ClassAdjustments]
        I --> O[MonsterHealth]
        J --> P[WeaponDamage]
        J --> Q[StrengthBonus]
        J --> R[LevelBonus]
    end
    
    subgraph Core Dependencies
        A --> S[headers.h]
        A --> T[dice.h]
        A --> U[py.flags]
        A --> V[game.treasure]
        A --> W[dg.floor]
        A --> X[monsters]
        A --> Y[creatures_list]
    end
```

## Data Flow and Process Flow

```mermaid
flowchart LR
    A[Player initiates bash] --> B{Get direction}
    B -- Invalid direction --> C[Return]
    B -- Valid direction --> D{Check confusion}
    D -- Confused --> E[Random direction]
    D -- Not confused --> F[Use selected direction]
    F --> G[Calculate target position]
    G --> H{Target has creature}
    H -- Yes --> I[playerBashPosition()]
    H -- No --> J{Target has treasure}
    J -- Closed door --> K[playerBashClosedDoor()]
    J -- Chest --> L[playerBashClosedChest()]
    J -- Other --> M[Print generic message]
    J -- No treasure --> N{Target is wall}
    N -- Wall --> O[Print empty space message]
    N -- Not wall --> P[Print generic message]
    
    subgraph Bash Processing
        I --> Q[Check fear status]
        Q -- Afraid --> R[Print fear message]
        Q -- Not afraid --> S[playerBashAttack()]
        K --> T[Calculate bash chance]
        T --> U{Chance succeeds}
        U -- Yes --> V[Open door]
        U -- No --> W{DEX check}
        W -- Fail --> X[Paralysis effect]
        W -- Success --> Y[Print hold message]
        L --> Z{Destroy chest chance}
        Z -- Success --> AA[Destroy chest]
        Z -- No --> AB{Lock break chance}
        AB -- Success --> AC[Unlock chest]
        AB -- No --> AD[Print hold message]
    end
```

## Core Components

### Main Function: `playerBash()`

The primary entry point for the bash functionality. This function:

1. Gets player input for direction
2. Handles confusion effects
3. Calculates target coordinates
4. Determines what type of object is being bashed
5. Routes to appropriate handler functions

### Supporting Functions

#### `playerBashAttack(Coord_t coord)`
Handles attacks against creatures:
- Calculates hit probability based on player stats
- Applies damage calculation with critical hit modifiers
- Manages monster health and death conditions
- Implements stun effects for successful hits
- Handles player balance penalties

#### `playerBashPosition(Coord_t coord)`
Wrapper function that checks for fear status before attempting an attack:
- Prevents cowardly behavior when player is afraid
- Delegates to `playerBashAttack()` when appropriate

#### `playerBashClosedDoor(Coord_t coord, int dir, Tile_t &tile, Inventory_t &item)`
Handles bashing closed doors:
- Calculates success probability based on strength and weight
- Implements door opening mechanics
- Handles door destruction (50% chance)
- Manages movement after successful bash
- Applies paralysis effects for failed attempts

#### `playerBashClosedChest(Inventory_t &item)`
Handles bashing chests:
- 10% chance to completely destroy chest and contents
- 10% chance to break locks on locked chests
- Provides feedback for failed attempts

## Integration Points

This module integrates with several core game systems:

- **Player Statistics System** ([player_stats.md](player_stats.md)): Uses strength, dexterity, and weight attributes
- **Inventory Management** ([inventory_system.md](inventory_system.md)): Interacts with treasure items and equipment
- **Monster System** ([monster_system.md](monster_system.md)): Handles creature attacks and combat resolution
- **Dungeon Generation** ([dungeon_generation.md](dungeon_generation.md)): Works with tile and feature data structures
- **Combat System** ([combat_system.md](combat_system.md)): Uses hit probability calculations and damage formulas

## External Dependencies

The module depends on:
- `headers.h`: Core game headers and definitions
- `dice.h`: Random number generation and dice rolling functions
- Global game state variables (`py`, `game`, `dg`, `monsters`, `creatures_list`)
- Configuration constants from various system modules

## Implementation Details

### Probability Calculations

The bash success rate uses a complex formula that considers:
- Player strength
- Player weight
- Item properties (lock status, etc.)
- Random chance elements

### Damage Calculation

Damage follows this pattern:
1. Base weapon damage roll
2. Critical blow calculation based on strength and weapon weight
3. Additional bonuses from player weight and level
4. Minimum damage enforcement

### Status Effects

Failed bashes can result in:
- **Paralysis**: Temporary inability to act
- **Stun**: Temporary creature incapacitation
- **Off-balance**: Reduced accuracy on subsequent actions

## Error Handling and Edge Cases

The module handles several edge cases:
- Confused players get random directions
- Fear prevents creature attacks
- Empty spaces cannot be bashed
- Various item types respond differently to bash attempts
- Proper messaging for all outcomes

## Performance Considerations

The module is designed for minimal performance impact during normal gameplay:
- All calculations are lightweight
- No expensive operations in hot paths
- Efficient use of existing game state data
- Minimal memory allocation

## Related Modules

For complete understanding, see:
- [player_stats.md](player_stats.md): Player attribute system
- [inventory_system.md](inventory_system.md): Treasure and item handling
- [monster_system.md](monster_system.md): Creature combat mechanics
- [combat_system.md](combat_system.md): General combat algorithms
- [dungeon_generation.md](dungeon_generation.md): Dungeon tile and feature management
