# textui_xboard Module

## 1. Purpose

The `textui_xboard` module is the **text-based user interface** of dokchess that
implements the classic [XBoard / WinBoard "Chess Engine Communication
Protocol"](https://www.gnu.org/software/xboard/engine-intf.html). It allows any
XBoard-compatible GUI (or a simple pipe/terminal in tests) to drive a dokchess
[`Engine`](engine_core.md) by exchanging plain-text lines over standard
input/output (or any other `Reader`/`Writer` pair).

The module is intentionally small and has exactly two classes:

| Class | Responsibility |
|---|---|
| [`XBoard`](#xboard) | The protocol adapter/loop: reads commands, drives the engine, writes responses. |
| [`MoveParser`](#moveparser) | Pure text ⇄ domain conversion of chess moves in XBoard's coordinate notation. |

It sits at the top of the application, translating between the **outside
world** (GUI process talking XBoard protocol) and the **inside world**
(dokchess [`Position`](domain_model.md) / [`Move`](domain_model.md) domain
objects and the [`Engine`](engine_core.md) abstraction).

## 2. Architecture Overview

```mermaid
graph TB
    GUI[XBoard/WinBoard GUI<br/>or test harness] -- text lines over<br/>stdin/stdout --> XBoard

    subgraph textui_xboard module
        XBoard["XBoard<br/>(protocol loop, Observer&lt;Move&gt;)"]
        MoveParser["MoveParser<br/>(text ⇄ Move conversion)"]
        XBoard --> MoveParser
    end

    XBoard -- setupPieces / determineYourMove /<br/>performMove / close --> Engine["Engine interface<br/>(engine_core)"]
    XBoard -- getLegalMoves --> ChessRules["ChessRules interface<br/>(rules_core)"]
    MoveParser -- builds/reads --> Move["Move / Position / Square / Piece<br/>(domain_model)"]

    click Engine "engine_core.md"
    click ChessRules "rules_core.md"
    click Move "domain_model.md"
```

The module depends on:

* [`domain_model`](domain_model.md) — for `Move`, `Position`, `Square`, `Piece`,
  `PieceType` used to represent and parse moves and board state.
* [`engine_core`](engine_core.md) — for the `Engine` interface that is driven
  by the `XBoard` loop (`setupPieces`, `determineYourMove`,
  `performMove`, `close`).
* [`rules_core`](rules_core.md) — for the optional `ChessRules` interface used
  to validate that a move received from the GUI is actually legal before it
  is forwarded to the engine.

It does **not** depend on [`opening`](opening.md)/[`opening_polyglot`](opening_polyglot_book.md)
or [`engine_search`](engine_search_minimax.md) directly — those are wired
together by the top-level [`main`](main.md) module, which constructs a
concrete `Engine` (e.g. `DefaultEngine`) and hands it to `XBoard`.

## 3. Component Details

### XBoard

`XBoard` (`org.dokchess.textui.xboard.XBoard`) is the central class of the
module. It implements `rx.Observer<Move>` so that it can subscribe to the
`Observable<Move>` returned by `Engine.determineYourMove()` and react to
intermediate/final move announcements.

**Configuration (dependency injection via setters)**

| Setter | Purpose |
|---|---|
| `setInput(Reader)` | Source of protocol commands (wrapped internally in a `BufferedReader`). Typically `System.in`; tests can pass a `StringReader`. |
| `setOutput(Writer)` | Sink for protocol responses. Typically `System.out`; tests can pass a `StringWriter`. |
| `setChessRules(ChessRules)` | Optional. If set, incoming opponent moves are validated against `getLegalMoves`; illegal moves are rejected with `Illegal move: <line>`. |
| `setEngine(Engine)` | Required. The engine instance that computes moves and holds/updates its own internal game state. |

**Main loop — `play()`**

`play()` runs a blocking read/dispatch loop until `quit` is received or the
input stream ends (EOF). Supported commands:

| Command received | Behaviour |
|---|---|
| `quit` / EOF | Stops the loop and calls `engine.close()`. |
| `xboard` | Acknowledges with an empty line. |
| `protover 2` | Replies `feature done=1` (no advanced features are negotiated). |
| `new` | Resets to a fresh `Position` and calls `engine.setupPieces(position)`. |
| `go` | Subscribes to `engine.determineYourMove()`; the engine computes dokchess's move asynchronously. |
| `<coord-move>` (e.g. `e2e4`, `e7e8q`) | Parsed via `MoveParser.fromXboard`. If `ChessRules` is configured, checked for legality. Then applied to the engine (`performMove`) and to the local `position`, and the engine is asked to compute its reply (`go`-like behaviour). |
| anything else | Replies `Error (unknown command): <line>`. |

**Reacting to engine output (`Observer<Move>`)**

* `onNext(Move move)` — an improved move was found during search; it is
  logged as a comment line (`# better move found: ...`) and stored as the
  current best move candidate.
* `onCompleted()` — search finished; the stored best move is sent to the GUI
  via `MoveParser.toXboard`, applied to the engine (`performMove`) and to the
  local `position`.
* `onError(Throwable)` — reported to the GUI as `tellusererror <message>`.

```mermaid
sequenceDiagram
    participant GUI
    participant XBoard
    participant MoveParser
    participant ChessRules
    participant Engine

    GUI->>XBoard: "e2e4" (line)
    XBoard->>MoveParser: fromXboard(line, position)
    MoveParser-->>XBoard: Move
    opt ChessRules configured
        XBoard->>ChessRules: getLegalMoves(position)
        ChessRules-->>XBoard: Collection<Move>
    end
    XBoard->>Engine: performMove(move)
    XBoard->>Engine: determineYourMove()
    Engine-->>XBoard: Observable<Move>

    loop search progress
        Engine-->>XBoard: onNext(candidateMove)
    end
    Engine-->>XBoard: onCompleted()
    XBoard->>MoveParser: toXboard(bestMove)
    MoveParser-->>XBoard: "move e7e5"
    XBoard->>Engine: performMove(bestMove)
    XBoard->>GUI: "move e7e5"
```

### MoveParser

`MoveParser` (`org.dokchess.textui.xboard.MoveParser`) is a small, stateless
utility class responsible for converting between XBoard's plain-text
coordinate notation and dokchess's `Move` domain object.

* **`fromXboard(String input, Position position)`** — parses strings matching
  `[a-h][1-8][a-h][1-8][qrnb]?` (e.g. `e2e4`, `e7e8q`) into a `Move`. It
  consults the supplied `Position` to:
  * look up the moving `Piece` at the origin square,
  * detect whether the destination square is occupied (→ capture flag),
  * detect pawn promotion (pawn reaching rank 0/7) and decode the promotion
    letter into a `PieceType`.
  Returns `null` if the string does not match the expected pattern (the
  caller, `XBoard`, treats this as "unknown command").

* **`toXboard(Move move)`** — formats a `Move` back into the wire format,
  prefixed with `move ` (e.g. `move e7e8q`), lower-casing the promotion piece
  letter as required by the protocol.

```mermaid
classDiagram
    class MoveParser {
        +Move fromXboard(String input, Position position)
        +String toXboard(Move move)
    }
    class XBoard {
        -Reader input
        -Writer output
        -ChessRules chessRules
        -Engine engine
        -Move bestMove
        -Position position
        -MoveParser moveParser
        +setInput(Reader)
        +setOutput(Writer)
        +setChessRules(ChessRules)
        +setEngine(Engine)
        +play()
        +onNext(Move)
        +onCompleted()
        +onError(Throwable)
    }
    XBoard --> MoveParser : uses
    class ObserverMove {
        <<interface>>
    }
    XBoard ..|> ObserverMove
```

## 4. How this module fits into the system

```mermaid
graph LR
    main["main<br/>(wires everything together)"] --> XBoardMod["textui_xboard"]
    main --> EngineCore["engine_core"]
    EngineCore --> EngineSearch["engine_search_*"]
    EngineCore --> EngineEval["engine_eval"]
    EngineCore --> OpeningLib["opening / opening_polyglot_*"]
    EngineCore --> RulesCore["rules_core"]
    RulesCore --> RulesPieceMoves["rules_piece_moves"]
    RulesCore --> RulesMovementFw["rules_movement_framework"]
    XBoardMod --> DomainModel["domain_model"]
    XBoardMod --> RulesCore
    XBoardMod --> EngineCore

    click main "main.md"
    click EngineCore "engine_core.md"
    click RulesCore "rules_core.md"
    click DomainModel "domain_model.md"
```

The [`main`](main.md) module (application entry point) is responsible for
constructing a concrete `ChessRules` (e.g. `DefaultChessRules`) and `Engine`
(e.g. `DefaultEngine`, wired with an opening book and a search algorithm),
and injecting them into an `XBoard` instance whose input/output are attached
to the process's standard streams (or, in tests, to in-memory
readers/writers — see `XBoardIntegTest` in
[`integration_tests`](integration_tests.md)).

Because `XBoard` depends only on the `Engine` and `ChessRules`
**interfaces**, it is fully decoupled from the concrete search algorithm
([`engine_search_minimax`](engine_search_minimax.md),
[`engine_search_parallel`](engine_search_parallel.md)), evaluation function
([`engine_eval`](engine_eval.md)) or opening book implementation
([`opening_polyglot_book`](opening_polyglot_book.md)) in use — any conforming
implementation can be substituted without touching this module.

## 5. Sub-modules

This module consists of only two tightly coupled classes in a single package
and does not warrant further sub-module decomposition; both classes are
documented together above.
