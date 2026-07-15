# AGENTS.md — numerical-mooc

Purpose: Project #24 legacy preservation. This repository is classified as `Fork / Education` with `legacy` profile and Advisory enforcement. Do not make unsupported maturity, security, maintenance, or production-readiness claims.

Canonical docs:
- `README.md` root preservation notice
- `docs/ARCHITECTURE.yaml` machine-readable source of truth
- `docs/ARCHITECTURE.md` rationale and maintained-library/revival notes

Provenance and attribution:
- Origin owner: `googa27`; issue: https://github.com/googa27/arxiv-implementation-lab/issues/23
- Upstream/canonical reference: https://github.com/numerical-mooc/numerical-mooc.git
- Preserve history, existing public names, authorship, copyright notices, and file contents. Do not delete, rewrite, or hide inherited material in this preservation change.

Safety boundaries:
- License/provenance: Root LICENSE is MIT; preserve copyright and attribution from upstream course authors.
- Data posture: Educational static notebooks/assets only; upstream policy and asset-level licenses govern reuse.
- Private-data rule: Do not add student records, grades, private forum exports, or restricted course data.
- Security/hardware warning: Notebooks are executable code; run only in isolated environments after inspecting cells and dependencies.

Exact commands:
- Setup: no supported automated setup is declared; treating runtime setup as a revival gate is required.
- Tests: no inherited runtime test suite is claimed; run the architecture checker only.
- Lint/format: no lint/format command is declared.
- Architecture: `python scripts/check_portfolio_architecture.py`

Implementation rules for future work:
- Research upstream/current maintained libraries, standards, datasets, licenses, and security posture before changing runtime code.
- Prefer maintained libraries; custom code must be limited to domain semantics, adapters, composition, or genuinely missing algorithms with oracle/reference tests.
- Avoid invasive refactors of inherited code. Record exact no-growth exceptions and compatibility risks before structural changes.
- Do not introduce generated caches, secrets, private identifiers, restricted data, or fabricated outputs.
- Keep AI-facing contracts deterministic and local. Add Hermes skills for recurring workflows only; plugin/MCP needs stable public contracts, measured multi-client need, least privilege, and separate verification.
- Human/notebook interface: Notebook-first educational use; no forced package, src-layout, or dunder redesign in this preservation pass.
- Core posture: No core coupling.

Revival gates:
- Sync/reconcile with upstream numerical-mooc before changing lessons.
- Pin a teaching environment and verify representative notebooks deterministically.
- Audit third-party media/data asset licenses before redistribution or remix.
- Keep pedagogical code clearly separated from any production numerical library claim.

Definition of done for preservation edits:
- README, AGENTS, `docs/ARCHITECTURE.yaml`, `docs/ARCHITECTURE.md`, and tests agree.
- `python scripts/check_portfolio_architecture.py` passes.
- Only advisory governance files are changed unless a separate reviewed revival task authorizes runtime edits.

### AI-assisted change controls

- Treat agent output as untrusted until a human reviews it and executable repository gates verify it. The human author remains accountable.
- Keep agent changes small, single-purpose, and completely reviewable. Generated tests are not a sufficient sole oracle for generated implementation.
- New dependencies require human approval plus package-existence, maintenance, API, license, vulnerability, and typosquat checks; lock reproducibly.
- Security-sensitive code (authentication, cryptography, parsers, serialization, SQL, filesystem, subprocess, network, permissions, or private data) requires dedicated human review.
- Use least privilege: workspace-scoped writes, network/secret access only when approved, no autonomous merge/deploy, and exact command/result provenance.
- Measure AI impact with lead time, review time, CI failures, reverts, escaped defects, and churn; do not infer productivity from self-report.

### Semantic source-tree hierarchy

- Do **not** balance source folders like AVL/B-trees. Package boundaries follow information hiding, cohesion, coupling, public contracts, ownership, and change patterns; naturally heavy-tailed sizes are expected.
- Empty marker packages and speculative folder scaffolds are forbidden unless an exact, dated structural-role exception exists. Keep future plans in architecture/roadmap documents.
- `__init__.py` is a compatibility/public facade only: imports, re-exports, `__all__`, metadata, and bounded lazy hooks. Domain classes and business functions belong in cohesive modules.
- Severe branch concentration is a review trigger, not a command to redistribute files. Fix it only when dependency, churn, ownership, or comprehension evidence shows a bad boundary.

- AI/hierarchy policy: `python3 scripts/check_ai_hierarchy_policy.py`
