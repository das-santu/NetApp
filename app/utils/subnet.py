import ipaddress


def calculate_subnets(network_cidr: str, prefix_length: int):
    try:
        network = ipaddress.ip_network(network_cidr)
        if prefix_length <= network.prefixlen:
            raise ValueError("Prefix length must be greater than network prefix length")

        subnets = list(network.subnets(new_prefix=prefix_length))
        return [str(subnet) for subnet in subnets]
    except Exception as e:
        raise ValueError(f"Invalid input: {e}")


def find_free_subnet(network_cidr: str, prefix: int, existing_subnets: list[str]) -> str:
    """
    Find the first non-overlapping subnet of the given prefix within the network.
    """
    network = ipaddress.ip_network(network_cidr, strict=False)
    existing_subnet_objects = [ipaddress.ip_network(cidr, strict=False) for cidr in existing_subnets]

    # Generate all possible subnets of the given prefix within the network
    for possible_subnet in network.subnets(new_prefix=prefix):
        if not any(possible_subnet.overlaps(existing) for existing in existing_subnet_objects):
            return str(possible_subnet)  # Return the first non-overlapping subnet
    return None  # No free subnet available
