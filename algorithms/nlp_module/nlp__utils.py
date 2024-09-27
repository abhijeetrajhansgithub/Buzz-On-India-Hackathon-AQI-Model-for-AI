import re
from collections import Counter
from typing import List

# Define a basic set of stop words (you can expand this list)
STOP_WORDS = {
    "the", "is", "in", "at", "of", "on", "and", "a", "me", "tell", "say", "brief"
    "to", "it", "that", "this", "for", "by", "with", "from", "about", "as",
    "an", "he", "she", "they", "we", "you", "are", "was", "were", "be",
    "or", "if", "but", "so", "then", "have", "has", "had", "can", "will",
    "would", "could", "should", "there", "here", "I", "my", "your", "their", "our", "its",
    "no", "yes", "not", "all", "some", "any", "do", "did", "does", "done",
    "up", "down", "out", "over", "under", "into", "back", "off", "just",
    "get", "make", "know", "want", "like", "say", "see", "go", "come", "take",
    "think", "look", "give", "find"
}



def clean_and_tokenize(text: str) -> List[str]:
    # Convert to lowercase, remove non-alphabetical characters, and tokenize
    tokens = re.findall(r'\b\w+\b', text.lower())
    # Remove stop words
    return [token for token in tokens if token not in STOP_WORDS]


def calculate_match_percentage(query_tokens: List[str], key_tokens: List[str]) -> float:
    # Create frequency counters for query and key tokens
    query_counter = Counter(query_tokens)
    key_counter = Counter(key_tokens)

    # Find the total number of matching tokens
    total_tokens = len(query_tokens)
    matching_tokens = sum((query_counter & key_counter).values())  # Intersection of token counts

    # Calculate the percentage of matching tokens
    return matching_tokens / total_tokens if total_tokens > 0 else 0


def query_key_comparator(query: str, key: str, threshold: float = 0.66667) -> bool:
    # Tokenize and clean both query and key
    query_tokens = clean_and_tokenize(query)
    key_tokens = clean_and_tokenize(key)

    # Calculate match percentage
    match_percentage = calculate_match_percentage(query_tokens, key_tokens)
    # print(match_percentage)

    # Compare match percentage with threshold
    return match_percentage > threshold


