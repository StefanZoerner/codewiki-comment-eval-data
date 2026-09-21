# config_cpp Module Documentation

## Brief Introduction

The `config_cpp` module serves as the central configuration repository for the Umoria game engine. It defines all game constants, settings, and parameters that control gameplay behavior, dungeon generation, monster properties, player characteristics, and other core game mechanics. This module provides a single source of truth for all configurable values, making it easier to tune and modify game behavior without scattered hard-coded values throughout the codebase.

## Architecture Overview

```mermaid
graph TD
    A[config_cpp Module] --> B[Game Files Configuration]
    A --> C[Game Options]
    A --> D[Dungeon Generation]
    A --> E[Treasure System]
    A --> F[Monster Behavior]
    A --> G[Player Characteristics]
    A --> H[Object Identification]
    A --> I[Spell System]
    A --> J[Store Management]

    B --> B1[Data File Paths]
    C --> C1[User Preferences]
    C --> C2[Gameplay Settings]
    D --> D1[Dungeon Parameters]
    D --> D2[Object Placement]
    E --> E1[Treasure Constants]
    E --> E2[Item Flags]
    E --> E3[Chest Properties]
    F --> F1[Monster Spawn Rates]
    F --> F2[Movement Patterns]
    F --> F3[Spell Abilities]
    F --> F4[Defense Properties]
    G --> G1[Experience Limits]
    G --> G2[Hunger System]
    G --> G3[Regeneration Rates]
    G --> G4[Weight Capacity]
    G --> G5[Status Effects]
    H --> H1[Identification Flags]
    I --> I1[Spell Types]
    I --> I2[Spell Names]
    J --> J1[Store Inventory]
```

## Detailed Component Documentation

### Game Files Configuration

The `files` namespace contains all relative file paths used by the game. These paths are relative to the executable binary location and define where various game data files are stored.

```mermaid
graph LR
    subgraph File_Configuration
        A[splash_screen] --> B[data/splash.txt]
        C[welcome_screen] --> D[data/welcome.txt]
        E[license] --> F[LICENSE]
        G[versions_history] --> H[data/versions.txt]
        I[help] --> J[data/help.txt]
        K[help_wizard] --> L[data/help_wizard.txt]
        M[help_roguelike] --> N[data/rl_help.txt]
        O[help_roguelike_wizard] --> P[data/rl_help_wizard.txt]
        Q[death_tomb] --> R[data/death_tomb.txt]
        S[death_royal] --> T[data/death_royal.txt]
        U[scores] --> V[scores.dat]
        W[save_game] --> X[game.sav]
    end
```

### Game Options

The `options` namespace defines user-configurable game settings that can be modified at runtime or during initialization.

```mermaid
graph LR
    subgraph Game_Options
        A[display_counts] --> B[Boolean]
        C[find_bound] --> D[Boolean]
        E[run_cut_corners] --> F[Boolean]
        G[run_examine_corners] --> H[Boolean]
        I[run_ignore_doors] --> J[Boolean]
        K[run_print_self] --> L[Boolean]
        M[highlight_seams] --> N[Boolean]
        O[prompt_to_pickup] --> P[Boolean]
        Q[use_roguelike_keys] --> R[Boolean]
        S[show_inventory_weights] --> T[Boolean]
        U[error_beep_sound] --> V[Boolean]
    end
```

### Dungeon Generation Parameters

The `dungeon` namespace controls all aspects of dungeon generation including room placement, tunneling patterns, and object distribution.

```mermaid
graph TD
    subgraph Dungeon_Parameters
        A[DUN_RANDOM_DIR] --> B[9]
        C[DUN_DIR_CHANGE] --> D[70]
        E[DUN_TUNNELING] --> F[15]
        G[DUN_ROOMS_MEAN] --> H[32]
        I[DUN_ROOM_DOORS] --> J[25]
        K[DUN_TUNNEL_DOORS] --> L[15]
        M[DUN_STREAMER_DENSITY] --> N[5]
        O[DUN_STREAMER_WIDTH] --> P[2]
        Q[DUN_MAGMA_STREAMER] --> R[3]
        S[DUN_MAGMA_TREASURE] --> T[90]
        U[DUN_QUARTZ_STREAMER] --> V[2]
        W[DUN_QUARTZ_TREASURE] --> X[40]
        Y[DUN_UNUSUAL_ROOMS] --> Z[300]
        
        subgraph Object_Placement
            AA[LEVEL_OBJECTS_PER_ROOM] --> AB[7]
            AC[LEVEL_OBJECTS_PER_CORRIDOR] --> AD[2]
            AE[LEVEL_TOTAL_GOLD_AND_GEMS] --> AF[2]
        end
    end
```

### Treasure System Constants

The `treasure` namespace defines treasure generation rules, magic item properties, and object flag definitions.

```mermaid
graph TD
    subgraph Treasure_Constants
        A[MIN_TREASURE_LIST_ID] --> B[1]
        C[TREASURE_CHANCE_OF_GREAT_ITEM] --> D[12]
        E[LEVEL_STD_OBJECT_ADJUST] --> F[125]
        G[LEVEL_MIN_OBJECT_STD] --> H[7]
        I[LEVEL_TOWN_OBJECTS] --> J[7]
        K[OBJECT_BASE_MAGIC] --> L[15]
        M[OBJECT_MAX_BASE_MAGIC] --> N[70]
        O[OBJECT_CHANCE_SPECIAL] --> P[6]
        Q[OBJECT_CHANCE_CURSED] --> R[13]
        S[OBJECT_LAMP_MAX_CAPACITY] --> T[15000]
        U[OBJECT_BOLTS_MAX_RANGE] --> V[18]
        W[OBJECTS_RUNE_PROTECTION] --> X[3000]
        
        subgraph Object_Flags
            Y[TR_STATS] --> Z[0x0000003F]
            AA[TR_STR] --> AB[0x00000001]
            AC[TR_INT] --> AD[0x00000002]
            AE[TR_WIS] --> AF[0x00000004]
            AG[TR_DEX] --> AH[0x00000008]
            AI[TR_CON] --> AJ[0x00000010]
            AK[TR_CHR] --> AL[0x00000020]
            AM[TR_SEARCH] --> AN[0x00000040]
            AO[TR_SLOW_DIGEST] --> AP[0x00000080]
            AQ[TR_STEALTH] --> AR[0x00000100]
            AS[TR_AGGRAVATE] --> AT[0x00000200]
            AU[TR_TELEPORT] --> AV[0x00000400]
            AW[TR_REGEN] --> AX[0x00000800]
            AY[TR_SPEED] --> AZ[0x00001000]
            
            BA[TR_EGO_WEAPON] --> BB[0x0007E000]
            BC[TR_SLAY_DRAGON] --> BD[0x00002000]
            BE[TR_SLAY_ANIMAL] --> BF[0x00004000]
            BG[TR_SLAY_EVIL] --> BH[0x00008000]
            BI[TR_SLAY_UNDEAD] --> BJ[0x00010000]
            BK[TR_FROST_BRAND] --> BL[0x00020000]
            BM[TR_FLAME_TONGUE] --> BN[0x00040000]
            
            BO[TR_RES_FIRE] --> BP[0x00080000]
            BQ[TR_RES_ACID] --> BR[0x00100000]
            BS[TR_RES_COLD] --> BT[0x00200000]
            BU[TR_SUST_STAT] --> BV[0x00400000]
            BW[TR_FREE_ACT] --> BX[0x00800000]
            BY[TR_SEE_INVIS] --> BZ[0x01000000]
            CA[TR_RES_LIGHT] --> CB[0x02000000]
            CC[TR_FFALL] --> CD[0x04000000]
            CE[TR_BLIND] --> CF[0x08000000]
            CG[TR_TIMID] --> CH[0x10000000]
            CI[TR_TUNNEL] --> CJ[0x20000000]
            CK[TR_INFRA] --> CL[0x40000000]
            CM[TR_CURSED] --> CN[0x80000000]
        end
        
        subgraph Chest_Properties
            CO[CH_LOCKED] --> CP[0x00000001]
            CQ[CH_TRAPPED] --> CR[0x000001F0]
            CS[CH_LOSE_STR] --> CT[0x00000010]
            CU[CH_POISON] --> CV[0x00000020]
            CW[CH_PARALYSED] --> CX[0x00000040]
            CY[CH_EXPLODE] --> CZ[0x00000080]
            DA[CH_SUMMON] --> DB[0x00000100]
        end
    end
```

### Monster Behavior Parameters

The `monsters` namespace controls monster spawning rates, behaviors, and combat properties.

```mermaid
graph TD
    subgraph Monster_Parameters
        A[MON_CHANCE_OF_NEW] --> B[160]
        C[MON_MAX_SIGHT] --> D[20]
        E[MON_MAX_SPELL_CAST_DISTANCE] --> F[20]
        G[MON_MAX_MULTIPLY_PER_LEVEL] --> H[75]
        I[MON_MULTIPLY_ADJUST] --> J[7]
        K[MON_CHANCE_OF_NASTY] --> L[50]
        M[MON_MIN_PER_LEVEL] --> N[14]
        O[MON_MIN_TOWNSFOLK_DAY] --> P[4]
        Q[MON_MIN_TOWNSFOLK_NIGHT] --> R[8]
        S[MON_ENDGAME_MONSTERS] --> T[2]
        U[MON_ENDGAME_LEVEL] --> V[50]
        W[MON_SUMMONED_LEVEL_ADJUST] --> X[2]
        Y[MON_PLAYER_EXP_DRAINED_PER_HIT] --> Z[2]
        AA[MON_MIN_INDEX_ID] --> AB[2]
        AC[SCARE_MONSTER] --> AD[99]
        
        subgraph Movement_Behavior
            AE[CM_ALL_MV_FLAGS] --> AF[0x0000003F]
            AG[CM_ATTACK_ONLY] --> AH[0x00000001]
            AI[CM_MOVE_NORMAL] --> AJ[0x00000002]
            AK[CM_ONLY_MAGIC] --> AL[0x00000004]
            AM[CM_RANDOM_MOVE] --> AN[0x00000038]
            AO[CM_20_RANDOM] --> AP[0x00000008]
            AQ[CM_40_RANDOM] --> AR[0x00000010]
            AS[CM_75_RANDOM] --> AT[0x00000020]
            AU[SPECIAL] --> AV[0x003F0000]
            AW[CM_INVISIBLE] --> AX[0x00010000]
            AY[CM_OPEN_DOOR] --> AZ[0x00020000]
            BA[CM_PHASE] --> BB[0x00040000]
            BC[CM_EATS_OTHER] --> BD[0x00080000]
            BE[CM_PICKS_UP] --> BF[0x00100000]
            BG[CM_MULTIPLY] --> BH[0x00200000]
            BI[CM_SMALL_OBJ] --> BJ[0x00800000]
            BK[CM_CARRY_OBJ] --> BL[0x01000000]
            BM[CM_CARRY_GOLD] --> BN[0x02000000]
            BO[CM_TREASURE] --> BP[0x7C000000]
            BQ[CM_TR_SHIFT] --> BR[26]
            BS[CM_60_RANDOM] --> BT[0x04000000]
            BU[CM_90_RANDOM] --> BV[0x08000000]
            BW[CM_1D2_OBJ] --> BX[0x10000000]
            BY[CM_2D2_OBJ] --> BZ[0x20000000]
            CA[CM_4D2_OBJ] --> CB[0x40000000]
            CC[CM_WIN] --> CD[0x80000000]
        end
        
        subgraph Spell_Definitions
            CE[CS_FREQ] --> CF[0x0000000F]
            CG[CS_SPELLS] --> CH[0x0001FFF0]
            CI[CS_TEL_SHORT] --> CJ[0x00000010]
            CK[CS_TEL_LONG] --> CL[0x00000020]
            CM[CS_TEL_TO] --> CN[0x00000040]
            CO[CS_LGHT_WND] --> CP[0x00000080]
            CQ[CS_SER_WND] --> CR[0x00000100]
            CS[CS_HOLD_PER] --> CT[0x00000200]
            CU[CS_BLIND] --> CV[0x00000400]
            CW[CS_CONFUSE] --> CX[0x00000800]
            CY[CS_FEAR] --> CZ[0x00001000]
            DA[CS_SUMMON_MON] --> DB[0x00002000]
            DC[CS_SUMMON_UND] --> DD[0x00004000]
            DE[CS_SLOW_PER] --> DF[0x00008000]
            DG[CS_DRAIN_MANA] --> DH[0x00010000]
            DI[CS_BREATHE] --> DJ[0x00F80000]
            DK[CS_BR_LIGHT] --> DL[0x00080000]
            DM[CS_BR_GAS] --> DN[0x00100000]
            DO[CS_BR_ACID] --> DP[0x00200000]
            DQ[CS_BR_FROST] --> DR[0x00400000]
            DS[CS_BR_FIRE] --> DT[0x00800000]
        end
        
        subgraph Defense_Properties
            DU[CD_DRAGON] --> DV[0x0001]
            DW[CD_ANIMAL] --> DX[0x0002]
            DY[CD_EVIL] --> DZ[0x0004]
            EA[CD_UNDEAD] --> EB[0x0008]
            EC[CD_WEAKNESS] --> ED[0x03F0]
            EE[CD_FROST] --> EF[0x0010]
            EG[CD_FIRE] --> EH[0x0020]
            EI[CD_POISON] --> EJ[0x0040]
            EK[CD_ACID] --> EL[0x0080]
            EM[CD_LIGHT] --> EN[0x0100]
            EO[CD_STONE] --> EP[0x0200]
            EQ[CD_NO_SLEEP] --> ER[0x1000]
            ES[CD_INFRA] --> ET[0x2000]
            EU[CD_MAX_HP] --> EV[0x4000]
        end
    end
```

### Player Characteristics

The `player` namespace defines player-related constants including experience limits, hunger system, regeneration rates, and status effects.

```mermaid
graph TD
    subgraph Player_Parameters
        A[PLAYER_MAX_EXP] --> B[9999999]
        C[PLAYER_USE_DEVICE_DIFFICULTY] --> D[3]
        E[PLAYER_FOOD_FULL] --> F[10000]
        G[PLAYER_FOOD_MAX] --> H[15000]
        I[PLAYER_FOOD_FAINT] --> J[300]
        K[PLAYER_FOOD_WEAK] --> L[1000]
        M[PLAYER_FOOD_ALERT] --> N[2000]
        O[PLAYER_REGEN_FAINT] --> P[33]
        Q[PLAYER_REGEN_WEAK] --> R[98]
        S[PLAYER_REGEN_NORMAL] --> T[197]
        U[PLAYER_REGEN_HPBASE] --> V[1442]
        W[PLAYER_REGEN_MNBASE] --> X[524]
        Y[PLAYER_WEIGHT_CAP] --> Z[130]
        
        subgraph Status_Effects
            AA[PY_HUNGRY] --> AB[0x00000001]
            AC[PY_WEAK] --> AD[0x00000002]
            AE[PY_BLIND] --> AF[0x00000004]
            AG[PY_CONFUSED] --> AH[0x00000008]
            AI[PY_FEAR] --> AJ[0x00000010]
            AK[PY_POISONED] --> AL[0x00000020]
            AM[PY_FAST] --> AN[0x00000040]
            AO[PY_SLOW] --> AP[0x00000080]
            AQ[PY_SEARCH] --> AR[0x00000100]
            AS[PY_REST] --> AT[0x00000200]
            AU[PY_STUDY] --> AV[0x00000400]
            AW[PY_INVULN] --> AX[0x00001000]
            AY[PY_HERO] --> AZ[0x00002000]
            BA[PY_SHERO] --> BB[0x00004000]
            BC[PY_BLESSED] --> BD[0x00008000]
            BE[PY_DET_INV] --> BF[0x00010000]
            BG[PY_TIM_INFRA] --> BH[0x00020000]
            BI[PY_SPEED] --> BJ[0x00040000]
            BK[PY_STR_WGT] --> BL[0x00080000]
            BM[PY_PARALYSED] --> BN[0x00100000]
            BO[PY_REPEAT] --> BP[0x00200000]
            BQ[PY_ARMOR] --> BR[0x00400000]
            BS[PY_STATS] --> BT[0x3F000000]
            BU[PY_STR] --> BV[0x01000000]
            BW[PY_INT] --> BX[0x02000000]
            BY[PY_WIS] --> BZ[0x04000000]
            CA[PY_DEX] --> CB[0x08000000]
            CC[PY_CON] --> CD[0x10000000]
            CE[PY_CHR] --> CF[0x20000000]
            CG[PY_HP] --> CH[0x40000000]
            CI[PY_MANA] --> CJ[0x80000000]
        end
    end
```

### Object Identification System

The `identification` namespace manages how objects are identified and tracked within the game.

```mermaid
graph LR
    subgraph Identification_Flags
        A[OD_TRIED] --> B[0x1]
        C[OD_KNOWN1] --> D[0x2]
        E[ID_MAGIK] --> F[0x1]
        G[ID_DAMD] --> H[0x2]
        I[ID_EMPTY] --> J[0x4]
        K[ID_KNOWN2] --> L[0x8]
        M[ID_STORE_BOUGHT] --> N[0x10]
        O[ID_SHOW_HIT_DAM] --> P[0x20]
        Q[ID_NO_SHOW_P1] --> R[0x40]
        S[ID_SHOW_P1] --> T[0x80]
    end
```

### Spell System Configuration

The `spells` namespace defines spell types and naming conventions.

```mermaid
graph LR
    subgraph Spell_Configuration
        A[SPELL_TYPE_NONE] --> B[0]
        C[SPELL_TYPE_MAGE] --> D[1]
        E[SPELL_TYPE_PRIEST] --> F[2]
        G[NAME_OFFSET_SPELLS] --> H[0]
        I[NAME_OFFSET_PRAYERS] --> J[31]
    end
```

### Store Management Parameters

The `stores` namespace controls store inventory management and trading behavior.

```mermaid
graph LR
    subgraph Store_Parameters
        A[STORE_MAX_AUTO_BUY_ITEMS] --> B[18]
        C[STORE_MIN_AUTO_SELL_ITEMS] --> D[10]
        E[STORE_STOCK_TURN_AROUND] --> F[9]
    end
```

## Integration with Other Modules

This module integrates with several other core modules:

- **[game_logic.md](game_logic.md)**: Uses dungeon generation parameters for level creation
- **[monster_system.md](monster_system.md)**: References monster behavior and spell definitions
- **[player_system.md](player_system.md)**: Depends on player characteristics for character stats and status effects
- **[inventory_system.md](inventory_system.md)**: Utilizes treasure system constants for item generation
- **[spell_system.md](spell_system.md)**: Accesses spell type definitions for class-based abilities

## Usage Guidelines

All configuration values should be accessed through their respective namespaces rather than directly accessing individual variables. This ensures consistency and makes future modifications easier to implement. The configuration values are typically read-only after initialization and should not be modified during gameplay unless specifically designed for dynamic adjustment.

## Maintenance Notes

When modifying configuration values:
1. Ensure changes align with intended gameplay balance
2. Test thoroughly with existing game mechanics
3. Update related documentation if applicable
4. Consider impact on save file compatibility
5. Document any significant changes to default values

This module serves as the foundation for all game behavior customization and should be treated as a critical component requiring careful consideration during any modifications.
