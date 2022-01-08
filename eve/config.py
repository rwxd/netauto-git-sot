from typing import Dict
from pathlib import Path

schmema_mapping: Dict[str, Path] = {
    'system.yml': Path('schemas/system.schema.json'),
    'topology.yml': Path('schemas/topology.schema.json'),
}
