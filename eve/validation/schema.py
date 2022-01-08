from pathlib import Path
import jsonschema
import json
import yaml
from eve.config import schmema_mapping
from eve.structure import get_all_configuration_files


def validate_schemas() -> bool:
    files = get_all_configuration_files()
    for file in files:
        validate_schema(file)


def validate_schema(file: Path) -> bool:
    file_name = file.name
    schema_path = schmema_mapping.get(file_name)
    if schema_path is None:
        raise ValueError(f'No schema file found for {file_name}')

    with open(schema_path, 'r') as f:
        schema = json.load(f)

    with open(file, 'r') as f:
        data = yaml.safe_load(f)

    schema_folder_uri = 'file://' + str(schema_path.parent.absolute()) + '/'
    resolver = jsonschema.RefResolver(referrer=schema, base_uri=schema_folder_uri)

    try:
        jsonschema.validate(data, schema, resolver=resolver)
    except jsonschema.ValidationError as e:
        raise jsonschema.ValidationError(f'{str(file)} - {e.message}')

    return True
