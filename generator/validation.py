from pathlib import Path
import jsonschema
import json
from yaml import safe_load


def raise_on_file_not_found(path: Path) -> None:
    if not path.exists():
        raise ValueError(f'{path} does not exist')


def validate_device_config(config_path: Path) -> bool:
    '''Validate a device configuration'''
    raise_on_file_not_found(config_path)
    schema_file = Path('schemas/device.schema.json')

    with open(schema_file, 'r') as f:
        schema = json.load(f)

    with open(config_path, 'r') as f:
        device_config = safe_load(f)

    jsonschema.validate(device_config, schema)
    return True
