# Domain Module

## Purpose

The **domain** module defines the fundamental data model of DokChess: the vocabulary of
squares, pieces, moves and positions that every other part of the system is built upon.
It has **no dependency on any other DokChess module** — it is the bedrock of the
application. All higher-level modules (move generation, search, evaluation, opening
books, and the text UI) operate on the types defined here.

The module is intentionally minimal and immutable wherever possible: `Piece`, `Square`
and `Move` are value objects, while `Position` exposes a `performMove()` method that
returns a brand-new `Position` rather than mutating the board in place. This makes the
model safe to share across threads — an important property since the
[engine_search](engine_search.md) module explores many positions in parallel.

## Architecture Overview

```mermaid
classDiagram
    class Square {
        -int file
        -int rank
        +Square(int rank, int file)
        +Square(String name)
        +getFile() int
        +getRank() int
    }

    class Squares {
        <<utility>>
        +a1 : Square
        +h8 : Square
        ...
    }

    class Piece {
        -PieceType type
        -Colour colour
        +getType() PieceType
        +getColour() Colour
        +asLetter() char
        +is(PieceType) boolean
        +is(Colour) boolean
    }

    class PieceType {
        <<enumeration>>
        KING
        QUEEN
        ROOK
        BISHOP
        KNIGHT
        PAWN
        +fromLetter(char) PieceType
        +getLetter() char
    }

    class Colour {
        <<enumeration>>
        WHITE
        BLACK
        +otherColour() Colour
    }

    class CastlingType {
        <<enumeration>>
        WHITE_KINGSIDE
        WHITE_QUEENSIDE
        BLACK_KINGSIDE
        BLACK_QUEENSIDE
        +fromLetter(char) CastlingType
        +asLetter() char
    }

    class Move {
        -Piece piece
        -Square from
        -Square to
        -boolean capture
        -PieceType promotion
        +isCapture() boolean
        +isCastling() boolean
        +isPromotion() boolean
        +isPawnAdvancesTwo() boolean
    }

    class Position {
        -Colour toMove
        -Piece[][] board
        -Square enPassantSquare
        -Set~CastlingType~ castlingsAvailable
        +Position()
        +Position(String fen)
        +getPiece(int,int) Piece
        +performMove(Move) Position
        +findSquaresWith(Piece) List~Square~
        +findSquareWithKing(Colour) Square
        +castlingAllowed(CastlingType) boolean
    }

    class ForsythEdwardsNotation {
        <<utility>>
        +fromString(Position, String)
        +toString(Position) String
    }

    Piece --> PieceType
    Piece --> Colour
    Move --> Piece
    Move --> Square
    Move --> PieceType : promotion
    Position --> Piece
    Position --> Colour
    Position --> Square : enPassantSquare
    Position --> CastlingType
    Position ..> ForsythEdwardsNotation : delegates parsing/formatting
    Position ..> Move : consumes
    Squares --> Square : constants
```

## Sub-modules

The domain module is documented in two focused parts:

| Sub-module | Description |
|---|---|
| [domain_model](domain_model.md) | The core chess vocabulary: `Square`, `Squares`, `Piece`, `Colour`, `PieceType`, `CastlingType`, `Move`, and the `Position` aggregate that ties them together, including move application (`performMove`) and castling-rights bookkeeping. |
| [domain_fen](domain_fen.md) | The `ForsythEdwardsNotation` helper that converts between a `Position` object and its textual [FEN](https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation) representation, used for setting up positions and for external interoperability (e.g. opening books, XBoard protocol). |

## How the Domain Module Fits into the System

```mermaid
flowchart TB
    subgraph domain["domain (this module)"]
        A[Square / Squares]
        B[Piece / PieceType / Colour]
        C[Move]
        D[Position]
        E[ForsythEdwardsNotation]
    end

    subgraph rules["rules"]
        R[ChessRules / DefaultChessRules]
    end

    subgraph engine["engine_core, engine_eval, engine_search"]
        EN[Engine / Search / Evaluation]
    end

    subgraph opening["opening, opening_polyglot"]
        OP[OpeningLibrary / PolyglotOpeningBook]
    end

    subgraph textui["textui_xboard"]
        UI[XBoard / MoveParser]
    end

    domain --> rules
    domain --> engine
    domain --> opening
    domain --> textui
    rules --> engine
    opening --> engine
    engine --> textui
```

* **[rules](rules.md)** uses `Position`, `Move`, `Piece` and `Square` to enumerate legal
  moves for each piece type and to validate castling and check conditions.
* **[engine_core](engine_core.md)**, **[engine_eval](engine_eval.md)** and
  **[engine_search](engine_search.md)** (search algorithms and material evaluation)
  operate purely on `Position` objects produced via `performMove()`, and return/rank
  `Move` objects.
* **[opening](opening.md)** and **[opening_polyglot](opening_polyglot.md)** map
  `Position` (via FEN/Zobrist-like hashing) to known book moves.
* **[textui_xboard](textui_xboard.md)** parses moves typed by a user or GUI into `Move`
  objects (via `Square` coordinates) and renders `Position`/`Move` back to the user, and
  also relies on `ForsythEdwardsNotation`-style FEN strings for the XBoard protocol.

Because none of the domain classes depend on rules, engine, opening or UI code, the
domain module can be understood, tested and reused in complete isolation — it is the
recommended starting point for any developer new to the DokChess codebase.
