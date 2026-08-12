# 19 Hardware and Cost

> India pricing, approximate as of August 2026. Rent before you buy, and start on the free tiers.

> Setup Approx Cost Spec What You Can Run Notes

- LET'S CODE  \|  OPEN SOURCE TOOLKIT FOR BUILDING AI AGENTS 2026
- India pricing, approximate as of August 2026. Rent before you buy, and start on the free tiers.
- Setup | Approx Cost | Spec | What You Can Run | Notes
- Google Colab free tier | Free | T4 with 16GB | 7B to 9B models in 4 bit, QLoRA fine tuning of small models | The correct starting point. Sessions disconnect, so checkpoint to Drive
- Kaggle notebooks | Free | 2 x T4 or P100, 30 hours a week | Same as Colab with longer sessions and two GPUs | Underused by students, the weekly quota is generous
- Local laptop, 8GB RAM, no GPU | Already owned | CPU only | 1B to 4B models through Ollama or llama.cpp, quantised | Good enough for routers, classifiers and learning the agent loop
- Local laptop, 16GB RAM, Apple silicon | Already owned | Unified memory | 7B to 14B at usable speed thanks to shared memory | Apple silicon is the best value local inference machine right now
- RTX 3060 12GB desktop | About 25,000 to 30,000 INR used | 12GB VRAM | 7B to 14B in 4 bit, comfortable QLoRA on 7B | The classic Indian student budget build for serious local work
- RTX 4060 Ti 16GB | About 45,000 to 55,000 INR | 16GB VRAM | 14B in 4 bit, 7B in 8 bit, faster fine tuning | Best new card under 60,000 INR for VRAM per rupee
- RTX 3090 or 4090 24GB | About 60,000 to 1,80,000 INR | 24GB VRAM | 32B in 4 bit, 14B in FP16, serious fine tuning | A used 3090 remains the enthusiast value pick
- Rented cloud GPU, A100 40GB | About 100 to 200 INR per hour | 40GB VRAM | 70B in 4 bit, full fine tune of small models | Rent by the hour instead of buying. Stop the instance the moment you finish
- Rented cloud GPU, H100 80GB | About 200 to 400 INR per hour | 80GB VRAM | Large MoE models, high throughput vLLM serving | Only rent this once you know exactly what you are running
- Spot and interruptible instances | 50 to 80 percent cheaper | Varies | Training and batch jobs that can checkpoint and resume | SkyPilot handles the interruption recovery for you
- API first, no hardware | Pay per token | None | Everything, at someone else cost | Cheapest path until roughly 20 to 50 million tokens a month, then self hosting starts winning
- VPS for the agent itself | About 400 to 1,200 INR a month | 2 to 4 vCPU, 4 to 8GB RAM | The agent, database and UI, with the model called over an API | Most agents need no GPU at all. Only the model does
