from pathlib import Path
from typing import List, Dict, Union
from eve.utils import recursive_key_lookup


def get_searchpaths(scope: Dict[str, Union[List, str]]) -> List[Path]:
    '''Returns the seachpaths for the given scope'''
    paths = [
        'common/',
        'environment/{scope[system][general][tenant]}/{scope[system][general][location][datacenter]}/',
        'environment/{scope[system][general][tenant]}/',
        'os/{scope[system][software][os]}/{scope[system][software][os_version]}',
        'os/{scope[system][software][os]}/',
        *[
            f'groups/{scope["system"]["general"]["tenant"]}/{group}/'
            for group in scope.get('system', {}).get('groups', [])[::-1]
        ],
        'hosts/{scope[system][general][tenant]}/{scope[system][general][fqdn]}/',
    ]

    for idx in range(len(paths)):
        try:
            paths[idx] = paths[idx].format(scope=scope)
        except KeyError:
            paths[idx] = None  # type: ignore
    searchpaths = [Path(path) for path in paths if path]
    return searchpaths
