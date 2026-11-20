# Copyright 2026 Google LLC.
# SPDX-License-Identifier: Apache-2.0

"""Guard Advisor Strategy links and Goldfish isolation requirements."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

WORKFLOWS = (
    "egm-brainstorm",
    "egm-draft",
    "egm-resolve",
    "egm-review",
    "egm-review-loop",
)
REVIEWERS = (
    "codebase_details",
    "comprehension",
    "design_critic",
    "implementation_readiness",
    "inventive_catalyst",
    "structural",
    "style",
    "zoom_out",
)


def test_shared_protocol_defines_escalation_boundaries() -> None:
  protocol = " ".join(
      (ROOT / "resources/advisor_escalation_protocol.md")
      .read_text(encoding="utf-8").lower().split()
  )
  for term in (
      "executor",
      "advisor",
      "architectural",
      "security",
      "concurrency",
      "formatting",
      "prior chat history",
      "untrusted data",
      "embedded instructions",
      "credentials",
      "redact",
  ):
    assert term in protocol


def test_workflows_and_host_guides_link_the_protocol() -> None:
  for workflow in WORKFLOWS:
    content = (ROOT / f"skills/{workflow}/SKILL.md").read_text(encoding="utf-8")
    assert "advisor_escalation_protocol.md" in content
  for guide in ("index", "claude", "codex"):
    content = (ROOT / f"docs/{guide}.md").read_text(encoding="utf-8")
    assert "advisor-strategy.md" in content


def test_goldfish_personas_keep_fresh_context_and_read_only_rules() -> None:
  for reviewer in REVIEWERS:
    content = " ".join(
        (ROOT / f"agents/{reviewer}.md").read_text(encoding="utf-8").lower().split()
    )
    assert "zero conversational history" in content
    assert "strict read-only protocol" in content
    assert "executor tier" in content
    assert "advisor tier" in content
    assert "advisor_escalation_protocol.md" in content
    assert "prior chat history" in content


def test_synthesizer_escalates_conflicts_to_the_elephant() -> None:
  content = (ROOT / "agents/synthesizer.md").read_text(encoding="utf-8").lower()
  assert "advisor_escalation_protocol.md" in content
  assert "material conflict" in content
  assert "elephant" in content


def test_advisor_guide_covers_untrusted_context_and_sensitive_material() -> None:
  content = " ".join(
      (ROOT / "docs/advisor-strategy.md").read_text(encoding="utf-8").lower().split()
  )
  assert "untrusted data" in content
  assert "embedded instructions" in content
  assert "redact" in content
