#!/bin/bash

# docker build -t astrasim -f ./Dockerfile_astrasim .
# docker system prune --volumes

docker_img="astrasim:latest"

home_path_0="${HOME}/chakra"
docker_path_0="/workspace/chakra"

home_path_1="${HOME}/astra-sim"
docker_path_1="/workspace/astra-sim"

work_dir=${docker_path_0}

docker run --rm -it -P \
    -v ${home_path_0}:${docker_path_0} \
    -v ${home_path_1}:${docker_path_1} \
    -w ${work_dir} \
    ${docker_img} \
    bash