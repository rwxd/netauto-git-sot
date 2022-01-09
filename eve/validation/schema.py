from pathlib import Path
import yaml
import json
from eve.config import schemas
from eve.structure import get_all_configuration_files
from rich.console import Console
import jsonschema

console = Console()


def validate_schemas() -> bool:
    files = get_all_configuration_files()
    return all([validate_schema(file) for file in files])


def validate_schema(file: Path) -> bool:
    valid = True
    for schema in schemas:
        if schema[0] == file.name:
            with open(schema[1], 'r') as f:
                loaded_json_schema = json.load(f)

            with open(file, 'r') as f:
                data = yaml.safe_load(f)

            schema_folder_uri = 'file://' + str(schema[1].parent.absolute()) + '/'
            resolver = jsonschema.RefResolver(
                referrer=loaded_json_schema, base_uri=schema_folder_uri
            )

            try:
                jsonschema.validate(data, loaded_json_schema, resolver=resolver)
            except jsonschema.ValidationError as e:
                console.print(f'[red]{str(file)} - {e.message}[/red]')
                valid = False

    return valid
