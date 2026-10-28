from src.portfolio_opt.optimizer import equal_weights


def test_equal_weights_sum_to_one() -> None:
    w = equal_weights(5)
    assert abs(float(w.sum()) - 1.0) < 1e-12
