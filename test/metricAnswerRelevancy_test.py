from deepeval import assert_test
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase
from demos.juiz import obter_juiz
from dataset.loader_datase import carregar_dataset
from chatbot import perguntar
import pytest


JUIZ = obter_juiz()
dataset = carregar_dataset()


@pytest.mark.AnswerRelevancy
class TestAnswerRelancy:

    @pytest.mark.parametrize("golden", dataset.goldens)
    def testing(self, golden):
        actual_output = perguntar(golden.input)
        test_case = LLMTestCase(
            input=golden.input,
            actual_output=actual_output,
            expected_output=golden.expected_output,
            retrieval_context=golden.retrieval_context,
        )

        assert_test(test_case=test_case, metrics=[AnswerRelevancyMetric(model=JUIZ, threshold=0.7)])