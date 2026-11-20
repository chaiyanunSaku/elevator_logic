# My experiment results

Fill in this template with actual observations. Short bullets are sufficient.

Name / student ID: Chaiyanun Sakulsaowapakkul 6681299

Tool, visible software version and model(s): Claude Code 2.1.329 (terminal, Windows); model Claude Opus 5.5 for coordinator and all three subagents.

Route: Automatic workers

## Agent outputs

| Role | What it delivered | Brief excerpt or screenshot link |
|---|---|---|
| Dispatcher builder | Implemented `choose_elevator` in dispatcher.py only: rules 1–4 from POLICY.md using `rules.eligible_ids`, tie-breaker A by id, reasons naming the rule used. Edited the workspace directly. | "I edited `dispatcher.py` directly in the workspace and changed no other file." [report](screenshots/dispatcher_builder_report.png), [results](screenshots/dispatcher_builder_results.png), [both runs finished](screenshots/both_builders_finished.png) |
| Display builder | Implemented `run_scenarios` in app.py only: shows each scenario, both elevators and the request, calls `choose_elevator` once, prints Selected A/B/WAIT and the reason. Edited the workspace directly. | "I edited app.py directly … and no other file. Both app tests pass." [report](screenshots/display_builder_report.png) |
| Reviewer | No implementation defect and no policy inconsistency. One policy tradeoff in Rule 2: A at 8 moving down with 455 kg, B idle at the caller's floor 5 → A chosen. | "I found no implementation defects and no policy inconsistencies. I raised one concern, a policy tradeoff." [report](screenshots/reviewer_report.png), [concern](screenshots/reviewer_concern.png) |

## Compare with my predictions

Run `python app.py` after adding S6. Compare with the predictions you wrote in POLICY.md before implementation.

| Scenario | Expected selection | Actual selection and reason | Matches my policy? |
|---|---|---|---|
| S1 | A | A, Rule 2: A (moving down at floor 8, 3 floors away) is the only eligible moving car and passes floor 5 going down, so it is chosen. B (idle at floor 4, 1 floor away) is left free for other calls. | Yes |
| S3 | A | A, same Rule 2 reason as S1. | Yes. The reason does not mention A's existing stop at floor 5, because my Rule 2 does not use scheduled stops. |
| S6 | B | B, Rule 2: B (moving up at floor 1, 3 floors away) is the only eligible moving car and passes floor 4 going up, so it is chosen. A (idle at floor 6, 2 floors away) is left free for other calls. | Yes |

- Supplied suite command and actual result: py -m unittest -v, Ran 6 tests, OK.
- One review finding or concern I checked: Rule 2 in `choose_elevator` (policy tradeoff, not a defect). The reviewer tested A moving down from floor 8 with 455 kg and B idle at the caller's floor 5 (0 floors away); my policy picks A. I checked that this follows my written Rule 2 exactly, since Rule 2 does not look at distance or load. My decision: keep the policy.
- Change made, if needed: No code or policy change. I briefly considered adding an exception (choose the idle car if it is already at the caller's floor), but decided to keep my policy because I want it to be consistent: the same rule applies to every call, so the result is predictable, and it matches the tradeoff I already accepted. I accept that this can frustrate a caller who sees an idle elevator at their floor.
- Does my policy serve my stated priority? Yes. In S6 it sends moving B (3 floors away) and keeps the nearer idle A (2 floors away) free, which is exactly my priority. The cost is that the caller waits for a farther car and about 4 passenger-equivalents in B get an extra stop.
- What did I have to coordinate between the agents? Both builders ran at the same time, so the display builder tested app.py while dispatcher.py was still an empty stub; its 4 dispatcher tests errored with NotImplementedError and it checked the display with a temporary fake dispatcher. I had to wait for both to finish, then rerun the full tests and `py app.py` after integration to see the real results.
