from pathlib import Path
from typing import List, Dict


def searchpaths(scope: Dict[str, str]) -> List[Path]:
    paths = [
        'hosts/{scope[tenant]}/{scope[hostname]}/',
        'environment/{scope[tenant]}/{scope[location][datacenter]}/{scope[hostname]}',
        'os/{scope[os]}/',
        'os/{scope[os]}/{scope[os_version]}',
        *['groups/{group}' for group in scope.get('groups', [])],
    ]

    for idx in range(len(paths)):
        try:
            paths[idx] = paths[idx].format(scope=scope)
        except KeyError:
            paths[idx] = None
    return [Path(path) for path in paths if path]


example_scope = {
    "hostname": "leaf1",
    "tenant": "mycompany",
    "location": {"datacenter": "nyc1"},
    "os": "cumulus",
    "os_version": "5.0",
}

paths = searchpaths(example_scope)

for path in paths:
    print(path)
