from typing import List
from pydantic import BaseModel
from generator.models.device_configuration import JsonSchemaForNetworkConfiguration


class Tenant(BaseModel):
    name: str
    devices: List[JsonSchemaForNetworkConfiguration]


class Organization(BaseModel):
    name: str
    tenants: List[Tenant]


class Repository(BaseModel):
    organizations: List[Organization]
