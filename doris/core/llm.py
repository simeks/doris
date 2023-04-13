import sys

from transformers import (
    AutoTokenizer,
    LlamaForCausalLM,
    PreTrainedTokenizerBase
)

# Not ideal but gptq is not a "package"
sys.path.append('third_party/GPTQ-for-LLaMa')

from llama_inference import load_quant

# TODO: Fix this
_models = {
    'alpaca7B': {
        'model': '/mnt/c/projects/alpaca-native-4bit/',
        'checkpoint': '/mnt/c/projects/alpaca-native-4bit/alpaca7b-4bit.pt',
        'wbits': 4,
        'groupsize': 128
    }
}


def load_model(model_id: str) -> tuple[LlamaForCausalLM, PreTrainedTokenizerBase]:
    """ Load a quantized model

    Args:
        model: Path to the model
        checkpoint: Path to the checkpoint
        wbits: Number of bits to quantize the weights
        groupsize: Number of groups to quantize the weights

    Returns:
        The quantized model and tokenizer
    """

    model = load_quant(
        _models[model_id]['model'],
        _models[model_id]['checkpoint'],
        _models[model_id]['wbits'],
        _models[model_id]['groupsize']
    )
    tokenizer = AutoTokenizer.from_pretrained(_models[model_id]['model'])

    return model, tokenizer
