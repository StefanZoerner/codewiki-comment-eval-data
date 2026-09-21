# Monster Manager C++ Module Documentation

## Brief Introduction

The `monster_manager_cpp` module is responsible for managing all monster-related operations within the game. It handles monster creation, placement, movement, and cleanup. This module interfaces with the dungeon management system to place monsters in appropriate locations and maintains the monster data structures that track each creature's state and properties.

## Module Overview

This module provides core functionality for monster management including:
- Monster allocation and deallocation
- Monster placement algorithms
- Monster level-based spawning
- Monster summoning mechanics
- Monster compaction for performance optimization

## Architecture and Component Relationships

### Core Data Structures

```mermaid
classDiagram
    class Monster_t {
        <<struct>>
        int16_t id
        int16_t creature_id
        int16_t hp
        int16_t speed
        Coord_t pos
        int16_t stunned_amount
        bool sleeping
        uint8_t distance_from_player
        bool lit
    }
    
    class MonsterManager {
        -Monster_t monsters[MON_TOTAL_ALLOCATIONS]
        -int16_t monster_levels[MON_MAX_LEVELS + 1]
        -Monster_t blank_monster
        -int16_t next_free_monster_id
        -int16_t monster_multiply_total
        +monsterPlaceNew()
        +monsterPlaceWinning()
        +monsterPlaceNewWithinDistance()
        +monsterSummon()
        +monsterSummonUndead()
        +compactMonsters()
    }
    
    class Coord_t {
        <<struct>>
        int16_t x
        int16_t y
    }
    
    MonsterManager --> Monster_t : manages
    MonsterManager --> Coord_t : uses
```

### Module Dependencies

```mermaid
graph TD
    A[monster_manager_cpp] --> B[dungeon_manager]
    A --> C[creature_manager]
    A --> D[player_manager]
    A --> E[config_module]
    A --> F[random_generator]
    A --> G[utils_module]
    
    B --> H[dungeon_floor]
    C --> I[creature_database]
    D --> J[player_state]
    E --> K[monster_config]
    F --> L[random_functions]
    G --> M[coordinate_utils]
    
    style A fill:#f9f,stroke:#333
    style B fill:#bbf,stroke:#333
    style C fill:#bfb,stroke:#333
    style D fill:#fbb,stroke:#333
    style E fill:#ff9,stroke:#333
    style F fill:#9ff,stroke:#333
    style G fill:#9f9,stroke:#333
```

## Detailed Component Documentation

### Monster Management Functions

#### `monsterPlaceNew`
Places a new monster at a specified coordinate with given properties.

```mermaid
sequenceDiagram
    participant MM as MonsterManager
    participant DM as DungeonManager
    participant CM as CreatureManager
    
    MM->>CM: Get creature data by ID
    MM->>DM: Check coordinate validity
    MM->>MM: Initialize monster properties
    MM->>DM: Set creature_id in floor tile
    MM->>MM: Return success status
```

#### `monsterPlaceWinning`
Places the winning monster at a random location when player wins.

#### `monsterPlaceNewWithinDistance`
Places multiple monsters within a specified distance from the player.

#### `monsterSummon`
Summons a monster adjacent to a given coordinate.

#### `monsterSummonUndead`
Summons an undead monster specifically.

#### `compactMonsters`
Removes distant monsters to optimize memory usage.

### Data Flow and Processing

```mermaid
flowchart TD
    A[Game Start] --> B[Initialize Monster Arrays]
    B --> C[Load Monster Levels]
    C --> D[Set Next Free ID]
    D --> E[Main Game Loop]
    E --> F{Monster Spawn Needed?}
    F -->|Yes| G[monsterPlaceNew/monsterSummon]
    F -->|No| H[Process Monster Actions]
    G --> I[Allocate Monster ID]
    I --> J[Set Monster Properties]
    J --> K[Update Dungeon Grid]
    K --> L[Return Success]
    H --> M[Monster AI Processing]
    M --> N[Update Monster State]
    N --> O[Check for Cleanup]
    O --> P{Monster Too Far?}
    P -->|Yes| Q[Compact Monsters]
    P -->|No| R[Continue Game]
```

## Integration Points

### With Dungeon Management
The monster manager directly interacts with the dungeon grid through `dg.floor[coord.y][coord.x].creature_id` to place and update monster positions.

### With Creature Database
Uses `creatures_list[creature_id]` to access creature properties like hit dice, speed, defenses, and sprite information.

### With Player Management
References `py.pos` and `py.flags.speed` to calculate monster speeds and distances.

### With Configuration System
Depends on configuration values from `config::monsters` namespace for:
- Monster level definitions
- Spawn probabilities
- Movement patterns
- Combat behaviors

## Key Algorithms

### Monster Allocation Algorithm
```mermaid
graph LR
    A[popm()] --> B{next_free_monster_id < MON_TOTAL_ALLOCATIONS?}
    B -->|Yes| C[Return next_free_monster_id]
    B -->|No| D[compactMonsters()]
    D --> E{compactMonsters() successful?}
    E -->|Yes| F[Return next_free_monster_id]
    E -->|No| G[Return -1]
```

### Level-Based Monster Selection
```mermaid
graph TD
    A[monsterGetOneSuitableForLevel] --> B{Level = 0?}
    B -->|Yes| C[Random from level 0]
    B -->|No| D{Level > MON_MAX_LEVELS?}
    D -->|Yes| E[Set level = MON_MAX_LEVELS]
    D -->|No| F[Check MON_CHANCE_OF_NASTY]
    F -->|Nasty| G[Add normal distribution offset]
    F -->|Regular| H[Select from level range]
```

## Performance Considerations

The monster manager implements several optimization strategies:
1. **Memory Compaction**: Removes distant monsters to prevent memory bloat
2. **Efficient Allocation**: Uses a simple counter-based allocation system
3. **Batch Placement**: Handles multiple monster placements efficiently
4. **Collision Avoidance**: Ensures proper coordinate validation before placement

## Error Handling

The module includes robust error handling:
- Returns false when monster allocation fails
- Uses abort() when critical monster placement fails during win condition
- Validates coordinates and dungeon states before placing monsters
- Implements retry mechanisms for monster placement

## External References

For detailed information about related systems, see:
- [creature_manager.md](creature_manager.md)
- [dungeon_manager.md](dungeon_manager.md)
- [player_manager.md](player_manager.md)
- [config_module.md](config_module.md)
