# Character C++ Module Documentation

## Introduction

The `character_cpp` module handles the complete character creation process for players in the game. This module manages all aspects of character generation including stat allocation, race selection, class assignment, history generation, and initial equipment setup. It serves as the primary interface for creating new player characters and ensures proper initialization of all character attributes.

## Module Overview

This module contains the core logic for character creation, including:
- Stat generation using dice rolls
- Race and class selection
- History generation based on racial background
- Age, height, and weight calculation
- Gold distribution based on character attributes
- Character name input

## Architecture and Component Relationships

```mermaid
graph TD
    A[characterCreate] --> B[characterChooseRace]
    A --> C[characterSetGender]
    A --> D[characterGenerateStatsAndRace]
    A --> E[characterGetHistory]
    A --> F[characterSetAgeHeightWeight]
    A --> G[characterGetClass]
    A --> H[playerCalculateStartGold]
    A --> I[getCharacterName]
    
    D --> J[characterGenerateStats]
    D --> K[createModifyPlayerStat]
    D --> L[character_races]
    
    E --> M[character_backgrounds]
    E --> N[playerClearHistory]
    
    G --> O[displayRaceClasses]
    G --> P[generateCharacterClass]
    
    P --> Q[classes]
    P --> R[playerStatAdjustmentConstitution]
    
    subgraph "Character Generation Flow"
        A
        B
        C
        D
        E
        F
        G
        H
        I
    end
    
    subgraph "Supporting Functions"
        J
        K
        L
        M
        N
        O
        P
        Q
        R
    end
```

## Data Flow and Processing

```mermaid
sequenceDiagram
    participant U as User
    participant C as characterCreate()
    participant R as characterChooseRace()
    participant G as characterSetGender()
    participant S as characterGenerateStatsAndRace()
    participant H as characterGetHistory()
    participant A as characterSetAgeHeightWeight()
    participant C2 as characterGetClass()
    participant G2 as playerCalculateStartGold()
    participant N as getCharacterName()
    
    U->>C: Start character creation
    C->>R: Display race options
    R->>U: Wait for race selection
    U->>C: Select race
    C->>G: Display gender options
    G->>U: Wait for gender selection
    U->>C: Select gender
    C->>S: Generate base stats
    S->>J: Roll dice for stats
    J->>S: Return generated stats
    S->>K: Apply race adjustments
    K->>S: Return adjusted stats
    S->>H: Generate character history
    H->>M: Process background data
    H->>S: Return history data
    S->>A: Calculate age/height/weight
    A->>S: Return physical attributes
    S->>C2: Display class options
    C2->>U: Wait for class selection
    U->>C: Select class
    C->>G2: Calculate starting gold
    G2->>C: Return gold amount
    C->>N: Get character name
    N->>C: Return name
    C->>U: Display final character sheet
```

## Core Components

### Character Creation Process

The main entry point `characterCreate()` orchestrates the entire character creation process:

1. **Race Selection**: Players choose from available races using `characterChooseRace()`
2. **Gender Selection**: Players select their character's gender using `characterSetGender()`
3. **Stat Generation**: Base stats are generated and adjusted for race using `characterGenerateStatsAndRace()`
4. **History Generation**: Character background is created using `characterGetHistory()`
5. **Physical Attributes**: Age, height, and weight are calculated using `characterSetAgeHeightWeight()`
6. **Class Selection**: Players choose their character class using `characterGetClass()`
7. **Gold Calculation**: Starting gold is determined based on character attributes using `playerCalculateStartGold()`
8. **Name Input**: Final character name is collected using `getCharacterName()`

### Stat Generation System

The stat generation uses a unique rolling system:

```mermaid
graph LR
    A[Roll 3d3, 4d4, 5d5...] --> B[Sum all dice]
    B --> C{Total <= 42 OR >= 54}
    C -->|Yes| A
    C -->|No| D[Assign to 6 stats]
    D --> E[Apply race modifiers]
```

### Race and Class Integration

The module integrates with external data structures:
- `character_races[]`: Contains race-specific attributes and modifiers
- `classes[]`: Contains class-specific bonuses and penalties
- `character_backgrounds[]`: Provides historical context for characters

### Attribute Adjustment Functions

The module includes specialized functions for modifying character attributes:

```mermaid
graph TD
    A[createModifyPlayerStat] --> B{Adjustment < 0}
    B -->|Yes| C[decrementStat]
    B -->|No| D[incrementStat]
    C --> E[Apply decrement rules]
    D --> F[Apply increment rules]
```

## External Dependencies

This module depends on several other modules and systems:

- [headers.h](headers.md): Provides global definitions and includes
- [player.h](player.md): Manages player state and attributes
- [config.h](config.md): Configuration settings for game parameters
- [input.h](input.md): Input handling for user interactions
- [display.h](display.md): Screen rendering and text output functions

## Key Functions

### Primary Entry Points
- `characterCreate()`: Main character creation routine
- `characterChooseRace()`: Handles race selection UI
- `characterGetClass()`: Manages class selection process

### Stat Management
- `characterGenerateStats()`: Generates base character stats
- `createModifyPlayerStat()`: Applies race/class adjustments to stats
- `playerCalculateStartGold()`: Calculates starting gold amount

### Character Information
- `characterGetHistory()`: Generates character background story
- `characterSetAgeHeightWeight()`: Calculates physical attributes
- `displayCharacterHistory()`: Displays character background

## Data Structures Used

The module works with several key data structures:

- `Race_t`: Defines race properties and modifiers
- `Class_t`: Defines class bonuses and penalties  
- `Background_t`: Stores historical background information
- `PlayerAttr`: Enum for player attribute types
- `Coord_t`: Coordinate system for screen positioning

## Process Flows

### Character Creation Loop

```mermaid
graph TD
    A[Start character creation] --> B[Display race selection]
    B --> C[User selects race]
    C --> D[Display gender selection]
    D --> E[User selects gender]
    E --> F[Generate stats and apply race modifiers]
    F --> G[Generate character history]
    G --> H[Calculate physical attributes]
    H --> I[Display character sheet]
    I --> J{User accepts?}
    J -->|No| F
    J -->|Yes| K[Select class]
    K --> L[Calculate starting gold]
    L --> M[Get character name]
    M --> N[Finalize character]
```

### Stat Modification Logic

The module implements different stat modification rules based on current stat values:

```mermaid
graph TD
    A[Stat modification] --> B{Stat Value Range}
    B -->|< 18| C[Simple increment/decrement]
    B -->|18-88| D[Randomized adjustment]
    B -->|88-108| E[Higher randomization]
    B -->|> 108| F[Minimal changes]
```

## Integration Points

This module integrates with:
- Player state management through `py` global structure
- Input/output systems for user interaction
- Configuration systems for game parameters
- Display systems for character information presentation

The character creation process is designed to be modular and extensible, allowing for easy addition of new races, classes, and character features while maintaining consistent behavior across the game system.
