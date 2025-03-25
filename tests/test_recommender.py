import os
import pytest
from src.recommender.collaborative_filtering import train_recommender, evaluate_recommender

@pytest.fixture
def config_file():
    """
    Fixture to provide the path to the configuration file for testing.
    """
    return "configs/test_collaborative_filtering.yaml"

def test_train_recommender(config_file):
    """
    Test the training functionality of the recommender system.
    """
    if not os.path.exists(config_file):
        pytest.skip(f"Configuration file '{config_file}' not found.")
    try:
        result = train_recommender(config_file)
        assert result is not None, "Training result should not be None."
        assert "best_valid_score" in result, "Training result should include 'best_valid_score'."
        print("Training Test Passed.")
    except FileNotFoundError as e:
        pytest.fail(f"FileNotFoundError: {e}")
    except RuntimeError as e:
        pytest.fail(f"RuntimeError: {e}")

def test_evaluate_recommender(config_file):
    """
    Test the evaluation functionality of the recommender system.
    """
    if not os.path.exists(config_file):
        pytest.skip(f"Configuration file '{config_file}' not found.")
    try:
        result = evaluate_recommender(config_file)
        assert result is not None, "Evaluation result should not be None."
        assert "test_result" in result, "Evaluation result should include 'test_result'."
        print("Evaluation Test Passed.")
    except FileNotFoundError as e:
        pytest.fail(f"FileNotFoundError: {e}")
    except RuntimeError as e:
        pytest.fail(f"RuntimeError: {e}")