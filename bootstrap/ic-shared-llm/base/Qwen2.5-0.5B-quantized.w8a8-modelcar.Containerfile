FROM quay.io/redhat-ai-services/huggingface-modelcar-builder:latest as base

# Set the HF_TOKEN with --build-arg HF_TOKEN="hf_..." at build time
ARG HF_TOKEN

# The model repo to download
ENV MODEL_REPO="RedHatAI/Qwen2.5-0.5B-quantized.w8a8"

# Download the necessary model files
RUN python3 download_model.py --model-repo ${MODEL_REPO}

# Final image containing only the essential model files
FROM registry.access.redhat.com/ubi9/ubi-micro:9.5

COPY --from=base /models /models

USER 1001