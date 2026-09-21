# identification_cpp Module Documentation

## Introduction

The `identification_cpp` module handles the identification and description of game objects, including items, monsters, and dungeon features. It provides functions for identifying game objects by character representation, generating item descriptions, managing item identification flags, and handling item inscriptions. This module works closely with the inventory management system and game object definitions to provide detailed information about items in the player's possession.

## Architecture Overview

```mermaid
graph TD
    A[identification_cpp] --> B[Object Identification]
    A --> C[Item Description Generation]
    A --> D[Item Identification Management]
    A --> E[Monster Identification]
    
    B --> B1[character lookup]
    B --> B2[description generation]
    
    C --> C1[formatting]
    C --> C2[attribute display]
    C --> C3[inscriptions]
    
    D --> D1[flag management]
    D --> D2[identification state]
    D --> D3[tried status]
    
    E --> E1[monster names]
    E --> E2[creature descriptions]
```

## Component Relationships

### Core Components

The main component in this module is `identification.cpp`, which contains:

1. **Object Character Descriptions**: Functions to map character representations to descriptive text
2. **Item Identification Logic**: Management of item identification states and flags
3. **Item Description Generation**: Complex formatting logic for displaying item details
4. **Inscription Handling**: Functions for adding and managing item inscriptions
5. **Monster Identification**: Functions for describing monsters in the game world

### Data Structures

The module uses several key data structures:

```mermaid
classDiagram
    class objects_identified {
        <<array>>
        - uint8_t[OBJECT_IDENT_SIZE]
    }
    
    class magic_item_titles {
        <<array>>
        - char[MAX_TITLES][10]
    }
    
    class Inventory_t {
        - int category_id
        - int sub_category_id
        - int items_count
        - int identification
        - int special_name_id
        - int misc_use
        - int to_hit
        - int to_damage
        - int to_ac
        - int ac
        - int flags
        - char inscription[INSCRIPTION_SIZE]
    }
    
    class Monster_t {
        - int creature_id
        - bool lit
    }
    
    objects_identified --> Inventory_t
    magic_item_titles --> Inventory_t
```

## Dependencies

This module depends on several other modules:

- [headers.h](headers.md): Provides global definitions and includes
- [config](config.md): Configuration settings for identification flags and constants
- [game_objects](game_objects.md): Object definitions and properties
- [monsters](monsters.md): Monster definitions and creature information
- [inventory](inventory.md): Inventory management functions
- [utils](utils.md): Utility functions like string manipulation

## Data Flow

```mermaid
sequenceDiagram
    participant Player
    participant IdentificationModule
    participant GameObjects
    participant Inventory
    
    Player->>IdentificationModule: Request object identification
    IdentificationModule->>IdentificationModule: Lookup character description
    IdentificationModule->>GameObjects: Get object properties
    IdentificationModule->>Player: Display description
    
    Player->>IdentificationModule: Identify item
    IdentificationModule->>Inventory: Update identification flags
    IdentificationModule->>Player: Show updated item info
    
    Player->>IdentificationModule: Describe item
    IdentificationModule->>Inventory: Get item data
    IdentificationModule->>IdentificationModule: Format description
    IdentificationModule->>Player: Display formatted description
```

## Detailed Functionality

### Object Identification

The module provides functions to identify game objects by their character representation:

```cpp
void identifyGameObject()
```
This function prompts the user for a character and displays its description. It uses the `objectDescription()` helper function to map characters to descriptive text.

### Item Identification Management

The module maintains identification state for items through bit flags:

```cpp
void itemSetAsIdentified(int category_id, int sub_category_id)
void itemSetAsTried(Inventory_t const &item)
void spellItemIdentifyAndRemoveRandomInscription(Inventory_t &item)
```

These functions manage the identification state of items, tracking whether they've been identified, tried, or have specific identification attributes.

### Item Description Generation

The most complex functionality involves generating detailed item descriptions:

```cpp
void itemDescription(obj_desc_t description, Inventory_t const &item, bool add_prefix)
```

This function generates comprehensive item descriptions that include:
- Base item names
- Modifiers (colors, materials, etc.)
- Damage statistics
- Attribute bonuses
- Inscriptions
- Special properties

### Inscryption System

The module handles item inscriptions through these functions:

```cpp
void itemInscribe()
void itemAppendToInscription(Inventory_t &item, uint8_t item_ident_type)
void itemReplaceInscription(Inventory_t &item, const char *inscription)
```

These functions allow players to add custom inscriptions to items and manage existing ones.

## Process Flows

### Item Identification Process

```mermaid
flowchart TD
    A[User requests identification] --> B{Character valid?}
    B -- Yes --> C[Lookup description]
    C --> D[Display description]
    B -- No --> E[Error message]
    
    F[User identifies item] --> G{Valid category?}
    G -- Yes --> H[Set identification flag]
    H --> I[Clear tried flag]
    G -- No --> J[Return]
    
    K[User describes item] --> L[Get item data]
    L --> M[Format description]
    M --> N[Display formatted description]
```

### Item Description Generation

```mermaid
flowchart TD
    A[Generate item description] --> B{Item category}
    B --> C[Apply category-specific formatting]
    C --> D{Modify needed?}
    D -- Yes --> E[Apply modifiers]
    D -- No --> F[Use base name]
    F --> G[Add suffixes]
    G --> H[Add damage info]
    H --> I[Add attribute bonuses]
    I --> J[Add inscriptions]
    J --> K[Finalize format]
```

## Integration Points

This module integrates with:

1. **Inventory System**: Manages item identification flags and states
2. **Game Objects**: Uses object definitions for naming and properties
3. **Player Interface**: Provides text output for game interactions
4. **Monster System**: Handles monster identification messages
5. **Configuration**: Uses configuration options for display behavior

## Constants and Configuration

The module relies on several configuration constants:

- `OBJECT_IDENT_SIZE`: Size of identification tracking array
- `MAX_TITLES`: Maximum number of magic item titles
- Various identification flag constants from `config::identification`
- Item category constants from `TV_*` defines

## Error Handling

The module implements basic error checking:
- Invalid character input validation
- Boundary checks for arrays and indices
- Category validation for item operations
- Safe string operations to prevent buffer overflows

## Performance Considerations

The module is designed for efficiency:
- Pre-computed lookup tables for object descriptions
- Bit flag operations for fast identification state checks
- Minimal memory allocation during runtime
- Optimized string operations for item descriptions

This module forms a critical part of the game's user interface, providing essential information about the player's environment and possessions while maintaining efficient performance characteristics.
