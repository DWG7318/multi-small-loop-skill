# Migration From MSLK to CLK

## Canonical rename

```text
Multi Small Loop Skill → Chain Loop Skill
MSLK                  → CLK
$multi-small-loop-skill → $chain-loop-skill
multi-small-loop-skill/ → chain-loop-skill/
MSLK_* receipts       → CLK_* receipts
MSLK START            → CLK START
```

The method remains a staged, full-barrier multi-chain method. The rename makes the
Chain identity explicit and distinguishes it from SLK and GLK.

## Historical runs

Never rewrite an active or completed MSLK evidence chain. A historical run keeps its
version, folder, receipt prefixes, IDs, and verdicts.

To migrate unfinished work:

1. freeze the last valid MSLK state and evidence index;
2. create a new CLK plan/version and append-only ID mapping;
3. install `chain-loop-skill/`;
4. generate fresh CLK readiness receipts and simulation;
5. bind fresh or explicitly migrated roles/environments;
6. preserve historical candidates and verdicts;
7. resume only from a verified safe boundary.

## Repository rename

After the 2.0.0 PR is merged, rename the GitHub repository:

```text
DWG7318/multi-small-loop-skill
→ DWG7318/chain-loop-skill
```

GitHub normally redirects the old repository URL, but local remotes and installed
skill folders must be updated explicitly.

```bash
git remote set-url origin https://github.com/DWG7318/chain-loop-skill.git
```
