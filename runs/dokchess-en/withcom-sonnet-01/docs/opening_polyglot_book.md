# Opening Polyglot Book

## Introduction

The **opening_polyglot_book** module provides the concrete, ready-to-use implementation of an opening book for the dokchess engine: `PolyglotOpeningBook`. It loads industry-standard Polyglot (`.bin`) opening book files, indexes their entries in memory, and — given any `Position` — looks up a matching, book-recommended `Move`.

This module is the "book" half of the [opening_polyglot](opening_polyglot.md) module family. While the sibling module [opening_polyglot_format](opening_polyglot_format.md) is concerned with the low-level binary *format* of a Polyglot file (parsing raw 16-byte records and bit-level move encoding), `opening_polyglot_book` is concerned with *using* that data: computing lookup keys from a chess position (via FEN) and selecting a move among possibly several book candidates.

The module implements the generic [`OpeningLibrary`](opening.md) contract, so it can be plugged into the chess [`engine_core`](engine_core.md) as an optional, fast "book move" source that is consulted before the engine falls back to tree search.

---

## Purpose and Core Functionality

A Polyglot opening book is a binary file consisting of a sequence of fixed-size (16 byte) entries. Each entry associates a **Zobrist-style 64-bit position key** with a **move** and a **weight** (popularity/strength indicator). Chess GUIs and engines use such files to play known, well-tested opening moves instead of spending computation time calculating them from scratch.

This module's responsibilities are:

1. **Loading** a `.bin` file or `InputStream` into memory as a list of `BookEntry` records (delegating the byte-level decoding to `BookEntry`/`PolyglotTools` from `opening_polyglot_format`).
2. **Computing the Polyglot Zobrist key** for an arbitrary chess `Position` — via its FEN string — so it can be compared against the keys stored in the loaded book. This is the job of the package-private `FenTools` class.
3. **Matching** entries whose key equals the position's key (several entries can share a key because multiple book moves may be known for the same position).
4. **Selecting** one move among the matches, according to a configurable `SelectionMode` (`FIRST`, `MOST_PLAYED`, `RANDOM`).
5. **Translating** the chosen `BookEntry` (raw square coordinates) into a domain-level `Move` object, ready to be applied to the game via the [`domain_model`](domain_model.md) types (`Square`, `Piece`, `Move`).

---

## Components

| Component | Visibility | Responsibility |
|---|---|---|
| `PolyglotOpeningBook` | `public` | Implements `OpeningLibrary`; loads book data, performs lookups, applies selection mode, produces `Move` objects. |
| `FenTools` | package-private | Computes the 64-bit Polyglot Zobrist key for a position, given its FEN string (piece placement, castling rights, side to move; en passant is a known unimplemented gap — see below). |

Related components from the sibling module `opening_polyglot_format` that this module depends on:

| Component | Module | Responsibility |
|---|---|---|
| `BookEntry` | [opening_polyglot_format](opening_polyglot_format.md) | Decodes a single raw 16-byte Polyglot record into key/move/weight fields. |
| `PolyglotTools` | [opening_polyglot_format](opening_polyglot_format.md) | Low level bit/byte helpers: `long`↔byte[] conversion, file/rank string encoding, weight decoding. |
| `SelectionMode` | opening_polyglot (parent) | Enum describing how to pick a move among several matching book entries. |

---

## Architecture

### Class relationships

```mermaid
classDiagram
    class OpeningLibrary {
        <<interface>>
        +lookUpMove(Position) Move
    }

    class PolyglotOpeningBook {
        -SelectionMode selectionMode
        -List~BookEntry~ entries
        +PolyglotOpeningBook(File)
        +PolyglotOpeningBook(InputStream)
        +setSelectionMode(SelectionMode)
        +lookUpMove(Position) Move
        ~readData(File)
        ~readData(InputStream)
        ~findEntriesByFen(String) List~BookEntry~
        ~findEntriesByKey(long) List~BookEntry~
        ~findEntriesByKey(byte[]) List~BookEntry~
    }

    class FenTools {
        <<utility>>
        +calculateKeyFromFen(String) long
        +calculatePieceFromFen(String) long
        +calculateCastleFromFen(String) long
        +calculateEnpassentFromFen(String) long
        +calculateTurnFromFen(String) long
        +kindOfPiece(char) int
    }

    class BookEntry {
        -byte[] key
        -byte[] move
        -byte[] weight
        +getKey() byte[]
        +getMoveFrom() String
        +getMoveTo() String
        +getWeightAsInt() int
        +compareTo(BookEntry) int
    }

    class PolyglotTools {
        <<utility>>
        +fileAndRankToString(int,int) String
        +twoBytesToInt(byte[]) int
        +longToByteArray(long) byte[]
    }

    class SelectionMode {
        <<enumeration>>
        FIRST
        MOST_PLAYED
        RANDOM
    }

    PolyglotOpeningBook ..|> OpeningLibrary
    PolyglotOpeningBook --> BookEntry : holds many
    PolyglotOpeningBook --> FenTools : uses (key calc)
    PolyglotOpeningBook --> PolyglotTools : uses (key encode)
    PolyglotOpeningBook --> SelectionMode : uses
    BookEntry --> PolyglotTools : uses (decode)
    FenTools --> FenTools : uses internal random64 table
```

### Module dependency overview

```mermaid
graph TD
    subgraph opening_polyglot_book [opening_polyglot_book - this module]
        POB[PolyglotOpeningBook]
        FT[FenTools]
    end

    subgraph opening_polyglot_format
        BE[BookEntry]
        PT[PolyglotTools]
        SM[SelectionMode]
    end

    subgraph opening [opening]
        OL[OpeningLibrary interface]
    end

    subgraph domain_model
        POS[Position]
        MV[Move]
        SQ[Square]
        PC[Piece]
    end

    subgraph engine_core
        FL[FromLibrary]
        DE[DefaultEngine]
    end

    POB -->|implements| OL
    POB --> BE
    POB --> FT
    POB --> PT
    POB --> SM
    POB --> POS
    POB --> MV
    POB --> SQ
    POB --> PC
    FL --> OL
    DE --> FL
    DE -.->|"may be injected as OpeningLibrary"| POB
```

See [domain](domain.md) for `Position`, `Move`, `Square`, `Piece`, and [engine_core](engine_core.md) for how `OpeningLibrary` implementations (like this one) are consumed via `FromLibrary`/`DefaultEngine`.

---

## Data Flow: Looking Up a Move

`lookUpMove(Position)` is the single public operation exposed to callers (through the `OpeningLibrary` interface). Internally it proceeds through several steps:

```mermaid
sequenceDiagram
    participant Caller as Caller (e.g. FromLibrary)
    participant Book as PolyglotOpeningBook
    participant Pos as Position
    participant Fen as FenTools
    participant Entries as List~BookEntry~
    participant Entry as BookEntry (chosen)

    Caller->>Book: lookUpMove(position)
    Book->>Pos: toString()  (FEN)
    Pos-->>Book: fen
    Book->>Fen: calculateKeyFromFen(fen)
    Fen-->>Book: 64-bit key
    Book->>Entries: filter by matching key bytes
    Entries-->>Book: matches (0..n BookEntry)
    alt no matches
        Book-->>Caller: null
    else matches found
        alt selectionMode == MOST_PLAYED
            Book->>Entries: sort by weight desc
        else selectionMode == RANDOM
            Book->>Entries: shuffle
        else FIRST (default)
            Note over Book: keep original book order
        end
        Book->>Entry: get(0)
        Entry-->>Book: moveFrom / moveTo (algebraic strings)
        Book->>Pos: getPiece(fromSquare), getPiece(toSquare)
        Pos-->>Book: piece, capture flag
        Book-->>Caller: new Move(piece, from, to, capture)
    end
```

### Key computation detail (`FenTools`)

The Polyglot key is a XOR combination of several Zobrist-style sub-keys, each derived from a lookup into a fixed 781-entry `random64[]` table (standard Polyglot random numbers):

```mermaid
flowchart LR
    FEN[FEN string] --> Split[Split into 6 space-separated fields]
    Split --> Piece[Piece placement field]
    Split --> Turn[Active colour field]
    Split --> Castle[Castling rights field]
    Split --> EnPassant[En passant field]

    Piece --> PieceKey["calculatePieceFromFen(): XOR random64[64*kind + 8*rank + file] for every piece on board"]
    Turn --> TurnKey["calculateTurnFromFen(): random64[780] if white to move, else 0"]
    Castle --> CastleKey["calculateCastleFromFen(): XOR random64[768..771] for each available castling right (K,Q,k,q)"]
    EnPassant --> EPKey["calculateEnpassentFromFen(): NOT IMPLEMENTED - always returns 0"]

    PieceKey --> XOR{{XOR}}
    TurnKey --> XOR
    CastleKey --> XOR
    EPKey --> XOR
    XOR --> Key[64-bit Polyglot key]
```

> **Known limitation:** `calculateEnpassentFromFen` is a stub (`TODO: Missing Implementation`) and always returns `0`. This means positions that differ only by en passant availability will compute the *same* key, potentially causing missed or slightly inaccurate book lookups in en-passant-eligible positions. This is a documented gap in the current implementation, not accidental behavior.

---

## Loading the Book

The book can be constructed either from a `File` or directly from an `InputStream`, which is convenient for loading a book bundled as a classpath resource.

```mermaid
flowchart TD
    A["new PolyglotOpeningBook(File/InputStream)"] --> B[selectionMode = FIRST]
    B --> C["readData(...)"]
    C --> D[Wrap in BufferedInputStream]
    D --> E{available bytes > 0?}
    E -- yes --> F[Read next 16 raw bytes]
    F --> G["new BookEntry(rawBytes)"]
    G --> H["entries.add(bookEntry)"]
    H --> E
    E -- no --> I[Loading complete: entries populated in memory]
```

Each 16-byte raw record is decoded by `BookEntry` (see [opening_polyglot_format](opening_polyglot_format.md)) into:
- an 8-byte **key** (compared against the position's computed key),
- a 2-byte **move** (packed from/to file & rank bits, decoded via `PolyglotTools`),
- a 2-byte **weight** (used for `MOST_PLAYED` selection, decoded via `PolyglotTools.twoBytesToInt`).

---

## Selection Strategies

`SelectionMode` governs which move is returned when multiple `BookEntry` records share the same key (i.e., multiple known continuations exist for the same position):

| Mode | Behavior |
|---|---|
| `FIRST` (default) | Returns the first match in the order entries were read from the file. |
| `MOST_PLAYED` | Sorts matches by weight, descending (`BookEntry.compareTo` inverts natural order), and returns the top one — i.e., the statistically most popular move. |
| `RANDOM` | Shuffles the matches and returns one at random, adding opening variety across games. |

```mermaid
stateDiagram-v2
    [*] --> MatchesFound
    MatchesFound --> FIRST: selectionMode == FIRST
    MatchesFound --> MOST_PLAYED: selectionMode == MOST_PLAYED
    MatchesFound --> RANDOM: selectionMode == RANDOM
    FIRST --> ReturnFirstElement
    MOST_PLAYED --> SortDescendingByWeight
    SortDescendingByWeight --> ReturnFirstElement
    RANDOM --> ShuffleList
    ShuffleList --> ReturnFirstElement
    ReturnFirstElement --> [*]
```

---

## Integration with the Engine

`PolyglotOpeningBook` implements [`OpeningLibrary`](opening.md), the single-method contract expected by the engine's move pipeline. Within [engine_core](engine_core.md), `FromLibrary` is a `DetermineMove` pipeline stage that queries an `OpeningLibrary` first; if a book move is found, it is emitted immediately without falling through to tree search (`FromSearch` / `MinimaxParallelSearch`, see [engine_search](engine_search.md)). `DefaultEngine` wires this up:

```mermaid
graph LR
    A[DefaultEngine] -->|constructs, if book supplied| B[FromLibrary]
    B -->|delegates to OpeningLibrary| C[PolyglotOpeningBook]
    B -->|falls back if no move found| D[FromSearch]
    D --> E[MinimaxParallelSearch]
    C -.->|lookUpMove uses| F[Position / FEN]
```

This means a `PolyglotOpeningBook` instance is typically created once at engine start-up (loading a `.bin` file) and handed to `DefaultEngine`'s constructor as the `openingLibrary` argument, so early-game moves are served instantly from the book while later, unfamiliar positions fall through to the minimax search engine.

---

## Design Notes & Limitations

- **Immutability of loaded data**: entries are loaded once at construction; the class exposes no API to add/remove entries afterward, keeping the book read-only and thread-safe for concurrent lookups (aside from the `Collections.sort`/`shuffle` calls mutating the *local* `matches` list, not the shared `entries` list).
- **Package-private helper methods** (`findEntriesByFen`, `findEntriesByKey`, `getEntries`) are intentionally not part of the public API — they exist primarily to support the class's own logic and its unit tests within the same package.
- **En passant key gap**: as noted above, `FenTools.calculateEnpassentFromFen` is unimplemented; consumers relying on exact Polyglot-key compatibility in en-passant-eligible positions should be aware book lookups might not perfectly match reference Polyglot implementations in that edge case.
- **Byte-level encoding details** (bit-packing of move squares, big/little-endian handling of weights and keys) are entirely delegated to `BookEntry`/`PolyglotTools` in [opening_polyglot_format](opening_polyglot_format.md), keeping this module focused purely on lookup/selection logic rather than binary parsing.

---

## Related Documentation

- [opening.md](opening.md) — the generic `OpeningLibrary` interface this module implements.
- [opening_polyglot_format.md](opening_polyglot_format.md) — binary record decoding (`BookEntry`, `PolyglotTools`) that this module depends on.
- [domain.md](domain.md) / [domain_model.md](domain_model.md) — `Position`, `Move`, `Square`, `Piece` value types used to represent chess state and moves.
- [domain_fen.md](domain_fen.md) — FEN (de)serialization used by `Position.toString()` to produce the FEN string this module parses.
- [engine_core.md](engine_core.md) — `Engine`, `DefaultEngine`, `FromLibrary`, `DetermineMove` pipeline that consumes this module as an optional opening book source.
- [engine_search.md](engine_search.md) — the search-based fallback (`MinimaxParallelSearch`) used when no book move is available.
