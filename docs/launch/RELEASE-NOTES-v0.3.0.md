# v0.3.0 — First community contributions and field stories

This release adds the first contributions from outside the original author, plus three real incidents with the guardrails that came out of them.

Highlights:

- Adds workflow card 41, [Agent-Generated Test Review](../../workflows/41-agent-generated-test-review.md), for deciding whether tests an agent wrote actually protect behaviour. Thanks @luohui1 (#14).
- Adds the worked example [Diff review catches agent scope drift](../../examples/agent-scope-drift-caught-by-diff-review.md). Thanks @ogunleyejuliet (#18).
- Adds the failure example [Agent claims tests passed without running them](../../examples/agent-claims-tests-passed.md). Thanks @iamlogesh26-crypto (#17).
- Adds three field-tested stories from running up to ten coding-agent sessions at once:
  - [A guardrail built for one agent became a 90% false alarm at ten](../../examples/field-story-one-guardrail-ten-agents.md)
  - [Eight ways a green test suite proved nothing](../../examples/field-story-tests-that-cannot-fail.md)
  - [When the verification evidence itself was wrong](../../examples/field-story-verification-evidence-lied.md)
- Links every worked example to the workflow cards that prevent its failure.

Want to contribute? Issue #10 is open for more real agent failure stories, and the [curation policy](../curation-policy.md) explains what fits.
