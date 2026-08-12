# 11 Fine-tuning and RL

> Fine tune for format and cost, not for facts. Use retrieval for facts.

| Tool | Sub-Category | What It Does | Best Use Case | Language | License | Difficulty | Adoption | Link |
|---|---|---|---|---|---|---|---|---|
| Unsloth | Fine-tuning | Custom kernels that make LoRA and QLoRA fine tuning roughly two times faster with far less VRAM | Fine tuning a 7B to 14B model on a single free Colab GPU | Python | Apache-2.0 | Beginner | Very High | https://github.com/unslothai/unsloth |
| LLaMA-Factory | Fine-tuning | Unified YAML and web UI for 100 plus models covering SFT, DPO, PPO and quantised training | Fine tuning without writing a training loop | Python | Apache-2.0 | Beginner | Very High | https://github.com/hiyouga/LLaMA-Factory |
| Axolotl | Fine-tuning | Config driven training with multi GPU, sequence packing and every popular fine tune method | Reproducible team fine tuning runs | Python | Apache-2.0 | Intermediate | Very High | https://github.com/axolotl-ai-cloud/axolotl |
| TRL | Post-training | Hugging Face library for SFT, DPO, GRPO and reward modelling | The reference implementation of modern alignment methods | Python | Apache-2.0 | Intermediate | Very High | https://github.com/huggingface/trl |
| PEFT | Efficiency | LoRA, QLoRA, adapters and prompt tuning as a thin layer over transformers | Training 1 percent of parameters instead of all of them | Python | Apache-2.0 | Beginner | Very High | https://github.com/huggingface/peft |
| torchtune | Fine-tuning | Native PyTorch recipes with no framework abstraction between you and the training loop | Learning what actually happens during fine tuning | Python | BSD-3 | Intermediate | High | https://github.com/pytorch/torchtune |
| verl | RL training | Volcano Engine reinforcement learning library used for large scale agentic RL | Training agents with multi turn tool use rewards | Python | Apache-2.0 | Advanced | Very High | https://github.com/volcengine/verl |
| OpenRLHF | RL training | Ray and vLLM based RLHF framework that scales to 70B plus models | Full RLHF pipelines outside a big lab | Python | Apache-2.0 | Advanced | High | https://github.com/OpenRLHF/OpenRLHF |
| ART | Agent RL | Reinforcement learning trainer aimed specifically at improving agent behaviour with GRPO | Making a small model beat a big one at your narrow task | Python | Apache-2.0 | Advanced | Emerging | https://github.com/OpenPipe/ART |
| DeepSpeed | Scaling | ZeRO optimiser stages, offloading and pipeline parallelism for large training runs | Training models that do not fit on one GPU | Python, C++ | Apache-2.0 | Advanced | Very High | https://github.com/deepspeedai/DeepSpeed |
| Megatron-LM | Scaling | NVIDIA tensor and pipeline parallel training used for frontier scale pretraining | Pretraining and very large continued training | Python | Custom | Advanced | Very High | https://github.com/NVIDIA/Megatron-LM |
| Accelerate | Scaling | One API to run the same training script on CPU, one GPU, many GPUs or TPU | Removing device specific code from your trainer | Python | Apache-2.0 | Beginner | Very High | https://github.com/huggingface/accelerate |
| llm-compressor | Quantisation | vLLM native library for GPTQ, AWQ, SmoothQuant and FP8 compression | Shrinking a fine tuned model before serving | Python | Apache-2.0 | Intermediate | High | https://github.com/vllm-project/llm-compressor |
| AutoAWQ | Quantisation | Activation aware 4 bit quantisation with good quality retention and fast inference | 4 bit weights for consumer GPU serving | Python | MIT | Intermediate | High | https://github.com/casper-hansen/AutoAWQ |
| GPTQModel | Quantisation | Maintained GPTQ toolkit supporting current model architectures | Quantising newly released models | Python | Apache-2.0 | Intermediate | Medium | https://github.com/ModelCloud/GPTQModel |
| bitsandbytes | Quantisation | 8 bit and 4 bit primitives that make QLoRA possible | Loading a big model in 4 bit to fine tune it | Python, CUDA | MIT | Beginner | Very High | https://github.com/bitsandbytes-foundation/bitsandbytes |
| Optimum | Optimisation | Bridges transformers to ONNX Runtime, OpenVINO and other accelerators | Deploying to CPU or edge hardware | Python | Apache-2.0 | Intermediate | High | https://github.com/huggingface/optimum |
| Distilabel | Synthetic data | Pipelines for generating and judging synthetic training data with multiple models | Building a fine tuning dataset when you have none | Python | Apache-2.0 | Intermediate | High | https://github.com/argilla-io/distilabel |
| Argilla | Data curation | Collaborative annotation platform for building and cleaning instruction datasets | Human review of agent traces turned into training data | Python | Apache-2.0 | Beginner | High | https://github.com/argilla-io/argilla |
| SkyPilot | Compute | Runs training and serving jobs on the cheapest available GPUs across clouds with spot recovery | Cutting GPU spend without vendor lock in | Python | Apache-2.0 | Intermediate | Very High | https://github.com/skypilot-org/skypilot |
