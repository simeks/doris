import sys

from celery import Task

from transformers import (
    LlamaForCausalLM,
    PreTrainedTokenizerBase
)

from ...workers.worker_gpu import app
from ...core import llm

class InferenceTask(Task):
    def __init__(self):
        self._model = None
        self._tokenizer = None

    def model(self) -> tuple[LlamaForCausalLM, PreTrainedTokenizerBase]:
        if self._model is None or self._tokenizer is None:
            self._model, self._tokenizer = llm.load_model('alpaca7B')
        return self._model, self._tokenizer


@app.task(bind=True, base=InferenceTask)
def inference_task(self, data):
    model, tokenizer = self.model()
    
    t = tokenizer.encode(data)
    print(f'{data} -> {t}')

