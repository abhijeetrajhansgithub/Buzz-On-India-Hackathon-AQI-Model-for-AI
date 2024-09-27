
document.getElementById('suggestionsIcon').onclick = function() {
    document.getElementById('suggestionsModal').style.display = "block";
}

document.getElementById('suggestions-modalClose').onclick = function() {
    document.getElementById('suggestionsModal').style.display = "none";
}

window.onclick = function(event) {
    if (event.target === document.getElementById('suggestionsModal')) {
        document.getElementById('suggestionsModal').style.display = "none";
    }
}