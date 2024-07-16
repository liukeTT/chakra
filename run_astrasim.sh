#!/bin/bash

ASTRASIM_DIR="/workspace/astra-sim"
CHAKRA_DIR="/workspace/chakra"

# build astrasim
${ASTRASIM_DIR}/build/astra_analytical/build.sh
BINARY="${ASTRASIM_DIR}/build/astra_analytical/build/bin/AstraSim_Analytical_Congestion_Unaware"
#BINARY="${ASTRASIM_DIR}/build/astra_analytical/build/bin/AstraSim_Analytical_Congestion_Aware"

for comm in "allreduce" "alltoall" "allgather" "reducescatter"; do
for comm_size in 1024 1048576 1073741824; do
for TOPO in "Switch" "Ring" "FullyConnected"; do
    # chakra: generated et
    WORKLOAD="${CHAKRA_DIR}/et/${comm}/${comm_size}/node"

    # astrasim: system config
    SYSTEM="${ASTRASIM_DIR}/inputs/system/${TOPO}.json"
    NETWORK="${ASTRASIM_DIR}/inputs/network/analytical/${TOPO}.yml"
    MEMORY="${ASTRASIM_DIR}/inputs/remote_memory/analytical/no_memory_expansion.json"

    # run astrasim
    ${BINARY} \
        --workload-configuration="${WORKLOAD}" \
        --system-configuration="${SYSTEM}" \
        --network-configuration="${NETWORK}" \
        --remote-memory-configuration="${MEMORY}" \
        >> ./et/${comm}/${comm_size}/astrasim.${TOPO}
done
done
done