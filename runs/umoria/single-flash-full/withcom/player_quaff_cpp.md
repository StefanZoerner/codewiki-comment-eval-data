# player_quaff_cpp Module Documentation

## Brief Introduction

The `player_quaff_cpp` module handles the logic for players quaffing (drinking) potions in the game. It processes potion effects, manages player status changes, and handles identification of potions. This module is part of the core gameplay mechanics that affect player attributes, status conditions, and magical effects.

## Module Overview

This module implements the quaffing functionality for potions, including:
- Potion effect processing and application
- Player attribute modifications
- Status condition management
- Potion identification and experience gain
- Food consumption from potions

## Architecture and Component Relationships

```mermaid
graph TD
    A[quaff()] --> B[playerDrinkPotion()]
    B --> C[PotionSpellTypes]
    B --> D[Player Attribute Functions]
    B --> E[Status Condition Functions]
    B --> F[Experience Management]
    B --> G[Identification Logic]
    
    D --> H[playerStatRandomIncrease()]
    D --> I[playerStatRestore()]
    D --> J[spellLoseSTR/INT/WIS/CHR/CON/DEX]
    
    E --> K[spellChangePlayerHitPoints()]
    E --> L[playerCureBlindness()]
    E --> M[playerCureConfusion()]
    E --> N[playerCurePoison()]
    E --> O[spellSlowPoison()]
    E --> P[spellRestorePlayerLevels()]
    E --> Q[playerRemoveFear()]
    
    F --> R[displayCharacterExperience()]
    F --> S[spellLoseEXP()]
    
    G --> T[itemIdentify()]
    G --> U[itemSetAsTried()]
    G --> V[itemSetColorlessAsIdentified()]
    
    subgraph "Core Game Systems"
        D
        E
        F
        G
    end
    
    subgraph "Game Mechanics"
        A
        B
        C
    end
```

## Data Flow and Process Flow

```mermaid
flowchart TD
    A[Player initiates quaff command] --> B{Inventory has potions?}
    B -- No --> C[Display "No potions" message]
    B -- Yes --> D[Find potion range in inventory]
    D --> E[Get user input for potion selection]
    E --> F{Selected potion has flags?}
    F -- No --> G[Display "less thirsty" message]
    F -- Yes --> H[playerDrinkPotion()]
    H --> I[Process potion effects]
    I --> J{Effect identified?}
    J -- Yes --> K[Update identification]
    J -- No --> L[Mark as tried]
    K --> M[Apply experience gain]
    K --> N[Update item identification]
    L --> O[Mark item as tried]
    M --> P[Display updated experience]
    N --> Q[Update character display]
    O --> Q
    Q --> R[Consume food from potion]
    R --> S[Update item count description]
    S --> T[Destroy consumed potion]
```

## Key Components and Functionality

### Main Entry Point: `quaff()`
The primary function that handles the player's quaffing action. It:
- Checks for available potions in inventory
- Gets user selection for which potion to quaff
- Processes the potion effect through `playerDrinkPotion()`
- Handles identification and experience gain
- Manages food consumption and item destruction

### Core Processing: `playerDrinkPotion()`
Processes individual potion effects based on flags and item type:
- **Attribute Changes**: Strength, Intelligence, Wisdom, Charisma, Constitution, Dexterity
- **Status Conditions**: Blindness, Confusion, Poison, Sleep, Paralysis
- **Combat Effects**: Healing, Damage, Haste, Slowness
- **Special Effects**: Experience gain, Identification, Resists, Vision

### Potion Spell Types Enum
The `PotionSpellTypes` enum defines all possible potion effects:
- **Attribute Modification**: Strength, Intelligence, Wisdom, Charisma, Constitution, Dexterity
- **Status Conditions**: Blindness, Confusion, Poison, Sleep, Paralysis
- **Healing Effects**: Light, Serious, Critical wounds, General healing
- **Magical Effects**: Haste, Slowness, Invulnerability, Heroism, Super Heroism
- **Resistance Effects**: Heat, Cold resistance
- **Detection**: Invisibility detection
- **Poison Treatment**: Slow poison, neutralize poison
- **Mana Restoration**: Restore mana
- **Experience**: Gain/Lose experience
- **Miscellaneous**: Salt water, boldness, restore life levels

## Integration with Other Modules

This module integrates with several core game systems:

### Inventory Management
- Uses `inventoryFindRange()` to locate potions in inventory
- Calls `inventoryGetInputForItemId()` for user selection
- Implements `inventoryDestroyItem()` to remove consumed potions
- Works with `itemTypeRemainingCountDescription()` for inventory updates

### Character System
- Interfaces with `playerStatRandomIncrease()` and `playerStatRestore()` for attribute changes
- Uses `spellChangePlayerHitPoints()` for healing effects
- Integrates with `playerCureBlindness()`, `playerCureConfusion()`, `playerCurePoison()` for status removal
- Calls `playerRemoveFear()` for fear-related effects

### Experience and Progression
- Connects to `displayCharacterExperience()` for experience updates
- Uses `spellLoseEXP()` for experience loss effects
- Implements experience gain through `py.misc.exp` manipulation

### Item Identification
- Relies on `itemSetColorlessAsIdentified()` for identification logic
- Uses `itemIdentify()` for full identification
- Implements `itemSetAsTried()` for unidentifiable potions

## Dependencies

This module depends on:
- [headers.h](headers.md) - Core game headers and definitions
- [inventory_system](inventory_system.md) - Inventory management functions
- [character_system](character_system.md) - Player attribute and status functions
- [experience_system](experience_system.md) - Experience calculation and display
- [item_system](item_system.md) - Item identification and management

## Error Handling and Edge Cases

The module handles several edge cases:
- Empty inventory checks before potion selection
- Flag validation for potion effects
- Status condition prevention (e.g., cannot sleep when already paralyzed)
- Experience overflow protection
- Food consumption limits for salt water potions
- Proper identification state management

## Performance Considerations

The module is designed for efficient processing of potion effects:
- Bit manipulation for flag processing (`getAndClearFirstBit()`)
- Early returns for simple cases
- Minimal memory allocation during execution
- Direct access to player state variables

## Security and Safety

The module ensures safe operation by:
- Validating potion flags before processing
- Checking status conditions before applying effects
- Preventing duplicate status applications
- Managing experience values within safe ranges
- Proper cleanup of consumed items
