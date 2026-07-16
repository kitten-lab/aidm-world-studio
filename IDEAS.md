# Ideas (not committed to build)

Living list of half-finished concepts and polish intents for **AIDM World Studio**.  
Review occasionally; promote an item only when it beats “expand the engine again.”

**Current product stance:** stop expanding; perfect tool use. Prefer display, look sheets, help surfaces, word choice, and interaction clarity over new VEN kinds or systems.

---

## Focus now (tool use & presentation)

- **Look sheets** — presence tables, section order, density when rooms get full; progressive disclosure later
- **Ways on look** — restore inline ways (grouped table) for rapid movement without a second command; balance vs clutter in event/portal rooms
- **Help display** — how help is shown (pane, index, word choice, discoverability)
- **Action vocabulary** — keep refining verbs/labels (e.g. Ways vs Exits); consistency over novelty
- **Catalog lists** — extend the realm/vens mini-table polish to more lists only when it helps scanning
- **Word choices in status / hints** — quieter, clearer, less builder-noise
- **Content measure 72** — **phase 1 shipped:** `CONTENT_MEASURE`, ASCII turn HR, book `PAGE_VIEW_WIDTH`, studio ruler
- **Book reader modal (soft)** — **shipped:** full-width soft-dim reader; leaves; ←/→; Esc; `e` edit; `+` add leaf
- **Leaf title in singular studio** — **shipped:** Title field above body (`e` / `book page edit … <<studio`)
- **Leaf** — formal name for a book page unit in the reader; CLI may still say “page”

### Book reader + studio (design lock)

**Problem (solved for reader):** Side book pane was ~56 wide and shifted the log; authors couldn’t trust ASCII/`<<studio` layout at measure 72.

**Canonical measure:** **72 columns** for authored body text (studio + book leaves). Help rail stays optional chrome; do not author *for* the rail.

**Reader (shipped — soft modal):**
- Near-full-width modal over the log (`book_ui.make_book_reader_screen`)
- Soft dim backdrop (not blackout)
- ←/→ (also h/l) leaves, Esc/q close
- **`e`** opens singular studio for current leaf (title + body)
- **`+`** (plus; not bare `a`) adds a **leaf after current**, then opens studio
- Quiet toasts; return to reader — never dump edit noise into the world log

**Studio stays page-singular.** No multi-leaf buffer session. Structure lives in the reader; content lives in **STUDIO Writer** one leaf at a time (shared buffer for desc / lore / folio).

**Not preferred:** always-two-panes; multi-page `<<studio`; bare `a` for add (too easy to fat-finger).

---

## Parked (book / leaves)

### Organize leaves in a book
Reorder, remove, and otherwise organize leaves inside a BOK from the reader (or a small structure surface). Not now — add/edit/browse is enough. When promoted: stay out of singular studio; keep leaf ops on the reader.

---

## Design lock — lean VEN roots (**shipped in code**)

**Intent:** Adventure that knows itself — concepts that know how they interact.  
**Not:** invent a full VEN producer yet. **Not:** classic MUD taxonomy sprawl (goal/desire/purpose/feeling/archetype/material/event/realm/timeline all as peer roots).

**Roots are known systems of being** (selectors). **Subtypes** are author-chosen word labels that begin to define rule sets. **Primes** are named species; **instances** are lived copies.

### Proposed root set (7)

| Root | Role (baseline rules) |
|------|------------------------|
| **person** | Lived voice / body of needs; may hold sense, etc. |
| **place** | **Space** — the street, the outside, the ground you stand on. Not “inside of a house.” |
| **container** | Something **put on** a place (or carried) that you can **go into** / open / hold things. House on the street; box on the floor. May be marked **traversable into**. |
| **thing** | General “stuff”; expand via subtypes later (app, tool, material…). *Not* leaf-bearing by default. |
| **folio** | **Root** — thing-you-put-leaves-in (da Vinci). Distinct conditional usage already (soft reader, leaves, + leaf, studio, measure 72). Subtypes: **book**, **file-folder**, **sketchbook**, … |
| **symbol** | Abstract sense that acts by meaning (motif, law, sign…). Root of *concept* talk. |
| **sense** | Felt / atmospheric / drive-like presence (feeling, longing, pressure…). |

### Folio (locked — root, not a subtype of thing)

- **Why root:** already has a full rule set beyond general things (open → leaf reader, leaf stack, STUDIO Writer on a leaf, content measure). That *is* a known system of being.  
- **Why not “just thing”:** `folio/book`, `folio/file-folder`, `folio/sketchbook` are flavors of *leaf-bearing*, not of generic inventory.  
- **Leaf** stays the formal unit of content inside a folio.  
- **Book** demotes from root → **subtype** (or casual prime name) under **folio**.  
- Surface language can migrate book → folio over time; instance codes may keep **BOK-** prefix for a while (legacy kind code) or rebrand later.  
- **STUDIO Writer** (was “BOK Studio”) = shared buffer brand for *all* `<<studio` work (desc, lore, folio leaves) — not folio-only.
### Place vs container (locked intuition)

- **My street** = **place** (space outside).  
- **My house** = **container** someone put *on* that place; I can go *inside* it.  
- A room is not a competing root: either a **place** facet or a **container** you enter — not both as peer “kinds of room” without a rule. Prefer: **place** = open space; **container** = enterable volume with inside.

### Archetype (locked intuition)

- Archetype is **not** a peer of feeling under sense alone.  
- Archetype is closer to **a person of a symbol** — the *persons of symbols*.  
- Root affinity: **person** (type of person) *and/or* born from **symbol** (concept that walks).  
- Implementation options later (pick one when migrating):  
  - `person/archetype`  
  - or symbol that *elevates* / relates as person  
  - or sense that is *person-shaped* — weaker than “archetype ⊂ person of symbol”

### Fold map (today → lean)

| Current kind(s) | Lean home |
|-----------------|-----------|
| person | **person** |
| place | **place** (space; subtypes: road, porch, void… — not “house” as pure place) |
| object, material | **thing** |
| book | **folio** (+ subtype book / file-folder / sketchbook…) |
| concept | **symbol** |
| feeling, goal, desire, purpose | **sense** (subtype or prime) |
| archetype | **person/archetype** (or person-of-symbol) — *not* just sense |
| event | TBD: sense, symbol, or thing-with-rules |
| realm, timeline | layers / chrome — not roots |
| other | drop or rare escape hatch |

### What this is *not*

- Not full VEN producer / freeform ontology editor  
- Not “every kind must have subtypes”  
- Not pen-on-paper→book yet (capacity / elevate later)  
- **File-folder:** `folio/file-folder` (or prime under folio) — not a new root; not a generic thing  

### Shipped (strip pass)

- `KINDS` = person place container thing folio symbol sense + realm timeline  
- Aliases at create: book→folio/book, object→thing, feeling→sense/feeling, archetype→person/archetype, …  
- Codes: FOL, THG, SNS, CTR, SYM, … (legacy BOK/OBJ still parse where needed)  
- Look Things = thing/folio/container; Force = person/archetype; sense/event → Happened Here  
- Seeds use normalize on create_ven so old seed strings still work  

**Still soft:** surface commands still say `book open` (resolves folio); full help reword; deep subtype rule sets.

---

## Parked (systems / later)

### Submissions / forms / receipts

A VEN that behaves like a **form** (desk, counter, divine union filing). Using it prints a **receipt** (instance) with formatted fields. Examples: ticket counter, ineffable submissions dept.  
Prefer subtype-first (`object/form` or `book/receipt`) before a full new kind. Not now.

### VEN Studio (sibling app under AIDM)
Deep prime authoring (create, compose, lore, books) outside World Studio; write to `~/.aidm/ven-collector`. World Studio stays the stage; import becomes common. Collector + `.ven` packs are the thin waist already in progress.

### Look density / caps
When rooms hold many objects or ways: “+N more”, container-first presence, avoid flooding look. Related to ways-on-look tradeoff.

### Threshold / feel-first seed
Charged small start (not void, not full story spine); name that can age (not product chrome). Bootstrap now exists as the bare pole; Threshold remains optional middle.

### Progressive help / onboarding
Help and first-room hints tuned for “play as I feel” without drowning in builder commands.

### Cross-world / multi-file
Multiple world files as versions/templates; live portals between DBs deferred. Collector packs for idea migration.

### Extended VEN codes after I/E
World-stamped / expanded codes only when something has traveled; baseline codes stay simple in-DB.

---

## Shipped (orientation — not a changelog)

Reminders of recent foundations so polish builds on solid ground:

- VEN codes (`XXX-NNN`); instance refs `CODE-0001`
- `~/.aidm/ven-collector` · `vens export` / `ven load` (prime + instance packs)
- Place templates: free-standing `spawn` of place primes; dig still unique primes
- Portal `run` / `logout`; install-in-container; place subtypes
- Look buckets: Here / Things / Happened Here / Force / Also present
- Shared-width presence rows (no per-table headers)
- Ways: command + grouped list; look only counts (inline restore parked above)
- Seeds: story, classic, void, **bootstrap** (Nothing + Small note)
- `vens rename` primes; `rename me` avatar
- Catalog tables: realm/timeline list & places, vens list

---

## How to use this file

1. Add ideas under **Parked** with one short paragraph max.  
2. Promote to **Focus now** only if it is presentation / tool clarity, or an explicit exception.  
3. When shipping something from here, move a one-liner into **Shipped** or delete the parked entry.  
4. Do not treat this as a promise to implement everything.

*Last reviewed: 2026-07-16 (book reader / 72 measure / book edit session)*
