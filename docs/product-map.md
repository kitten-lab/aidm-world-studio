# Product map — ADM / World Studio / Silo

**Doctrine and design intent**, not a changelog and not a promise to build everything listed.  
Captured so plans live in the **repo** (open in VS), not only in AI chat.

*Last updated: 2026-07-16*

---

## Purpose of this document

- Hold the **larger product map** while World Studio stays the first true root *tool*.
- Keep **multiple thought chains** visible at once (history, lore, Silo, Chester, readiness).
- Separate **what the stage is now** from **what Forestry / AIDM need later**.

Related: [IDEAS.md](../IDEAS.md) (near-term polish / parked studio work).

---

## One hunger, many media

| Attempt | What it held |
|---------|----------------|
| adm-documentation / OpenAI chats | Doctrine + product building (later set partly stuck in phone `conversations.json`) |
| mypi / silo-my-pocket-internet / imported.to | Pocket internet, switchboard, world-web |
| endless-door-network | Passage: destinations, dialects, ROMs, Chester crates |
| Chester’s Imports / vaults | Import aesthetics, terminals, Loom, Art-I-Facts |
| silo-the-forgetting-house | Identity as fragments (emotional thesis) |
| **World Studio** | First **right beginning root** — primes/instances, place, paths, folio, wiki |

Each medium hit a ceiling and felt like failure of the *whole*. None has to be the whole. Siblings and archives beat “one more total rewrite.”

---

## Cosmology

### Silo (Dark Tower sense)

- **Silo** = world that **contains all worlds**, including itself.
- Multiverse: different creators → different worlds that can **connect**.
- **Maker / VEN-maker world**: stories, primes, packs for import into people’s **seed worlds**.
- **Disney pattern**: primary world → timeline launches → mods run server timelines of variants.
- All of that sits *inside* Silo (including Silo as a world among worlds).

### ADM vs AIDM (yod = crown)

The yod is **not** “OpenAI product language.” It is **your** myth: when something completes its work, it may receive the letter — Adam finishes the thousand years and wears the crown.

| Name | Role |
|------|------|
| **ADM** | The field / continuity **system** (architecture, “all things are ven”) |
| **AIDM** | **Prime narrative agent** (+ storytelling sub-agents) — only after work is complete enough to wear the **yod**. *Not* the name of every tool. |
| **World Studio** | Human stage / pen — first true root tool; **no crown required** |

Putting “AIDM” on the *studio* can irritate because the crown sits on the hammer before the agent has earned it. Product title can stay **World Studio** under an ADM/Silo umbrella; repo names may lag.

### imported.to

1. External ARG spill →  
2. **Worlds have an internet** →  
3. That internet can **touch the outside** (doors, not a feed).

Pocket / EDN / Chester = passage & switchboard. World Studio = substance (what exists). **Stack, don’t merge.**

---

## Data Forestry & Chester Crate

Not “another kind of folio.” **Meaning storage for simulation and re-entry:**

1. Take a **concept** (root)  
2. **Fragment** into pieces  
3. **Tag** pieces to related data  
4. Keep pieces **connected to root** (lineage / graph)  
5. Track **time of event over time**  
6. Store in **organized lookup + system reports**

Purpose: narrative planning, observe threads, **enter at any point**.

### Tavern example

- Location **spacing** limits what you hear.  
- Tavern **chatter box** — ambient chatter, location-scoped.  
- People store **overheard knowledge** → NPCs can **gossip**.  
- **Decay** for objects, rumors, VENs.  
- **Weight** — what matters over time in *which* narratives.

### Chester’s beings as VEN / archetype

IdentityMan, TimeTraveler, ForkliftMan, ToolBringer, etc. are **known as names** — archetypes of **Chester, the Importer** — not bare PHP functions.

- **Chester** ≈ prime / symbol of Import  
- **Crate workers** ≈ `person/archetype` (persons of that symbol)  
- **Crate contents** ≈ fragments tagged back to root  

Codebase “animals” (dialects, ROMs, shells) sit in the same family: **named systems of being**.

---

## Layer stack

```text
                         SILO (cosmology container)
                                  │
                    ┌─────────────┴─────────────┐
                    │           ADM             │
                    │    continuity system      │
                    └─────────────┬─────────────┘
          ┌───────────────────────┼───────────────────────┐
          │                       │                       │
   World Studio              Passage net              Data Forestry
   (substance stage)         (doors / pocket          (crates, tags,
   author · walk             internet / imported.to)  threads, reports,
   folio · wiki                                       decay, gossip)
          │                       │                       │
          └───────────────────────┼───────────────────────┘
                                  │
                         AIDM (when earned)
                    prime narrative agent + subs
```

Maker world (export packs) ↔ seed worlds (import) under Silo.

---

## Myth / ship worlds / archives

- Lived myth + **core system worlds** you want to ship into the studio live partly in:
  - `z/logs` (mythic storyline set)
  - Phone OpenAI export (later product-building set — hard to access now)
  - adm-documentation messy forest
  - Silo / Forgetting House / personal world DBs

**Doctrine:** attic can wait; **floor is World Studio**. Salvage archives when chosen.

---

## Readiness (AI co-build)

- First AI in the codebase co-builds **tools**, does not write the ship world.
- System is **not ready** for major narrative expansion even if readiness *feels* close.
- Large builds (full Forestry, gossip, AIDM agent) **break on expansion** without history/lore control.
- Strengthen **record and lore** first — do not crown the agent early.

---

## Present-state vs history (critical gap)

World Studio today is largely **current state**:

| Tracked now | Missing / meager |
|-------------|------------------|
| Current position / containment | Who moved what, when, from → to |
| Room desc | No narrative history of desc changes (text log = editor snapshots only) |
| Lore | Uneven writers (talk yes, desc no); freeform `when` |
| Session undo | Not long-term narrative audit |

**Bite later:** cannot phase lore through main desc; cannot reconstruct “how the room became this”; gossip/decay have no honest feed; AIDM invents continuity.

### Lore / when doctrine

- **Mythic when** stays free text (Cow over the Moon) — good for story.  
- **Technical dates / unix** should be first-class *or* not pretend to be special (today they aren’t).  
- **Narrative moments** should not be fake technical fields unless the moment is a **VEN event reference**, not a string that looks like a date.

---

## History design (next foundation theme)

**Name:** **history** — not “journal.”

### Intent

- Organized record of change over time (even if not fully *shown* in UI at first).  
- **Room states** as history points (cosmology: “timeline points”).  
- **Visit** prior points: **view only** — look / examine-type; **no** take, put, go, dig, @desc.  
- **Cannot edit the past** — only open a viewport and leave back to present.  
- **Manual snapshots** preferred over logging every footstep / every position.

### Collision: multiverse `timeline` vs history point

| Term | Meaning |
|------|---------|
| **timeline** (coords) | Multiverse layer on instances (already in studio) |
| **history point** | Frozen **room** state on a place’s history spine (preferred command language) |
| “timeline point” | OK in myth/docs; avoid as primary CLI name |

### Two uses of the same base tool

| Use | Focus |
|-----|--------|
| **Room history / snapshots** | Place as node viewport on the past |
| **Item history** | Path of one instance over time (same spine, different lens) |

### Snapshots

- **Created manually** (builder marks a moment).  
- Nodes along the past — **viewports**, not live branches.  
- **Future** timeline splits may come from turning a snap into a *new* present — later, explicit.  
- v1 scope: **room-local** (desc + contents bag at mark time), not full-world freeze.

### Optional event log vs manual snaps

- Product *feel*: you choose when a state is worth keeping.  
- A thin event log may help Forestry later; it is not “record everything.”  
- Talk → lore asymmetry with desc remains a fix target once history exists.

### Forestry waist (when ready)

```text
mutation / manual snap → history point (+ optional event rows)
        → (optional) lore / event VEN
        → (later) decay, gossip, crates
```

### Implementation order (when coding — not yet)

1. Store + manual mark history points (room)  
2. List + read-only visit (look/examine only)  
3. Item-history lens  
4. Optional event log for Forestry  
5. No AIDM consumer; no edit-past; no silent restore-as-present  

---

## What not to do now

- Force AIDM onto studio chrome or let AI author the ship world  
- Rewrite adm-documentation in one pass  
- Full Data Forestry / decay / gossip  
- Collapse Pocket Internet into World Studio  
- Require phone logs rescued before next feature  
- Expand ontology (new roots) to fake history  
- Use `timeline` as the history-point command name  

---

## Open threads (parallel — not pick-one)

Keep these alive; any can be deepened without killing the others:

1. **History** — mark UX, snapshot payload, item vs room, visit chrome  
2. **Lore / when-types / event-ref** — mythic vs calendar vs VEN moment  
3. **Desc ↔ lore phasing** — promote, not only replace  
4. **Silo / maker / seed / Disney timelines** — import graph  
5. **Chester archetypes** — how they land as primes in studio  
6. **Ship worlds** — which core seeds belong in the studio spine  
7. **Archive salvage** — phone JSON + `z/logs` indexing when ready  
8. **Naming** — product “World Studio” vs repo `aidm-world-studio` vs ADM field  

---

## Discussion protocol (for AI + human)

- Prefer **large freeform** replies that hold multiple chains.  
- End with **decisions or details wanted** as a checklist (multi-OK), not a single forced tract.  
- **Durable plans go in this repo** (this file + IDEAS); session plan files are not enough.

---

## Decisions / details still open (feedback welcome)

When you have energy, any of these help — none blocks the others:

- [ ] Exact command names you *like* (`history mark`, `history visit`, …) vs what to avoid  
- [ ] Whether **manual snap only** is strict for v1, or “manual + optional thin event log”  
- [ ] What **item history** must show first (places visited? containers? last mover?)  
- [ ] Whether **visit** should freeze the player in-place (viewport overlay) vs a special “ghost look”  
- [ ] How loud “you are viewing the past” should be in chrome  
- [ ] Preferred public product title string (World Studio / ADM World Studio / other) while repo stays as-is  

---

*Promoted from Builds architecture discussion into repo so it cannot vanish with a chat export.*
