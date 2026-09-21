# inventory_cpp Module Documentation

## Overview

The `inventory_cpp` module provides core functionality for managing player inventory in the Moria game system. It handles item collection, stacking, carrying capacity calculations, item destruction, dropping, and various damage effects on inventory items. This module interfaces with the player's equipment system and dungeon objects to maintain consistent inventory state.

## Architecture

```mermaid
graph TD
    A[Player Inventory System] --> B[Item Management]
    A --> C[Equipment Integration]
    A --> D[Damage Effects]
    A --> E[Carrying Capacity]
    
    B --> B1[Item Collection]
    B --> B2[Item Destruction]
    B --> B3[Item Dropping]
    B --> B4[Item Stacking]
    
    C --> C1[Equipment Status]
    C --> C2[Equipment Removal]
    
    D --> D1[Corrosive Gas]
    D --> D2[Poison Gas]
    D --> D3[Fire Damage]
    D --> D4[Cold Damage]
    D --> D5[Lightning Bolt]
    D --> D6[Acid Damage]
    
    E --> E1[Weight Calculation]
    E --> E2[Capacity Checking]
```

## Component Relationships

### Core Data Structures

The inventory system relies on several key data structures:

- **Inventory_t**: Represents individual items in the player's inventory
- **PlayerPack_t**: Manages the player's carrying capacity and unique items count
- **PlayerEquipment**: Enum defining equipment slots (Wield, Body, etc.)

### Key Functions

#### Item Management Functions

```mermaid
flowchart LR
    subgraph ItemManagement
        A[inventoryCollectAllItemFlags]
        B[inventoryDestroyItem]
        C[inventoryTakeOneItem]
        D[inventoryDropItem]
        E[inventoryCarryItem]
        F[inventoryCanCarryItem]
        G[inventoryCanCarryItemCount]
    end
    
    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
```

#### Damage Effect Functions

```mermaid
flowchart LR
    subgraph DamageEffects
        A[damageCorrodingGas]
        B[damagePoisonedGas]
        C[damageFire]
        D[damageCold]
        E[damageLightningBolt]
        F[damageAcid]
    end
    
    A -->|acid_damage| B
    B -->|poison_damage| C
    C -->|fire_damage| D
    D -->|cold_damage| E
    E -->|lightning_damage| F
    F -->|acid_damage| A
```

## Module Dependencies

This module depends on several other system components:

- [headers.h](headers.md): Provides essential type definitions and global variables
- [player.cpp](player.md): Interfaces with player status and equipment systems
- [dungeon.cpp](dungeon.md): Manages dungeon objects and floor interactions
- [game.cpp](game.md): Accesses game-wide treasure and object data
- [messages.cpp](messages.cpp): Handles message printing to user interface

## Detailed Function Descriptions

### Item Collection and Flags

```cpp
uint32_t inventoryCollectAllItemFlags()
```
Collects all item flags from equipped items (Wield through Light) and returns them as a combined bitmask.

### Item Destruction

```cpp
void inventoryDestroyItem(int item_id)
```
Destroys an item by reducing stack count or removing it entirely from inventory. Updates weight and maintains inventory ordering.

### Item Transfer Operations

```cpp
void inventoryTakeOneItem(Inventory_t *to_item, Inventory_t *from_item)
```
Copies one item from source to destination, handling single-stackable items properly.

### Item Dropping

```cpp
void inventoryDropItem(int item_id, bool drop_all)
```
Handles dropping items from inventory onto dungeon floor, including equipment removal and proper weight management.

### Damage Handling

```cpp
static int inventoryDamageItem(bool (*item_type)(Inventory_t *), int chance_percentage)
```
Applies damage to items based on type and chance percentage, removing damaged items from inventory.

### Equipment Interaction

```cpp
bool inventoryDiminishLightAttack(bool noticed)
bool inventoryDiminishChargesAttack(uint8_t creature_level, int16_t &monster_hp, bool noticed)
bool executeDisenchantAttack()
```
Functions that interact with equipment during combat attacks, affecting light sources, staff/wand charges, and enchantments.

### Carrying Capacity Management

```cpp
bool inventoryCanCarryItemCount(Inventory_t const &item)
bool inventoryCanCarryItem(Inventory_t const &item)
int inventoryCarryItem(Inventory_t &new_item)
```
Functions that determine if items can be carried and handle adding items to inventory with proper stacking logic.

### Item Identification and Properties

```cpp
bool inventoryItemSingleStackable(Inventory_t const &item)
bool inventoryItemStackable(Inventory_t const &item)
bool inventoryItemIsCursed(const Inventory_t &item)
void inventoryItemRemoveCurse(Inventory_t &item)
```
Helper functions for determining item properties and managing cursed items.

### Damage Type Specific Functions

```cpp
void damageCorrodingGas(const char *creature_name)
void damagePoisonedGas(int damage, const char *creature_name)
void damageFire(int damage, const char *creature_name)
void damageCold(int damage, const char *creature_name)
void damageLightningBolt(int damage, const char *creature_name)
void damageAcid(int damage, const char *creature_name)
```
Specialized damage handlers that affect inventory items based on damage type and resistance properties.

## Data Flow

```mermaid
sequenceDiagram
    participant P as Player
    participant I as InventorySystem
    participant D as Dungeon
    participant G as Game
    
    P->>I: Request item action
    I->>I: Validate action
    I->>P: Update status flags
    I->>D: Modify dungeon objects
    I->>G: Update treasure list
    G->>I: Return updated state
    I->>P: Display messages
```

## Integration Points

The inventory system integrates with:

1. **Player Status**: Updates PY_STR_WGT flag when weight changes
2. **Dungeon Objects**: Manages treasure placement and deletion
3. **Game Objects**: Accesses object definitions and properties
4. **Equipment System**: Coordinates with player equipment management
5. **Combat System**: Handles damage effects on inventory items

## Usage Patterns

The module follows these usage patterns:

1. **Item Addition**: Using `inventoryCarryItem()` to add new items to inventory
2. **Item Removal**: Through `inventoryDestroyItem()` or `inventoryDropItem()`
3. **Status Updates**: Automatic flag updates when inventory changes
4. **Damage Application**: Automatic item damage based on environmental effects
5. **Equipment Management**: Integration with equipment slot operations

This module forms a critical part of the game's resource management system, ensuring players can effectively manage their inventory while maintaining game balance through proper carrying capacity limits and item durability mechanics.
