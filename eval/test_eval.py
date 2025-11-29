from google.adk.evaluation.agent_evaluator import AgentEvaluator
import pytest

import os


@pytest.mark.asyncio
async def test_IGOTYOU_agent_evaluation():
    """Test the agent's basic ability"""
    eval_results = await AgentEvaluator.evaluate(
        agent_module="IGotYou_Agent.agent",
        eval_dataset_file_path_or_dir=os.path.join(
            os.path.dirname(__file__), "simple_eval.test.json"),
    )

    if eval_results:
        for result in eval_results:
            assert result.passed, f"Evaluation failed for {result.eval_set_path} with score {result.overall_score}"
