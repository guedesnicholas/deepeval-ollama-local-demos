import os
from deepeval.dataset import EvaluationDataset

def carregar_dataset():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(BASE_DIR, "golden_dataset.json")

    dataset = EvaluationDataset()
    dataset.add_goldens_from_json_file(
        file_path= json_path,
        input_key_name="input",
        expected_output_key_name="expected_output",
        retrieval_context_key_name="retrieval_context",

    )
    return dataset