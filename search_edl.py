import ipaddress

def load_data_from_file(file_path):
    """
    Load the EDL data from the given file.
    
    Args:
        file_path (str): The path to the file containing the EDL data.
        
    Returns:
        list: A list of tuples containing EDL Name and Data.
    """
    data = []
    with open(file_path, "r") as file:
        for line in file:
            if "EDL Name:" in line and "Data:" in line:
                parts = line.strip().split(", ")
                edl_name = parts[0].replace("EDL Name: ", "").strip()
                data_entry = parts[1].replace("Data: ", "").strip()
                data.append((edl_name, data_entry))
    return data

def search_data(user_input, data, search_type):
    """
    Search for the user input in the data based on the search type (IPv4, IPv6, or URL).
    
    Args:
        user_input (str): The user input to search for.
        data (list): The list of tuples containing EDL Name and Data.
        search_type (str): The type of data to search for ('ipv4', 'ipv6', 'url').
        
    Returns:
        list: A list of matching EDL names and data entries.
    """
    results = []

    try:
        if search_type == 'ipv4' or search_type == 'ipv6':
            user_network = ipaddress.ip_network(user_input, strict=False)

            for edl_name, entry in data:
                try:
                    entry_network = ipaddress.ip_network(entry, strict=False)

                    # Ensure both are of the same IP version before comparison
                    if user_network.version == entry_network.version:
                        if user_network.subnet_of(entry_network) or user_network.supernet_of(entry_network) or user_network == entry_network:
                            results.append(f"EDL Name: {edl_name}, Data: {entry}")

                except ValueError:
                    continue  # Skip non-IP entries for IP searches
        elif search_type == 'url':
            for edl_name, entry in data:
                if user_input in entry:
                    results.append(f"EDL Name: {edl_name}, Data: {entry}")

    except ValueError:
        print("Invalid input format.")
    
    return results

def main():
    # Load the data from the extracted file
    file_path = "extracted_data_with_edls.txt"
    data = load_data_from_file(file_path)
    
    # Ask the user for the type of search (ipv4, ipv6, or url)
    search_type = input("Enter the search type (ipv4, ipv6, url): ").strip().lower()
    if search_type not in ['ipv4', 'ipv6', 'url']:
        print("Invalid search type. Please enter 'ipv4', 'ipv6', or 'url'.")
        return
    
    # Ask the user for the search term
    user_input = input(f"Enter the {search_type} to search for: ").strip()
    
    # Perform the search
    results = search_data(user_input, data, search_type)
    
    if results:
        print("\nMatching results:")
        for result in results:
            print(result)
    else:
        print(f"No matches found for {search_type}: {user_input}")

if __name__ == "__main__":
    main()
