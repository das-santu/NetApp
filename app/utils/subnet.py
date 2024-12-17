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


def find_free_subnet(network_cidr, existing_subnets, prefix):
    # Convert network CIDR into an ipaddress network object
    parent_network = ipaddress.ip_network(network_cidr)
    used_subnets = [ipaddress.ip_network(subnet.subnet) for subnet in existing_subnets]

    # Generate subnets with the desired prefix length
    for candidate in parent_network.subnets(new_prefix=prefix):
        if candidate not in used_subnets:
            return str(candidate)  # Return first available subnet
    return None
