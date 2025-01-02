import argparse
import sys
import yaml
from cerberus import Validator

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


class MetadataValidator:
    def __init__(self, schema_path: str):
        self.schema = self._load_schema(schema_path)
        self.validator = Validator(self.schema)

    @staticmethod
    def _load_schema(schema_path: str) -> dict:
        with open(schema_path, "r") as schema_file:
            return yaml.safe_load(schema_file)

    @staticmethod
    def load_metadata(metadata_path: str) -> dict:
        with open(metadata_path, "r") as metadata_file:
            return yaml.safe_load(metadata_file)

    def validate(self, metadata_path: str) -> bool:
        metadata = self.load_metadata(metadata_path)
        if self.validator.validate(metadata):
            return True
        else:
            print(self.validator.errors)
            return False


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata", help="Path to metadata file", required=True)
    parser.add_argument("--schema", help="Path to schema file", required=True)
    return parser.parse_args()


def main(args):
    validator = MetadataValidator(args.schema)

    if validator.validate(args.metadata):
        print("Metadata file is valid.")
        sys.exit(EXIT_SUCCESS)
    else:
        print("Metadata file is invalid.")
        sys.exit(EXIT_FAILURE)


if __name__ == "__main__":
    arguments = parse_arguments()
    main(arguments)
