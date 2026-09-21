# Character Handling Module Documentation

## Introduction

The `character_h` module provides the foundational data structures and functions for character management in the game system. This module defines the core character attributes, race characteristics, class specifications, and background information that are essential for character creation and gameplay mechanics. It serves as a critical component that interfaces with various subsystems including combat, magic, and character progression systems.

## Core Data Structures

### Race Structure (Race_t)
The `Race_t` structure defines all racial characteristics that affect character stats and abilities:

```mermaid
classDiagram
    class Race_t {
        <<struct>>
        name: const char*
        str_adjustment: int16_t
        int_adjustment: int16_t
        wis_adjustment: int16_t
        dex_adjustment: int16_t
        con_adjustment: int16_t
        chr_adjustment: int16_t
        base_age: uint8_t
        max_age: uint8_t
        male_height_base: uint8_t
        male_height_mod: uint8_t
        male_weight_base: uint8_t
        male_weight_mod: uint8_t
        female_height_base: uint8_t
        female_height_mod: uint8_t
        female_weight_base: uint8_t
        female_weight_mod: uint8_t
        disarm_chance_base: int16_t
        search_chance_base: int16_t
        stealth: int16_t
        fos: int16_t
        base_to_hit: int16_t
        base_to_hit_bows: int16_t
        saving_throw_base: int16_t
        hit_points_base: uint8_t
        infra_vision: uint8_t
        exp_factor_base: uint8_t
        classes_bit_field: uint8_t
    }
```

### Class Structure (Class_t)
The `Class_t` structure contains class-specific attributes and modifiers:

```mermaid
classDiagram
    class Class_t {
        <<struct>>
        title: const char*
        hit_points: uint8_t
        disarm_traps: uint8_t
        searching: uint8_t
        stealth: uint8_t
        fos: uint8_t
        base_to_hit: uint8_t
        base_to_hit_with_bows: uint8_t
        saving_throw: uint8_t
        strength: int16_t
        intelligence: int16_t
        wisdom: int16_t
        dexterity: int16_t
        constitution: int16_t
        charisma: int16_t
        class_to_use_mage_spells: uint8_t
        experience_factor: uint8_t
        min_level_for_spell_casting: uint8_t
    }
```

### Background Structure (Background_t)
The `Background_t` structure handles character background information used in character generation:

```mermaid
classDiagram
    class Background_t {
        <<struct>>
        info: const char*
        roll: uint8_t
        chart: uint8_t
        next: uint8_t
        bonus: uint8_t
    }
```

## Module Architecture

The character_h module integrates with several other system components:

```mermaid
graph TD
    A[character_h] --> B[character_create]
    A --> C[combat_system]
    A --> D[magic_system]
    A --> E[stats_system]
    A --> F[gameplay_core]
    
    subgraph "System Integration"
        B --> C
        B --> D
        B --> E
        B --> F
    end
```

## Functionality Overview

### Character Creation Function
The primary function in this module is `characterCreate()`, which initializes character parameters based on race, class, and background selections. This function coordinates with other modules to ensure proper character initialization.

## Data Flow

```mermaid
sequenceDiagram
    participant C as characterCreate()
    participant R as Race Database
    participant Cl as Class Database
    participant B as Background System
    participant S as Stats Manager
    
    C->>R: Retrieve race data
    C->>Cl: Retrieve class data
    C->>B: Get background information
    C->>S: Apply stat modifications
    S-->>C: Return final character stats
```

## Component Interactions

The character_h module interacts with several other modules:

1. **Stats Management** ([stats.md](stats.md)): Processes racial and class stat adjustments
2. **Combat System** ([combat.md](combat.md)): Uses base to hit values and saving throws
3. **Magic System** ([magic.md](magic.md)): Accesses spell casting requirements and experience factors
4. **Gameplay Core** ([gameplay.md](gameplay.md)): Integrates with main game loop and character progression

## Implementation Details

The module uses fixed-size integer types to ensure consistent memory usage across different platforms. All string pointers are declared as `const char*` to prevent accidental modification of static strings.

## Dependencies

This module depends on:
- Standard C library headers for basic data types
- Memory management functions for dynamic allocation if needed
- Game state management for accessing current character data

## Usage Patterns

The typical usage pattern involves:
1. Loading race, class, and background data from configuration files
2. Calling `characterCreate()` to initialize a new character
3. Using the returned character data in gameplay calculations
4. Updating character statistics during gameplay events

## Related Modules

For complete character management, see:
- [stats.md](stats.md) - Statistical processing and calculation
- [combat.md](combat.md) - Combat-related character attributes
- [magic.md](magic.md) - Spellcasting and magical abilities
- [gameplay.md](gameplay.md) - Core gameplay integration

## Performance Considerations

The module is designed for minimal overhead with fixed-size structures that allow efficient memory access. All operations should be fast enough for real-time gameplay without significant performance impact.

## Future Extensibility

The modular design allows for easy extension of character attributes while maintaining backward compatibility with existing character data structures. New fields can be added to the structures without breaking existing functionality.
