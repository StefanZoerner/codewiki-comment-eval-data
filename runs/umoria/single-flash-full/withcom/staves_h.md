# staves_h Module Documentation

## Brief Introduction

The `staves_h` module provides the interface definitions for staff-related functionalities within the system. This header file declares the core functions that enable staff usage and wand aiming operations, serving as a contract between different components that interact with magical implements.

## Comprehensive Documentation

This module defines the public API for staff manipulation functionality. It contains function declarations that allow other modules to utilize staff-based operations without requiring knowledge of implementation details.

### Function Declarations

The module exposes two primary functions:

- `staffUse()`: Handles the activation and utilization of staff objects
- `wandAim()`: Manages wand targeting and aiming mechanics

These functions form the foundation for magical implement interactions within the system architecture.

### Module Relationships

The `staves_h` module serves as an interface layer that connects to various subsystems including:
- [magic_system](magic_system.md) - For magical effect processing
- [inventory_management](inventory_management.md) - For staff and wand handling
- [combat_engine](combat_engine.md) - For targeting and spell casting

### Data Flow

```mermaid
graph TD
    A[Combat System] --> B[staves_h]
    C[Inventory System] --> B
    D[Magic System] --> B
    B --> E[Staff Implementation]
    B --> F[Wand Implementation]
```

### Component Interaction

```mermaid
sequenceDiagram
    participant C as Combat System
    participant S as staves_h
    participant M as Magic System
    
    C->>S: staffUse()
    S->>M: Process staff effects
    M-->>S: Return effect data
    S-->>C: Complete staff operation
    
    C->>S: wandAim()
    S->>M: Calculate aim parameters
    M-->>S: Return targeting data
    S-->>C: Complete aiming operation
```

### Architecture Integration

The `staves_h` module fits into the broader system architecture as follows:

```mermaid
graph LR
    subgraph "Core Systems"
        A[Input Handler]
        B[Game Logic]
        C[Rendering Engine]
    end
    
    subgraph "Magical Implement Systems"
        D[staves_h]
        E[spell_system]
        F[item_system]
    end
    
    A --> D
    B --> D
    D --> E
    D --> F
    E --> C
    F --> C
```

### Process Flows

#### Staff Usage Process
```mermaid
flowchart TD
    A[User initiates staff use] --> B{Validate staff}
    B -- Valid --> C[Activate staff effects]
    C --> D[Apply magical properties]
    D --> E[Update game state]
    B -- Invalid --> F[Display error]
    
    style A fill:#e1f5fe
    style B fill:#fff3e0
    style C fill:#e8f5e9
    style D fill:#e8f5e9
    style E fill:#f3e5f5
    style F fill:#ffebee
```

#### Wand Aiming Process
```mermaid
flowchart TD
    A[User initiates wand aim] --> B{Calculate target position}
    B -- Valid --> C[Adjust wand orientation]
    C --> D[Verify line of sight]
    D -- Clear --> E[Enable targeting]
    D -- Blocked --> F[Show obstruction]
    B -- Invalid --> G[Display error]
    
    style A fill:#e1f5fe
    style B fill:#fff3e0
    style C fill:#e8f5e9
    style D fill:#e8f5e9
    style E fill:#f3e5f5
    style F fill:#ffebee
    style G fill:#ffebee
```

## References

This module depends on and integrates with several other system components:
- [magic_system.md](magic_system.md) - Provides magical effect processing capabilities
- [inventory_management.md](inventory_management.md) - Handles staff and wand inventory management
- [combat_engine.md](combat_engine.md) - Integrates with combat targeting systems

The module's interface design follows the principles established in [system_architecture.md](system_architecture.md) for maintaining clean separation of concerns while enabling effective communication between subsystems.
