#!/usr/bin/env python3

import argparse

from chakra.third_party.utils.protolib import encodeMessage as encode_message
from chakra.et_def.et_def_pb2 import (
    Node as ChakraNode,
    DoubleList,
    FloatList,
    Int32List,
    Int64List,
    Uint32List,
    Uint64List,
    Sint32List,
    Sint64List,
    Fixed32List,
    Fixed64List,
    Sfixed32List,
    Sfixed64List,
    BoolList,
    StringList,
    BytesList,
    GlobalMetadata,
    AttributeProto as ChakraAttr,
    METADATA_NODE,
    MEM_LOAD_NODE,
    MEM_STORE_NODE,
    COMP_NODE,
    COMM_SEND_NODE,
    COMM_RECV_NODE,
    COMM_COLL_NODE,
    ALL_REDUCE,
    ALL_TO_ALL,
    ALL_GATHER,
    REDUCE_SCATTER,
)

NODE_ID = 0

def get_node(node_name: str, node_type: int) -> ChakraNode:
    global NODE_ID
    node = ChakraNode()
    node.id = NODE_ID
    node.name = node_name
    node.type = node_type
    NODE_ID += 1
    return node


def get_comm_type_attr(comm_type: int) -> ChakraAttr:
    return ChakraAttr(name="comm_type", int64_val=comm_type)


def get_involved_dim_attr(num_dims: int) -> ChakraAttr:
    return ChakraAttr(name="involved_dim", bool_list=BoolList(values=[True] * num_dims))


def one_comm_coll_node_allreduce(num_npus: int, num_dims: int, comm_size: int, output_dir: str) -> None:
    for npu_id in range(num_npus):
        output_filename = f"{output_dir}/node.{npu_id}.et"
        with open(output_filename, "wb") as et:
            encode_message(et, GlobalMetadata(version="0.0.4"))

            node = get_node("ALL_REDUCE", COMM_COLL_NODE)
            node.attr.append(ChakraAttr(name="is_cpu_op", bool_val=False))
            node.attr.append(get_comm_type_attr(ALL_REDUCE))
            node.attr.append(ChakraAttr(name="comm_size", uint64_val=comm_size))
            attr = get_involved_dim_attr(num_dims)
            node.attr.append(attr)
            encode_message(et, node)


def one_comm_coll_node_alltoall(num_npus: int, num_dims: int, comm_size: int, output_dir: str) -> None:
    for npu_id in range(num_npus):
        output_filename = f"{output_dir}/node.{npu_id}.et"
        with open(output_filename, "wb") as et:
            encode_message(et, GlobalMetadata(version="0.0.4"))

            node = get_node("ALL_TO_ALL", COMM_COLL_NODE)
            node.attr.append(ChakraAttr(name="is_cpu_op", bool_val=False))
            node.attr.append(get_comm_type_attr(ALL_TO_ALL))
            node.attr.append(ChakraAttr(name="comm_size", uint64_val=comm_size))
            attr = get_involved_dim_attr(num_dims)
            node.attr.append(attr)
            encode_message(et, node)


def one_comm_coll_node_allgather(num_npus: int, num_dims: int, comm_size: int, output_dir: str) -> None:
    for npu_id in range(num_npus):
        output_filename = f"{output_dir}/node.{npu_id}.et"
        with open(output_filename, "wb") as et:
            encode_message(et, GlobalMetadata(version="0.0.4"))

            node = get_node("ALL_GATHER", COMM_COLL_NODE)
            node.attr.append(ChakraAttr(name="is_cpu_op", bool_val=False))
            node.attr.append(get_comm_type_attr(ALL_GATHER))
            node.attr.append(ChakraAttr(name="comm_size", uint64_val=comm_size))
            attr = get_involved_dim_attr(num_dims)
            node.attr.append(attr)
            encode_message(et, node)


def one_comm_coll_node_reducescatter(num_npus: int, num_dims: int, comm_size: int, output_dir: str) -> None:
    for npu_id in range(num_npus):
        output_filename = f"{output_dir}/node.{npu_id}.et"
        with open(output_filename, "wb") as et:
            encode_message(et, GlobalMetadata(version="0.0.4"))

            node = get_node("REDUCE_SCATTER", COMM_COLL_NODE)
            node.attr.append(ChakraAttr(name="is_cpu_op", bool_val=False))
            node.attr.append(get_comm_type_attr(REDUCE_SCATTER))
            node.attr.append(ChakraAttr(name="comm_size", uint64_val=comm_size))
            attr = get_involved_dim_attr(num_dims)
            node.attr.append(attr)
            encode_message(et, node)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Execution Trace Generator"
    )
    parser.add_argument(
        "--comm",
        type=str,
        default="allreduce",
    )
    parser.add_argument(
        "--num_npus",
        type=int,
        default=64,
        help="Number of NPUs"
    )
    parser.add_argument(
        "--num_dims",
        type=int,
        default=2,
        help="Number of dimensions in the network topology"
    )
    parser.add_argument(
        "--comm_size",
        type=int,
        default=65536,
        help="Communication size of communication nodes"
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="./et",
        help="Default communication size of communication nodes"
    )
    args = parser.parse_args()

    num_npus = args.num_npus
    num_dims = args.num_dims
    comm_size = args.comm_size
    output_dir = args.output_dir

    if args.comm == "allreduce":
        one_comm_coll_node_allreduce(num_npus, num_dims, comm_size, output_dir)
    elif args.comm == "alltoall":
        one_comm_coll_node_alltoall(num_npus, num_dims, comm_size, output_dir)
    elif args.comm == "allgather":
        one_comm_coll_node_allgather(num_npus, num_dims, comm_size, output_dir)
    elif args.comm == "reducescatter":
        one_comm_coll_node_reducescatter(num_npus, num_dims, comm_size, output_dir)
    else:
        "Error: not supported communication kernel"


if __name__ == "__main__":
    main()
