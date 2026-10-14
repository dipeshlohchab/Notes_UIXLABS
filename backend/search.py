"""Search helpers: parsing, MongoDB filter, and ranking."""
import re


def parse_query(q: str) -> list[str]:
    """Split a query into distinct, lowercased words (order preserved)."""
    words: list[str] = []
    for w in q.lower().split():
        if w not in words:
            words.append(w)
    return words


def mongo_filter(words: list[str]) -> dict:
    """Every word must appear (case-insensitive) in the title or the body."""
    if not words:
        return {}
    return {
        "$and": [
            {
                "$or": [
                    {"title": {"$regex": re.escape(w), "$options": "i"}},
                    {"body": {"$regex": re.escape(w), "$options": "i"}},
                ]
            }
            for w in words
        ]
    }


def title_score(note: dict, words: list[str]) -> int:
    """Number of distinct search words found in the title."""
    title = note["title"].lower()
    return sum(1 for w in words if w in title)


def rank(notes: list[dict], words: list[str]) -> list[dict]:
    """Most distinct title matches first, then most recently updated."""
    return sorted(
        notes,
        key=lambda n: (title_score(n, words), n["updated_at"]),
        reverse=True,
    )
