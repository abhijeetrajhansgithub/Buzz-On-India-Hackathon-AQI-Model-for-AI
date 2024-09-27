// Get modal element for AQI Update
var aqiModal = document.getElementById("AQIupdateModel");

// Get the button that opens the modal
var aqiBtn = document.getElementById("AQI_update");

// Get the <span> element that closes the modal
var aqiSpan = document.getElementById("closeAQIUpdate");

// When the user clicks the button, open the modal
aqiBtn.onclick = function() {
    aqiModal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
aqiSpan.onclick = function() {
    aqiModal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target === aqiModal) {
        aqiModal.style.display = "none";
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('AQIupdateModel');
    const closeModalBtn = document.getElementById('closeAQIUpdate');
    const form = document.getElementById('inputForm-for-aqi');
    const resultElement = document.getElementById('aqi-update-result').querySelector('span');

    // Close modal when the "x" button is clicked
    closeModalBtn.onclick = function() {
        modal.style.display = 'none';
    };

    // Fetch API for AQI update when the form is submitted
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent form from refreshing the page

        // Send a POST request to the Flask backend to get AQI update
        fetch('/get_aqi_results', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then(response => response.json())
        .then(data => {
            // Display the AQI update result inside the modal
            resultElement.innerHTML = data.message;
            resultElement.style.color = 'maroon'

            // Optionally, keep the modal open to display results
            modal.style.display = 'block';
        })
        .catch(error => {
            console.error('Error:', error);
            resultElement.innerHTML = 'Failed to get the result. Please try again later.';
        });
    });

    // Optional: If you want the modal to close when clicked outside the modal content
    window.onclick = function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    };
});

