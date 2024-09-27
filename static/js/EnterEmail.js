// Get modal element for Email Update
var emailModal = document.getElementById("EnterEmail");

// Get the button that opens the modal
var emailBtn = document.getElementById("get_email_update");

// Get the <span> element that closes the modal
var emailSpan = document.getElementById("closeEmail");

// When the user clicks the button, open the modal
emailBtn.onclick = function() {
    emailModal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
emailSpan.onclick = function() {
    emailModal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == emailModal) {
        emailModal.style.display = "none";
    }
}
