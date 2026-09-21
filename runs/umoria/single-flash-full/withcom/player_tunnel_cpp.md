# player_tunnel_cpp Module Documentation

## Brief Introduction

The `player_tunnel_cpp` module implements the core functionality for player tunneling operations within the game world. This module handles the logic for players attempting to dig through various terrain types including walls, rubble, and secret doors. It manages digging mechanics based on player attributes, equipment, and terrain properties while ensuring proper game balance and preventing exploits.

## Module Overview

This module provides the implementation for the player tunneling action, which allows characters to excavate through different types of terrain in the dungeon. The system considers player strength, equipped tools, and terrain characteristics to determine digging success and outcomes.

## Architecture and Component Relationships

### Core Components

The module consists of a single source file `player_tunnel.cpp` containing:

1. **Validation Functions** - `playerCanTunnel()` - Validates tunneling attempts
2. **Calculation Functions** - `playerDiggingAbility()` - Computes digging effectiveness
3. **Terrain-Specific Handlers** - Functions for different wall types and rubble
4. **Main Tunneling Logic** - `playerTunnel()` - Orchestrates the entire tunneling process

### Data Flow

```mermaid
graph TD
    A[Player Tunnel Command] --> B[playerTunnel()]
    B --> C[Direction Validation]
    B --> D[Position Calculation]
    B --> E[playerCanTunnel()]
    E --> F{Valid Tunnel?}
    F -->|No| G[Abort Tunnel]
    F -->|Yes| H[Creature Check]
    H --> I{Creature Present?}
    I -->|Yes| J[Attack Creature]
    I -->|No| K[Tool Check]
    K --> L{Tool Available?}
    L -->|No| M[Hand Digging Message]
    L -->|Yes| N[playerDiggingAbility()]
    N --> O[dungeonDigAtLocation()]
    O --> P{Terrain Type}
    P -->|Wall| Q[dungeonDigGraniteWall/...()]
    P -->|Rubble| R[dungeonDigRubble()]
    P -->|Secret Door| S[playerSearch()]
```

### Dependencies

This module depends on several other system components:

- [headers.h](headers.md) - Provides essential game definitions and includes
- [game_state](game_state.md) - Accesses global game state variables
- [player_movement](player_movement.md) - Handles player position calculations
- [creature_system](creature_system.md) - Manages creature interactions during tunneling
- [object_system](object_system.md) - Handles treasure and feature management
- [message_system](message_system.md) - Displays user feedback messages

## Detailed Function Documentation

### `playerCanTunnel()`
Validates whether a player can tunnel through a specific location. Prevents illegal tunneling attempts such as:
- Tunneling through empty space
- Tunneling through non-diggable features
- Prevents free attacks by blocking invalid tunneling paths

### `playerDiggingAbility()`
Calculates the player's digging effectiveness based on:
- Base strength attribute
- Tool properties (if equipped)
- Weapon weight and handling considerations
- Equipment-related modifiers

### `dungeonDigGraniteWall()`, `dungeonDigMagmaWall()`, `dungeonDigQuartzWall()`
Specialized handlers for different wall types with varying difficulty levels and success thresholds.

### `dungeonDigRubble()`
Handles rubble removal with additional random chance for finding hidden objects.

### `dungeonDigAtLocation()`
Main dispatcher function that routes tunneling attempts to appropriate terrain handlers.

### `playerTunnel()`
Primary entry point that orchestrates the complete tunneling process:
1. Handles confusion effects
2. Calculates target position
3. Validates tunneling conditions
4. Checks for creatures in the way
5. Processes digging with available tools
6. Handles special cases like secret doors

## Process Flow

```mermaid
flowchart TD
    A[Start Tunnel Action] --> B{Confused?}
    B -->|Yes| C[Random Direction]
    B -->|No| D[Use Selected Direction]
    D --> E[Calculate Target Position]
    E --> F[playerCanTunnel()]
    F -->|Invalid| G[Display Error Message]
    F -->|Valid| H[Check Creature Presence]
    H -->|Creature| I[Attack Creature]
    H -->|No Creature| J[Check Tool Availability]
    J -->|No Tool| K[Hand Digging Message]
    J -->|Has Tool| L[Calculate Digging Ability]
    L --> M[Process Terrain Type]
    M -->|Wall| N[Wall-Specific Handler]
    M -->|Rubble| O[Rubble Handler]
    M -->|Secret Door| P[Search Handler]
```

## Integration Points

This module integrates with several core systems:

1. **Player State Management** - Accesses player attributes and inventory
2. **Game World Interaction** - Modifies dungeon tiles and features
3. **Combat System** - Handles creature encounters during tunneling
4. **Object System** - Manages treasure removal and placement
5. **UI/Feedback System** - Provides appropriate messages to the player

## Game Balance Considerations

The tunneling system implements several balance mechanisms:
- Difficulty scaling based on terrain type
- Tool effectiveness bonuses and penalties
- Weight-based penalties for heavy equipment
- Random chance elements for success/failure
- Prevention of exploit scenarios (free attacks, etc.)

## Error Handling

The module includes robust error checking:
- Invalid tunneling attempts are rejected
- Special cases are handled with appropriate abort conditions
- Boundary checks prevent undefined behavior
- Clear messaging informs players of tunneling limitations

## Performance Characteristics

The module maintains efficient performance through:
- Minimal conditional branching
- Direct access to cached player statistics
- Early termination of invalid operations
- Optimized random number generation usage

This module forms a critical part of the dungeon exploration mechanics, enabling players to navigate complex environments through strategic excavation while maintaining game balance and preventing exploitation.
