# Design Bible — Timeline Rental

> *You're not playing a Blade Runner game. You're renting a damaged tape of a world that keeps forgetting itself.*

---

## North star

The game should feel like:

- Walking into a **24-hour video store** that exists between timelines
- Inserting a VHS that **glitches between possible histories**
- Reading narration you'd **quote to a friend at 2am**
- Making choices where **the outcome wasn't decided until you looked**

Four tests (same as Sessions): look, read, sound, feel like art.

---

## Visual language — Neon Noir

### Palette

| Name | Hex | Use |
|------|-----|-----|
| Rain Black | `#0d0d12` | Background, letterbox bars |
| Neon Cyan | `#00e5ff` | Interactive elements, "alive" UI |
| Replicant Amber | `#ff9a3c` | Warnings, collapse events, memory |
| Blood Neon | `#ff2a6d` | Danger, observation, emotional peaks |
| Smog Gray | `#4a5568` | Distant buildings, inactive choices |
| Wet White | `#cbd5e1` | Primary dialogue text |

### Typography

| Role | Font |
|------|------|
| Narration / inner monologue | **IBM Plex Serif** or **Crimson Pro** |
| Dialogue / UI | **Share Tech Mono** or **VT323** |
| Store signage | **Press Start 2P** (sparingly — title screen only) |

### Pixel art direction

- **Low-res intentional** — 320×180 internal, scaled up with `pixelated` CSS equivalent in pygame
- **Silhouettes over detail** — rain, neon edges, cigarette glow
- **No realistic sprites.** Suggest, don't depict.
- **Color limits** — 16–32 colors per scene max

### Motion

- **Rain overlay** — always, subtle parallax
- **Neon flicker** — random 2–4 frame drops, not seizure mode
- **Text typewriter** — narration appears char-by-char, skippable
- **Collapse flash** — amber full-screen 3 frames, then new timeline

---

## The store (hub)

Between tapes, you stand in **Timeline Rental**:

- Shelves of tapes — most are static/decayed
- One tape glows: **BLADE RUNNER [damaged]**
- CRT TV shows static that almost resolves into faces
- Ollama-generated **store clerk fragments** — never full conversations, always uncanny

Copy example:
> *"That one's been rewinding since Tuesday. Or maybe Tuesday never happened here."*

---

## Blade Runner tape (v1)

Not a retelling. A **pastiche multiverse**:

- Acid rain alley
- Voight-Kampff-ish test — but the test changes based on collapsed timelines
- A photo that shows different people depending on observation history
- The unicorn question — reframed as "how many versions of this memory are superposed?"

See [docs/BLADE_RUNNER.md](./docs/BLADE_RUNNER.md).

---

## Quantum UX — how players feel multiverse

### Superposition (hidden)

Player choices don't immediately branch the story. Outcomes accumulate as **amplitudes** until an observation event.

**Player-visible hints:**
- UI shows `TIMELINES: 3 active` in corner (mono font, cyan)
- Occasional déjà vu lines: *"You've been here. Or someone like you."*
- Same NPC says slightly different things on replay

### Observation / collapse

Triggered by:
- Looking at the photo
- Answering the Voight-Kampff question
- Entering a specific room

**Effect:**
- Amber flash
- Narration: what collapsed, what died
- `TIMELINES: 1` — the receipt updates

### Multiverse receipt (end of session)

```
═══════════════════════════════════
  TIMELINE RENTAL — RETURN SLIP
═══════════════════════════════════
  TAPE:     blade runner [damaged]
  RENTED:   2026-05-28 01:14
  RETURNED: 2026-05-28 01:47

  COLLAPSED:  you chose mercy (timeline B)
  LOST:       timeline A — you ran
              timeline C — you never entered

  "the rain remembers what you forgot"
═══════════════════════════════════
```

---

## Sound design

| Element | Treatment |
|---------|-----------|
| Ambience | Rain loop + distant synth drone (Vangelis-adjacent, original) |
| UI | Soft tape-insert mechanical click |
| Collapse | Vinyl scratch + amber tone 440Hz→220Hz |
| Dialogue | No voice acting v1 — text + subtle blip per char |

Reference: Blade Runner 2049 score (sparse), VA-11 Hall-A rain, Kentucky Route Zero narration pacing.

---

## Anti-patterns

- Generic cyberpunk FPS aesthetic
- Rick Deckard cosplay / direct movie quotes as crutch
- Branching dialogue trees that feel like a corporate RPG
- Explaining quantum mechanics in tutorial popups
- Light mode anything

---

## Success criteria

1. You replay the 10-minute v1 scene and get a different collapsed ending
2. The multiverse receipt is something you'd screenshot
3. A friend watches over your shoulder and says "what the fuck is this" (compliment)
4. It feels like Sessions' evil twin — same literary DNA, different body
