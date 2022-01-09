from typing import List, Tuple
from pathlib import Path

from pydantic.types import Json
from eve.models.system import JsonSchemaForSystemConfiguration
from eve.models.topology import JsonSchemaForTopologyConfiguration
from eve.models.system import JsonSchemaForSystemConfiguration

schemas: List[Tuple[str, Path, object]] = [
    (
        'system.yml',
        Path('schemas/system.schema.json'),
        JsonSchemaForSystemConfiguration,
    ),
    (
        'topology.yml',
        Path('schemas/topology.schema.json'),
        JsonSchemaForTopologyConfiguration,
    ),
    ('build.yml', Path('schemas/build.schema.json'), JsonSchemaForSystemConfiguration),
]
