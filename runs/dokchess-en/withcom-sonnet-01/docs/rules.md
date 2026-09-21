# Rules Module

## Purpose

The `rules` module implements the **Laws of Chess** for the dokchess engine. It is responsible for:

- Generating the legal moves available in a given [`Position`](domain_model.md) for the side to move.
- Detecting check, checkmate, and stalemate.
- Providing the canonical starting position of a game.

The module is deliberately kept independent of any search, evaluation, or UI concerns. It operates purely on the
immutable domain types defined in the [`domain`](domain.md) module (`Position`, `Move`, `Square`, `Piece`, `Colour`,
`PieceType`, `CastlingType`) and exposes a single public entry point, the `ChessRules` interface, with
`DefaultChessRules` as the standard implementation. Consumers such as the [`engine_core`](engine_core.md) module
(e.g. `DefaultEngine`, `DetermineMove`) and the [`textui_xboard`](textui_xboard.md) module rely on this interface to
drive gameplay without needing to know how individual pieces move or how attacks are detected.

## Architecture Overview

The module is organized into three cooperating layers:

1. **Public Rules API** – the `ChessRules` interface and its `DefaultChessRules` implementation, which orchestrate
   move generation and game-state queries.
2. **Movement Framework** – abstract base classes (`Movement`, `ComplexMovement`) and the `Tools` utility class,
   which provide shared building blocks (ray-tracing, single-step reachability, attack detection) used by every
   piece-specific move generator.
3. **Piece Move Generators** – one class per piece type/movement rule (`KnightMoves`, `RookMoves`, `BishopMoves`,
   `QueenMoves`, `KingMoves`, `PawnMoves`, `CastlingMoves`) that compute pseudo-legal move candidates for a piece on
   a given square.

```mermaid
graph TD
    subgraph "Public Rules API"
        CR[ChessRules interface]
        DCR[DefaultChessRules]
        CR -.implements.-> DCR
    end

    subgraph "Piece Move Generators"
        KM[KnightMoves]
        RM[RookMoves]
        BM[BishopMoves]
        QM[QueenMoves]
        KgM[KingMoves]
        PM[PawnMoves]
        CM[CastlingMoves]
    end

    subgraph "Movement Framework"
        MV[Movement]
        CPX[ComplexMovement]
        T[Tools]
    end

    DCR --> KM
    DCR --> RM
    DCR --> BM
    DCR --> QM
    DCR --> KgM
    DCR --> PM
    DCR --> CM
    DCR -->|isCheck / isCheckmate / isStalemate| T

    KM --> CPX
    RM --> CPX
    BM --> CPX
    QM --> CPX
    KgM --> CPX
    CPX --> MV
    PM --> MV
    CM --> MV
    CM -->|castling safety| T

    subgraph "domain module"
        POS[Position]
        MOVE[Move]
        SQ[Square]
        PC[Piece]
    end

    MV --> POS
    MV --> SQ
    MV --> PC
    DCR --> MOVE

    classDef ext fill:#eee,stroke:#999,stroke-dasharray: 5 5;
    class POS,MOVE,SQ,PC ext;
```

### Consumers of this module

```mermaid
graph LR
    Engine["engine_core (DefaultEngine, DetermineMove)"] -->|getLegalMoves / isCheck / isCheckmate / isStalemate| CR[ChessRules]
    XBoard["textui_xboard (XBoard, MoveParser)"] --> CR
    CR --> DCR[DefaultChessRules]
```

See [`engine_core`](engine_core.md) for how legal moves feed into search (`engine_search`) and
[`textui_xboard`](textui_xboard.md) for how a UI protocol consumes rules to validate and apply moves.

## Sub-modules

| Sub-module | Description |
|---|---|
| [rules_core](rules_core.md) | The `ChessRules` public contract and `DefaultChessRules`, which coordinates all piece move generators, filters out moves that leave the mover's own king in check, and answers check/checkmate/stalemate/starting-position queries. |
| [rules_movement_framework](rules_movement_framework.md) | Shared abstractions `Movement` and `ComplexMovement` for computing move candidates, plus the `Tools` utility that determines whether a square is attacked by a given colour (used for check detection and castling safety). |
| [rules_piece_moves](rules_piece_moves.md) | Concrete move generators for each piece type and for castling: `KnightMoves`, `RookMoves`, `BishopMoves`, `QueenMoves`, `KingMoves`, `PawnMoves`, `CastlingMoves`. |

## Move Generation Flow

The following sequence illustrates how `DefaultChessRules.getLegalMoves` produces the legal move list for a
position:

```mermaid
sequenceDiagram
    participant Caller as Caller (e.g. engine_core)
    participant DCR as DefaultChessRules
    participant PieceGen as Piece Move Generator
    participant Tools as Tools.isSquareAttacked

    Caller->>DCR: getLegalMoves(position)
    loop for each own-coloured square
        DCR->>PieceGen: addMoveCandidates(square, position, moves)
        PieceGen-->>DCR: pseudo-legal move candidates
    end
    loop for each candidate move
        DCR->>DCR: newPos = position.performMove(move)
        DCR->>Tools: isSquareAttacked(newPos, ownKingSquare, opponentColour)
        Tools-->>DCR: true/false
        alt king would be in check
            DCR->>DCR: remove move
        end
    end
    DCR-->>Caller: legal moves
```

Check, checkmate, and stalemate are derived from the same building blocks:

- `isCheck(position, colour)` locates the king and asks `Tools.isSquareAttacked`.
- `isCheckmate(position)` returns true when the side to move is in check and `getLegalMoves` is empty.
- `isStalemate(position)` returns true when `getLegalMoves` is empty but the side to move is **not** in check.

## Related Modules

- [`domain`](domain.md) — immutable board/position representation consumed by every class in this module.
- [`engine_core`](engine_core.md) — uses `ChessRules` to enumerate legal moves and to evaluate terminal game states
  during search.
- [`textui_xboard`](textui_xboard.md) — uses `ChessRules` to validate user/opponent moves in the xboard protocol.
