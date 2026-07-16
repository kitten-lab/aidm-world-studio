# AIDM World Studio

A **VEN-based** MUD-like multiverse builder (**AIDM** — dream-maker / crowned Adam): walk places in a terminal, author characters, materials, feelings, and lore, and treat almost everything as a **Virtual Entity** with **instances**.

Parked ideas and polish intent (not a roadmap promise): see [`IDEAS.md`](IDEAS.md).

## Ideas in play

| Concept | Meaning |
|--------|---------|
| **VEN** | Prime / canonical virtual entity (place, person, object, feeling, realm, timeline, material, …) |
| **Instance** | A situated occurrence of a VEN (this cathedral *here*, this thread *now*) |
| **Lineage** | Specialization tree of primes (`parent_ven_id`): FILE → Secret Document → elevated children |
| **Composition** | Prime-level parts (`ven_parts`): Him composed of Concept / Archetype primes (not inventory) |
| **Containment** | Any instance may hold others (room → people/objects; person → feelings/archetypes) |
| **Elevate** | Lived instance → **new Prime VEN** under the origin prime; the lived copy **rebinds** to that prime |
| **Links** | Typed exits: `spatial`, `dimensional`, `temporal`, `narrative`, `conditional` |
| **Lore revisions** | Append-only history on a place (or VEN), optionally tagged by timeline / when-label |

Storage is a single **SQLite** world file (`worlds/*.world.db`). Optional YAML export can come later; the DB is the source of truth for simulation.

## Requirements

- Python 3.11+
- `pip install -r requirements.txt` (or `pip install -e .`)

## Quick start

```powershell
cd C:\Builds\world-studio
py -3.12 -m pip install -e .
py -3.12 -m world_studio --reseed
```

Default seed is **story** (hearth / ancient stories / lovers across time). Classic cathedral–mirror–shatter:

```powershell
py -3.12 -m world_studio --reseed --seed classic
```

**Void** — build from nothing: one empty place, no exits, one strange romantic book:

```powershell
py -3.12 -m world_studio --reseed --seed void
```

**Bootstrap** — barest useful start (plain primes only):

```powershell
py -3.12 -m world_studio --reseed --seed bootstrap
```

If `py` is not on PATH, use the full installer path:

```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe" -m pip install -e C:\Builds\world-studio
& "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe" -m world_studio --reseed
```

### Textual TUI (at-a-glance sidebar)

```powershell
python -m world_studio --textual --reseed
```

Plain REPL shows a **situation strip** above each `›` prompt (you @ place · coords · inv · exits).  
Use **`status`** (aliases: `sit`, `whereami`, `where`) for the full situation block.

**↑ / ↓** at the prompt recalls previous commands (REPL via `prompt_toolkit`, TUI built-in).

### One-shot commands (good for scripts / tests)

```powershell
python -m world_studio -c look -c "go along the story road" -c inv -c "take letter"
```

## Seed tour (story — default)

You start in **THE-HEARTH-OF-UNFINISHED-MAPS** (`WOVEN` / `TOLD-TIME`).

1. `look` — unfinished maps, quill, quiet invitation  
2. `go east` — Gallery of First Names  
3. `go into the living shelves` — Hall of Stories Still Being Told  
4. `go along the story road` — Twin Overlook (lovers across time)  
5. `go a generation later` — same overlook on **ECHO**  
6. Optional far path: hall → `deeper into the side wing` → `years after the break` (**SHATTERED**, kept off the opening)

### Classic seed

```powershell
python -m world_studio --reseed --seed classic
```

Start: **THE-CATHEDRAL-OF-ORDINARY-LIGHT** → mirror → Archive → `years later` SHATTERED.

### Void seed (blank canvas)

```powershell
python -m world_studio --reseed --seed void
```

Start: **THE-VOID** (`UNFORMED` / `FIRST-BREATH`) — no exits, no NPCs.  
On the floor: **A Book That Loves You Backwards** (`book open` / `book pages`).  
Then dig, link, @desc, create, spawn — the world is yours.

### Bootstrap seed (bare)

```powershell
python -m world_studio --reseed --seed bootstrap
```

Start: **Herenow** (instance of prime **Place**) · realm **Base** / timeline **Start**.  
You are **Builder** (`person/archetype`). No floor props, no paths — dig your own ditch.

### Builder loop (example)

```text
dig Quiet Gallery
link north -> Quiet Gallery both
go north
@desc Soft light on unfinished canvases.\nDust tastes like turpentine.
@desc + A window holds afternoon.
undo
```

Multiline description:

```text
@desc <<
First paragraph.
Second paragraph.
.
```

## In-game help

- **`help`** / **`?`** — short command index  
- **`help <term>`** — detail + examples (e.g. `help look`, `help @desc`, `help undo`)  
- **VEN lore:** `lore ven …` · `lore ven … add Title | body`  
- **Timeline / realm:** `timeline list` · `timeline set …` · `dig … timeline …`

```powershell
python -m world_studio -c help -c "help lore"
```

### Help in a second terminal (standalone)

Leave the catalog open beside the studio — **no world DB**, same topics. On a TTY this opens a **simple Textual display** (scrollable body + input):

```powershell
# Textual help UI (default on interactive terminal)
python -m world_studio.help_cli
python -m world_studio.help_cli look

# one-shot print (scripts / pipes)
python -m world_studio.help_cli --print
python -m world_studio.help_cli --print look

# line-mode loop (no Textual)
python -m world_studio.help_cli -i

# after pip install -e .
world-studio-help
world-studio-help look
world-studio-help --print lore
```

In the Textual UI: type a **number** or **topic**, Enter; **0** returns to the index; **q** or **Esc** quits.

## Command cheat sheet

- **Walk:** `look`, `go <exit>`, `status` / `sit` / `whereami`, `exits`, `map` / `map <depth>`, `take` / `drop`, `inv`, `examine`, `who`
- **Lore:** `lore`, `lore add Title | body`, `lore search <q>`
- **Build:** `dig`, `link <exit> -> <place> [type] [both]`, `@desc` / `@desc +` / `@desc clear`, `create` (`… of <parent>`), `spawn`, `put`, `elevate` (`… as Name`), `compose`, `lineage`, `vens` / `vens tree`
- **Undo:** `undo` / `u` — last successful builder mutation this session (not `go`)

## Project layout

```
world-studio/
  src/world_studio/
    schema.sql    # VEN / instance / containment / links / lore
    world.py      # domain operations
    commands.py   # parser + handlers
    seed.py       # story + classic sample multiverses
    undo.py       # session undo stack
    cli.py        # Rich REPL + Textual
  worlds/         # created on first run (seed.world.db)
```

## Roadmap (short)

- Graph map UI (filter by realm/timeline, color by link type)
- Richer lore: diff views, ordered when-labels, attach to any VEN kind
- YAML import/export for git-friendly lore packs
- Instance history (who held which material when)
- Persistent undo / redo; on-demand spellcheck
- VEN / timeline / realm **side panes** (like help) for long catalogs
- Optional durable instance handles beyond sequential `#0001` refs
- Shared **VEN library / packs** (export lineage + composition; Studio imports into a world)
- Optional **VENproducer** shell focused on production graphs without the walk loop
