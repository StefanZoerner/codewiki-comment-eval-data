# Character Handling Module Documentation

## Introduction

The `character_h` module provides the foundational data structures and function declarations for creating and managing player characters in the game system. This module defines the core attributes that determine character capabilities, racial traits, class abilities, and background information that collectively shape the player's in-game persona.

## Core Data Structures

### Race Structure (Race_t)
The `Race_t` structure defines the racial characteristics that influence a character's base attributes and abilities:

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
The `Class_t` structure defines the class-specific modifiers and abilities that affect gameplay mechanics:

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
The `Background_t` structure stores historical information and social class details for character backgrounds:

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

## Function Declaration

### characterCreate()
The `characterCreate()` function serves as the primary interface for initializing and generating player characters within the game system.

## Module Relationships

This module works in conjunction with several other system components:

- **[character_gen](character_gen.md)**: Handles the actual generation logic for player characters using the defined structures
- **[attributes](attributes.md)**: Manages the attribute calculations and modifications based on race and class data
- **[classes](classes.md)**: Provides class-specific rules and mechanics that interact with the Class_t structure
- **[races](races.md)**: Contains race definitions and management that populate the Race_t structure

## Data Flow

```mermaid
flowchart TD
    A[Character Generation System] --> B[characterCreate()]
    B --> C[Race Selection]
    B --> D[Class Selection]
    B --> E[Background Assignment]
    C --> F[Populate Race_t]
    D --> G[Populate Class_t]
    E --> H[Populate Background_t]
    F --> I[Attributes Calculation]
    G --> I
    H --> I
    I --> J[Final Character Object]
```

## Implementation Details

The module uses standard C data types with specific sizes to ensure portability across different platforms. The use of `int16_t` for adjustments allows for both positive and negative modifiers while maintaining precision. The `const char*` pointers provide string references for descriptive fields without requiring memory allocation during runtime.

## Usage Patterns

1. **Initialization**: The structures are typically populated from configuration files or database entries
2. **Runtime Access**: Game systems reference these structures to apply racial and class bonuses
3. **Character Creation**: The `characterCreate()` function orchestrates the combination of these elements into a complete character profile

## Dependencies

This module depends on:
- Standard C library headers for basic data types
- [attributes](attributes.md) for attribute calculation logic
- [classes](classes.md) for class-specific behavior implementation
- [races](races.md) for race definitions and validation

## Notes

The module intentionally separates character definition from character creation logic, allowing for flexible character generation systems that can utilize the same data structures across different game contexts. The use of bit fields and modifiers enables complex interactions between race, class, and background elements while maintaining performance through simple arithmetic operations.
