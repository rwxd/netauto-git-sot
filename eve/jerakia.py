"""Key-value store functions."""

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
from eve.schemas import get_object_for_schema_name
from eve.utils import recursive_attribute_lookup
from typing import Any


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
    def lookup(self, device: str, namespace: str, key: str) -> Any:
        '''Lookup a value in Jerakia for a given device.
        The key can be multiple layers deep e.g. "foo.bar.baz"
        '''
        scope = self.classifier.scope(find_host_dir(device))
        found = None
        for path in self.searchpaths(scope):
            path = self.datapath.joinpath(path).joinpath(f'{namespace}.yml')
            if not path.exists():
                logger.warning(f'Could not find {path}')
                continue
            data = self.yaml_load(path)
            parsed_schema = get_object_for_schema_name(path.name).parse_obj(data)
            if '.' in key:
                traversal = key.split('.')
                value = recursive_attribute_lookup(parsed_schema, traversal)
            else:
                value = getattr(parsed_schema, key)

            if value is None:
                logger.debug(f'Could not find {key} in {path}')
                continue

            current = copy.deepcopy(value)
            if found is None:
                found = current
            elif type(found) == object:
                current.update(found.dict())
                found = current
            elif type(found) == list:
                found.extend(current)
        return found
