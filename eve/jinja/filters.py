from ipaddress import ip_address, ip_interface, ip_network
import ansible.plugins.filter.core
import ansible_collections

_registered_jinja_filters = []
_imported_jinja_filters = [
    (
        ansible.plugins.filter.core,
        [
            "regex_search",
            "regex_replace",
            "to_json",
            "to_yaml",
            "to_nice_yaml",
            "b64decode",
            ("get_hash", "hash"),
            ("get_encrypted_password", "password_hash"),
        ],
    ),
    (
        ansible_collections.ansible.netcommon.plugins.filter.ipaddr,
        ["ipaddr", "ipmath", "ipsubnet", "ipv4", "ipv6", "cidr_merge", "hwaddr"],
    ),
]


def jinjafilter(f):
    '''Adds the filter'''
    _registered_jinja_filters.append(f)
    return f


@jinjafilter
def ipv(address) -> int:
    '''Returns the IP Version as an integer'''
    net = ip_network(address)
    return net.version
