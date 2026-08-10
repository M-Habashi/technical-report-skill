# Agent contribution guide

This repository packages one installable Codex skill under `skills/build-technical-report`.

## Source of truth

- Treat `skills/build-technical-report/assets/report-template` as the canonical template.
- Keep the root `README.md` focused on installation and discovery; put build instructions in `SKILL.md` and focused details in `references/`.
- Do not duplicate the template elsewhere in the repository.

## Editing workflow

1. Read `skills/build-technical-report/SKILL.md`.
2. Read only the reference file routed by that skill for the component being changed.
3. Keep article markup, behavior, configuration, and styling in their existing component directories.
4. Preserve demo labels until all example values have been replaced with project evidence.
5. Run both validators after changing the package:

   ```powershell
   python skills/build-technical-report/scripts/validate_report.py skills/build-technical-report/assets/report-template
   python <skill-creator-path>/scripts/quick_validate.py skills/build-technical-report
   ```

6. Serve the template over HTTP and verify article navigation, hashes, below-header scrollbar and hover state, slider, legend, zoom, Reset, console, mobile layout, 200% text reflow, and print output—including heading contrast on the light page.
7. Refresh `docs/technical-report-preview.png` after material visual changes.

These repository checks apply to development of the canonical package and template. Reports created with the skill follow the first-build-only verification cadence in `SKILL.md`.

## Constraints

- Keep the template dependency-free and runnable without a build step.
- Use `pnpm` if JavaScript tooling is ever introduced.
- Do not turn `index.html` into a monolith; articles belong in `components/` and in the registry.
- Preserve accessibility labels, reduced-motion behavior, print styles, and the no-horizontal-overflow mobile layout.
- Avoid gradients, glass effects, decorative shadows, excessive cards, and ornamental animation.
