import requests
from bs4 import BeautifulSoup
import re


def extract_data_from_url(url):
    """
    Extract IPv4, IPv6 addresses, and domain-style URLs from the content of a given URL.

    Args:
        url (str): The URL to fetch and parse.

    Returns:
        list: A list of extracted IPv4, IPv6 addresses, and URLs.
    """
    try:
        response = requests.get(url)
        print(response.text)
        response.raise_for_status()  # Ensure the request was successful
        
        # Regex patterns
        ipv4_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}(?:/\d{1,2})?\b'
        ipv6_pattern = r'\b(?:[a-fA-F0-9]{1,4}:){1,7}:?(?:[a-fA-F0-9]{1,4})?(?:/\d{1,3})?\b'
        url_pattern = r'\b(?:https?://)?(?:\*\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'

        # Combine results
        ipv4_matches = re.findall(ipv4_pattern, response.text)
        ipv6_matches = re.findall(ipv6_pattern, response.text)
        url_matches = re.findall(url_pattern, response.text)
        
        ipv6_matches = re.findall(ipv6_pattern, response.text)
        print("IPv6 Matches:", ipv6_matches)



        return ipv4_matches + ipv6_matches + url_matches
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []


def main():

    url = "https://saasedl.paloaltonetworks.com/feeds/googleworkspace/all/ipv6"
    extract_data_from_url(url)

if __name__ == "__main__":
    main()
