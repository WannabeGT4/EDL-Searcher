from fastapi import FastAPI
from pydantic import BaseModel
import ipaddress
import re
from typing import List, Tuple

app = FastAPI()

class SearchRequest(BaseModel):
    search_type: str
    user_input: str

def load_data_from_file(file_path: str) -> List[Tuple[str, str]]:
    """Loads and parses data from the specified file."""
    data = []
    with open(file_path, "r") as file:
        for line in file:
            if "EDL Name:" in line and "Data:" in line:
                parts = [p.strip() for p in line.strip().split(", ")]
                if len(parts) == 2:
                    edl_name = parts[0].replace("EDL Name: ", "")
                    data_entry = parts[1].replace("Data: ", "")
                    data.append((edl_name, data_entry))
    return data

def is_ipv4(address: str) -> bool:
    """Checks if the address is a valid IPv4 address."""
    try:
        ip = ipaddress.ip_address(address)
        return isinstance(ip, ipaddress.IPv4Address)
    except ValueError:
        return False

def is_ipv6(address: str) -> bool:
    """Checks if the address is a valid IPv6 address."""
    try:
        ip = ipaddress.ip_address(address)
        return isinstance(ip, ipaddress.IPv6Address)
    except ValueError:
        return False

def is_cidr(address: str) -> bool:
    """Checks if the address is in CIDR notation (e.g., 76.223.80.89/32)."""
    return '/' in address

def search_data(user_input: str, data: List[Tuple[str, str]], search_type: str) -> List[str]:
    """Searches for matching EDL entries based on the input type."""
    results = []
    
    try:
        if search_type in {"ipv4", "ipv6"}:
            user_network = ipaddress.ip_network(user_input, strict=False)
            for edl_name, entry in data:
                try:
                    entry_network = ipaddress.ip_network(entry, strict=False)
                    if user_network.version == entry_network.version and (
                        user_network.subnet_of(entry_network) or
                        user_network.supernet_of(entry_network) or
                        user_network == entry_network
                    ):
                        results.append(f"EDL Name: {edl_name}, Data: {entry}")
                except ValueError:
                    continue  # Skip non-IP data
        elif search_type == "url":
            # URL search - exclude IPv4 and IPv6 addresses
            for edl_name, entry in data:
                # Skip entries that are IPv4 or IPv6 addresses, or CIDR blocks
                if is_ipv4(entry) or is_ipv6(entry) or is_cidr(entry):
                    continue  # Skip IPv4/IPv6 entries and CIDR blocks
                if user_input in entry:
                    results.append(f"EDL Name: {edl_name}, Data: {entry}")
        elif search_type == "ipv4":
            # Exact IPv4 search - match against specific address (not CIDR)
            for edl_name, entry in data:
                if is_ipv4(entry):
                    # Check if the entry is just an IP address (not a network)
                    ip = entry.split('/')[0]  # Strip off the CIDR part if present
                    if user_input == ip:
                        results.append(f"EDL Name: {edl_name}, Data: {entry}")
    except ValueError:
        return []  # Return empty if the user input is invalid

    return results

@app.post("/api/search", response_model=List[str])
async def search(request: SearchRequest):
    """API endpoint to handle search requests."""
    data = load_data_from_file("/var/www/html/data/extracted_data_with_edls.txt")
    return search_data(request.user_input, data, request.search_type)
