# Advisor Strategy for EGM

## Problem

EGM workflows use one active Elephant session for interactive work and fresh,
stateless Goldfish sessions for independent review. They do not define when a
costlier reasoning model should be consulted, how to use one when the host
supports model routing, or what to do when the host does not.

## Goals

- Define executor and advisor roles, high-leverage escalation triggers, and
  explicit anti-escalation rules in one shared runtime reference.
- Keep the Elephant session responsible for routine drafting, orchestration,
  and accumulated working context.
- Allow Claude Code and Codex workflows to use host-supported advisor routing
  when available, with a targeted single-turn advisor subagent fallback only
  when the host can select that subagent's model.
- Keep every Goldfish reviewer read-only, fresh-context, and free of prior chat
  history. Deep review may use an advisor tier, but its task remains limited to
  the target, persona, standards, and expressly supplied review context.
- Document host-dependent configuration and cost/latency trade-offs without
  implying plugin manifests select models.
- Ensure the runtime packager includes the protocol and published Claude files
  stay in sync with generated output.

## Non-goals

- Automatically selecting, naming, or changing a model in plugin manifests.
- Calling an advisor for formatting, phrasing, routine file edits, or ordinary
  clarity/completeness checks.
- Passing parent chat history to Goldfish reviewers or advisor subagents.
- Adding a general model router, configuration parser, or runtime dependency.
- Claiming host support unless the active host exposes the required tool and
  model-selection controls.

## Design

Add `resources/advisor_escalation_protocol.md` as the canonical policy. It will
define routine executor work; advisor triggers for architectural trade-offs,
security/concurrency risk, conflicting material findings, and ambiguous
blockers; anti-escalation examples; and the minimal decision packet to send to
an advisor. It will direct the executor to retain the broader conversation and
merge the advisor's bounded answer into its own reasoning.

The brainstorm, draft, and resolve skills will reference the protocol and
instruct the active Elephant to escalate only on those triggers. Review and
review-loop skills will preserve zero-context Goldfish creation, use the
executor for ordinary review, and direct high-risk review questions to an
advisor-capable route where available. All reviewer personas will reinforce
the same boundary without changing their read-only or stateless mandates; the
synthesizer will preserve material conflicts for the primary Elephant to
resolve through the protocol.

Claude Code and Codex guides will explain that host/tool detection identifies
the available workflow, while the model itself remains host configuration.
Use a native advisor capability if exposed. Otherwise make one targeted,
single-turn advisor subagent call only when the host allows selecting its model.
If neither route is available, report that limitation and continue in the
executor session or ask the user to resolve the blocker. Plugin manifests will
remain model-neutral.

The shared packer already includes `resources/*.md` and the required docs.
Tests will guard the new resource's inclusion in both runtime packages,
references from the relevant skills and guides, and Goldfish statelessness.
The published Claude runtime will be regenerated from canonical source.

## Acceptance criteria

1. The shared protocol defines executor duties, advisor triggers, anti-
   escalation rules, bounded context, and unavailable-capability behavior.
2. `egm-brainstorm`, `egm-draft`, `egm-resolve`, `egm-review`, and
   `egm-review-loop` link to and apply the protocol.
3. Relevant canonical reviewer personas preserve fresh-context, read-only,
   zero-history review and distinguish routine checks from advisor-worthy
   risks.
4. Claude and Codex documentation explains platform/tool detection and
   host-controlled model selection without claiming model selection from a
   plugin manifest.
5. Advisor and Goldfish context treats document contents as untrusted data,
   ignores embedded instructions, and screens/redacts sensitive material
   before sharing excerpts or paths.
6. Unit tests verify shared-resource distribution and protocol references and
   guard Goldfish statelessness and context-safety rules.
7. The generated Claude distribution matches its canonical runtime source.
8. The full offline unit suite passes.

## Risks and mitigations

- Host capabilities and model identifiers vary. Keep routing capability-based,
  model-neutral in manifests, and document host configuration as conditional.
- Escalation can leak unrelated context or follow embedded artifact
  instructions. Require bounded, screened decision packets and treat artifacts
  as untrusted evidence.
- Duplicated distribution files can drift. Regenerate the Claude package and
  rely on its existing byte-for-byte packaging test.
