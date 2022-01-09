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
            scope['datacenter'] = recursive_key_lookup(
                system.dict(), ['general', 'location', 'datacenter']
            )
            scope['groups'] = recursive_key_lookup(system.dict(), ['general', 'groups'])
            scope['os'] = recursive_key_lookup(system.dict(), ['software', 'os'])
            scope['os_version'] = recursive_key_lookup(
                system.dict(), ['software', 'version']
            )
            scope['tenant'] = recursive_key_lookup(system.dict(), ['general', 'tenant'])
            scope['fqdn'] = recursive_key_lookup(system.dict(), ['general', 'fqdn'])

        # remove key with empty value
        cleaned_scope: Dict[str, Union[str, List]] = {
            k: v for k, v in scope.items() if v
        }
        return cleaned_scope
