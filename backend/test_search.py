from datetime import datetime, timedelta, timezone

from search import mongo_filter, parse_query, rank, title_score

T0 = datetime(2026, 1, 1, tzinfo=timezone.utc)


def note(title, days=0):
    return {"title": title, "body": "", "updated_at": T0 + timedelta(days=days)}


def test_parse_query_lowercases_and_dedupes():
    assert parse_query("  Foo foo BAR ") == ["foo", "bar"]
    assert parse_query("   ") == []


def test_filter_requires_every_word():
    f = mongo_filter(["a", "b"])
    assert len(f["$and"]) == 2
    assert mongo_filter([]) == {}


def test_filter_escapes_regex_characters():
    f = mongo_filter(["c++"])
    assert f["$and"][0]["$or"][0]["title"]["$regex"] == r"c\+\+"


def test_title_score_counts_distinct_words():
    assert title_score(note("Red red Apple"), ["red", "apple", "pear"]) == 2


def test_rank_by_title_matches_then_recency():
    both_old = note("apple pie", days=1)
    one_new = note("apple", days=5)
    one_newest = note("pie", days=9)
    zero = note("misc", days=20)  # matched via body only
    ranked = rank([zero, one_new, both_old, one_newest], ["apple", "pie"])
    assert ranked == [both_old, one_newest, one_new, zero]
