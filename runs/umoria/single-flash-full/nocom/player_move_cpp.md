# Player Move C++ Module Documentation

## Introduction

The `player_move_cpp` module handles all player movement logic and interactions within the dungeon environment. This module manages player navigation, trap detection and activation, object collection, and combat initiation. It serves as the primary interface between player input and game world state changes.

## Module Overview

This module contains the core logic for player movement operations including:
- Movement validation and position updates
- Trap detection and activation
- Object picking up and inventory management
- Combat initiation with monsters
- Dungeon lighting and visibility updates

## Architecture and Component Relationships

```mermaid
graph TD
    A[Player Move Module] --> B[Movement Logic]
    A --> C[Trap Handling]
    A --> D[Object Collection]
    A --> E[Combat Initiation]
    A --> F[Dungeon Updates]
    
    B --> B1[playerMove()]
    B --> B2[playerMovePosition()]
    B --> B3[playerRandomMovement()]
    
    C --> C1[playerStepsOnTrap()]
    C --> C2[trapOpenPit(), trapArrow(), etc.]
    
    D --> D1[carry()]
    D --> D2[inventoryCanCarryItemCount()]
    D --> D3[inventoryCarryItem()]
    
    E --> E1[playerAttackPosition()]
    
    F --> F1[dungeonMoveCreatureRecord()]
    F --> F2[dungeonLightRoom()]
    F --> F3[dungeonMoveCharacterLight()]

    subgraph Core Functions
        B1
        C1
        D1
        E1
        F1
    end
    
    subgraph Supporting Functions
        B2
        B3
        C2
        D2
        D3
        F2
        F3
    end
```

## Data Flow and Process Flow

### Main Movement Process

```mermaid
flowchart LR
    A[Input Direction] --> B[playerRandomMovement()]
    B --> C{Random Movement?}
    C -->|Yes| D[Random Direction]
    C -->|No| E[Use Input Direction]
    
    E --> F[playerMovePosition()]
    F --> G{Valid Position?}
    G -->|No| H[Return]
    G -->|Yes| I[Get Tile Info]
    
    I --> J{Tile Occupied?}
    J -->|Yes| K[Check Monster]
    J -->|No| L[Process Tile Features]
    
    K --> M{Monster Visible?}
    M -->|Yes| N[Initiate Combat]
    M -->|No| O[Free Turn]
    
    L --> P{Feature Type}
    P -->|Open Space| Q[Move Player]
    P -->|Blocked| R[Block Movement]
    
    Q --> S[Update Position]
    S --> T[Update Dungeon State]
    T --> U[Check for Objects]
    U --> V{Object Present?}
    V -->|Yes| W[Handle Object Collection]
    V -->|No| X[Continue Game Loop]
```

## Key Components and Their Interactions

### Movement System

The `playerMove()` function orchestrates all player movement operations. It handles:
- Direction validation and random movement when confused
- Position updating and coordinate calculations
- Tile feature processing and collision detection
- Dungeon state synchronization

### Trap System

The trap handling system uses the `playerStepsOnTrap()` function which:
- Identifies trap types from treasure items
- Executes appropriate trap effects based on trap type
- Manages trap visibility changes
- Handles trap-specific damage calculations

### Object Collection

The `carry()` function manages player object interaction:
- Determines if objects can be picked up based on inventory capacity
- Handles gold collection and display
- Manages inventory space limitations
- Processes user confirmation prompts for item pickup

### Combat System

When encountering monsters, the system either:
- Initiates combat via `playerAttackPosition()`
- Grants free turns for non-visible monsters
- Handles running mechanics and combat tracking

## Integration Points

This module integrates with several other system components:

- **[inventory_cpp.md](inventory_cpp.md)**: For inventory management during object collection
- **[dungeon_cpp.md](dungeon_cpp.md)**: For dungeon state updates and lighting management
- **[monster_cpp.md](monster_cpp.md)**: For combat initiation and monster handling
- **[player_cpp.md](player_cpp.md)**: For player status and attribute management
- **[store_cpp.md](store_cpp.md)**: For store entrance traps

## Dependencies

The module depends on:
- `headers.h`: Contains all necessary includes and definitions
- Game state structures (`py`, `dg`, `game`)
- Utility functions for random number generation and string operations
- Core game systems for inventory, dungeon, and monster management

## Error Handling and Edge Cases

The module handles various edge cases:
- Confused player movement (random direction selection)
- Inventory capacity limits during item collection
- Trap activation with proper damage calculation
- Blocked movement scenarios with appropriate messaging
- Visibility and lighting updates for dungeon exploration

## Performance Considerations

The module is designed for efficient execution during gameplay:
- Minimal memory allocation during normal operation
- Early returns for invalid conditions
- Optimized conditional checks for common scenarios
- Batch processing of dungeon updates when possible

## Configuration Dependencies

This module respects configuration options such as:
- `config::options::prompt_to_pickup`: Controls user confirmation for item collection
- Various player status flags for movement behavior
- Game difficulty settings affecting trap effectiveness

## Related Modules

For complete understanding, see:
- [inventory_cpp.md](inventory_cpp.md): Inventory management
- [dungeon_cpp.md](dungeon_cpp.md): Dungeon generation and management
- [monster_cpp.md](monster_cpp.md): Monster behavior and combat
- [player_cpp.md](player_cpp.md): Player character attributes and status
- [store_cpp.md](store_cpp.md): Store entrance functionality
