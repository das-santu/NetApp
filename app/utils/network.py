import ipaddress


def calculate_network_utilization(network, reserved_subnets) -> dict:

    # Get network cidr
    network_cidr = ipaddress.ip_network(network.cidr, strict=False)
    total_ips = network_cidr.num_addresses
    used_ips = 0

    # Calculate Used IPs
    for subnet in reserved_subnets:
        subnet_cidr = ipaddress.ip_network(subnet.subnet, strict=False)
        used_ips += subnet_cidr.num_addresses

    # Calculate Percentages
    reserved_percentage = (used_ips / total_ips) * 100
    available_percentage = 100 - reserved_percentage

    return {
        "network": network.cidr,
        "total_ips": total_ips,
        "used_ips": used_ips,
        "reserved_percentage": round(reserved_percentage, 2),
        "available_percentage": round(available_percentage, 2),
    }
