#!/usr/bin/env python3

import argparse
import json
import pathlib
import boto3
import sys

def load_environment_config(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def write_environment_param(env_dict, param_name="/iac/environment"):
    ssm = boto3.client("ssm")
    print(f"Writing parameter {param_name} to SSM Parameter Store...")
    ssm.put_parameter(
        Name=param_name,
        Value=json.dumps(env_dict, separators=(",", ":")),
        Type="String",
        Overwrite=True,
        Tier="Standard"
    )
    print("Environment parameter set successfully.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", required=True, help="Environment name (e.g. dev, prod)")
    parser.add_argument("--path", default="account_environments", help="Path to environment files")
    parser.add_argument("--param-name", default="/iac/environment", help="Parameter Store name to write")
    args = parser.parse_args()

    file_path = pathlib.Path(args.path) / f"{args.env}.json"
    if not file_path.exists():
        print(f"Environment file not found: {file_path}")
        sys.exit(1)

    env_config = load_environment_config(file_path)
    write_environment_param(env_config, param_name=args.param_name)

if __name__ == "__main__":
    main()
