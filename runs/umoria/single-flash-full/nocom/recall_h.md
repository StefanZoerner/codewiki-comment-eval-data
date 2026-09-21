# recall_h Documentation

## Brief Introduction

The `recall_h` module provides the header definitions and declarations necessary for creature memory recall functionality within the game system. This module defines the data structures used to store and retrieve creature information, along with function prototypes for accessing and displaying creature recall data.

## Module Overview

The `recall_h` module serves as the interface definition for creature memory recall operations. It declares the `Recall_t` structure that stores detailed information about creatures, along with arrays of descriptive strings for various creature attributes and behaviors. The module also exposes functions for retrieving and processing creature recall information.

## Data Structures

### Recall_t Structure

The `Recall_t` structure holds comprehensive information about a creature's characteristics and behaviors:

```c
typedef struct {
    uint32_t movement;           // Movement pattern identifier
    uint32_t spells;             // Spell casting abilities
    uint16_t kills;              // Number of kills
    uint16_t deaths;             // Number of deaths
    uint16_t defenses;           // Defense capabilities
    uint8_t wake;                // Wake-up behavior flag
    uint8_t ignore;              // Ignore behavior flag
    uint8_t attacks[MON_MAX_ATTACKS]; // Attack types array
} Recall_t;
```

### Global Variables

The module declares several global arrays containing descriptive strings for different creature attributes:

- `recall_description_attack_type[25]` - Attack type descriptions
- `recall_description_attack_method[20]` - Attack method descriptions  
- `recall_description_how_much[8]` - Quantity descriptions
- `recall_description_move[6]` - Movement description
- `recall_description_spell[15]` - Spell descriptions
- `recall_description_breath[5]` - Breath attack descriptions
- `recall_description_weakness[6]` - Weakness descriptions

## Function Prototypes

### memoryRecall Function

```c
int memoryRecall(int monster_id);
```

Retrieves and processes recall information for a specific monster by ID. Returns an integer status code indicating success or failure.

### recallMonsterAttributes Function

```c
void recallMonsterAttributes(char command);
```

Processes and displays creature attributes based on the provided command character. This function likely handles user commands for viewing different aspects of creature recall data.

## Component Relationships

The `recall_h` module works in conjunction with other system components:

- **[monster_h](monster_h.md)**: Depends on `MON_MAX_CREATURES` and `MON_MAX_ATTACKS` constants for array sizing
- **[memory_h](memory_h.md)**: Integrates with memory management systems for storing creature recall data
- **[display_h](display_h.md)**: Works with display systems to render creature recall information to users

## Architecture Integration

The module fits into the broader system architecture as part of the creature information management subsystem. It provides the foundational data structures and interfaces needed for:

1. Creature knowledge tracking
2. Memory recall functionality
3. Information display systems
4. Game state persistence

## Dependencies

This module depends on:
- Constants defined in [monster_h](monster_h.md) (MON_MAX_CREATURES, MON_MAX_ATTACKS)
- Standard C library headers for basic data types
- Memory management components from [memory_h](memory_h.md)

## Usage Context

The `recall_h` module is typically used when:
- Players want to examine creature characteristics
- Game systems need to access stored creature information
- Display systems require formatted creature data
- Memory management systems update creature recall entries

## Implementation Notes

The module uses fixed-size arrays for creature recall data, which means the maximum number of creatures and attacks must be defined elsewhere in the system. The use of `uint8_t` and `uint16_t` types suggests memory efficiency considerations for large creature databases.

For detailed implementation of the actual recall functionality, see the corresponding [recall.c](recall.c.md) implementation file.
