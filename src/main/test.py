import argparse
import importlib.util
import json
import pathlib

from typing import Any, Callable, Dict

from azure.identity import DefaultAzureCredential, get_bearer_token_provider

import guidance

from aether_utils.jsonl_utils_multiprocessing import line_map_mp, ItemMapper
from aether_utils.logging_utils import get_standard_logger_for_file


_logger = get_standard_logger_for_file(__file__)

USER_MODULE = "user_module"
GUIDANCE_FUNCTION = "guidance_generation"


def parse_args():
    parser = argparse.ArgumentParser(add_help=True)

    # Information about the datasets
    datasets_group = parser.add_argument_group("Datasets")
    datasets_group.add_argument("--input_dataset", type=pathlib.Path, required=True)
    datasets_group.add_argument("--output_dataset", type=pathlib.Path, required=True)
    datasets_group.add_argument("--error_dataset", type=pathlib.Path, required=True)

    # Information about the guidance program
    parser.add_argument("--guidance_program", type=pathlib.Path, required=True)
    parser.add_argument("--guidance_workers", type=int, required=True)
    parser.add_argument("--max_errors", type=int, required=True)

    # Information about the model
    model_group = parser.add_argument_group("Model Endpoint")
    model_group.add_argument("--azure_openai_endpoint", type=str, required=True)
    model_group.add_argument("--azure_openai_deployment", type=str, required=True)
    model_group.add_argument("--azure_openai_model", type=str, required=True)
    model_group.add_argument("--azure_openai_api_version", type=str, required=True)

    args = parser.parse_args()
    return args

