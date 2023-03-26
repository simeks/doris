# doris

Conversational AI sandbox

## Notes

### LLaMA/Alpaca

* LLaMA [1]: 65B LLM by Meta
* Alpaca [2]: fine-tuned version of LLaMA
* [GPTQ repo](https://github.com/IST-DASLab/gptq) [3]
* [GPTQ-for-LLaMA](https://github.com/qwopqwop200/GPTQ-for-LLaMa) LLaMA-specific implementation of GOTQ [3]

### Weights

* [LLaMA 7B](https://huggingface.co/decapoda-research/llama-7b-hf)
* [LLaMA 13B 4 bit](https://huggingface.co/decapoda-research/llama-13b-hf-int4)
* [Alpaca 7B](https://huggingface.co/chavinlo/alpaca-native), natively fine-tuned, i.e. no LoRA [4].
* [Alpaca 7B 4bit](https://huggingface.co/ozcur/alpaca-native-4bit) 4 bit quantized weights.
* [Alpaca 30B 4bit](https://huggingface.co/elinas/alpaca-30b-lora-int4), 4 bit, trained using LoRA [4].

### Install GPTQ-for-LLaMa

> Assumes requirements.txt has been installed.

1. Clone GPTQ-for-LLaMA: `git clone https://github.com/qwopqwop200/GPTQ-for-LLaMa.git`
2. In GPTQ folder: `CUDA_PATH=/usr/local/cuda-11.7 python setup_cuda.py install` (assuming project environment is active)
3. Test installation: `CUDA_VISIBLE_DEVIES=0 python test_kernel.py`

## References

1. Hugo Touvron, et al., LLaMA: Open and Efficient Foundation Language Models, https://arxiv.org/abs/2302.13971

2. Rohan Taori, et al., Stanford Alpaca: An Instruction-following LLaMA model, https://github.com/tatsu-lab/stanford_alpaca

3. Elias Frantar, et al., GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers, https://arxiv.org/abs/2210.17323

4. Edward J. Hu, et al., LoRA: Low-Rank Adaptation of Large Language Models, https://arxiv.org/abs/2106.09685
