# Advisor Strategy Implementation Plan

## Goal

Define model-tier escalation across EGM's interactive and review workflows,
distribute the policy to supported runtimes, and document host-dependent
configuration without claiming the plugin chooses models.

## Architecture

One shared resource owns executor/advisor responsibilities, escalation
triggers, guardrails, and context boundaries. Canonical skills and reviewer
personas link to that policy; Claude and Codex guides explain platform detection
and capability-dependent routing. The packer requires the resource, and the
Claude distribution is regenerated from source.

## Tech Stack

Markdown instructions and docs, Python packaging script, pytest, YAML
frontmatter validation.

## Slice: advisor-integration

**Interfaces**

- `resources/advisor_escalation_protocol.md` is the canonical runtime policy.
- `docs/advisor-strategy.md` explains operation and host configuration.
- Existing skills and personas link to the shared policy without changing
  plugin model selection or Goldfish isolation.

**Dependencies:** None.

**PR policy:** `batched`.

### Task 1: Integrate Advisor Strategy

1. Add failing unit coverage for policy links, required package inclusion, and
   stateless reviewer constraints.
2. Add and document the shared protocol. Require it in
   `scripts/pack_plugin.py` and verify the runtime archive contains it.
3. Update `egm-brainstorm`, `egm-draft`, `egm-resolve`, `egm-review`, and
   `egm-review-loop` instructions to apply the protocol.
4. Update all reviewer personas plus the synthesizer for tier-aware routing.
   Keep each Goldfish fresh-context, read-only, and free of prior chat history;
   let the synthesizer return material conflicts to the active Elephant.
5. Add host pairing and model-neutral plugin guidance to
   `docs/advisor-strategy.md`; link it from `docs/index.md`, `docs/claude.md`,
   and `docs/codex.md`.
6. Regenerate `distributions/claude/` using `scripts/pack_plugin.py` and verify
   it matches canonical sources.
7. Run `pytest tests/unit` and address failures.

## Acceptance Criteria

- Shared protocol defines routine executor work, advisor triggers, explicit
  anti-escalation, bounded decision context, and unavailable-capability
  behavior.
- All five requested workflows reference the protocol and route only
  high-leverage decisions to advisor-capable paths.
- Reviewer definitions preserve stateless, read-only behavior; ordinary
  clarity/completeness checks stay on the executor tier.
- Claude and Codex guides explain capability detection and host-owned model
  selection. Manifests remain model-neutral.
- Unit checks cover policy references, package inclusion, and reviewer
  statelessness.
- The generated Claude runtime matches the packer's output.
- The offline unit suite passes.
