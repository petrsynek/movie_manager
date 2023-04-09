
function run() {
    // Main function to run the scrip when the page loads
    // Ensures that the internal variables are not accessible from the console polluting global scope

    var enabledFilters = {}

    const currentUrl = window.location.href;

    // Function to create the filter checkboxes
    function createFilterSet(filters) {
        const container = document.getElementById("checkbox-set");

        // For each key in the filters object
        for (const key in filters) {
            // Create a new paragraph element with name of the field
            const p = document.createElement("p");
            p.style.fontWeight = "bold"
            p.style.padding = "10px";
            p.style.backgroundColor = "#4c5063";
            p.style.color = "#fcfcfc";
            p.textContent = key.toUpperCase();
            container.appendChild(p);

            // Create a checkbox for each value in the field
            const values = filters[key];
            for (const value of values) {
                const label = document.createElement("label");
                label.style.fontSize = "10px";
                const checkbox = document.createElement("input");
                checkbox.type = "checkbox";
                checkbox.name = key;
                checkbox.value = value;

                // Add event listener to the checkbox that will invoke the search function
                checkbox.onchange = function() {
                    search();
                }
                label.appendChild(checkbox);
                label.appendChild(document.createTextNode(value));
                container.appendChild(label);
            }
        }
    }

    // Function to fetch the filters from the server
    async function fetchFilters() {
        const response = await fetch(`${currentUrl}api/searchfields`);
        filterData = await response.json();
        createFilterSet(filterData);
    }


    // Function that retrieves the filters from the checkboxes for use in search
    function getCheckedFilters() {
        const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
        let filters = {};
        checkboxes.forEach((checkbox) => {
            if (filters[checkbox.name]) {
                filters[checkbox.name].push(checkbox.value);
            } else {
                filters[checkbox.name] = [checkbox.value];
            }
        });
        return filters;
    }

    // Ordering switch
    function toggleOrder() {
        // h
        var switchVariable = document.getElementById("ordering-switch");
        var switchButton = document.getElementById("switch-button");

        if (switchButton.innerHTML === "Name: Ascending") {
            switchButton.innerHTML = "Name: Descending";
            switchVariable.value = "false";
        } else {
            switchButton.innerHTML = "Name: Ascending";
            switchVariable.value = "true";
        }
        search();
    }

    // Bind the toggleOrder function to the switch button
    var switchButton = document.getElementById("switch-button");
    switchButton.onclick = toggleOrder;

    // Set the range of pages to show
    const startNumber = 1;
    var endNumber = 1;

    // Set the initial selected page to None
    var selectedNumber = 1;

    function updateSelectedNumberDisplay() {
        // Create an array of numbers to show
        const numbers = Array.from({length: endNumber - startNumber + 1}, (_, index) => startNumber + index);

        // Get the container element to hold the number elements
        const numbersContainer = document.getElementById('numbers-container');

        // Create and add the number elements to the container
        numbersContainer.innerHTML = '';
        for (let i = 0; i < numbers.length; i++) {
            const numberElement = document.createElement('div');
            numberElement.classList.add('number-element');
            numberElement.textContent = numbers[i];
            numberElement.addEventListener('click', () => {
                // Set the selected number variable and update the display
                selectedNumber = numbers[i];
                // Update the page content
                renderData();
                // Remove the 'active' class from all number elements
                document.querySelectorAll('.number-element').forEach(element => element.classList.remove('active'));
                // Add the 'active' class to the clicked number element
                numberElement.classList.add('active');
            });
            numbersContainer.appendChild(numberElement);
            if (numbers[i] === selectedNumber) {
                numberElement.classList.add('active');
            }
        }
    }

    // Call the updateSelectedNumberDisplay function to set the initial display
    updateSelectedNumberDisplay();


    var moviesData = [];

    const imagesPerPage = 10;

    // Function to display the movies on the page
    function renderData() {
        // If there is no data, return
        if (moviesData.length === 0) {
            const resultsDiv = document.getElementById("results");
            resultsDiv.innerHTML = "";
            return;
        }

        // Get the container element to hold the results
        const resultsDiv = document.getElementById("results");
        resultsDiv.innerHTML = "";
        for (let i = (selectedNumber-1)*imagesPerPage; i < Math.min((selectedNumber)*imagesPerPage, moviesData.length) ; i++) {

            const card = document.createElement("div");
            card.className = "card";
            card.value = moviesData[i].name; // this is here for on click function
            card.addEventListener("click", openInFrame)

            const image = document.createElement("img");
            image.src = moviesData[i].image;
            image.value = moviesData[i].name; // this is here for on click function

            const name = document.createElement("p");
            name.innerHTML = moviesData[i].name;
            name.value = moviesData[i].name; // this is here for on click function

            card.appendChild(image);
            card.appendChild(name);
            resultsDiv.appendChild(card);
        }
    }

    // Function to fetch and display movie details in a frame
    function openInFrame (event) {
        // Get the information from the card values
        // as this has to be on every elements in the card i had to add it to all of them in the renderData function
        // definitely not the best way to do it but it works
        var movieTitle = event.target.value;

        // Fetch the dictionary data
        fetch(`${currentUrl}api/moviedetail?movie_name=${movieTitle}`)
        .then(function(response) {
            return response.json();
        }) // this then notation is way more cool, but I'm not going to rewrite the whole thing
        .then(function(dictionary) {
            // Display the dictionary and card information in frame
            var frame = document.createElement("div");
            frame.classList.add("frame");

            var dictionaryDisplay = document.createElement("div");
            dictionaryDisplay.classList.add("dictionary-display");
            dictionaryDisplay.innerHTML = "<strong>Title:</strong> " + movieTitle + "<br><br>" +
            "<strong>Description:</strong> " + '<pre>' + JSON.stringify(dictionary, null, 4) + '</pre>';

            frame.appendChild(dictionaryDisplay);
            document.body.appendChild(frame);

            // Add a click event listener to the frame to close it when clicked
            frame.addEventListener("click", function() {
            document.body.removeChild(frame);
            });
        })
        .catch(function(error) {
            console.error(error);
        });
    }

    // Function that querries the API for search results
    async function search() {
        // Get the search term from the search box
        const query = document.getElementById("search-box").value || "";

        // Get the ordering switch value
        var switchVariable = document.getElementById("ordering-switch");

        // Get the filters
        const filters = JSON.stringify(getCheckedFilters());

        // Fetch the search results from the API
        const response = await fetch(`${currentUrl}api/search?search_term=${query}&order=${switchVariable.value}&filters=${filters}`);
        moviesData = await response.json();

        // Reset the page content and variables
        selectedNumber = 1;
        endNumber = Math.ceil(moviesData.length/imagesPerPage);

        // Update the page content
        updateSelectedNumberDisplay();
        renderData();
    }

    // Bind the search function on keyup event of the search box
    const searchBox = document.getElementById("search-box");
    searchBox.addEventListener("keyup", function(event) {
        search();
    });

    // Make the initial search
    fetchFilters();
    search();
}
