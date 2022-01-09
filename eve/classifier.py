from pathlib import Path
from functools import lru_cache
from typing import Dict
from eve.structure import get_system
from typing import List, Optional, Union, Any


class Classifier:
    def __init__(self):
        pass

    @lru_cache(maxsize=None)
    def scope(self, device: Path) -> Dict:
        system = get_system(device)
        scope: Dict[str, Optional[Union[str, List]]] = {}

        if system:
            scope['os'] = recursive_key_lookup(
                system.dict(), ['general', 'software', 'os']
            )
            scope['datacenter'] = recursive_key_lookup(
                system.dict(), ['general', 'location', 'datacenter']
            )
            scope['groups'] = recursive_key_lookup(system.dict(), ['general', 'groups'])
            scope['os'] = recursive_key_lookup(
                system.dict(), ['general', 'software', 'os']
            )
            scope['os_version'] = recursive_key_lookup(
                system.dict(), ['general', 'software', 'os_version']
            )
            scope['tenant'] = recursive_key_lookup(system.dict(), ['general', 'tenant'])
            scope['fqdn'] = recursive_key_lookup(system.dict(), ['general', 'fqdn'])

        # remove key with empty value
        cleaned_scope: Dict[str, Union[str, List]] = {
            k: v for k, v in scope.items() if v
        }
        return cleaned_scope


def recursive_key_lookup(data: dict, traversal: List[str]) -> Any:
    for key in traversal:
        if key in data:
            if type(data[key]) == dict:
                traversal.remove(key)
                return recursive_key_lookup(data[key], traversal)
            else:
                return data[key]
    return None
