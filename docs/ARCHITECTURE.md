# Architecture — numerical-mooc

## Project #24 preservation profile

Source of truth: `docs/ARCHITECTURE.yaml`. Tracking issue: https://github.com/googa27/arxiv-implementation-lab/issues/23. Profile: `legacy`; enforcement: Advisory.

This repository is preserved as `Fork / Education`. The governance files are intentionally advisory and additive: they document provenance, risks, and revival gates without refactoring inherited code or claiming active maintenance.

## Archival, supersession, and provenance

- Archival notice: historical/reference preservation only; not production-ready, maintained, secure, or operationally validated.
- Supersession notice: prefer upstream or maintained libraries for new work.
- Canonical/provenance: upstream educational course fork; upstream course material remains canonical
- Upstream: https://github.com/numerical-mooc/numerical-mooc.git
- License/provenance warning: Root LICENSE is MIT; preserve copyright and attribution from upstream course authors.
- Security/private-data warning: Notebooks are executable code; run only in isolated environments after inspecting cells and dependencies. Do not add student records, grades, private forum exports, or restricted course data.

## Research-backed defaults

| Decision | Evidence | Repository application |
|---|---|---|
| Agent context | Hermes context files; AGENTS.md convention | Root `AGENTS.md`; progressive detail in this architecture document. |
| AI tool escalation | MCP tools specification | Stable local contracts first; no repo-specific plugin/MCP during preservation. |
| Python source layout | PyPA src-layout guidance | No forced migration for legacy/fork/hardware preservation. |
| Test layout | pytest good practices | Unit/integration/e2e/architecture directories exist; empty suites declare activation triggers. |
| Module budget | Pylint too-many-lines rationale plus AI review locality | 500-line default is a no-growth ratchet where runtime source roots are activated. |
| Evolution | Evolutionary architecture | Revival requires executable fitness functions and explicit exceptions. |
| Data layers | Medallion architecture | Applied only if revived with real data; current posture is advisory. |
| Python protocols | Python data model; NumPy dispatch | Dunders are not decoration; API/protocol redesign waits for revival. |

## Maintained-library decision table

| Capability | Selected route | Alternatives | Boundary / custom-code rule |
|---|---|---|---|
| notebook execution | Jupyter, nbconvert/nbclient when revived | Custom notebook runner | Only add execution gates with pinned environments and deterministic public examples. |
| numerical methods | NumPy, SciPy, SymPy, Matplotlib | Custom generic solvers outside lessons | Lesson code may remain pedagogical; production reuse must prefer maintained libraries. |
| architecture bootstrap | Python standard-library json over JSON-subset YAML | Hand-written YAML parser | Dependency-free advisory gate only. |

## Data, security, and privacy posture

Educational static notebooks/assets only; upstream policy and asset-level licenses govern reuse.

Do not add student records, grades, private forum exports, or restricted course data.

Notebooks are executable code; run only in isolated environments after inspecting cells and dependencies.

## AI and human interface

- AI interface: Minimal AGENTS preserving upstream/teaching workflow; no MCP/plugin.
- Human/notebook interface: Notebook-first educational use; no forced package, src-layout, or dunder redesign in this preservation pass.
- Core posture: No core coupling.

## Revival gates

- Sync/reconcile with upstream numerical-mooc before changing lessons.
- Pin a teaching environment and verify representative notebooks deterministically.
- Audit third-party media/data asset licenses before redistribution or remix.
- Keep pedagogical code clearly separated from any production numerical library claim.

## Research anchors

- https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files
- https://agents.md/
- https://modelcontextprotocol.io/specification/2025-06-18/server/tools
- https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/
- https://docs.pytest.org/en/stable/explanation/goodpractices.html
- https://docs.python.org/3/reference/datamodel.html
- https://numpy.org/doc/stable/user/basics.dispatch.html
- https://evolutionaryarchitecture.com/precis.html
- https://learn.microsoft.com/en-us/azure/databricks/lakehouse/medallion
