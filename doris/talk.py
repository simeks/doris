import torch

from llm import load_model

dev = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

class Doris:
    def __init__(self):
        self.model, self.tokenizer = load_model('alpaca7B')
        self.model = self.model.to(dev)

    def encode(self, text: str) -> torch.Tensor:
        return self.tokenizer.encode(text, return_tensors='pt').to(dev)
    
    def decode(self, tokens: torch.Tensor) -> str:
        return self.tokenizer.decode(tokens[0])

    def infer(self, input: torch.Tensor, max_tokens: int) -> torch.Tensor:
        return self.model.generate(
            input,
            do_sample=True,
            max_new_tokens=max_tokens,
            temperature=0.7,
        )

    def instruct(self, instruction: str, inp: str):
        inp_str = f'### Input:\n{inp}\n'
        prompt = f'### Instruction:\n{instruction}\n{inp_str if inp else ""}### Response:\n'
        tokens = self.encode(prompt)
        start_t = tokens.shape[1]
        stop_t = -1
        while True:
            output = self.infer(tokens, max_tokens=2)
            for i in range(start_t, output.shape[1]):
                t = output[0, i]
                if t == 2:
                    stop_t = i
                    break
            yield self.decode(output[:,start_t:stop_t])
            if stop_t != -1:
                return
            tokens = output
            start_t = tokens.shape[1]-1
