from pathlib import Path
from typing import List, Optional
import yaml
import os
from eve.models.system import JsonSchemaForSystemConfiguration


def get_system(path: Path) -> Optional[JsonSchemaForSystemConfiguration]:
    if path.is_dir():
        files = list_files(path)
        for file in files:
            if file.name == 'system.yml':
                path = file
    with open(path, 'r') as f:
        loaded = yaml.safe_load(f)
    system = JsonSchemaForSystemConfiguration.parse_obj(loaded)
    return system


def get_all_configuration_files() -> List[Path]:
    files = Path('data/').glob('**/*.yml')
    return list(files)


def get_hosts() -> List[Path]:
    hosts = []
    for company in list_subdirectories(Path('data/hosts')):
        for host in list_subdirectories(company):
            hosts.append(host)
    return hosts


def find_host_dir(host: str) -> Path:
    for item in get_hosts():
        if item.name == host:
            return item
    else:
        raise ValueError(f'Could not find a host directory for {host}')


def list_subdirectories(directory: Path) -> List[Path]:
    dirs = []
    for it in os.scandir(str(directory)):
        if it.is_dir():
            dirs.append(directory.joinpath(it.name))
    return dirs


def list_files(directory: Path) -> List[Path]:
    files = []
    for file in directory.iterdir():
        if file.is_file():
            files.append(file)
    return files
