---
description: Keep participant procedures, real UI images, architecture diagrams, and editable sources consistent.
applyTo: "**/*.md,docs/diagrams/**,docs/images/**"
---

# Documentation and image changes

- Follow the [shared instructions](../copilot-instructions.md) for audience,
  language, and placement. See
  [change targets and checks](../../docs/development/README.md#change-targets-and-checks)
  for related prose, diagrams, screenshots, and Notebook updates.
- Participant procedures must state the starting state, input sources/defaults,
  actions, and success checks. Do not leave undefined inputs with only "ask the
  administrator"; focus explanation on difficult settings. Put implementation
  details and exception handling in existing developer/administrator guides.
- Verify product support against current primary sources and target versions.
  A successful model deployment does not establish support for all IQ, evaluation,
  optimization, and Hosted uses. Label unverified uses and refer to existing
  sources of truth for pinned values.
- Use real UI captures for operating instructions, never generated mock screenshots.
  Keep official UI labels and input explanations in prose as well; images alone
  must not be required to complete the procedure.
- Limit emphasis to red boxes around confusing inputs/settings. Avoid unnecessary
  red numbering or revealing answers. Check cropped boxes, text clipping, and
  correspondence with prose after processing. Opaquely mask credentials and
  personal or live environment identifiers.
- Record capture sources and processing in
  [image and icon attribution](../../docs/images/ATTRIBUTION.md) when adding or
  replacing images. Historical examples and official sample images are not proof
  of success at the current revision. Do not relabel Japanese or obsolete captures
  as current English results.
- Follow [editing architecture diagrams](../../docs/development/architecture.md#editing-architecture-diagrams).
  Compare with implementation and Labs; update editable source, PowerPoint, PNG,
  and prose together. Do not overwrite manual PowerPoint edits with stale JSON
  or use historical diagrams to regenerate the current design.
- Distinguish logical boundaries, communication paths, processing order, ownership,
  and creation time. A runtime or feature omitted from a diagram is not necessarily
  removed from the core workshop. Check published images and editable files
  separately; preview rendering gaps do not prove data loss.
- Distinguish document link/structure checks from participant-path verification.
  Follow the [instructor runbook](../../instructor/runbook.md#real-environment-validation-scope)
  for end-to-end scope, interruption, and completion.
