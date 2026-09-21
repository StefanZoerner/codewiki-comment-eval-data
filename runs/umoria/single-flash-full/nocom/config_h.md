# config_h Module Documentation

## Brief Introduction

The `config_h` module serves as the central configuration repository for the game system, defining constants and parameters that control various aspects of gameplay behavior, dungeon generation, monster properties, player attributes, and more. This module provides a structured approach to managing game configuration values through namespaces and constants, ensuring consistency across different parts of the application.

## Module Architecture

```mermaid
graph TD
    A[config_h Module] --> B[files]
    A --> C[options]
    A --> D[dungeon]
    A --> E[treasure]
    A --> F[monsters]
    A --> G[player]
    A --> H[identification]
    A --> I[spells]
    A --> J[stores]

    B --> B1[splash_screen]
    B --> B2[welcome_screen]
    B --> B3[license]
    B --> B4[versions_history]
    B --> B5[help]
    B --> B6[help_wizard]
    B --> B7[help_roguelike]
    B --> B8[help_roguelike_wizard]
    B --> B9[death_tomb]
    B --> B10[death_royal]
    B --> B11[scores]
    B --> B12[save_game]

    C --> C1[display_counts]
    C --> C2[find_bound]
    C --> C3[run_cut_corners]
    C --> C4[run_examine_corners]
    C --> C5[run_ignore_doors]
    C --> C6[run_print_self]
    C --> C7[highlight_seams]
    C --> C8[prompt_to_pickup]
    C --> C9[use_roguelike_keys]
    C --> C10[show_inventory_weights]
    C --> C11[error_beep_sound]

    D --> D1[DUN_RANDOM_DIR]
    D --> D2[DUN_DIR_CHANGE]
    D --> D3[DUN_TUNNELING]
    D --> D4[DUN_ROOMS_MEAN]
    D --> D5[DUN_ROOM_DOORS]
    D --> D6[DUN_TUNNEL_DOORS]
    D --> D7[DUN_STREAMER_DENSITY]
    D --> D8[DUN_STREAMER_WIDTH]
    D --> D9[DUN_MAGMA_STREAMER]
    D --> D10[DUN_MAGMA_TREASURE]
    D --> D11[DUN_QUARTZ_STREAMER]
    D --> D12[DUN_QUARTZ_TREASURE]
    D --> D13[DUN_UNUSUAL_ROOMS]
    
    D --> D14[objects]
    D14 --> D15[OBJ_OPEN_DOOR]
    D14 --> D16[OBJ_CLOSED_DOOR]
    D14 --> D17[OBJ_SECRET_DOOR]
    D14 --> D18[OBJ_UP_STAIR]
    D14 --> D19[OBJ_DOWN_STAIR]
    D14 --> D20[OBJ_STORE_DOOR]
    D14 --> D21[OBJ_TRAP_LIST]
    D14 --> D22[OBJ_RUBBLE]
    D14 --> D23[OBJ_MUSH]
    D14 --> D24[OBJ_SCARE_MON]
    D14 --> D25[OBJ_GOLD_LIST]
    D14 --> D26[OBJ_NOTHING]
    D14 --> D27[OBJ_RUINED_CHEST]
    D14 --> D28[OBJ_WIZARD]
    D14 --> D29[MAX_GOLD_TYPES]
    D14 --> D30[MAX_TRAPS]
    D14 --> D31[LEVEL_OBJECTS_PER_ROOM]
    D14 --> D32[LEVEL_OBJECTS_PER_CORRIDOR]
    D14 --> D33[LEVEL_TOTAL_GOLD_AND_GEMS]

    E --> E1[MIN_TREASURE_LIST_ID]
    E --> E2[TREASURE_CHANCE_OF_GREAT_ITEM]
    E --> E3[LEVEL_STD_OBJECT_ADJUST]
    E --> E4[LEVEL_MIN_OBJECT_STD]
    E --> E5[LEVEL_TOWN_OBJECTS]
    E --> E6[OBJECT_BASE_MAGIC]
    E --> E7[OBJECT_MAX_BASE_MAGIC]
    E --> E8[OBJECT_CHANCE_SPECIAL]
    E --> E9[OBJECT_CHANCE_CURSED]
    E --> E10[OBJECT_LAMP_MAX_CAPACITY]
    E --> E11[OBJECT_BOLTS_MAX_RANGE]
    E --> E12[OBJECTS_RUNE_PROTECTION]
    
    E --> E13[flags]
    E13 --> E14[TR_STATS]
    E13 --> E15[TR_STR]
    E13 --> E16[TR_INT]
    E13 --> E17[TR_WIS]
    E13 --> E18[TR_DEX]
    E13 --> E19[TR_CON]
    E13 --> E20[TR_CHR]
    E13 --> E21[TR_SEARCH]
    E13 --> E22[TR_SLOW_DIGEST]
    E13 --> E23[TR_STEALTH]
    E13 --> E24[TR_AGGRAVATE]
    E13 --> E25[TR_TELEPORT]
    E13 --> E26[TR_REGEN]
    E13 --> E27[TR_SPEED]
    E13 --> E28[TR_EGO_WEAPON]
    E13 --> E29[TR_SLAY_DRAGON]
    E13 --> E30[TR_SLAY_ANIMAL]
    E13 --> E31[TR_SLAY_EVIL]
    E13 --> E32[TR_SLAY_UNDEAD]
    E13 --> E33[TR_FROST_BRAND]
    E13 --> E34[TR_FLAME_TONGUE]
    E13 --> E35[TR_RES_FIRE]
    E13 --> E36[TR_RES_ACID]
    E13 --> E37[TR_RES_COLD]
    E13 --> E38[TR_SUST_STAT]
    E13 --> E39[TR_FREE_ACT]
    E13 --> E40[TR_SEE_INVIS]
    E13 --> E41[TR_RES_LIGHT]
    E13 --> E42[TR_FFALL]
    E13 --> E43[TR_BLIND]
    E13 --> E44[TR_TIMID]
    E13 --> E45[TR_TUNNEL]
    E13 --> E46[TR_INFRA]
    E13 --> E47[TR_CURSED]
    
    E --> E48[chests]
    E48 --> E49[CH_LOCKED]
    E48 --> E50[CH_TRAPPED]
    E48 --> E51[CH_LOSE_STR]
    E48 --> E52[CH_POISON]
    E48 --> E53[CH_PARALYSED]
    E48 --> E54[CH_EXPLODE]
    E48 --> E55[CH_SUMMON]

    F --> F1[MON_CHANCE_OF_NEW]
    F --> F2[MON_MAX_SIGHT]
    F --> F3[MON_MAX_SPELL_CAST_DISTANCE]
    F --> F4[MON_MAX_MULTIPLY_PER_LEVEL]
    F --> F5[MON_MULTIPLY_ADJUST]
    F --> F6[MON_CHANCE_OF_NASTY]
    F --> F7[MON_MIN_PER_LEVEL]
    F --> F8[MON_MIN_TOWNSFOLK_DAY]
    F --> F9[MON_MIN_TOWNSFOLK_NIGHT]
    F --> F10[MON_ENDGAME_MONSTERS]
    F --> F11[MON_ENDGAME_LEVEL]
    F --> F12[MON_SUMMONED_LEVEL_ADJUST]
    F --> F13[MON_PLAYER_EXP_DRAINED_PER_HIT]
    F --> F14[MON_MIN_INDEX_ID]
    F --> F15[SCARE_MONSTER]
    
    F --> F16[move]
    F16 --> F17[CM_ALL_MV_FLAGS]
    F16 --> F18[CM_ATTACK_ONLY]
    F16 --> F19[CM_MOVE_NORMAL]
    F16 --> F20[CM_ONLY_MAGIC]
    F16 --> F21[CM_RANDOM_MOVE]
    F16 --> F22[CM_20_RANDOM]
    F16 --> F23[CM_40_RANDOM]
    F16 --> F24[CM_75_RANDOM]
    F16 --> F25[CM_SPECIAL]
    F16 --> F26[CM_INVISIBLE]
    F16 --> F27[CM_OPEN_DOOR]
    F16 --> F28[CM_PHASE]
    F16 --> F29[CM_EATS_OTHER]
    F16 --> F30[CM_PICKS_UP]
    F16 --> F31[CM_MULTIPLY]
    F16 --> F32[CM_SMALL_OBJ]
    F16 --> F33[CM_CARRY_OBJ]
    F16 --> F34[CM_CARRY_GOLD]
    F16 --> F35[CM_TREASURE]
    F16 --> F36[CM_TR_SHIFT]
    F16 --> F37[CM_60_RANDOM]
    F16 --> F38[CM_90_RANDOM]
    F16 --> F39[CM_1D2_OBJ]
    F16 --> F40[CM_2D2_OBJ]
    F16 --> F41[CM_4D2_OBJ]
    F16 --> F42[CM_WIN]
    
    F --> F43[spells]
    F43 --> F44[CS_FREQ]
    F43 --> F45[CS_SPELLS]
    F43 --> F46[CS_TEL_SHORT]
    F43 --> F47[CS_TEL_LONG]
    F43 --> F48[CS_TEL_TO]
    F43 --> F49[CS_LGHT_WND]
    F43 --> F50[CS_SER_WND]
    F43 --> F51[CS_HOLD_PER]
    F43 --> F52[CS_BLIND]
    F43 --> F53[CS_CONFUSE]
    F43 --> F54[CS_FEAR]
    F43 --> F55[CS_SUMMON_MON]
    F43 --> F56[CS_SUMMON_UND]
    F43 --> F57[CS_SLOW_PER]
    F43 --> F58[CS_DRAIN_MANA]
    F43 --> F59[CS_BREATHE]
    F43 --> F60[CS_BR_LIGHT]
    F43 --> F61[CS_BR_GAS]
    F43 --> F62[CS_BR_ACID]
    F43 --> F63[CS_BR_FROST]
    F43 --> F64[CS_BR_FIRE]
    
    F --> F65[defense]
    F65 --> F66[CD_DRAGON]
    F65 --> F67[CD_ANIMAL]
    F65 --> F68[CD_EVIL]
    F65 --> F69[CD_UNDEAD]
    F65 --> F70[CD_WEAKNESS]
    F65 --> F71[CD_FROST]
    F65 --> F72[CD_FIRE]
    F65 --> F73[CD_POISON]
    F65 --> F74[CD_ACID]
    F65 --> F75[CD_LIGHT]
    F65 --> F76[CD_STONE]
    F65 --> F77[CD_NO_SLEEP]
    F65 --> F78[CD_INFRA]
    F65 --> F79[CD_MAX_HP]

    G --> G1[PLAYER_MAX_EXP]
    G --> G2[PLAYER_USE_DEVICE_DIFFICULTY]
    G --> G3[PLAYER_FOOD_FULL]
    G --> G4[PLAYER_FOOD_MAX]
    G --> G5[PLAYER_FOOD_FAINT]
    G --> G6[PLAYER_FOOD_WEAK]
    G --> G7[PLAYER_FOOD_ALERT]
    G --> G8[PLAYER_REGEN_FAINT]
    G --> G9[PLAYER_REGEN_WEAK]
    G --> G10[PLAYER_REGEN_NORMAL]
    G --> G11[PLAYER_REGEN_HPBASE]
    G --> G12[PLAYER_REGEN_MNBASE]
    G --> G13[PLAYER_WEIGHT_CAP]
    
    G --> G14[status]
    G14 --> G15[PY_HUNGRY]
    G14 --> G16[PY_WEAK]
    G14 --> G17[PY_BLIND]
    G14 --> G18[PY_CONFUSED]
    G14 --> G19[PY_FEAR]
    G14 --> G20[PY_POISONED]
    G14 --> G21[PY_FAST]
    G14 --> G22[PY_SLOW]
    G14 --> G23[PY_SEARCH]
    G14 --> G24[PY_REST]
    G14 --> G25[PY_STUDY]
    G14 --> G26[PY_INVULN]
    G14 --> G27[PY_HERO]
    G14 --> G28[PY_SHERO]
    G14 --> G29[PY_BLESSED]
    G14 --> G30[PY_DET_INV]
    G14 --> G31[PY_TIM_INFRA]
    G14 --> G32[PY_SPEED]
    G14 --> G33[PY_STR_WGT]
    G14 --> G34[PY_PARALYSED]
    G14 --> G35[PY_REPEAT]
    G14 --> G36[PY_ARMOR]
    G14 --> G37[PY_STATS]
    G14 --> G38[PY_STR]
    G14 --> G39[PY_INT]
    G14 --> G40[PY_WIS]
    G14 --> G41[PY_DEX]
    G14 --> G42[PY_CON]
    G14 --> G43[PY_CHR]
    G14 --> G44[PY_HP]
    G14 --> G45[PY_MANA]

    H --> H1[OD_TRIED]
    H --> H2[OD_KNOWN1]
    H --> H3[ID_MAGIK]
    H --> H4[ID_DAMD]
    H --> H5[ID_EMPTY]
    H --> H6[ID_KNOWN2]
    H --> H7[ID_STORE_BOUGHT]
    H --> H8[ID_SHOW_HIT_DAM]
    H --> H9[ID_NO_SHOW_P1]
    H --> H10[ID_SHOW_P1]

    I --> I1[SPELL_TYPE_NONE]
    I --> I2[SPELL_TYPE_MAGE]
    I --> I3[SPELL_TYPE_PRIEST]
    I --> I4[NAME_OFFSET_SPELLS]
    I --> I5[NAME_OFFSET_PRAYERS]

    J --> J1[STORE_MAX_AUTO_BUY_ITEMS]
    J --> J2[STORE_MIN_AUTO_SELL_ITEMS]
    J --> J3[STORE_STOCK_TURN_AROUND]
```

## Component Interactions

### Configuration Data Flow

```mermaid
sequenceDiagram
    participant GameEngine
    participant ConfigModule
    participant DungeonGen
    participant MonsterSystem
    participant PlayerSystem
    participant TreasureSystem

    GameEngine->>ConfigModule: Request configuration values
    ConfigModule-->>GameEngine: Return constant values
    
    GameEngine->>DungeonGen: Use dungeon parameters
    DungeonGen-->>ConfigModule: Access DUN_* constants
    
    GameEngine->>MonsterSystem: Apply monster settings
    MonsterSystem-->>ConfigModule: Access MON_* constants
    
    GameEngine->>PlayerSystem: Configure player attributes
    PlayerSystem-->>ConfigModule: Access PLAYER_* constants
    
    GameEngine->>TreasureSystem: Set treasure rules
    TreasureSystem-->>ConfigModule: Access TREASURE_* constants
```

## Integration Points

This module integrates with several other system components:

- **[dungeon_gen](dungeon_gen.md)** - Uses dungeon generation constants for room creation and tunneling algorithms
- **[monster_system](monster_system.md)** - Relies on monster behavior and combat parameters
- **[player_system](player_system.md)** - Provides player attribute and status definitions
- **[treasure_system](treasure_system.md)** - Accesses treasure distribution and object properties
- **[ui_system](ui_system.md)** - Uses file path constants for UI elements like splash screens and help files

## Key Design Principles

1. **Namespace Organization**: Constants are grouped logically within namespaces to improve maintainability
2. **Type Safety**: All constants use appropriate integer types (uint8_t, uint16_t) for memory efficiency
3. **Readability**: Meaningful constant names provide clear semantic meaning
4. **Centralized Management**: All game configuration values are defined in one location for easy modification

## Usage Examples

The configuration constants are typically accessed directly by other modules:

```cpp
// Example usage in dungeon generation
if (dungeon_param == config::dungeon::DUN_RANDOM_DIR) {
    // Handle random direction logic
}

// Example usage in monster behavior
if (monster_flags & config::monsters::move::CM_INVISIBLE) {
    // Process invisible monster behavior
}
```

## Dependencies

This module has no external dependencies but is referenced by multiple other modules including:
- [dungeon_gen](dungeon_gen.md)
- [monster_system](monster_system.md)
- [player_system](player_system.md)
- [treasure_system](treasure_system.md)
- [ui_system](ui_system.md)

## Maintenance Notes

When modifying configuration values:
1. Ensure type compatibility with existing code
2. Update related documentation if constants have semantic changes
3. Verify that dependent systems still function correctly
4. Consider impact on game balance and difficulty levels
