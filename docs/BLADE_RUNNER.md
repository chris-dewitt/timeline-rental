# Blade Runner Tape — v1 Content Guide

**Inspired by.** Not ** copying **. Pastiche multiverse.

---

## What we're capturing (the soul)

- Acid rain, neon, overcrowded future that feels lonely
- Memory as unreliable artifact — photos, dreams, implanted or not
- The question of empathy / humanity — reframed across timelines
- Vangelis-adjacent melancholy — we make our own drones

## What we avoid

- Direct character names in marketing (fine in internal dev docs with care)
- Iconic lines as punchlines ("tears in rain" — no)
- Warner Bros logos, exact Voight-Kampff script
- "Are you a replicant?" as the only twist

---

## v1 playable loop (~15 min)

### Scene 0: Timeline Rental (hub)
- CRT static that almost resolves into a face
- Damaged tape glows on the shelf; clerk one-liners
- Insert tape → intro crawl

### Scene 1: Intro / alley approach
- Title crawl: *a tape that keeps forgetting which ending it had*
- Rain. Neon sign flickers: **"NEXUS REPAIR"**
- Walking right shifts atmospheric beats (puddles → cigarette doorway)
- Blood-neon graffiti easter egg

### Scene 2: The room
- Enter beat: examiner already started
- Table. Photo in superposition. Whiskey glass you can't drink.
- NPC: **The Examiner** — gender ambiguous, calm, unsettling
- Three escalating empathy-test questions (certainty → wasp → phone)

### Scene 3: The photo (observation event)
- Develop sequence — three histories fight for the emulsion
- Interact → **COLLAPSE** (amber flash)
- Photo resolves differently per outcome:
  - **A:** A woman you almost remember
  - **B:** An empty street — you were never in the photo
  - **C:** Your face, wrong angle, wrong smile

### Scene 4: Receipt
- Multiverse return slip prints lost timelines
- Clerk fragment: Ollama one-liner (or curated fallback)
- Rent again or return to the store

---

## Sample original dialogue (curated fallback)

**Examiner:**
> "Describe, in as much detail as you can, the last time you felt certain."

**Examiner (if player hesitates):**
> "Certainty is a luxury. In this city, it's usually rented."

**Collapse narration (timeline B):**
> The photo developed backward. The street was always empty. You were the thing that wasn't supposed to be in frame.

---

## Ollama prompt sketch (`prompts/examiner.txt`)

```
You write dialogue for a noir sci-fi empathy examiner in a Blade Runner-inspired world.
Tone: calm, probing, Philip K. Dick paranoia. Short lines.
Not movie quotes. Original. The player lives in a multiverse — the examiner knows.
Context: {scene_context}
Player last said: {player_choice}
Write one examiner response (2 sentences max).
```

---

## Visual beats

- Rain never stops
- Neon reflects in puddles (simple sprite animation)
- Photo item glitches until observation
- Amber flash on collapse — 3 frames

---

## Connection to Superposition Sessions

Shared literary voice (`docs/VOICE.md` in both repos). Easter egg idea: a collapsed session title appears as graffiti in the alley in a later week.
