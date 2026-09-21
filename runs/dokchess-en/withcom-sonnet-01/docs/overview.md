# dokchess-en-withcom

## Purpose

`dokchess-en-withcom` is a **Java chess engine** implementation named DokChess. It provides a complete, playable chess program built from cleanly separated layers:

- An immutable **domain model** for board state, pieces, squares, and moves (with FEN support).
- A **rules engine** that generates legal moves and detects check/checkmate/stalemate.
- A **search and evaluation** subsystem (parallel minimax with material evaluation) that determines the engine's move.
- An **opening book** integration (Polyglot format) to short-circuit search in known openings.
- A **text UI** implementing the XBoard/WinBoard chess engine communication protocol, so the engine can be driven by any XBoard-compatible GUI.
- A **main entry point** that wires all of the above together into a runnable application.
- **Integration tests** validating the whole system end-to-end (full games and protocol sessions).

The design follows a strict layered/hexagonal dependency direction: the `domain` module has zero dependencies, `rules` depends only on `domain`, `engine_*` modules depend on `domain`/`rules`, `opening*` depends on `domain`/`opening`, and the `textui_xboard`/`main` modules compose everything at the top, keeping each layer independently testable and replaceable.

## End-to-End Architecture

### Module Dependency Graph

```mermaid
flowchart TB
    subgraph domain["domain (Position, Move, Piece, Square, FEN)"]
    end

    subgraph rules["rules (ChessRules / DefaultChessRules)"]
    end

    subgraph engine_eval["engine_eval (Evaluation / StandardMaterialEvaluation)"]
    end

    subgraph engine_search["engine_search (MinimaxAlgorithm / MinimaxParallelSearch)"]
    end

    subgraph engine_core["engine_core (Engine / DefaultEngine / DetermineMove chain)"]
    end

    subgraph opening["opening (OpeningLibrary)"]
    end

    subgraph opening_polyglot["opening_polyglot (PolyglotOpeningBook)"]
    end

    subgraph textui_xboard["textui_xboard (XBoard / MoveParser)"]
    end

    subgraph main["main (Main entry point)"]
    end

    subgraph integration_tests["integration_tests"]
    end

    domain --> rules
    domain --> engine_eval
    domain --> engine_search
    domain --> opening
    domain --> opening_polyglot
    domain --> textui_xboard

    rules --> engine_search
    rules --> engine_core
    rules --> textui_xboard

    engine_eval --> engine_search
    engine_search --> engine_core

    opening --> opening_polyglot
    opening --> engine_core
    opening_polyglot --> main

    engine_core --> textui_xboard
    engine_core --> main

    textui_xboard --> main

    main --> integration_tests
    textui_xboard --> integration_tests
    engine_core --> integration_tests
    rules --> integration_tests
```

### Runtime Flow: Determining and Playing a Move

```mermaid
sequenceDiagram
    participant GUI as XBoard GUI / stdin
    participant XBoard as textui_xboard.XBoard
    participant Engine as engine_core.DefaultEngine
    participant Library as opening.OpeningLibrary
    participant Search as engine_search.MinimaxParallelSearch
    participant Rules as rules.ChessRules
    participant Eval as engine_eval.Evaluation

    GUI->>XBoard: "e2e4" (move command)
    XBoard->>Rules: getLegalMoves(position) [validate]
    XBoard->>Engine: performMove(move)
    XBoard->>Engine: determineYourMove()
    Engine->>Library: lookUpMove(position)
    alt book move found
        Library-->>Engine: Move
    else no book move
        Engine->>Search: searchMove(position, observer)
        loop minimax tree search
            Search->>Rules: getLegalMoves / performMove
            Search->>Eval: evaluatePosition(leaf, colour)
        end
        Search-->>Engine: best Move (async)
    end
    Engine-->>XBoard: Observable<Move> onNext/onCompleted
    XBoard->>Engine: performMove(bestMove)
    XBoard->>GUI: "move <bestMove>"
```

### Application Bootstrap

```mermaid
sequenceDiagram
    participant JVM
    participant Main
    participant PolyglotOpeningBook
    participant DefaultChessRules
    participant DefaultEngine
    participant XBoard

    JVM->>Main: main(args)
    opt opening book path supplied
        Main->>PolyglotOpeningBook: new PolyglotOpeningBook(file)
    end
    Main->>DefaultChessRules: new DefaultChessRules()
    Main->>DefaultEngine: new DefaultEngine(chessRules, openingLibrary)
    Main->>XBoard: build & configure (stdin/stdout, engine, rules)
    Main->>XBoard: play()
    Note over XBoard: Blocks, running the XBoard protocol loop
```

## Core Modules Documentation

| Module | Description | Reference |
|---|---|---|
| **domain** | Immutable core chess vocabulary: `Square`, `Piece`, `Move`, `Position`, plus FEN conversion. Foundation for all other modules. | [domain.md](domain.md) (sub-modules: [domain_model](domain_model.md), [domain_fen](domain_fen.md)) |
| **rules** | Implements the Laws of Chess: legal move generation per piece type, castling, check/checkmate/stalemate detection via `ChessRules`/`DefaultChessRules`. | [rules.md](rules.md) (sub-modules: [rules_core](rules_core.md), [rules_movement_framework](rules_movement_framework.md), [rules_piece_moves](rules_piece_moves.md)) |
| **engine_core** | Orchestrates move determination via a Chain-of-Responsibility (`DetermineMove`): opening book lookup (`FromLibrary`) falling back to search (`FromSearch`). Defines the public `Engine`/`DefaultEngine` API. | [engine_core.md](engine_core.md) |
| **engine_eval** | Static position evaluation contract (`Evaluation`) and default material-counting implementation (`StandardMaterialEvaluation`), consumed at search leaf nodes. | [engine_eval.md](engine_eval.md) |
| **engine_search** | Minimax search algorithms: synchronous `MinimaxAlgorithm` and parallel, asynchronous `MinimaxParallelSearch` with `RatedMove` and cancellation support. | [engine_search.md](engine_search.md) (sub-modules: [engine_search_minimax](engine_search_minimax.md), [engine_search_parallel](engine_search_parallel.md)) |
| **opening** | Defines the `OpeningLibrary` port used to short-circuit search with known book moves. | [opening.md](opening.md) |
| **opening_polyglot** | Concrete `OpeningLibrary` implementation reading standard Polyglot `.bin` opening books, including Zobrist hashing and move decoding. | [opening_polyglot.md](opening_polyglot.md) (sub-modules: [opening_polyglot_format](opening_polyglot_format.md), [opening_polyglot_book](opening_polyglot_book.md)) |
| **textui_xboard** | Implements the XBoard/WinBoard text protocol (`XBoard`, `MoveParser`), bridging a GUI/terminal to the `Engine` and `ChessRules` abstractions. | [textui_xboard.md](textui_xboard.md) |
| **main** | Application composition root (`Main`) that wires rules, engine, opening book, and XBoard together and launches the protocol loop. | [main.md](main.md) |
| **integration_tests** | End-to-end tests: a full engine-vs-naive-opponent game (`EngineVsRandomIntegTest`) and an XBoard protocol session test (`XBoardIntegTest`). | [integration_tests.md](integration_tests.md) |