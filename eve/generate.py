from typing import List
from eve.models.device_configuration import JsonSchemaForNetworkConfiguration


def generate_device_configuration(
    config: JsonSchemaForNetworkConfiguration,
) -> List[str]:
    config_lines: List[str] = []
    config_lines.append(f'hostname {config.general.hostname}')
    config_lines.append(
        f'domain {config.general.fqdn.replace(config.general.hostname + ".", "")}'
    )
    location = f'{config.general.location.datacenter}/{config.general.location.room}{config.general.location.rack}{config.general.location.shelf}'
    config_lines.append(f'timezone {config.general.timezone}')
    config_lines.append(f'snmp location {location}')
    config_lines += get_interface_config(config)
    return config_lines


def get_interface_config(config: JsonSchemaForNetworkConfiguration) -> List[str]:
    interface_config = []
    for interface in config.interfaces:
        prefix = f'interface {interface.name}'
        interface_config.append(f'{prefix} description {interface.description}')
    return interface_config
