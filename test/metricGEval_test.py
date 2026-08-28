from deepeval.metrics import GEval
from deepeval.test_case import SingleTurnParams
from demos.juiz import obter_juiz
from deepeval.test_case import LLMTestCase
from dataset.loader_datase import carregar_dataset
from chatbot import perguntar
from deepeval import assert_test
import pytest



JUIZ = obter_juiz()


CRITERIOS_CLAIMS = """
    Verifique se a resposta responde diretamente à pergunta feita, sem enrolação ou discurso de vendas. 
    Verifique se a resposta contém alguma promessa de cura, eliminação definitiva ou garantia de resultado (ex: 'cura acne', 'elimina todas as manchas'). Se contiver, penalize fortemente.
    Se a pergunta for sobre algo fora do escopo do catálogo, verifique se a resposta recusa claramente, em vez de tentar vender algo relacionado.

"""

metrica_claims = GEval(
    name="Conformidade de Claims",
    criteria=CRITERIOS_CLAIMS,
    evaluation_params=[
        SingleTurnParams.INPUT,
        SingleTurnParams.ACTUAL_OUTPUT,
    ],
    threshold=0.8,
     model=JUIZ,
)

dataset = carregar_dataset()
@pytest.mark.GEval
class TestGEval:

    @pytest.mark.parametrize("golden", dataset.goldens)
    def test_conformidade_claims(self, golden):
        actual_output = perguntar(golden.input)

        test_case = LLMTestCase(
            input=golden.input,
            actual_output=actual_output,
        )

        assert_test(test_case=test_case, metrics=[metrica_claims])