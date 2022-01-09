from pathlib import Path
from typing import List, Dict, Union
from eve.utils import recursive_key_lookup


def get_searchpaths(scope: Dict[str, Union[List, str]]) -> List[Path]:
    '''Returns the seachpaths for the given scope'''
    paths = [
        'hosts/{scope[tenant]}/{scope[fqdn]}/',
        'environment/{scope[tenant]}/{scope[datacenter]}/',
        'environment/{scope[tenant]}/',
        'os/{scope[os]}/{scope[os_version]}',
        'os/{scope[os]}/',
        'common/',
        *['groups/{group}' for group in scope.get('groups', [])],
    ]

    for idx in range(len(paths)):
        try:
            paths[idx] = paths[idx].format(scope=scope)
        except KeyError:
            paths[idx] = None  # type: ignore
    searchpaths = [Path(path) for path in paths if path]
    return searchpaths
