# Chain Loop Skill (CLK)

A Codex skill for one project executed as fixed persistent Chains that advance
through ordered, fully synchronized Levels.

Canonical repository target: `DWG7318/chain-loop-skill`

Legacy repository before rename: `DWG7318/multi-small-loop-skill`

Current version: **2.0.0**

## Definition first

Every run starts from Full Calabash or Minimum Calabash:

```text
Grandpa → Product Architecture → Ontology
```

If absent, Supervisor establishes Minimum Calabash before Chain/Level planning.
Every real GO has `GO_CALABASH_TRACE` and a derived Verification Contract.

## Chain topology

```text
              CHAIN-A      CHAIN-B      CHAIN-C      CHAIN-D
LEVEL-01      GO-01-A      GO-01-B      GO-01-C      GO-01-D
                 ↓            ↓            ↓            ↓
             Verification Verification Verification Verification
                 └────────── full Level barrier ──────────┘
                                  ↓
LEVEL-02      GO-02-A      GO-02-B      GO-02-C      GO-02-D
```

The number means one synchronization Level; the suffix identifies a persistent
Chain. The next Level opens only after every required current-Level GO is
`GO_VERIFIED`.

## Roles

- Supervisor: Calabash, fixed Chain/Level plan, provisioning, autonomy, barriers,
  Owner-exclusive escalation, and final composition.
- Checker: one Chain's GO/CELL plan, CELL validation, detection, routing, and direct
  GO handoff.
- Worker: one CELL or product-rework round at a time.
- Verification: one fresh isolated GO-verdict attempt for one immutable candidate.

## Legacy naming

`CLK`, `Chain Loop Skill`, and `$chain-loop-skill` are canonical. `MSLK`,
`Multi Small Loop Skill`, and `$multi-small-loop-skill` are migration terms only.
Historical runs keep their historical identity; new runs do not.

## CLK versus GLK

CLK is fixed multi-chain execution with ordered Levels and full barriers. It has no
Grapher, conditional branch, partial unlock, cycle, dynamic Chain, or arbitrary GO
routing. Those belong to Graph Loop Skill (GLK).

## Install

Install `chain-loop-skill/` and invoke:

```text
$chain-loop-skill
```

## License

MIT.
