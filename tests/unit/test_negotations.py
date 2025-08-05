import pytest
from app.schemas.negotiations import CounterOfferRequest, FinalStatus
from app.business.negotiation import evaluate_counter_offer
from app.core.config import constants


@pytest.fixture
def base_request():
    return {
        "last_offer": 1500,
        "max_rate": 1700,
    }


def test_offer_above_max_rate(base_request):
    req = CounterOfferRequest(carrier_offer=1900, negotiation_round=1, **base_request)
    response = evaluate_counter_offer(req)

    assert response.final_status == FinalStatus.COUNTER
    assert response.counter_suggestion < req.max_rate
    assert "$" in response.message
    assert response.rounds_left == constants.MAX_NEGOTIATION_ROUNDS - 1


def test_offer_equals_last_offer(base_request):
    req = CounterOfferRequest(carrier_offer=1500, negotiation_round=2, **base_request)
    response = evaluate_counter_offer(req)

    assert response.final_status == FinalStatus.ACCEPTED
    assert response.counter_suggestion is None
    assert "transferring you" in response.message.lower()


def test_offer_above_last_but_under_max(base_request):
    req = CounterOfferRequest(carrier_offer=1600, negotiation_round=2, **base_request)
    response = evaluate_counter_offer(req)

    assert response.final_status == FinalStatus.ACCEPTED
    assert response.counter_suggestion is None


def test_negotiation_limit_reached(base_request):
    req = CounterOfferRequest(
        carrier_offer=1400,
        negotiation_round=constants.MAX_NEGOTIATION_ROUNDS,
        **base_request,
    )
    response = evaluate_counter_offer(req)

    assert response.final_status == FinalStatus.LIMIT_REACHED
    assert response.counter_suggestion is None
    assert response.rounds_left == 0


def test_standard_counteroffer_flow(base_request):
    req = CounterOfferRequest(carrier_offer=1200, negotiation_round=1, **base_request)
    response = evaluate_counter_offer(req)

    assert response.final_status == FinalStatus.COUNTER
    assert response.counter_suggestion > req.carrier_offer
    assert response.counter_suggestion <= req.max_rate
    assert "can do" in response.message.lower()
