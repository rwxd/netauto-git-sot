# generated by datamodel-codegen:
#   filename:  build.schema.json
#   timestamp: 2022-01-09T20:00:56+00:00

from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class Type(Enum):
    BuildConfiguration = 'BuildConfiguration'


class Template(BaseModel):
    source: str = Field(..., description='Source Jinja Template', title='Source')
    destination: str = Field(
        ..., description='Destination file name', title='Destination'
    )


class Check(BaseModel):
    description: Optional[str] = Field(
        None, description='Description of the check', title='Description'
    )
    script: str = Field(..., description='Script to run', title='Script')


class JsonSchemaForBuildConfiguration(BaseModel):
    type: Type
    templates: Optional[List[Template]] = Field(
        None,
        description='Templates to use for this build configuration',
        title='Templates',
    )
    checks: Optional[List[Check]] = Field(None, title='Checks')
