# Third-Party Notices

Agent Studio (this repository) is MIT-licensed; see [`LICENSE`](LICENSE)
(© 2026 Noah Raford). That license is unchanged. This file records third-party
material adapted into Agent Studio and its separate copyright and license.

## Agent Designer

Some of Agent Studio's durable-team machinery is **adapted with attribution** from
Agent Designer, a Pi skill for designing expert ensembles.

- Project: Agent Designer
- Version: v0.2.0
- Upstream: https://github.com/dbmcco/agent-designer
- Reviewed source commit: `5b365c451d88542ac0cb9c8f21d108073dfad7a1` (2026-08-24)
- License: MIT — © 2026 Braydon McCormick

### What was adapted

Concepts and structure — not verbatim files — were adapted from Agent Designer,
then rewritten to fit Agent Studio's evidence-first lifecycle and voice:

- `methodologies/kernel.md` — the versioned methodology kernel (the ten operating
  rules), adapted from Agent Designer's `methodologies/kernel.md`. Rule 1 is
  changed to Agent Studio's middle-path form.
- `methodologies/overlays/{scenario-planning,terrain-mapping,root-cause}.md` —
  adapted from Agent Designer's overlays and **rewritten to be staff-neutral**
  (no pre-staffed personas; no overlay guarantees a specialist).
- `templates/team.json.md` and `templates/team-readme.md` — the manifest and
  README shapes, adapted from Agent Designer's `panel.json` / panel-readme
  templates and generalized from panels to teams.
- `scripts/team_validate.py` — a structural validator in the spirit of Agent
  Designer's `validate-persona.sh` / `verify-bundle.sh`, reimplemented in Python
  for team packages.

### What is new Agent Studio policy (not from Agent Designer)

The evidence gate, the persona evidence families, the three-layer persona
contract, the persona mode switch and its caricature probe, the durability gate,
the Team Charter's separation of organization approval from candidate approval,
the promotion lifecycle, and the roster/rehire model are Agent Studio's own and
are not derived from Agent Designer.

### Upstream MIT license (reproduced verbatim)

```
MIT License

Copyright (c) 2026 Braydon McCormick

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
