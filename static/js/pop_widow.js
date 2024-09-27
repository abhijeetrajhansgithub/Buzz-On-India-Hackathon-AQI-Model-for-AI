// Get modal element for Manual Input
var manualModal = document.getElementById("manualInputModal");

// Get the button that opens the modal
var manualBtn = document.getElementById("manual_input");

// Get the <span> element that closes the modal
var manualSpan = document.getElementById("closeManualInput");

// When the user clicks the button, open the modal
manualBtn.onclick = function() {
    manualModal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
manualSpan.onclick = function() {
    manualModal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target === manualModal) {
        manualModal.style.display = "none";
    }
}
