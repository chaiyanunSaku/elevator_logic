# My dispatch policy

Fill in this template yourself before asking the builders to implement it. Short bullets and a small table are enough. You may discuss ideas or ask AI to challenge them, but make and explain your own choices.

## Priorities

- What I prioritise: Use the elevator that's already moving and keep the idle one free, so the idle car stays available for calls in the other direction. Floor distance and keeping a car free are proxies, not measured waiting time or energy.
- My exact selection rule: 1. If no elevator is eligible, WAIT. 2. If exactly one eligible elevator is moving, choose it. 3. If both are moving and eligible, choose the one with fewer floors from the caller. 4. If no eligible elevator is moving, choose the eligible one with fewer floors from the caller.
- My deterministic tie-breaker: If the distances are equal, choose elevator A.
- A tradeoff I accept: People already in the moving elevator get an extra stop at the caller's floor, no matter how full the car is. The caller may wait longer than if the nearer idle car came. The benefit is that the idle elevator is not started.

## Predictions before implementation

Use S1, one of S2/S3, and one valid scenario you create in scenarios.py. For your own case, change something meaningful: location, direction, load or scheduled stops. Name it S6.

| Scenario | My expected selection | Why it follows my policy | Benefit and cost / who is affected |
|---|---|---|---|
| S1 | A | A is moving down from 8 and passes floor 5 on its way to 1. 130 + 65 = 195 <= 520, so it's eligible. B is idle. Rule 2: exactly one eligible car is moving, so choose A  | Benefit: B is not started. Cost: about 2 passenger-equivalents in A get an extra stop at 5, and the caller waits for A to travel 3 floors instead of B's 1. |
| S3 | A | A is moving down and already has a scheduled stop at floor 5. It's eligible (195 <= 520). Rule 2: exactly one eligible car is moving, so choose A | Benefit: B is not started and A adds no extra stop, because it was stopping at 5 anyway. Cost: the caller still waits for A to come 3 floors, and boarding might hold A slightly longer. |
| S6: my scenario | B | B is moving up from floor 1 to 7 and passes floor 4. 260 + 65 = 325 ≤ 520, so it's eligible. A is idle and also eligible. Rule 2: exactly one eligible car is moving, so choose B, even though A is closer. | Benefit: A is not started and stays free for calls in the other direction. Cost: the caller waits for B to travel 3 floors instead of A's 2, and about 4 passenger-equivalents in B get an extra stop at floor 4. |

## Another defensible policy

- An alternative priority: Protect the people already aboard: don't add stops to a moving car unless it already has a scheduled stop at the caller's floor. Otherwise send the idle car. The benefit is that passengers aboard are not delayed; the cost is that the idle car is started more often.
- A scenario where it could choose differently, and why: In S6, B is moving up from 1 to 7 with no scheduled stop at floor 4. The alternative picks A (idle), so about 4 passenger-equivalents in B ride straight to 7 without an extra stop. My policy picks B to keep A free. In S3 both policies choose A, because A already stops at floor 5, so no extra stop is added.

If your predicted choices contradict your general rule, resolve that before implementation. If review later changes your mind, note the revision in EVIDENCE.md and update the policy and code together.
