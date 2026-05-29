# Timeline Rental

**A noir video store at the edge of causality. Every tape is a world that shouldn't exist.**

A playable Python game where classic films become branching realities — powered by real quantum collapse mechanics and local AI narration. v1 tape: **Blade Runner** (pastiche / inspired, not IP-laden fan game).

```
┌──────────────────────────────────────────────────────────┐
│  TIMELINE RENTAL                    OPEN 24h (maybe)     │
│  ─────────────────────────────────────────────────────   │
│  ▓▓▓  BLADE RUNNER [damaged]     superposition: ACTIVE   │
│  ░░░  CASABLANCA [missing]       timeline: collapsed     │
│  ░░░  VERTIGO [rewinding]        observer: YOU           │
│                                                          │
│  > insert tape                                           │
│  > the rain never stops in three of the timelines        │
└──────────────────────────────────────────────────────────┘
```

---

## What this is

| Layer | Role |
|-------|------|
| **Pygame** | Playable 2D scenes — walk, talk, choose, observe |
| **Quantum (Qiskit)** | Branching outcomes exist in superposition until "observation" collapses the timeline |
| **Local LLM (Ollama)** | Stream-of-consciousness narration, dialogue, alt-history fragments |
| **SQLite** | Multiverse save states — what existed, what collapsed, what never was |

Not a visual novel template. Not a quiz. A **timey-wimey rental shop** you replay at midnight.

---

## Prerequisites

- Python 3.11+
- [Ollama](https://ollama.com/) installed and running

```bash
ollama pull llama3.2
```

---

## Quick start

```bash
git clone https://github.com/chris-dewitt/timeline-rental.git
cd timeline-rental
python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -e .
copy .env.example .env

python -m timeline_rental
```

**Week 1 ships:** rain-soaked alley → examiner's room → photo observation → quantum collapse → multiverse receipt saved to SQLite.

### Controls

| Key | Action |
|-----|--------|
| Arrow keys | Walk |
| E | Interact (doorway, photo) |
| 1 / 2 | Dialogue choices |
| Space / Enter | Skip typewriter text |
| R | Rent again (from receipt) |
| Q | Quit |

---

## Project docs

| Doc | Purpose |
|-----|---------|
| [DESIGN.md](./DESIGN.md) | Art bible — neon noir, rain, multiverse UX |
| [ROADMAP.md](./ROADMAP.md) | Week-by-week build plan |
| [docs/QUANTUM.md](./docs/QUANTUM.md) | Branch/collapse mechanics |
| [docs/BLADE_RUNNER.md](./docs/BLADE_RUNNER.md) | v1 tape — scenes, tone, pastiche guide |
| [docs/VOICE.md](./docs/VOICE.md) | Narration & dialogue voice |

---

## Repo structure (planned)

```
timeline-rental/
├── src/timeline_rental/
│   ├── game/             # Pygame engine, scenes, input
│   ├── quantum/          # Timeline superposition & collapse
│   ├── narrative/        # Ollama integration, prompts
│   └── data/             # SQLite schema, save/load
├── assets/
│   ├── fonts/
│   ├── sprites/          # Minimal pixel art — atmosphere over fidelity
│   └── audio/            # Rain loops, synth drones, UI sounds
├── prompts/
├── saves/                # Player multiverse states (gitignored)
└── tests/
```

---

## v1 tape: Blade Runner

Rain. Neon reflected in puddles. The question isn't "are you a replicant?" — it's **which version of you is asking, and in how many timelines?**

See [docs/BLADE_RUNNER.md](./docs/BLADE_RUNNER.md).

---

## Working with agents

Same rules as Superposition Sessions:
1. Read `DESIGN.md` first
2. Quantum collapse is real Qiskit — not `random.choice`
3. Prompts in `prompts/` — curated, versioned
4. Blade Runner = **pastiche inspired by**, not trademark cosplay

---

## Philosophy

- **Playable first.** Every week adds something you can *do*.
- **Alternate history / multiverse.** Choices don't branch cleanly — they superpose until observed.
- **Actually good writing.** PKD paranoia × Black Mirror premise × your phone rotted your brain.
- **No finance. No homework.**

---

## License

MIT — rent timelines responsibly.
