# Domain FEN Module

## Introduction

The **domain_fen** module provides the `ForsythEdwardsNotation` utility class,
which converts between a chess [`Position`](domain_model.md) object and its
textual representation in **Forsyth–Edwards Notation (FEN)**. FEN is the
de-facto industry standard for encoding a complete chess board position
(piece placement, side to move, castling rights, en passant target square)
as a single, compact, human-readable string, e.g.:

```
rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
```

This module sits at the boundary between DokChess's internal, strongly
typed domain model and any external representation of a position based on
plain text. It is used by:

- The [`domain_model`](domain_model.md) module itself — `Position`'s
  string-based constructor and `toString()` method delegate directly to
  `ForsythEdwardsNotation`.
- Unit and integration tests throughout the codebase, which set up
  test positions from FEN strings for readability and interoperability with
  external chess tools.
- The [`opening_polyglot`](opening_polyglot.md) module, which has its own
  independent, low-level FEN parsing (`FenTools`) used to compute Polyglot
  Zobrist hash keys for opening-book lookups (see [Relationship to
  opening_polyglot](#relationship-to-opening_polyglot) below).

## Module Position in the System

```mermaid
graph TD
    subgraph domain["domain module"]
        DFEN[domain_fen<br/>ForsythEdwardsNotation]
        DMODEL[domain_model<br/>Position, Piece, Square,<br/>Move, Squares]
    end

    RULES[rules<br/>ChessRules, DefaultChessRules]
    ENGINE[engine_core / engine_search / engine_eval]
    OPENPOLY[opening_polyglot<br/>FenTools, PolyglotOpeningBook]
    TEXTUI[textui_xboard<br/>XBoard, MoveParser]
    TESTS[Unit & Integration Tests]

    DMODEL -->|"Position(String fen) / Position.toString()"| DFEN
    RULES --> DMODEL
    ENGINE --> RULES
    TEXTUI --> ENGINE
    OPENPOLY -.->|independent FEN parsing<br/>for Zobrist hashing| DMODEL
    TESTS -->|build positions from FEN literals| DMODEL

    style DFEN fill:#f9d77e,stroke:#333,stroke-width:2px
```

`ForsythEdwardsNotation` is package-private (default visibility) within
`org.dokchess.domain`. External code never calls it directly — instead,
callers use `new Position(fenString)` to parse a FEN string, or
`position.toString()` to serialize a `Position` back to FEN. This keeps FEN
handling as an internal implementation detail of the domain model.

## Core Component

### `ForsythEdwardsNotation`

A stateless utility (tool) class with a private constructor — it is never
instantiated. It exposes two static methods:

| Method | Direction | Description |
|---|---|---|
| `fromString(Position pos, String fen)` | FEN → Position | Parses a FEN string and mutates the given `Position` object's internal state (board, side to move, castling rights, en passant square). |
| `toString(Position position)` | Position → FEN | Builds a FEN string from a `Position` object's current state. |

Both methods operate on the package-private setters of
[`Position`](domain_model.md) (`setPiece`, `setToMove`,
`setCastlingsAvailable`, `setEnPassantSquare`), which is why
`ForsythEdwardsNotation` must live in the same package (`org.dokchess.domain`)
as `Position`.

#### FEN Format Recap

A FEN string consists of six space-separated fields, of which this class
fully supports the first four and produces static placeholder values for
the last two:

1. **Piece placement** — 8 ranks separated by `/`, from rank 8 down to rank
   1. Each rank lists pieces left-to-right (file a to h); digits represent
      consecutive empty squares; uppercase = White, lowercase = Black
      (e.g. `K` = white king, `q` = black queen).
2. **Active colour** — `w` or `b`.
3. **Castling availability** — a subset of `KQkq`, or `-` if none.
4. **En passant target square** — algebraic square (e.g. `e3`), or `-`.
5. **Halfmove clock** — *(not read; always written as `0`)*.
6. **Fullmove number** — *(not read; always written as `1`)*.

> **Known limitation:** As noted by a `TODO` in the source, the halfmove
> clock and fullmove counters are not tracked by `Position` and are always
> emitted as fixed values (`0 1`) by `toString()`. Parsing of these two
> trailing fields is likewise not implemented in `fromString()` (only the
> first four space-separated groups are consumed).

## `fromString`: Parsing FEN into a Position

```mermaid
flowchart TD
    A[Input: FEN string] --> B[Split on spaces into groups]
    B --> C[group0: piece placement]
    B --> D[group1: active colour]
    B --> E[group2: castling rights]
    B --> F[group3: en passant square]

    C --> C1[Iterate characters]
    C1 --> C2{Character type?}
    C2 -->|digit n| C3[Set n empty squares<br/>advance file by n]
    C2 -->|'/'| C4[Advance to next rank<br/>reset file to 0]
    C2 -->|letter| C5[Determine PieceType via<br/>PieceType.fromLetter]
    C5 --> C6[Determine Colour:<br/>uppercase=WHITE, lowercase=BLACK]
    C6 --> C7[pos.setPiece rank,file, new Piece]
    C7 --> C8[Advance file by 1]

    D --> D1{'w' or 'b'?}
    D1 -->|w| D2[pos.setToMove WHITE]
    D1 -->|b| D3[pos.setToMove BLACK]
    D1 -->|other| D4[throw IllegalArgumentException]

    E --> E1{'-'?}
    E1 -->|yes| E2[setCastlingsAvailable EnumSet.noneOf]
    E1 -->|no| E3[Parse each char via<br/>CastlingType.fromLetter<br/>build EnumSet]

    F --> F1{'-'?}
    F1 -->|yes| F2[setEnPassantSquare null]
    F1 -->|no| F3[new Square from name<br/>setEnPassantSquare]
```

Key implementation details:

- **Piece placement parsing** walks the string character by character,
  maintaining explicit `rank`/`file` counters (rather than delegating to
  `String.split("/")`), incrementing `rank` on `/` and `file` on every
  square consumed (empty or occupied).
- Piece letters are resolved to a `PieceType` via
  `PieceType.fromLetter(char)`; the letter's case determines the `Colour`
  (`Character.isUpperCase` → `WHITE`).
- Castling rights are parsed into a `java.util.EnumSet<CastlingType>` using
  `CastlingType.fromLetter(char)` for each character.
- The en passant field, if present, is turned directly into a
  [`Square`](domain_model.md) via its string-based constructor (e.g.
  `new Square("e3")`).
- Fields 5 and 6 (halfmove clock, fullmove number) are **not parsed**.

## `toString`: Serializing a Position into FEN

```mermaid
flowchart TD
    A[Input: Position] --> B[For each rank 0..7]
    B --> C[For each file 0..7]
    C --> D{piece present?}
    D -->|no| E[increment 'free' counter]
    D -->|yes| F[flush pending 'free' count<br/>as digit if > 0]
    F --> G[append piece.asLetter]
    G --> C
    E --> C
    C --> H[flush remaining 'free' count]
    H --> I{rank < 7?}
    I -->|yes| J[append '/']
    I -->|no| K[skip]
    J --> B
    K --> L[append ' ']

    L --> M{toMove}
    M -->|WHITE| N[append 'w']
    M -->|BLACK| O[append 'b']

    N --> P[append ' ']
    O --> P
    P --> Q{castlingsAvailable empty?}
    Q -->|yes| R[append '-']
    Q -->|no| S[for each CastlingType in order<br/>if contained, append its letter]

    R --> T[append ' ']
    S --> T
    T --> U{enPassantSquare == null?}
    U -->|yes| V[append '-']
    U -->|no| W[append square.toString]

    V --> X["append ' 0 1'<br/>(placeholder halfmove/fullmove)"]
    W --> X
    X --> Y[Return FEN string]
```

Key implementation details:

- Piece placement is built rank by rank (0 = rank 8, 7 = rank 1, matching
  `Position`'s internal indexing), accumulating consecutive empty squares
  into a `free` counter that is flushed as a digit whenever a piece is
  encountered or the rank ends.
- `Piece.asLetter()` supplies the correct case/letter combination directly.
- Castling rights are emitted in the fixed enum declaration order of
  `CastlingType` (typically `K`, `Q`, `k`, `q`), only including types
  present in `position.getCastlingsAvailable()`.
- The en passant square, if set, uses `Square.toString()` (e.g. `"e3"`).
- The halfmove clock and fullmove number are **hardcoded** to `"0 1"` since
  `Position` does not track them (see the `TODO` in the source).

## Relationship to Domain Model

`ForsythEdwardsNotation` is tightly coupled to
[`Position`](domain_model.md) and is only invoked from within that class:

```mermaid
sequenceDiagram
    participant Caller
    participant Position
    participant FEN as ForsythEdwardsNotation

    Caller->>Position: new Position(fenString)
    Position->>Position: allocate empty board[8][8]
    Position->>FEN: fromString(this, fenString)
    FEN->>Position: setPiece(rank, file, piece) *
    FEN->>Position: setToMove(colour)
    FEN->>Position: setCastlingsAvailable(set)
    FEN->>Position: setEnPassantSquare(square)
    FEN-->>Position: (void, Position mutated)
    Position-->>Caller: fully initialized Position

    Caller->>Position: position.toString()
    Position->>FEN: toString(this)
    FEN->>Position: getPiece(rank, file) *
    FEN->>Position: getToMove()
    FEN->>Position: getCastlingsAvailable()
    FEN->>Position: getEnPassantSquare()
    FEN-->>Position: FEN string
    Position-->>Caller: FEN string
```

Notes:

- `Position`'s no-argument constructor calls the FEN constructor internally
  with the standard starting position string, meaning the *default* chess
  starting setup is itself defined and validated via this module.
- Because `fromString`/`toString` invoke `Position`'s package-private
  setters/getters, `ForsythEdwardsNotation` must reside in the
  `org.dokchess.domain` package. It has default (package-private) access
  and cannot be used outside that package — all interaction with FEN happens
  indirectly through `Position`.
- See [`domain_model`](domain_model.md) for full details on `Position`,
  `Piece`, `Square`, `Move`, and the `Squares` constant holder, all of which
  this module depends on (`PieceType`, `Colour`, and `CastlingType` are
  enums defined alongside `Position` in the domain model).

## Usage Across the System

While `ForsythEdwardsNotation` itself is internal, FEN strings surface
throughout DokChess wherever a `Position` needs to be expressed compactly:

```mermaid
graph LR
    A["new Position(fen)"] --> B[Position object]
    B --> C["position.toString()"]
    C --> A2[FEN string]

    subgraph Consumers
        RULES2["rules module<br/>move generation & validation<br/>operates on Position objects"]
        ENGINE2["engine_search / engine_eval<br/>search over Position trees"]
        TESTS2["Unit & Integration Tests<br/>(e.g. EngineVsRandomIntegTest,<br/>XBoardIntegTest)"]
        XBOARD2["textui_xboard<br/>protocol commands may reference<br/>positions/moves"]
    end

    B --> RULES2
    RULES2 --> ENGINE2
    A2 --> TESTS2
    ENGINE2 --> XBOARD2
```

- The [`rules`](rules.md) module (`ChessRules`, `DefaultChessRules`, and the
  per-piece movement classes) consumes `Position` objects produced from FEN
  strings to generate and validate legal moves.
- The [`engine_search`](engine_search.md) and [`engine_eval`](engine_eval.md)
  modules traverse trees of `Position` objects (via `Position.performMove`)
  during search; test fixtures for these components are frequently
  bootstrapped from FEN literals for conciseness.
- The [`opening_polyglot`](opening_polyglot.md) module's `FenTools` class
  independently re-parses FEN strings (piece placement, castling, side to
  move) purely to compute Zobrist hash keys compatible with the Polyglot
  opening-book binary format. It does **not** reuse
  `ForsythEdwardsNotation`/`Position`; it works directly on raw FEN strings
  for performance and to avoid a dependency on the mutable `Position` API.
  This is a deliberate duplication — see
  [`opening_polyglot`](opening_polyglot.md) for details.

## Relationship to opening_polyglot

It's worth calling out explicitly that **two independent FEN parsers**
exist in the codebase:

| Aspect | `domain_fen` (`ForsythEdwardsNotation`) | `opening_polyglot` (`FenTools`) |
|---|---|---|
| Purpose | Build/serialize a full `Position` domain object | Compute a 64-bit Zobrist hash key for opening-book lookups |
| Output | `Position` object / FEN string | `long` hash key |
| Scope of fields parsed | Piece placement, side to move, castling, en passant | Piece placement, side to move, castling only (en passant hashing unimplemented) |
| Access | Package-private, used only via `Position` | Package-private, used only via `PolyglotOpeningBook` |

This separation keeps the performance-sensitive opening-book hashing free
of dependencies on the full `Position` object graph, at the cost of some
logic duplication between the two FEN parsers.

## Design Notes & Limitations

- **Package-private, tool-class design**: `ForsythEdwardsNotation` follows
  the "utility class" pattern — `final` class, private constructor, only
  static methods — signaling it holds no state and is not meant to be
  subclassed or instantiated.
- **Tight coupling to `Position`**: the class directly manipulates
  `Position`'s internal board array via package-private accessors rather
  than through a public API, which is why it must live in the same package.
- **Incomplete metadata support**: halfmove clock and fullmove number
  (fields 5 and 6 of FEN) are not modeled by `Position` at all; `toString()`
  always appends the fixed suffix `" 0 1"`, and `fromString()` never reads
  these fields. Any round-trip through `Position` will therefore lose
  original move-counter information from an input FEN string.
- **No validation of board consistency**: `fromString` does not verify that
  the resulting position is a legal chess position (e.g. correct number of
  kings, valid en passant square) — such validation, if performed, is the
  responsibility of the [`rules`](rules.md) module.
