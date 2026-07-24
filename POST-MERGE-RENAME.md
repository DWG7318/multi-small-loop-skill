# Post-Merge GitHub Rename

1. Merge `feat/clk-2.0.0` into `main` in `DWG7318/multi-small-loop-skill`.
2. In repository Settings → General, rename repository to `chain-loop-skill`.
3. Confirm repository ID remains `1298120736`, default branch is `main`, and old URL
   redirects.
4. Update description, topics, branch protections, GitHub App selection/indexing,
   release automation, badges, and any external links.
5. Create annotated tag `v2.0.0` only after post-rename tests pass.
6. Update Calabash and GLK references from MSLK to CLK in separate versioned PRs.
7. Reinstall the Codex skill under `chain-loop-skill/`; URL redirect does not rename
   local installations.
