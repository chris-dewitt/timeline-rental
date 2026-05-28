# Quantum Mechanics — Timeline Rental

How multiverse branching works under the hood.

---

## Core metaphor

| Quantum | Game |
|---------|------|
| Superposition | Multiple outcomes still possible |
| Amplitude | How likely each outcome is (hidden until collapse) |
| Measurement / observation | Player triggers collapse — one timeline wins |
| Entanglement (Week 4) | Choice in one run affects next run |

---

## v1 collapse flow

```
Player makes choices
        ↓
Choices update quantum circuit parameters (not immediate branch)
        ↓
Player hits OBSERVATION event
        ↓
Qiskit circuit runs → measured bitstring
        ↓
Bitstring maps to pre-authored outcome bundle (narration + state)
        ↓
Other outcomes marked LOST in receipt
```

---

## v1 circuit

3 qubits = up to 8 outcome buckets. v1 uses 3–4 active outcomes.

```python
# Pseudocode
def collapse_timeline(choice_history: list[int], seed: int) -> int:
    qc = QuantumCircuit(3, 3)

    # Player choices bias which gates fire
    for i, choice in enumerate(choice_history):
        if choice == 1:
            qc.x(i % 3)  # flip based on player

    qc.h([0, 1, 2])      # superposition
    qc.measure([0, 1, 2], [0, 1, 2])

    counts = run_sim(qc, shots=1024, seed=seed)
    return outcome_from_counts(counts)
```

---

## Outcome bundles

Pre-write 3–4 collapse outcomes per observation event. Quantum picks which bundle activates.

Each bundle contains:
- `narration`: collapse description
- `world_state`: flags for future runs
- `receipt_line`: one-liner for return slip
- `lost_timelines`: text for the paths that died

LLM can *embellish* bundles — not invent outcomes from scratch (keeps quality control).

---

## Entanglement (Week 4)

Bell pair between "session qubit" and "tape qubit":
- Run 1 collapse affects Run 2's initial bias
- Narratively: *"The store remembers you. Or a version of you."*

---

## Agent rule

Same as Sessions: Qiskit simulators for collapse. Player should feel uncertainty — backend should be real.
