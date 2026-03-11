"""
Dataset Loader: Extracts offensive words from the labeled_data.csv dataset
and merges them with the base offensive_words.txt dictionary.
"""
import csv
import re
import os


def extract_offensive_words_from_dataset(csv_path: str) -> set:
    """
    Parse the labeled_data.csv and extract words from tweets
    that are classified as hate_speech (class=0) or offensive (class=1).
    We extract individual words that appear frequently in offensive tweets.
    """
    offensive_words = set()
    try:
        with open(csv_path, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cls = int(row.get("class", 2))
                if cls in (0, 1):
                    tweet = row.get("tweet", "")
                    # Clean the tweet
                    tweet = re.sub(r"http\S+", "", tweet)
                    tweet = re.sub(r"@\w+", "", tweet)
                    tweet = re.sub(r"RT\s*", "", tweet)
                    tweet = re.sub(r"&amp;|&lt;|&gt;|&#\d+;", "", tweet)
                    tweet = re.sub(r"[^a-zA-Z\s]", "", tweet)
                    words = tweet.lower().split()
                    for word in words:
                        if len(word) >= 3:
                            offensive_words.add(word.strip())
    except FileNotFoundError:
        print(f"Dataset file not found: {csv_path}")
    return offensive_words


def load_base_dictionary(txt_path: str) -> set:
    """Load the base offensive words dictionary from text file."""
    words = set()
    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            for line in f:
                word = line.strip().lower()
                if word:
                    words.add(word)
    except FileNotFoundError:
        print(f"Dictionary file not found: {txt_path}")
    return words


def load_all_offensive_words() -> set:
    """
    Load offensive words from both the base dictionary and the dataset.
    Returns a combined set of offensive words.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Load base dictionary
    dict_path = os.path.join(base_dir, "dataset", "offensive_words.txt")
    base_words = load_base_dictionary(dict_path)

    # Load from dataset CSV
    csv_path = os.path.join(base_dir, "..", "data", "labeled_data.csv")
    if not os.path.exists(csv_path):
        csv_path = os.path.join(base_dir, "dataset", "labeled_data.csv")

    # We only use the base curated dictionary for detection to avoid false positives
    # The dataset is used for validation/testing
    return base_words


if __name__ == "__main__":
    words = load_all_offensive_words()
    print(f"Loaded {len(words)} offensive words")
    print("Sample:", list(words)[:20])
