from generator.models.structure import Organization, Repository, Tenant
from generator.models.device_configuration import JsonSchemaForNetworkConfiguration
from pathlib import Path
from typing import List
import os
import yaml


def load_repository_structure(repository_path: Path) -> Repository:
    organizations_path = repository_path.joinpath('organizations')
    repository = Repository(organizations=[])
    for org in list_subdirectories(organizations_path):
        organization = Organization(name=org.name, tenants=[])
        organization_path = organizations_path.joinpath(org.name)
        tenants_path = organization_path.joinpath('tenants')
        for ten in list_subdirectories(tenants_path):
            tenant = Tenant(name=ten.name, devices=[])
            tenant_path = tenants_path.joinpath(ten.name)
            devices_path = tenant_path.joinpath('devices')
            for dev in list_files(devices_path):
                device_path = devices_path.joinpath(dev.name)
                with open(device_path, 'r') as f:
                    loaded = yaml.safe_load(f)
                    device_config = JsonSchemaForNetworkConfiguration.parse_obj(loaded)
                tenant.devices.append(device_config)
            organization.tenants.append(tenant)
        repository.organizations.append(organization)
    return repository


def list_subdirectories(directory: Path) -> List[Path]:
    dirs = []
    for it in os.scandir(str(directory)):
        if it.is_dir():
            dirs.append(directory.joinpath(it.name))
    return dirs


def list_files(directory: Path) -> List[Path]:
    for file in directory.iterdir():
        if file.is_file():
            yield file
