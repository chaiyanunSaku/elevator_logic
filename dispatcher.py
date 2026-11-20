"""Builder 1 implements the student's policy here."""
from models import Elevator, Request, Decision
from rules import eligible_ids

TIE_BREAK_ID = "A"  # POLICY.md: if distances are equal, choose elevator A


def _distance(elevator: Elevator, request: Request) -> int:
    """Floors between the car and the caller (a proxy, not measured waiting time)."""
    return abs(elevator.floor - request.floor)


def _nearest(cars: list[Elevator], request: Request) -> tuple[Elevator, bool]:
    """Return the car with fewest floors to the caller and whether a tie was broken.

    Ties are resolved deterministically in favour of elevator A (POLICY.md).
    """
    best = min(_distance(car, request) for car in cars)
    closest = [car for car in cars if _distance(car, request) == best]
    if len(closest) == 1:
        return closest[0], False
    for car in closest:
        if car.id == TIE_BREAK_ID:
            return car, True
    return min(closest, key=lambda car: car.id), True


def _describe(car: Elevator, request: Request) -> str:
    state = "idle" if car.direction == "idle" else f"moving {car.direction}"
    return f"{car.id} ({state} at floor {car.floor}, {_distance(car, request)} floor(s) away)"


def _ineligible_note(elevators, eligible: list[str]) -> str:
    others = [car.id for car in elevators if car.id not in eligible]
    if not others:
        return ""
    names = " and ".join(others)
    return (f" {names} {'is' if len(others) == 1 else 'are'} not eligible "
            "(over capacity with the caller, or not passing this floor in the requested direction).")


def choose_elevator(elevators: tuple[Elevator, Elevator], request: Request) -> Decision:
    """Choose one eligible elevator according to POLICY.md; never mutate inputs."""
    eligible = eligible_ids(elevators, request)
    candidates = [car for car in elevators if car.id in eligible]

    # Rule 1: no eligible elevator -> WAIT (defer the assignment).
    if not candidates:
        return Decision(None, (
            f"Rule 1: no elevator is eligible for the {request.direction} call at floor "
            f"{request.floor} (each is over capacity with the caller or not passing this "
            "floor in the requested direction), so the assignment is deferred."
        ))

    note = _ineligible_note(elevators, eligible)
    moving = [car for car in candidates if car.direction != "idle"]
    idle = [car for car in candidates if car.direction == "idle"]

    # Rule 2: exactly one eligible elevator is moving -> choose it.
    if len(moving) == 1:
        chosen = moving[0]
        reason = (
            f"Rule 2: {_describe(chosen, request)} is the only eligible moving car and "
            f"passes floor {request.floor} going {request.direction}, so it is chosen."
        )
        if idle:
            other = idle[0]
            reason += (f" {_describe(other, request)} is left free for other calls"
                       " (keeping a car free is a proxy, not measured waiting time or energy).")
        return Decision(chosen.id, reason + note)

    # Rule 3: both eligible elevators are moving -> fewer floors from the caller.
    if len(moving) >= 2:
        chosen, tied = _nearest(moving, request)
        details = " vs ".join(_describe(car, request) for car in moving)
        reason = (f"Rule 3: both eligible cars are moving ({details}); "
                  f"{chosen.id} has fewer floors to the caller")
        if tied:
            reason = (f"Rule 3: both eligible cars are moving ({details}); distances are "
                      f"equal, so the tie-breaker chooses {chosen.id}")
        return Decision(chosen.id, reason + " (floor distance is a proxy, not measured waiting time)." + note)

    # Rule 4: no eligible elevator is moving -> fewer floors from the caller.
    chosen, tied = _nearest(idle, request)
    if len(idle) == 1:
        reason = (f"Rule 4: no eligible car is moving; {_describe(chosen, request)} "
                  "is the only eligible car, so it is chosen.")
    else:
        details = " vs ".join(_describe(car, request) for car in idle)
        if tied:
            reason = (f"Rule 4: no eligible car is moving ({details}); distances are equal, "
                      f"so the tie-breaker chooses {chosen.id}.")
        else:
            reason = (f"Rule 4: no eligible car is moving ({details}); {chosen.id} has fewer "
                      "floors to the caller (floor distance is a proxy, not measured waiting time).")
    return Decision(chosen.id, reason + note)
