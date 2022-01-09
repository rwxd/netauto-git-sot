from pathlib import Path
from functools import lru_cache
from typing import Dict
from eve.structure import get_system
from eve.utils import recursive_key_lookup
from typing import List, Optional, Union, Any


class Classifier:
    def __init__(self):
        pass

    @lru_cache(maxsize=None)
    def scope(self, device: Path) -> Dict:
        system = get_system(device)
        scope: Dict[str, Optional[Union[str, List]]] = {}

        if system:
            scope['system'] = system.dict()

        # remove key with empty value
        cleaned_scope: Dict[str, Union[str, List]] = {
            k: v for k, v in scope.items() if v
        }
        return cleaned_scope
