document.addEventListener("DOMContentLoaded", function () {
    // Get all search bars and dropdown
    const searchBar1 = document.querySelector(".searchBar1");
    const searchBar2 = document.querySelector(".searchBar2");
    const searchBar3 = document.querySelector(".searchBar3");
    const dropdown = document.querySelector(".dropdown");

    // Set the debounce delay in milliseconds
    const debounceDelay = 500; // Adjust as needed

    // Add input and change event listeners with debounce
    searchBar1.addEventListener("input", debounce(() => handleSearch(), debounceDelay));
    searchBar2.addEventListener("input", debounce(() => handleSearch(), debounceDelay));
    searchBar3.addEventListener("input", debounce(() => handleSearch(), debounceDelay));
    dropdown.addEventListener("change", () => handleSearch());

    // Run sorting only on first load
    //sortListItems('descending');

    function sortListItems(order) {
        // Get all list items
        const listItems = document.querySelectorAll(".list-item");

        // Convert NodeList to Array for sorting
        const sortedListItems = Array.from(listItems).sort((a, b) => {
            const versionA = getVersionNumber(a);
            const versionB = getVersionNumber(b);
            // Compare major, minor, and patch versions
            if (order === 'ascending') {
                return versionA.compare(versionB);
            } else {
                return versionB.compare(versionA);
            }
        });

        // Reorder list items based on sorted array
        const container = document.querySelector(".container");
        container.innerHTML = ""; // Clear container
        sortedListItems.forEach(item => {
            container.appendChild(item);
        });

        // Re-enable the sort button after sorting is completed
        setTimeout(() => {
            const sortButton = document.getElementById("sortButton");
            sortButton.disabled = false;
        }, 1000); // Adjust the timeout as needed
    }

    function getVersionNumber(item) {
        const versionText = item.querySelector(".version").textContent.trim();
        // Extract version number parts
        const [, major, minor, patch, extra] = versionText.match(/(\d+)\.(\d+)\.(\d+)(?:-h(\d+))?/);
        // Convert parts to numbers and combine them
        return {
            major: parseInt(major),
            minor: parseInt(minor),
            patch: parseInt(patch || "0"),
            extra: extra ? parseInt(extra) : 0,
            compare: function (other) {
                if (this.major !== other.major) {
                    return this.major - other.major; // Sort major version
                }
                if (this.minor !== other.minor) {
                    return this.minor - other.minor; // Sort minor version
                }
                if (this.patch !== other.patch) {
                    return this.patch - other.patch; // Sort patch version
                }
                // If patch versions are the same, compare extra versions
                return this.extra - other.extra; // Sort extra version
            }
        };
    }

    function handleSearch() {
        // Get search values
        const searchValue1 = searchBar1.value.toLowerCase();
        const searchValue2 = searchBar2.value.toLowerCase();
        const searchValue3 = searchBar3.value.toLowerCase();

        // Get dropdown value
        const dropdownValue = dropdown.value;

        // Iterate through list items and check for matches
        const listItems = document.querySelectorAll(".list-item");
        listItems.forEach(item => {
            const columnText1 = item.querySelector(".column:nth-child(2)").textContent.toLowerCase();
            const columnText2 = item.querySelector(".column:nth-child(3)").textContent.toLowerCase();
            const columnText3 = item.querySelector(".column:nth-child(4)").textContent.toLowerCase();
            const knownAddressedText = item.querySelector(".knownAddressed").textContent.toLowerCase();

            // Check if the list item should be displayed based on search and dropdown values
            const matchesSearch = columnText1.includes(searchValue1) &&
                columnText2.includes(searchValue2) &&
                matchPartialWords(columnText3, searchValue3);

            const matchesDropdown = (dropdownValue === "both") ||
                (dropdownValue === "known" && knownAddressedText.includes("known")) ||
                (dropdownValue === "addressed" && knownAddressedText.includes("addressed"));

            // Show/hide the list item based on the matches
            if (matchesSearch && matchesDropdown) {
                item.style.display = "flex";
            } else {
                item.style.display = "none";
            }
        });
    }

    function matchPartialWords(columnText, searchValue) {
        // Split the search value into words
        const searchWords = searchValue.split(/\s+/);

        // Check if all search words are present in the column text
        return searchWords.every(word => columnText.includes(word));
    }

    // Debounce function to delay the execution of a function
    function debounce(func, delay) {
        let timeoutId;
        return function () {
            const context = this;
            const args = arguments;
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => {
                func.apply(context, args);
            }, delay);
        };
    }

    // Sorting button
    const sortButton = document.getElementById("sortButton");
    let sortOrder = 'ascending';
    //sortButton.innerHTML = "Sort &#9660;"; // Down arrow
    sortButton.addEventListener("click", function () {
        // Disable the sort button
        this.disabled = true;

        sortOrder = sortOrder === 'ascending' ? 'descending' : 'ascending';
        sortListItems(sortOrder);
        this.innerHTML = sortOrder === 'ascending' ? "Sort &#9650;" : "Sort &#9660;";
    });
});
