# Opening Polyglot Module

## Introduction

The `opening_polyglot` module is a concrete implementation of the [`opening`](opening.md) module's
`OpeningLibrary` interface. It allows the DokChess engine to consult a standard **Polyglot** (`.bin`)
opening book — a widely-used binary format for chess opening books shared by many chess engines
(e.g. Fritz, Crafty, Stockfish tools) — and return a known "book move" for a given position instead
of relying on the (comparatively slow and shallow) search-based engine logic.

By plugging a `PolyglotOpeningBook` instance into the engine (see [`engine_core`](engine_core.md),
specifically `FromLibrary` / `DetermineMove`), the engine can play well-known opening theory
instantly and skip the [`engine_search`](engine_search.md) tree search for as long as the current
game continues to match entries recorded in the book.

## Purpose

* Parse a Polyglot binary opening book file/stream into in-memory records (`BookEntry`).
* Compute the Polyglot **Zobrist hash key** for a given chess position (expressed as FEN, see
  [`domain`](domain.md) module's `ForsythEdwardsNotation`) so that book entries can be matched
  against the current position.
* Decode the compact 16-bit move encoding used by the Polyglot format into `Square`/`Move` objects
  from the [`domain`](domain.md) module.
* Offer configurable strategies (`SelectionMode`) for choosing among several book moves that match
  the same position.

## Architecture Overview

```mermaid
flowchart TB
    subgraph opening_polyglot
        POB[PolyglotOpeningBook]
        BE[BookEntry]
        FT[FenTools]
        PT[PolyglotTools]
    end

    OL[OpeningLibrary<br/><i>opening module</i>]
    POS[Position / Move / Square / Piece<br/><i>domain module</i>]
    ENG[Engine / DetermineMove / FromLibrary<br/><i>engine_core module</i>]

    ENG -->|lookUpMove| POB
    POB -.implements.-> OL
    POB -->|reads binary data| BE
    POB -->|computes Zobrist key| FT
    BE -->|decodes move bytes| PT
    POB -->|builds key bytes| PT
    POB -->|constructs| POS
```

The module is split into two closely related sub-modules:

1. **[opening_polyglot_format](opening_polyglot_format.md)** — the low-level binary record format:
   `BookEntry` (a single 16-byte Polyglot record) and `PolyglotTools` (bit-manipulation helpers
   shared across the module for encoding/decoding squares, weights and keys).
2. **[opening_polyglot_book](opening_polyglot_book.md)** — the higher-level book logic:
   `PolyglotOpeningBook` (the public `OpeningLibrary` implementation, entry point used by the
   engine) and `FenTools` (Zobrist hash computation from a FEN string, used to look up matching
   entries).

## High-Level Data Flow

```mermaid
sequenceDiagram
    participant Engine as Engine (engine_core)
    participant Book as PolyglotOpeningBook
    participant Fen as FenTools
    participant Entries as List<BookEntry>
    participant Tools as PolyglotTools

    Engine->>Book: lookUpMove(position)
    Book->>Book: fen = position.toString()
    Book->>Fen: calculateKeyFromFen(fen)
    Fen->>Fen: XOR piece/castle/enpassant/turn random64 values
    Fen-->>Book: 64-bit Zobrist key
    Book->>Tools: longToByteArray(key)
    Tools-->>Book: 8-byte key
    Book->>Entries: findEntriesByKey(bytesKey)
    Entries-->>Book: matching BookEntry list
    Book->>Book: apply SelectionMode (FIRST/MOST_PLAYED/RANDOM)
    Book->>Entries: chosen.getMoveFrom()/getMoveTo()
    Entries->>Tools: fileAndRankToString(...)
    Book->>Book: build domain Move (piece, from, to, capture)
    Book-->>Engine: Move or null
```

## Loading a Book

```mermaid
sequenceDiagram
    participant Caller
    participant Book as PolyglotOpeningBook
    participant Stream as InputStream/File
    participant Entry as BookEntry

    Caller->>Book: new PolyglotOpeningBook(file | inputStream)
    Book->>Stream: open (Buffered)InputStream
    loop while bytes available
        Book->>Stream: read 16 raw bytes
        Book->>Entry: new BookEntry(rawBytes)
        Book->>Book: entries.add(entry)
    end
    Book-->>Caller: ready book (default SelectionMode.FIRST)
```

## Module Relationships

* **Depends on** [`domain`](domain.md): uses `Position`, `Move`, `Piece`, `Square` to translate
  book records into engine-usable chess moves, and relies on `Position.toString()` (backed by
  `ForsythEdwardsNotation`) to obtain a FEN representation of the current position.
* **Implements** [`opening`](opening.md): `PolyglotOpeningBook` is a concrete `OpeningLibrary`.
* **Consumed by** [`engine_core`](engine_core.md): the engine's `FromLibrary` result path and
  `DetermineMove` decision logic use an `OpeningLibrary` (potentially a `PolyglotOpeningBook`) to
  short-circuit search via [`engine_search`](engine_search.md) when a book move is available.

## Sub-module Documentation

| Sub-module | Description |
|---|---|
| [opening_polyglot_format](opening_polyglot_format.md) | Binary record parsing (`BookEntry`) and low-level bit/byte utilities (`PolyglotTools`) that decode Polyglot's compact move and weight encoding. |
| [opening_polyglot_book](opening_polyglot_book.md) | Zobrist hash key computation from FEN (`FenTools`) and the public opening-book API (`PolyglotOpeningBook`) that ties parsing, hashing, and move selection together. |
