77 Quelldatei(en), Vergleich je Datei gegen die Kommentare derselben Datei

  Datei                  Kandidaten  mit Komm. ohne Komm.     Verhaeltnis
  ------------------------------------------------------------------------
  data_creatures.cpp            148         31         12            2.6x
  player_run.cpp                218         44         26            1.7x
  inventory.h                    78         31         16            1.9x
  config.cpp                    184         24         10            2.4x
  dungeon_los.cpp               151         37         25            1.5x
  game.cpp                       66         26         14            1.9x
  treasure.cpp                  114         26         15            1.7x
  ui_inventory.cpp              169         26         15            1.7x
  monster.cpp                   244         31         21            1.5x
  monster_manager.cpp            80         24         14            1.7x
  rng.cpp                        73         28         18            1.6x
  data_stores.cpp                35         14          6            2.3x
  ui_io.cpp                     216         41         33            1.2x
  data_treasure.cpp             103         30         23            1.3x
  dungeon.h                      58         17         10            1.7x
  player_tunnel.cpp              43         17         10            1.7x
  game_run.cpp                  342         28         22            1.3x
  identification.cpp            119         21         15            1.4x
  ui.cpp                        105         27         21            1.3x
  curses.h                       15         10          5            2.0x
  data_player.cpp               100         21         16            1.3x
  game_objects.cpp               53         16         11            1.5x
  helpers.h                       9          8          3            2.7x
  identification.h               14          9          4            2.2x
  monster.h                      67         19         14            1.4x
  player_eat.cpp                 18          6          1            6.0x
  treasure.h                     37         13          8            1.6x
  data_tables.cpp                29         11          7            1.6x
  scores.h                       14         10          6            1.7x
  scrolls.cpp                    44          7          3            2.3x
  types.h                        30         15         11            1.4x
  version.h                      12          8          4            2.0x
  mage_spells.cpp                11          6          3            2.0x
  player_stats.cpp               67         18         15            1.2x
  data_store_owners.cpp          12          7          5            1.4x
  game_files.cpp                 54          9          7            1.3x
  player_magic.cpp               30         18         16            1.1x
  player_move.cpp               113         14         12            1.2x
  player_pray.cpp                20          6          4            1.5x
  rng.h                           2          2          0    2x (nur mit)
  spells.h                       18         10          8            1.2x
  store.h                        16          7          5            1.4x
  ui.h                           18         11          9            1.2x
  wizard.cpp                     39          8          6            1.3x
  data_recall.cpp                 3          2          1            2.0x
  dice.cpp                        7          4          3            1.3x
  dungeon.cpp                   161         26         25            1.0x
  main.cpp                       29          7          6            1.2x
  player_quaff.cpp               18          3          2            1.5x
  config.h                        7          1          1            1.0x
  game_death.cpp                 40          8          8            1.0x
  game_save.cpp                 144         13         13            1.0x
  headers.h                       9          4          4            1.0x
  inventory.cpp                  95         11         11            1.0x
  player_bash.cpp                69         14         14            1.0x
  player_throw.cpp               59         12         12            1.0x
  player_traps.cpp               11          2          2            1.0x
  recall.cpp                     87         13         13            1.0x
  scores.cpp                     66         20         20            1.0x
  staves.cpp                     20          2          2            1.0x
  character.h                    48         10         11            0.9x
  dice.h                          -  keine Kommentare
  helpers.cpp                    24          6          7            0.9x
  mage_spells.h                   -  keine Kommentare
  recall.h                        8          3          4            0.8x
  scrolls.h                       -  keine Kommentare
  staves.h                        -  keine Kommentare
  store_inventory.cpp            85         12         13            0.9x
  wizard.h                        -  keine Kommentare
  store.cpp                     132         17         19            0.9x
  character.cpp                  85         19         22            0.9x
  game.h                         88         20         23            0.9x
  dungeon_tile.h                 48         16         21            0.8x
  player.h                      165          8         16            0.5x

  spells.cpp                    299         21         29            0.7x
  dungeon_generate.cpp          165         25         37            0.7x
  player.cpp                    241         16         28            0.6x

  'Kandidaten': eindeutige Woerter, die nur im Kommentar dieser
  Datei stehen (nicht im kommentarfreien Quelltext derselben Datei).
  'mit/ohne Komm.': wie viele davon in der jeweiligen Doku auftauchen.
  'Verhaeltnis': mit / ohne Komm., je Datei. '-' bei 0 zu 0,
  '...x (nur mit)' wenn ohne Kommentare kein einziges Wort auftaucht.

  Beispiele (nur mit Kommentaren aufgetaucht):
    data_creatures.cpp     acid, cdefense, charmed, cmove, complete, frequency, hit, infra-vision
    player_run.cpp         adjacent, algorithm, array, break, corners, corridor, cut, determine
    inventory.h            alignment, always, array, but, category, character, dangling, dungeon
    config.cpp             binary, executable, experience, identified, level, limits, paths, relative
    dungeon_los.cpp        direct, ending, exceed, factor, fast, hall, highlight, integer-based
    game.cpp               binary, boolean, but, different, distribution, generates, maxval, null
    treasure.cpp           apply, consistency, counter, dragon, dungeon, ego, flame, food
    ui_inventory.cpp       appropriate, carried, designed, existing, heavy, keep, minimize, redraw
    monster.cpp            already, blindness, breath, creatures, died, direction, doors, flee
    monster_manager.cpp    allocate, always, available, chance, check, created, creatures, distribution
    rng.cpp                bit, computed, div, following, full, initialized, large, lehmer
    data_stores.cpp        alchemy, armory, general, index, magic-user, objects, owner, temple
    ui_io.cpp              characters, clearing, ctrl, delay, different, directory, errors, expand
    data_treasure.cpp      abilities, amulet, chests, doors, following, gems, magical, misc
    dungeon.h              character, item, items, level, multiple, non-living, parameters, size
    player_tunnel.cpp      boundary, doors, free, illegal, movement, prevent, special, tool
    game_run.cpp           changes, commands, create, different, loading, object, output, resting
    identification.cpp     already, appropriate, ascii, check, determines, don't, generated, handle
    ui.cpp                 area, boundary, changes, converts, inventory, light, map, mode
    curses.h               microsoft, pdcurses, studio, undefined, visual
    data_player.cpp        disarm, heights, hit, rank, saving, titles, weights
    game_objects.cpp       chest, doors, free, moved, secret, shop, space, stairs
    helpers.h              dependencies, external, generic, helper, standard
    identification.h       potions, rings, scrolls, size, staffs, wands
    monster.h              attacks, base, breeding, cloning, dungeon, messages, total
    player_eat.cpp         bloating, experience, gain, never, players, time
    treasure.h             enchanted, max, min, range, tval, visible, wear, wearable
    data_tables.cpp        descriptive, distribution, misc1, player, pseudo-normal
    scores.h               allowed, bytes, cpp, implemented, save
    scrolls.cpp            long, objects, short, turn
    types.h                but, desc, errors, executable, lint, obj, ones
    version.h              cmake, cmakelists, extract, txt, umoria
    mage_spells.cpp        cpp, magic, names
    player_stats.cpp       but, calculate, change, external, inventory, point, weapon
    data_store_owners.cpp  owner's, pricing
    game_files.cpp         access, time
    player_magic.cpp       detect, fire, period, time
    player_move.cpp        doors, legal, move, moves, moving, onto, panel, special
    player_pray.cpp        like, turn
    rng.h                  cpp, rng
    spells.h               base, holds, priest

    store.h                different, max, stock
    ui.h                   equipment, holds, save, stats
    wizard.cpp             light, specified
    data_recall.cpp        memory
    dice.cpp               damage
    dungeon.cpp            allocates, border, lights, normal, process, rooms, spots, trap
    main.cpp               option, saved
    player_quaff.cpp       lose
    game_death.cpp         gravestone
    game_save.cpp          death, read, reads, restoration, restored
    headers.h              umoria
    inventory.cpp          carry, category, checks, drops, finds
    player_bash.cpp        ability, bashed, directions, potentially
    player_throw.cpp       bonuses, maximum, weapon
    recall.cpp             core, lines, punctuation
    scores.cpp             birth, earned, multiple, page, saving, writing
    character.h            bit, player, social
    store_inventory.cpp    adds, general, group, stackable, torches, whether
    store.cpp              customer, incremental, overflow, players, prevents, valid
    character.cpp          output, routine, select, their
    game.h                 deviation, handle, loop, objects, startup, universe
    dungeon_tile.h         cave, floors, item, save, walls
    player.h               access, carrying, magical
    spells.cpp             actual, ball, bolt, depends, enchantment, etc, failure, mage
    dungeon_generate.cpp   builds, column, constants, entire, generate, store, stores, traps
    player.cpp             changes, closes, met, opens, recalculated, temporary

  Sichtbarer Effekt bei 49 von 72 Dateien (mindestens ein Kandidatenwort mehr mit als ohne Kommentare).

  Ueber alle Dateien: 1107 Treffer mit Kommentaren gegenueber 876 ohne -- Faktor 1.3.
  (Summe der Treffer, nicht Mittelwert der Einzelverhaeltnisse --
  sonst wuerden Dateien mit 1 vs. 0 genauso stark zaehlen wie
  Dateien mit 20 vs. 10.)