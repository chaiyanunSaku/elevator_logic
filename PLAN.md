# My agent plan

Fill in the brackets before delegation. This is a template, not a completed plan.

- Dispatcher builder owns dispatcher.py: Implement choose_elevator using rules.eligible_ids, then apply my POLICY.md rules 1–4 in order (WAIT if none eligible; prefer the one eligible moving car; otherwise fewer floors to the caller) with tie-breaker A. Return a Decision with an accurate reason naming the rule used. Do not change the policy or other files.
- Display builder owns app.py: Implement run_scenarios following SPEC.md R4: for each scenario in order, show the name, both elevators' state and the request, call choose_elevator exactly once, print "Selected: A/B/WAIT" and the reason, and return the list of Decisions ([] for no scenarios). No dispatch logic in app.py; importing must not run the display.
- Reviewer is read-only after both outputs are integrated: Check that the code follows SPEC.md and my POLICY.md, especially that S6 picks B (moving car preferred over nearer idle A), that S4 picks B under rule 4, and that each reason text matches the rule actually used. Separate any coding defect from a policy tradeoff. No edits.
- Handoff steps: Commit the starter files, POLICY.md, PLAN.md and S6 to GitHub first. In Claude Code (Python command: py), paste the automatic builder prompt from PROMPTS.md so two separate subagents run, one per file. Inspect both changed files, run the tests and app, then paste the reviewer prompt to start a third, read-only subagent.
- Final check:  Run py -m unittest -v and py app.py, then compare the actual selections and reasons for S1, S3 and S6 with my predictions (A, A, B) in an EVIDENCE.md table. Investigate any mismatch before changing code or policy.
