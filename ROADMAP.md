# Roadmap — Timeline Rental

Playable every week. Atmosphere non-negotiable.

---

## Week 1 — *Insert tape* ✓

**Goal:** Boot game → walk one scene → make one choice → see one collapse.

| Task | Done when |
|------|-----------|
| Pygame window — rain, neon alley, player dot/sprite | ✓ 320×180 scaled |
| One room, one NPC, one choice (2 options) | ✓ alley + examiner |
| Qiskit collapse picks outcome from superposed state | ✓ `quantum/collapse.py` |
| Amber collapse flash + narration text | ✓ 3-frame flash |
| SQLite save — one collapsed timeline | ✓ `data/db.py` + receipt |

---

## Week 2 — *The store* ✓

**Goal:** Hub between runs. Multiverse receipt. Replay value.

| Task | Done when |
|------|-----------|
| Timeline Rental hub scene | ✓ insert tape → intro → alley |
| Multiverse receipt screen | ✓ lost timelines + \|ψ⟩ bitstring |
| Ollama narration for collapse + store fragments | ✓ with fallbacks |
| Save multiple runs — gallery of receipts | ✓ [G] gallery in store |

---

## Week 3 — *Damaged tape* ✓

**Goal:** Blade Runner v1 full loop — photo, test, three collapses.

| Task | Done when |
|------|-----------|
| Photo observation — image shifts pre-collapse | ✓ quantum `photo_superposition` |
| Voight-Kampff pastiche scene | ✓ 3 questions, Ollama + fallbacks |
| 3 distinct collapsed endings | ✓ TIMELINE A / B / C titles |
| `TIMELINES: N active` UI counter | ✓ intro, alley, room |

---

## Week 4 — *Atmosphere pass* ← current

**Goal:** Visual + story polish on the damaged tape loop.

| Task | Done when |
|------|-----------|
| Richer alley / store / room neon-noir draw | ✓ layered buildings, CRT ghost-face, lamp cone |
| Atmospheric story beats while walking | ✓ alley position narration |
| Stronger examiner arc + choice-aware fallbacks | ✓ certainty → wasp → phone |
| Room enter beat + longer develop sequence | ✓ |
| Scanlines, vignette, neon glow, trench silhouette | ✓ |

---

## Week 5 — *Entangled tapes*

**Goal:** Choices echo across sessions.

| Task | Done when |
|------|-----------|
| Second tape slot (locked or teaser) | Future: Casablanca, Vertigo |
| Bell-state entanglement — choice in run N affects run N+1 | See docs/QUANTUM.md |
| Sound: rain loop, collapse tone | DESIGN.md audit |

---

## Week 6+ — Backlog

- [ ] Full second tape (Vertigo — spiral timelines)
- [ ] "Rewind" mechanic — uncollapse at cost
- [ ] Shared universe lore with Superposition Sessions (easter egg)
- [ ] CRT shader post-processing / audio

---

## Agent handoff

1. Check current week in this file
2. `DESIGN.md` before any art/copy
3. `docs/BLADE_RUNNER.md` for v1 content boundaries
4. Prompts in `prompts/` only
