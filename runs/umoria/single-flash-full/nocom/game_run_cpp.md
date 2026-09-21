# Game Run C++ Module Documentation

## Introduction

The `game_run_cpp` module serves as the core gameplay engine for the Moria game, managing the main game loop, player actions, dungeon navigation, and game state management. This module coordinates all major game systems including player movement, combat, inventory management, monster behavior, and dungeon generation.

## Architecture Overview

```mermaid
graph TD
    A[Game Start] --> B[Initialize Game State]
    B --> C[Load/Generate Character]
    C --> D[Main Game Loop]
    D --> E[Process Player Commands]
    E --> F[Update Game State]
    F --> G[Render Dungeon View]
    G --> H{Game Over?}
    H -->|No| D
    H -->|Yes| I[End Game]
    
    subgraph "Core Systems"
        D --> J[Player Management]
        D --> K[Monster System]
        D --> L[Dungeon Generation]
        D --> M[Inventory System]
        D --> N[Combat System]
    end
    
    subgraph "Game Flow"
        J --> O[Movement]
        J --> P[Status Effects]
        J --> Q[Regeneration]
        K --> R[Monster AI]
        L --> S[Dungeon Layout]
        M --> T[Item Handling]
        N --> U[Combat Mechanics]
    end
```

## Component Relationships

### Main Entry Point
The `startMoria` function serves as the primary entry point for the game, orchestrating the entire game lifecycle:

```mermaid
sequenceDiagram
    participant S as startMoria
    participant C as Character Creation
    participant G as Game Loop
    participant E as End Game
    
    S->>C: Initialize game state
    C->>S: Create character or load save
    S->>G: Enter main game loop
    G->>S: Process commands until game over
    S->>E: Clean up and exit
```

### Game Loop Structure
The main game loop (`playDungeon`) manages the continuous gameplay experience:

```mermaid
graph LR
    A[Start Turn] --> B[Update Status Effects]
    B --> C[Process Player Input]
    C --> D[Handle Commands]
    D --> E[Update Monsters]
    E --> F[Check Game Conditions]
    F --> G{Generate Level?}
    G -->|Yes| H[Generate New Level]
    G -->|No| I[Continue Game]
    I --> A
```

## Data Flow and Processing

### Player Command Processing
```mermaid
graph TD
    A[Input Command] --> B[Parse Command]
    B --> C{Valid Command?}
    C -->|Yes| D[Execute Command]
    C -->|No| E[Show Help/Error]
    D --> F[Update Game State]
    F --> G[Render Display]
    G --> H[Next Turn]
    
    subgraph "Command Execution"
        D --> I[Movement]
        D --> J[Combat]
        D --> K[Inventory]
        D --> L[Special Actions]
    end
```

### Game State Management
The module maintains complex game state through several key structures:

```mermaid
graph LR
    A[Player State] --> B[Character Stats]
    A --> C[Inventory]
    A --> D[Status Effects]
    A --> E[Location Info]
    
    B --> F[Attributes]
    B --> G[Hit Points]
    B --> H[Mana]
    B --> I[Experience]
    
    C --> J[Items]
    C --> K[Equipment]
    C --> L[Weight Limits]
    
    D --> M[Temporary Effects]
    D --> N[Permanent Status]
    D --> O[Timed Buffs]
    
    E --> P[Position]
    E --> Q[Dungeon Level]
    E --> R[Depth Tracking]
```

## Key Functions and Their Roles

### Game Initialization
The initialization functions prepare the game world:

- `initializeCharacterInventory()` - Sets up starting equipment
- `initializeMonsterLevels()` - Configures monster spawning levels
- `initializeTreasureLevels()` - Sets up treasure distribution
- `priceAdjust()` - Applies cost adjustments to items

### Player Management
Core player functionality includes:

- **Status Updates**: `playerUpdateBlindness()`, `playerUpdateConfusion()`, etc.
- **Regeneration**: `playerRegenerateHitPoints()`, `playerFoodConsumption()`
- **Light Management**: `playerUpdateLightStatus()`, `playerInitializePlayerLight()`
- **Movement**: `playerMove()`, `playerRunAndFind()`, `playerTunnel()`

### Combat and Interaction
Combat and interaction systems:

- **Combat Actions**: `playerBash()`, `playerThrowItem()`, `playerTeleport()`
- **Item Handling**: `inventoryExecuteCommand()`, `inventoryCarryItem()`
- **Spell System**: `getAndCastMagicSpell()`, `spellIdentifyItem()`
- **Dungeon Navigation**: `dungeonGoUpLevel()`, `dungeonGoDownLevel()`

### Game Loop Components
The main game loop processes:

1. **Turn Management**: `playDungeon()` controls the game turn sequence
2. **Command Processing**: `executeInputCommands()` handles user input
3. **State Updates**: All status effects and conditions are updated each turn
4. **Monster AI**: `updateMonsters()` manages enemy behavior
5. **Dungeon Generation**: `generateCave()` creates new dungeon levels

## Integration with Other Modules

This module integrates with several other core systems:

- **[character](character.md)**: Manages character creation and stats
- **[dungeon](dungeon.md)**: Handles dungeon generation and layout
- **[monster](monster.md)**: Controls monster placement and behavior
- **[inventory](inventory.md)**: Manages player inventory and items
- **[combat](combat.md)**: Processes combat mechanics and damage calculation
- **[magic](magic.md)**: Handles spell casting and magical effects
- **[store](store.md)**: Manages shop interactions and pricing

## Game Flow Control

The module implements sophisticated game flow control:

```mermaid
graph TD
    A[Game Start] --> B{Load Save?}
    B -->|Yes| C[Load Game State]
    B -->|No| D[Create New Character]
    
    C --> E[Initialize Systems]
    D --> E
    
    E --> F[Main Game Loop]
    F --> G{Character Dead?}
    G -->|No| H[Process Turn]
    H --> I{End of Level?}
    I -->|Yes| J[Generate New Level]
    I -->|No| F
    
    G -->|Yes| K[End Game]
    
    subgraph "Turn Processing"
        H --> L[Update Status]
        H --> M[Handle Input]
        H --> N[Update Monsters]
        H --> O[Render Display]
    end
```

## Error Handling and Safety

The module implements robust error handling:

- **Input Validation**: `validCountCommand()` validates command sequences
- **Boundary Checks**: Coordinate validation prevents out-of-bounds access
- **State Consistency**: Multiple safety checks ensure game state integrity
- **Resource Management**: Proper cleanup during game termination

## Performance Considerations

The module is designed for efficient performance:

- **Turn-based Processing**: Only processes necessary updates each turn
- **Efficient State Updates**: Batch processing of similar status effects
- **Memory Management**: Careful handling of game objects and arrays
- **Conditional Processing**: Only executes expensive operations when needed

## Configuration Dependencies

The module relies on several configuration settings:

- `config::options::use_roguelike_keys` - Controls key binding schemes
- `COST_ADJUSTMENT` - Modifies item prices
- Various constants from `config::player`, `config::monsters`, and `config::treasure`

This module forms the central nervous system of the Moria game, coordinating all gameplay elements and maintaining the game state throughout the player's adventure.
