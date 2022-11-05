"""
Utilities for string matching, particularly for search functionalities.
"""

from rapidfuzz import process


def fuzzy_match_list(text, txt_list, min_score=90) -> bool:
    """Check if a string is in a list using fuzzy matching."""
    return any(process.extract(text, txt_list, score_cutoff=min_score))


def fuzzy_match_list_choice(text, txt_list, min_score=90) -> list:
    """Return best matches in a list using fuzzy matching."""
    return (a[0] for a in process.extract(text, txt_list, score_cutoff=min_score))
