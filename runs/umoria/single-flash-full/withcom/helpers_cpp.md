# helpers_cpp Module Documentation

## Brief Introduction

The `helpers_cpp` module provides essential utility functions for string manipulation, number conversion, and time handling within the Moria game system. This module contains helper functions that support various core functionalities including message formatting, string insertion operations, and date/time utilities.

## Comprehensive Documentation

### Module Overview

The `helpers_cpp` module serves as a collection of utility functions that provide common operations needed throughout the Moria game engine. These functions handle tasks such as bit manipulation, string processing, number conversion, and time formatting.

### Key Components

#### Bit Manipulation Functions

```mermaid
graph TD
    A[getAndClearFirstBit] --> B{Find first set bit}
    B --> C{Clear bit and return position}
    C --> D[Returns bit position or -1]
```

The `getAndClearFirstBit` function efficiently identifies and clears the first set bit in a 32-bit unsigned integer, returning its position or -1 if no bits are set.

#### String Manipulation Functions

```mermaid
graph TD
    A[insertNumberIntoString] --> B{Find substring location}
    B --> C{Replace with number}
    C --> D[Format with sign option]
    
    E[insertStringIntoString] --> F{Search for pattern}
    F --> G{Insert replacement string}
    G --> H[Update original string]
```

Two primary string manipulation functions exist:
- `insertNumberIntoString`: Inserts a numeric value into a string at a specified location
- `insertStringIntoString`: Inserts one string into another at a specific pattern match

#### Character Utilities

```mermaid
graph TD
    A[isVowel] --> B{Character classification}
    B --> C{Return boolean result}
```

The `isVowel` function determines whether a character is a vowel (case-insensitive).

#### Number Conversion

```mermaid
graph TD
    A[stringToNumber] --> B{Validate input}
    B --> C{Check range errors}
    C --> D{Verify end of string}
    D --> E{Return converted number}
```

The `stringToNumber` function safely converts strings to integers with comprehensive error checking.

#### Time Utilities

```mermaid
graph TD
    A[getCurrentUnixTime] --> B{Get current timestamp}
    B --> C[Return Unix time as uint32_t]
    
    D[humanDateString] --> E{Get local time}
    E --> F{Format date string}
    F --> G[Return formatted date]
```

Time-related utilities include:
- `getCurrentUnixTime`: Retrieves current Unix timestamp
- `humanDateString`: Formats current date in human-readable format

### Component Interactions

```mermaid
sequenceDiagram
    participant M as Main Game Logic
    participant H as helpers_cpp
    participant S as System Services
    
    M->>H: Call insertNumberIntoString()
    H->>M: Return modified string
    
    M->>H: Call stringToNumber()
    H->>M: Return converted number
    
    M->>H: Call humanDateString()
    H->>S: Get current time
    S-->>H: Return time data
    H->>M: Return formatted date string
```

### Data Flow

```mermaid
graph LR
    A[Input Strings] --> B[helpers_cpp]
    B --> C[Processed Strings]
    C --> D[Output to Game Engine]
    
    E[User Input] --> F[helpers_cpp]
    F --> G[Converted Numbers]
    G --> H[Game Logic]
    
    I[Current Time] --> J[helpers_cpp]
    J --> K[Formatted Date]
    K --> L[Display System]
```

### Dependencies

This module depends on:
- Standard C++ libraries (`<cassert>`, `<cstdlib>`, `<cstring>`, `<ctime>`)
- [headers.h](headers.h.md) - Provides common type definitions and constants
- [moria_constants.h](moria_constants.h.md) - Contains game-specific constants

### Integration Points

The `helpers_cpp` module integrates with several other modules:

1. **Message System**: Uses `insertNumberIntoString` for formatting game messages
2. **Save/Load System**: Utilizes `stringToNumber` for parsing save files
3. **UI System**: Employs `humanDateString` for displaying game dates
4. **Game Logic**: Leverages `getAndClearFirstBit` for state management

### Error Handling

All functions implement proper error handling:
- `stringToNumber` performs comprehensive validation with errno checking
- Boundary checks prevent buffer overflows in string operations
- Safe bit manipulation prevents undefined behavior

### Performance Considerations

- Bit manipulation uses efficient bitwise operations
- String operations use optimized standard library functions
- Memory usage is minimal with stack-based allocations
- Time functions avoid unnecessary system calls

### Usage Examples

```cpp
// Example usage of string insertion
char message[MORIA_MESSAGE_SIZE];
strcpy(message, "Damage: {damage}");
insertNumberIntoString(message, "{damage}", 25, true);

// Example usage of number conversion
int damage_value;
if (stringToNumber("42", damage_value)) {
    // Use damage_value
}

// Example usage of time functions
char date_str[11];
humanDateString(date_str);
```

### Related Modules

For complete system understanding, see:
- [headers.h](headers.h.md) - Core type definitions
- [moria_constants.h](moria_constants.h.md) - Game constants
- [game_logic.md](game_logic.md) - Main game logic implementation
- [ui_system.md](ui_system.md) - User interface components
