#!/bin/bash

# if not install chakra package, uncomment following
python3 -m pip install . --user

# clean et folder
rm -fr ./et/*

# generate et
for comm in "allreduce" "alltoall" "allgather" "reducescatter"; do
for comm_size in 1024 1048576 1073741824; do
    output_dir="./et/${comm}/${comm_size}"
    mkdir -p ${output_dir}

    python3 -m et_generator.et_comms --comm ${comm} --num_npus 64 --num_dims 1 --comm_size ${comm_size} --output_dir ${output_dir}
done
done