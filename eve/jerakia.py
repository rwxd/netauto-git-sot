"""Key-value store functions."""

import logging
import yaml
import functools
import os
import copy
import yaml
from pathlib import Path
from eve.searchpaths import get_searchpaths
from eve.classifier import Classifier
from eve.structure import find_host_dir
from eve.logging import logger


class Jerakia(object):
    '''Implementation of Jerakia
    https://github.com/jerakia/jerakia
    '''

    def __init__(self, classifier: Classifier, datapath: Path):
        self.datapath = datapath
        self.classifier = classifier
        self.searchpaths = get_searchpaths

    @functools.lru_cache(maxsize=None)
    def yaml_load(self, path):
        if not os.path.exists(path):
            return None
        with open(path) as input:
            return yaml.safe_load(input)

    @functools.lru_cache(maxsize=None)
    def lookup(self, device: str, namespace: str, key: str):
        '''Lookup a value in Jerakia for a given device.'''
        device_path = find_host_dir(device)
        scope = self.classifier.scope(device_path)
        found = None
        searchpaths = self.searchpaths(scope)
        for path in searchpaths:
            path = self.datapath.joinpath(path).joinpath(f'{namespace}.yml')
            if not path.exists():
                logger.warning(f'Could not find {path}')
                continue
            data = self.yaml_load(path)
            if data is None or not key in data:
                continue
            current = copy.deepcopy(data[key])
            # if merge is None:
            #     return current
            # if found is None:
            #     found = current
            # elif merge == "hash":
            #     current.update(found)
            #     found = current
            # elif merge == "array":
            #     found.extend(current)
        return found
