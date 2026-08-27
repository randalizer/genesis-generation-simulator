from unittest.mock import patch

from genesis.pairing import PairingEngine


def test_final_compatibility_score_uses_spark_noise() -> None:
    engine = PairingEngine(
        strategy="oldest_first",
        rules=[],
        preference_rule=None,
        spark_min=-15,
        spark_max=15,
    )

    with patch("genesis.pairing.random.randint", return_value=7):
        assert engine._final_compatibility_score(40) == 47
