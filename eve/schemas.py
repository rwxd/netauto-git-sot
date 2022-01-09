from eve.config import schemas
from pydantic import BaseModel
from eve.exceptions import SchemaNotFound


def get_object_for_schema_name(file_name) -> BaseModel:
    for schema in schemas:
        if schema[0] == file_name:
            return schema[2]
    raise SchemaNotFound(f'Schema not found for file name {file_name}')
