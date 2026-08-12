# 03 Inference and Serving

> Ollama to learn, vLLM to serve, LiteLLM to keep your options open.

| Tool | Sub-Category | What It Does | Best Use Case | Language | License | Difficulty | Adoption | Link |
|---|---|---|---|---|---|---|---|---|
| vLLM | Serving engine | High throughput serving with paged attention, continuous batching and prefix caching | The default production inference server for open weights | Python, CUDA | Apache-2.0 | Intermediate | Very High | https://github.com/vllm-project/vllm |
| SGLang | Serving engine | Fast serving with RadixAttention prefix caching and a structured generation language | Agent workloads with heavy shared prefixes and JSON output | Python | Apache-2.0 | Advanced | Very High | https://github.com/sgl-project/sglang |
| Ollama | Local runtime | One command local model runner with a friendly CLI and an OpenAI compatible API | Laptop development and offline demos | Go | MIT | Beginner | Very High | https://github.com/ollama/ollama |
| llama.cpp | Local runtime | C and C++ inference with GGUF quantisation that runs on CPU, Apple silicon and modest GPUs | Running 7B to 30B models on hardware you already own | C++ | MIT | Intermediate | Very High | https://github.com/ggml-org/llama.cpp |
| LiteLLM | Gateway | One OpenAI shaped API in front of 100 plus providers with keys, budgets and fallbacks | Provider abstraction, cost control and team key management | Python | MIT | Beginner | Very High | https://github.com/BerriAI/litellm |
| TensorRT-LLM | Serving engine | NVIDIA compiled kernels for the lowest latency on their GPUs | Squeezing maximum tokens per second from H100 and L40S fleets | C++, Python | Apache-2.0 | Advanced | High | https://github.com/NVIDIA/TensorRT-LLM |
| Text Generation Inference | Serving engine | Hugging Face production server with tensor parallelism and token streaming | Teams already deep in the Hugging Face ecosystem | Rust, Python | Apache-2.0 | Intermediate | High | https://github.com/huggingface/text-generation-inference |
| LMDeploy | Serving engine | Compression and serving toolkit from the InternLM team with a strong quantised path | Serving quantised models at high concurrency | Python, C++ | Apache-2.0 | Advanced | Medium | https://github.com/InternLM/lmdeploy |
| LocalAI | Local runtime | Drop in OpenAI replacement that also serves image, audio and embedding models | One self hosted endpoint for every modality | Go | MIT | Intermediate | High | https://github.com/mudler/LocalAI |
| Xinference | Serving platform | Cluster aware serving of LLM, embedding, rerank and multimodal models | Small teams that need a mixed model fleet on a few GPUs | Python | Apache-2.0 | Intermediate | Medium | https://github.com/xorbitsai/inference |
| BentoML | Serving platform | Python first framework to package models and agents into scalable API services | Turning a notebook prototype into a deployable service | Python | Apache-2.0 | Intermediate | High | https://github.com/bentoml/BentoML |
| KServe | Serving platform | Kubernetes native model serving with autoscaling and canary rollouts | Platform teams standardising inference on Kubernetes | Go, Python | Apache-2.0 | Advanced | High | https://github.com/kserve/kserve |
| Triton Inference Server | Serving platform | NVIDIA multi framework server with dynamic batching and model ensembles | Mixed PyTorch, ONNX and TensorRT fleets | C++ | BSD-3 | Advanced | High | https://github.com/triton-inference-server/server |
| Ray Serve | Serving platform | Scalable Python serving with model composition and fractional GPU allocation | Multi model agent pipelines on one cluster | Python | Apache-2.0 | Advanced | High | https://github.com/ray-project/ray |
| MLC LLM | Edge runtime | Compiles models to run on browsers, phones, AMD and Apple GPUs via machine learning compilation | On device agents for Android, iOS and WebGPU | Python, C++ | Apache-2.0 | Advanced | Medium | https://github.com/mlc-ai/mlc-llm |
| llamafile | Local runtime | Ships a model and its runtime as a single executable file that runs on six operating systems | Handing someone a working local model with zero setup | C++ | Apache-2.0 | Beginner | Medium | https://github.com/Mozilla-Ocho/llamafile |
| ExLlamaV2 | Local runtime | Memory efficient quantised inference for consumer NVIDIA cards | Running larger models on a single RTX card | Python | MIT | Advanced | Medium | https://github.com/turboderp-org/exllamav2 |
| KTransformers | Local runtime | Offloads experts to CPU so very large mixture of experts models run on one GPU | Testing a 200B plus MoE model on a single workstation | Python, C++ | Apache-2.0 | Advanced | Emerging | https://github.com/kvcache-ai/ktransformers |
| OpenLLM | Serving platform | Run any open model as an OpenAI compatible endpoint with one command | Quick self hosted endpoints during development | Python | Apache-2.0 | Beginner | Medium | https://github.com/bentoml/OpenLLM |
