# Multi Small Loop Skill (MSLK)

A Codex skill for running one project as fixed parallel Chains that advance through
ordered, fully synchronized Levels.

Canonical repository: `DWG7318/multi-small-loop-skill`
Current version: **1.9.0**

## Definition first

Every run starts from a frozen full or Minimum Calabash:

```text
Grandpa → Product Architecture → Ontology
```

If none exists, Supervisor establishes Minimum Calabash from authoritative Owner
intent and project evidence before MSLK planning. Every GO traces to this baseline,
and every Verification Contract is derived from that trace.

## Multi-chain topology

```text
              CHAIN-A      CHAIN-B      CHAIN-C      CHAIN-D
LEVEL-01      GO-01-A      GO-01-B      GO-01-C      GO-01-D
                 ↓            ↓            ↓            ↓
             Verification Verification Verification Verification
                 └────────── full Level barrier ──────────┘
                                  ↓
LEVEL-02      GO-02-A      GO-02-B      GO-02-C      GO-02-D
```

The number means “same synchronization Level”; the suffix identifies the persistent
Chain. `GO-01-A` is a real GO. `GO-01` alone is not.

Every GO in the current Level can start together and is independently verified. The
next Level remains closed until every required current-Level GO is `GO_VERIFIED`.

## Roles

- **Supervisor** — Calabash, method selection, fixed Chain/Level plan, provisioning,
  autonomy envelope, deterministic Level barriers, Owner-exclusive escalation, and
  final composition audit.
- **Checker** — one Chain's GO/CELL planning, CELL validation, detection, routing,
  and direct GO handoff.
- **Worker** — one bounded CELL or product-rework round at a time.
- **Verification** — one fresh isolated attempt for one immutable GO candidate; it
  independently returns the GO evidence verdict.

At Level activation, Supervisor establishes every GO's Verification before the
first CELL. After all CELLs pass, Checker sends the frozen candidate directly to
Verification. Verification sends its signed verdict directly to Checker and
Supervisor; Supervisor is not a relay.

## Owner-free execution

A frozen `PROJECT_AUTONOMY_ENVELOPE` authorizes routine work without per-CELL,
per-GO, or per-Level Owner confirmation. Only an irreducible Owner-exclusive
product-definition, credential, legal, destructive, irreversible, materially
costly, physical, or external-account matter may reach Owner.

## Key 1.9.0 changes

- Mandatory full/Minimum Calabash and `GO_CALABASH_TRACE`.
- Fixed `LEVEL` and `CHAIN` structure with `GO-<LEVEL>-<CHAIN>` IDs.
- Full Level barriers; no partial unlock.
- Verification pre-binding, pre-establishment, direct Checker handoff, and direct
  signed verdict.
- Strong Checker/Verification environment and context isolation.
- Worker-owned product rework; no Checker self-repair/self-acceptance.
- No cross-GO CELL dependency or same-Level peer dependency.
- Detection tiers: `CELL_ALWAYS`, `CELL_TRIGGERED`, `GO_BOUNDARY`, `PROJECT_FINAL`.
- Routine Owner authorization forbidden inside the autonomy envelope.
- Optional project objective renamed `PROJECT_GOAL`.

## MSLK versus GLK

MSLK is staged, barrier-synchronized multi-chain execution. It does not implement
conditional branches, partial downstream unlock, cycles, arbitrary runtime routing,
dynamic Chains, or Grapher. Those capabilities belong to Graph Loop Skill (GLK).

## Install

Install `multi-small-loop-skill/` in the Codex skills directory and invoke:

```text
$multi-small-loop-skill
```

Formal work requires Calabash freeze, 25/25 role readiness, simulation, isolated
environments, pre-established Verification, autonomy, evidence, and Level gates.

## License

MIT.
