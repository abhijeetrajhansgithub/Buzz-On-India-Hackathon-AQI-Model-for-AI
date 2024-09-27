// Get the necessary elements
const summarizerLabel = document.getElementById('summarizerLabel');
const summarizerPopup = document.getElementById('summarizerPopup');

// Toggle popup display on click
summarizerLabel.addEventListener('click', function () {
    if (summarizerPopup.style.display === 'block') {
        summarizerPopup.style.display = 'none';  // Hide popup if it's already displayed
    } else {
        summarizerPopup.style.display = 'block';  // Show popup on click
        fetchSummary();  // Fetch summary when opening the popup
    }
});

// Function to fetch and display summary text in the popup
async function fetchSummary() {
    try {
        let response = await fetch('/get_summary');
        if (response.ok) {
            let summaryText = await response.text();
            document.getElementById('summarizerText').textContent = summaryText;
        } else {
            document.getElementById('summarizerText').textContent = "Error loading summary";
        }
    } catch (error) {
        document.getElementById('summarizerText').textContent = "Error fetching summary";
    }
}

// Hide the popup when clicking outside of it
window.addEventListener('click', function (event) {
    if (event.target !== summarizerLabel && !summarizerPopup.contains(event.target)) {
        summarizerPopup.style.display = 'none';  // Hide popup if click is outside
    }
});
