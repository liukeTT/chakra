#!/bin/bash

# if not install chakra package, uncomment following
# cd /workspace/chakra/
# python3 -m pip install . --user

# clean et folder
rm -fr ./et/*

# generate et
comm=$1
num_npus=$2
num_dims=$3
comm_size=$4

output_dir="/workspace/chakra/et"
mkdir -p ${output_dir}
python3 -m et_generator.et_comms --comm ${comm} --num_npus ${num_npus} --num_dims ${num_dims} --comm_size ${comm_size} --output_dir ${output_dir}