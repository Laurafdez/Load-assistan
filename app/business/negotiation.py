from app.schemas.negotiations import (
    CounterOfferRequest,
    CounterOfferResponse,
    FinalStatus,
)

from app.core.config import constants


def evaluate_counter_offer(req: CounterOfferRequest) -> CounterOfferResponse:
    """
    Evaluates a carrier's counteroffer and determines the next step in negotiation.

    Args:
        req (CounterOfferRequest): Incoming offer details from the carrier.

    Returns:
        CounterOfferResponse: Negotiation result including next suggestion or final decision.
    """
    carrier_offer = req.carrier_offer
    last_offer = req.last_offer
    round_num = req.negotiation_round
    max_rate = req.max_rate

    # 1. Carrier offer exceeds our max rate
    if carrier_offer > max_rate:
        gap = carrier_offer - max_rate
        counter_suggestion = max_rate - (
            (gap // 2) // constants.ROUNDING_STEP * constants.ROUNDING_STEP
        )

        return CounterOfferResponse(
            final_status=FinalStatus.COUNTER,
            counter_suggestion=counter_suggestion,
            rounds_left=constants.MAX_NEGOTIATION_ROUNDS - round_num,
            message=(
                f"Your offer of ${carrier_offer:.2f} "
                f"is above our max. Could you consider ${counter_suggestion:.2f}?"
            ),
        )

    # 2. Carrier accepts or beats our last offer
    if carrier_offer >= last_offer:
        return CounterOfferResponse(
            final_status=FinalStatus.ACCEPTED,
            counter_suggestion=None,
            rounds_left=max(constants.MAX_NEGOTIATION_ROUNDS - round_num, 0),
            message="Great — transferring you to our sales team to lock that in. One moment.",
        )

    # 3. Max number of rounds reached
    if round_num >= constants.MAX_NEGOTIATION_ROUNDS:
        return CounterOfferResponse(
            final_status=FinalStatus.LIMIT_REACHED,
            counter_suggestion=None,
            rounds_left=0,
            message="Thanks for staying with me. We’ve reached the limit of negotiation rounds.",
        )

    # 4. Suggest a new offer: split gap (round to nearest $10), never exceed max_rate
    gap = max_rate - carrier_offer
    incremental = (gap // 2) // constants.ROUNDING_STEP * constants.ROUNDING_STEP
    next_offer = min(carrier_offer + incremental, max_rate)

    return CounterOfferResponse(
        final_status=FinalStatus.COUNTER,
        counter_suggestion=next_offer,
        rounds_left=constants.MAX_NEGOTIATION_ROUNDS - round_num,
        message=f"Thanks — I can do ${next_offer:.2f}. What do you think?",
    )
