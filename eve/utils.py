from typing import List, Any


def recursive_key_lookup(data: dict, traversal: List[str]) -> Any:
    '''Recursively traverse a dictionary to get a keys value.
    Input data is a dictionary and traversal is a list of keys.
    Returns None if the key is not found.
    '''
    for key in traversal:
        if key in data:
            if type(data[key]) == dict:
                traversal.remove(key)
                return recursive_key_lookup(data[key], traversal)
            else:
                if len(traversal) == 1:
                    return data[key]
                return None
    return None


def recursive_attribute_lookup(data: object, traversal: List[str]) -> Any:
    '''Recursively traverse an object to get an attribute value.
    Returns None if the attribute is not found.
    '''
    for item in traversal:
        if hasattr(data, item):
            data = getattr(data, item)
            if type(data) == object:
                traversal.remove(item)
                return recursive_attribute_lookup(data, traversal)
            else:
                if len(traversal) == 1:
                    return data
                else:
                    return None
    return None
