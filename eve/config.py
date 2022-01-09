from typing import List, Tuple, Union
from pathlib import Path
from pydantic import BaseModel
from eve.models.system import JsonSchemaForSystemConfiguration
from eve.models.topology import JsonSchemaForTopologyConfiguration
from eve.models.build import JsonSchemaForBuildConfiguration

schemas: List[Tuple[str, Path, BaseModel]] = [
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
    ('build.yml', Path('schemas/build.schema.json'), JsonSchemaForBuildConfiguration),
]
