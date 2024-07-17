#!/bin/bash

ASTRASIM_DIR="/workspace/astra-sim"
CHAKRA_DIR="/workspace/chakra"
LLM_DIR="/workspace/llm-perf-model/gpt_inference"

# build astrasim
${ASTRASIM_DIR}/build/astra_analytical/build.sh
BINARY="${ASTRASIM_DIR}/build/astra_analytical/build/bin/AstraSim_Analytical_Congestion_Unaware"
#BINARY="${ASTRASIM_DIR}/build/astra_analytical/build/bin/AstraSim_Analytical_Congestion_Aware"

WORKLOAD="${CHAKRA_DIR}/et/node"

NETWORK="${LLM_DIR}/$1"
SYSTEM="${LLM_DIR}/$2"
MEMORY="${LLM_DIR}/$3"

# run astrasim
${BINARY} \
    --workload-configuration="${WORKLOAD}" \
    --system-configuration="${SYSTEM}" \
    --network-configuration="${NETWORK}" \
    --remote-memory-configuration="${MEMORY}"
