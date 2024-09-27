document.addEventListener("DOMContentLoaded", function() {
    // Ensure the DOM is fully loaded before attaching events

    // Get the modal and icon elements
    var forumModal = document.getElementById('communityForumModal');
    var forumIcon = document.getElementById('communityForumIcon');
    var closeForumModal = document.getElementById('closeForumModal');
    var submitBtn = document.getElementById('forumSubmitBtn');

    // Open the modal when the icon is clicked
    forumIcon.addEventListener("click", function() {
        forumModal.style.display = "block";
        loadComments();  // Load comments when the modal is opened
    });

    // Close the modal when the close (x) button is clicked
    closeForumModal.addEventListener("click", function() {
        forumModal.style.display = "none";
    });

    // Close the modal when the user clicks anywhere outside the modal
    window.addEventListener("click", function(event) {
        if (event.target === forumModal) {
            forumModal.style.display = "none";
        }
    });

    // Submit comment when button is clicked
    submitBtn.addEventListener("click", function() {
        postComment();  // Post the comment and reload the conversation
    });

    // Function to fetch and load comments into the modal
    async function loadComments() {
        try {
            let response = await fetch('/get_comments');
            if (response.ok) {
                let comments = await response.json();
                let conversationHistory = document.getElementById('forumConversationHistory');
                conversationHistory.innerHTML = '';  // Clear previous comments

                comments.forEach(commentObj => {
                    // Create a container for each comment
                    let commentContainer = document.createElement('div');
                    commentContainer.classList.add('comment-container');

                    // Create and style the timestamp element
                    let timestampElement = document.createElement('span');
                    timestampElement.classList.add('comment-timestamp');
                    timestampElement.textContent = `${commentObj.timestamp}`;

                    // Create and style the comment text element
                    let commentElement = document.createElement('span');
                    commentElement.classList.add('comment-text');
                    commentElement.textContent = ` ${commentObj.comment}`;

                    // Append timestamp and comment text to the container
                    commentContainer.appendChild(timestampElement);
                    commentContainer.appendChild(document.createElement('br'));
                    commentContainer.appendChild(document.createElement('br'));
                    commentContainer.appendChild(commentElement);
                    conversationHistory.appendChild(commentContainer);
                });
            }
        } catch (error) {
            console.error('Error loading comments:', error);
        }
    }

    // Function to post a new comment
    async function postComment() {
        let commentInput = document.getElementById('forumUserInput').value;

        if (commentInput.trim() === '') {
            alert('Please enter a comment!');
            return;
        }

        try {
            let response = await fetch('/post_comment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ comment: commentInput })
            });

            if (response.ok) {
                document.getElementById('forumUserInput').value = '';  // Clear the input field
                loadComments();  // Reload comments after posting
            } else {
                console.error('Failed to post comment');
            }
        } catch (error) {
            console.error('Error posting comment:', error);
        }
    }
});

