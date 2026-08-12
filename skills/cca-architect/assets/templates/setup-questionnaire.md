# Setup questionnaire — [WORKSPACE NAME]

> One-time onboarding. Configure the factory, not the product. Ask everything
> at once, in one pass. Use sensible defaults/examples, derive fields that can
> be inferred from other answers, and do not re-ask these questions on later
> runs.

1. What is this workspace called, and what does it repeatedly produce, maintain, or help you do? Example: "Weekly market brief" or "Product knowledge workspace".
2. Who reviews or uses its output, and what matters most to them? If there is no recurring reviewer, say so.
3. Paste 2–3 examples of output you consider good, if voice/style matters. The agent should derive concrete patterns from examples rather than ask for adjective-only descriptions.
4. What must the workspace never do? Include hard constraints, forbidden actions, or output patterns.
5. What stable formats, lengths, structures, citation rules, naming rules, or quality requirements should apply across runs?
6. If this workspace maintains knowledge, what recurring entities/concepts matter and where does durable source material come from? Skip if not applicable.
7. Walk through one representative run from start to finish. What distinct artifacts are produced, and where should a human review or redirect before the next step continues?
8. Which parts are deterministic enough for scripts or normal tooling rather than an agent?
9. Which external/system tools are required across runs? For each required tool, note whether it is already installed. Optional tools should remain optional and should not create mandatory stages.
10. Which agent runtimes or editors will operate this workspace? Record only what is needed to verify their current native instruction surfaces; do not assume adapter filenames from a static list.
11. What defaults should apply when a future run omits non-critical choices? Derive any defaults already implied by earlier answers rather than asking twice.

After collecting answers, populate the workspace's stable configuration/reference files, verify every setup placeholder is covered, and confirm no orphaned questionnaire answers or unresolved placeholders remain.
