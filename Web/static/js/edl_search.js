// Function to handle button click and activate the corresponding button
function setSearchType(type) {
    // Remove active class from all buttons
    document.querySelectorAll('.searchTypeButton').forEach(button => {
        button.classList.remove('active');
    });

    // Add active class to the clicked button
    document.getElementById(type + 'Button').classList.add('active');

    // Set the selected search type (optional, depending on your use case)
    selectedSearchType = type;

    // Update the placeholder and clear the search input
    updatePlaceholder(type);

    // Clear the input field and focus the cursor there
    const searchInput = document.getElementById('searchInput');
    searchInput.value = '';  // Clear the input field
    searchInput.focus();     // Set the cursor focus to the input field
}

// Function to update the input placeholder based on selected search type
function updatePlaceholder(type) {
    const searchInput = document.getElementById('searchInput');
    if (type === 'ipv4') {
        searchInput.placeholder = 'Enter IPv4 address';
    } else if (type === 'ipv6') {
        searchInput.placeholder = 'Enter IPv6 address';
    } else if (type === 'url') {
        searchInput.placeholder = 'Enter URL';
    }
}

// Function to perform the EDL search by calling the FastAPI endpoint
async function searchEDL() {
    const searchInput = document.getElementById('searchInput').value;
    const selectedType = document.querySelector('.searchTypeButton.active').id.replace('Button', '').toLowerCase();

    const resultsContainer = document.getElementById("results");
    resultsContainer.innerHTML = ""; // Clear previous results

    if (!searchInput) {
        resultsContainer.innerHTML = "<p>Please enter a search term.</p>";
        return;
    }

    // Prepare the request body
    const requestData = {
        search_type: selectedType,
        user_input: searchInput
    };

    try {
        // Send the request to the FastAPI backend
        const response = await fetch("/api/search", {  
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(requestData),
        });

        // Check if the response is ok (status 200-299)
        if (response.ok) {
            const results = await response.json();
            displayResults(results);
        } else {
            throw new Error("Failed to fetch results");
        }
    } catch (error) {
        console.error(error);
        resultsContainer.innerHTML = "<p>Error occurred while searching. Please try again.</p>";
    }
}

// Function to display the search results in the 'results' div
function displayResults(results) {
    const resultsContainer = document.getElementById("results");
    resultsContainer.innerHTML = ""; // Clear previous results

    if (results.length === 0) {
        resultsContainer.innerHTML = "<p>No results found.</p>";
    } else {
        results.forEach(result => {
            const resultDiv = document.createElement("div");
            resultDiv.classList.add("list-item");

            // Split the result into 'EDL Name' and 'Data'
            const [edlName, data] = result.split(", Data: ");
            
            // Create the HTML for bold EDL Name and Data
            const boldEdlName = `<strong>${edlName.replace("EDL Name: ", "")}</strong>`;
            const boldData = `<strong>${data}</strong>`;
            
            // Construct the result with "EDL Name: " and the bold Data
            const resultHtml = `EDL Name: ${boldEdlName}, Data: ${boldData}`;

            resultDiv.innerHTML = resultHtml;
            resultsContainer.appendChild(resultDiv);
        });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // Set default to IPv4
    updatePlaceholder('ipv4');

    // Add event listener for Enter key press on the input field
    const searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('keydown', function(event) {
        // Check if the pressed key is "Enter"
        if (event.key === 'Enter') {
            // Prevent form submission if the input is inside a form (optional)
            event.preventDefault();
            // Trigger the search function
            searchEDL();
        }
    });
});
