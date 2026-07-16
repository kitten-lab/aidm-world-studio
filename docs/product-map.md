# Product map — ADM / World Studio / Silo

**Doctrine and design intent**, not a changelog and not a promise to build everything listed.  
Captured so plans live in the **repo** (open in VS), not only in AI chat.

*Last updated: 2026-07-16*

---

## Purpose of this document

- Hold the **larger product map** while World Studio stays the first true root *tool*.
- Keep **multiple thought chains** visible at once (history, lore, Silo, Chester, readiness).
- Separate **what the stage is now** from **what Forestry / AIDM need later**.

Related: [IDEAS.md](../IDEAS.md) (near-term polish / parked studio work) · [CHANGELOG.md](../CHANGELOG.md) (what shipped, one-liners).

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
**Stance (2026-07-16 refine):** Prefer a **simple spine** over live time-play, locked bags on every node, or visit mode first. Do not overbuild fold/cursor/lock until this backbone exists.

### Intent (thin)

1. **Node positions** along a **timeline** (and with **realm**) — numbered notches for story order.  
2. **Creation / edit tooling** can take a **story when** = that node (e.g. `when @3` or bound to current authoring node).  
3. That when is stored on the material’s **history for the life of the item** (instance or prime, as appropriate).  
4. If story when is unknown: store **`@unknown`** *in relation to* the realm/timeline the act belongs to — never pretend craft `created_at` is story time.  
5. **Bags / visit / fold** stay later optional tools, not the floorboard.

**Not required for v0:** active play with nodes moving, auto event-VEN on name, room bag on every node, edit-locked past plates.

### Two clocks (always)

| Clock | Meaning |
|-------|---------|
| **Craft time** | When the builder typed / the row was written (`created_at`) |
| **Story when** | Node on (realm, timeline), or **`@unknown`** on that strand |

### Nodes

- **Numbered** along a timeline strand (0, 1, 2, …).  
- Optional **name** / **@desc** on a node later — nice; not required to create the backbone.  
- Naming a node does **not** have to spawn an event VEN (promote later if needed).  
- Subdivision (1.5 between 1 and 2) — later if needed.

### What spawn / create / lore / etc. store

On produce or relevant edit, record something like:

```text
realm_id / timeline_id   (strand — already familiar as layers)
story_when               node N  |  @unknown
crafted_at               wall clock
```

- Explicit `when @N` → node N on the **current** (or specified) timeline.  
- Omitted → **`@unknown`** on that realm/timeline (honest gap).  
- Mythic free text (“Cow Jump night”) can remain a **label** on a node or lore; the **structural** when is node or unknown.

### History journal (life of the item)

Thin log rows on instances (and optionally primes): “this material entered / was authored / was marked **@N** (or @unknown) on strand R/T.”  
Room **bags** are **not** required for this. Bags help later if you want to **revisit stage pictures** or adjust a beat; they are not the first foundation.

### Bags / visit / event VEN (deferred)

| Tool | Role (later) |
|------|----------------|
| Room bag | Optional freeze of place contents at a craft moment or node |
| Visit | Viewport of a bag — not required for story-when backbone |
| Event VEN | First-class occurrence; may **cite** a node; not every when |

### Collision: multiverse `timeline` layer vs history

| Term | Meaning |
|------|---------|
| **timeline** (coords) | Multiverse layer on instances (already in studio) |
| **node** | Ordered notch **along** that timeline |
| **@unknown** | On that strand, story position not set |
| **history** | Record of story_when (+ craft time) on materials over their life |

### Forestry waist (when ready)

```text
create/edit → history row (realm, timeline, node|@unknown, craft time)
           → (later) bags, event VENs, decay, gossip
```

### Implementation order

1. **Shipped (thin backbone):** nodes + `history_entries`; create/spawn/lore `when @N` / `@unknown`; `history nodes|here|on|ven`  
2. Optional: current authoring node shown on look/where  
3. Later: bags, visit, event promote, fold  

---

## What not to do now

- Force AIDM onto studio chrome or let AI author the ship world  
- Rewrite adm-documentation in one pass  
- Full Data Forestry / decay / gossip  
- Collapse Pocket Internet into World Studio  
- Require phone logs rescued before next feature  
- Expand ontology (new roots) to fake history  
- Live time-play with moving nodes as the first history feature  
- Require every node to be a full room bag  
- Use craft `created_at` as if it were story when  

---

## Open threads (parallel — not pick-one)

1. **History backbone** — node store, `@N` / `@unknown`, life-of-item history rows  
2. **Lore / when display** — always show craft vs story when  
3. **Desc ↔ lore phasing** — promote, not only replace  
4. **Silo / maker / seed / Disney timelines** — import graph  
5. **Chester archetypes** — how they land as primes in studio  
6. **Ship worlds** — which core seeds belong in the studio spine  
7. **Archive salvage** — phone JSON + `z/logs` indexing when ready  
8. **Naming** — product “World Studio” vs repo `aidm-world-studio` vs ADM field  
9. **Bags / visit** — deferred until backbone exists  
10. **Look/where** — show authoring node or only on demand 

---

## Discussion protocol (for AI + human)

- Prefer **large freeform** replies that hold multiple chains.  
- End with **decisions or details wanted** as a checklist (multi-OK), not a single forced tract.  
- **Durable plans go in this repo** (this file + IDEAS); session plan files are not enough.

---

## Decisions / details still open (feedback welcome)

- [ ] Default when spawn/create omits `@N` → always `@unknown`, or inherit “current authoring node” if set  
- [ ] Nodes scoped **per timeline instance** vs one global sequence  
- [ ] History rows on **instance only** vs also on prime  
- [ ] Whether look/where shows story node in v0 or only `history` / examine  
- [ ] Preferred public product title vs repo name  

---

*Promoted from Builds architecture discussion into repo so it cannot vanish with a chat export. History section simplified 2026-07-16: nodes + @when / @unknown first; bags/visit later.*
