import requests
from bs4 import BeautifulSoup
import re

def scrape_links(url, EDL_List_output_file):
    """
    Scrape the links starting with 'https://saasedl' and their corresponding names from the given URL,
    and save the results in a text file.

    Args:
        url (str): The URL to scrape.
        EDL_List_output_file (str): The file path to save the results.
    """
    # Fetch the page content
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful

    # Parse the page content using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Locate the <div class="container">
    container = soup.find("div", class_="container")

    # Initialize a list to store the results
    results = []

    # Iterate through all rows in the container
    if container:
        for row in container.find_all("tr"):
            # Extract the name from the <td class="text-nowrap"> element
            name_cell = row.find("td", class_="text-nowrap")
            name = name_cell.get_text(strip=True) if name_cell else None
            
            # If a name exists, find the first matching <a> tag
            if name:
                first_link = row.find("a", href=True)
                if first_link and first_link["href"].startswith("https://saasedl"):
                    # Add only the first link for this name to the results
                    results.append(f"Name: {name}, Link: {first_link['href']}")

    # Write the results to a text file
    with open(EDL_List_output_file, "w") as file:
        for result in results:
            file.write(result + "\n")

def load_edl_mapping(EDL_List_output_file):
    """
    Load the EDL mapping from the EDL-List file.

    Args:
        EDL_List_output_file (str): Path to the EDL list file.

    Returns:
        dict: A dictionary mapping URLs to their corresponding EDL names.
    """
    edl_mapping = {}
    with open(EDL_List_output_file, "r") as file:
        for line in file:
            # Parse lines in the format: "Name: <name>, Link: <url>"
            if line.startswith("Name:") and "Link:" in line:
                parts = line.split(", ")
                name = parts[0].replace("Name: ", "").strip()
                link = parts[1].replace("Link: ", "").strip()
                edl_mapping[link] = name
    return edl_mapping

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
        response.raise_for_status()  # Ensure the request was successful
        
        # Regex patterns
        ipv4_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}(?:/\d{1,2})?\b'
        ipv6_pattern = r'\b(?:[a-fA-F0-9]{1,4}:){1,7}:?(?:[a-fA-F0-9]{1,4})?(?:/\d{1,3})?\b'
        url_pattern = r'\b(?:https?://)?(?:\*\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'

        # Combine results
        ipv4_matches = re.findall(ipv4_pattern, response.text)
        ipv6_matches = re.findall(ipv6_pattern, response.text)
        url_matches = re.findall(url_pattern, response.text)
        
        return ipv4_matches + ipv6_matches + url_matches
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

def process_urls(EDL_List_output_file, edl_with_data_output_file):
    """
    Process the URLs in the EDL list, extract data (IPv4, IPv6, URLs) and associate them with EDL names,
    and save the results to a file.

    Args:
        EDL_List_output_file (str): Path to the file containing EDL list (name and URL).
        edl_with_data_output_file (str): Path to the file to save extracted data and their EDL names.
    """
    # Load EDL mapping
    edl_mapping = load_edl_mapping(EDL_List_output_file)
    
    # Initialize a list to store the results
    results = []

    # Process each URL in the mapping
    for url, name in edl_mapping.items():
        print(f"Processing EDL: {name} ({url})")
        data = extract_data_from_url(url)
        for entry in data:
            results.append(f"EDL Name: {name}, Data: {entry}")
    
    # Write the results to the output file
    with open(edl_with_data_output_file, "w") as file:
        for result in results:
            file.write(result + "\n")

    print(f"Results saved to {edl_with_data_output_file}")


def main():
    # Define the URL to scrape and the output file path
    # Define the EDL list file and output file
    url = "https://docs.paloaltonetworks.com/resources/edl-hosting-service"
    EDL_List_output_file = "EDL-List.txt"
    edl_with_data_output_file = "extracted_data_with_edls.txt"
    
    # Call the scrape_links function
    scrape_links(url, EDL_List_output_file)
    print(f"Results saved to {EDL_List_output_file}")
   
    # Process the URLs and extract IPs
    process_urls(EDL_List_output_file, edl_with_data_output_file)

if __name__ == "__main__":
    main()
