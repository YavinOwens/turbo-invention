from pathlib import Path
from turbo_invention.sar_ingest.facebook import FacebookParser

FIX = Path(__file__).parent / "fixtures"


def test_parses_posts_and_comments(tmp_path: Path):
    # mirror Meta's folder layout
    (tmp_path / "your_facebook_activity/posts").mkdir(parents=True)
    (tmp_path / "your_facebook_activity/comments_and_reactions").mkdir(parents=True)
    (tmp_path / "your_facebook_activity/posts/your_posts__check_ins__photos_and_videos_1.json"
     ).write_text((FIX / "posts_sample.json").read_text())
    (tmp_path / "your_facebook_activity/comments_and_reactions/comments.json"
     ).write_text((FIX / "comments_sample.json").read_text())

    docs = list(FacebookParser(tmp_path).iter_documents())
    kinds = {d.kind for d in docs}
    assert "post" in kinds
    assert "comment" in kinds
    assert all(d.platform == "facebook" for d in docs)
    assert any("machine learning" in d.text.lower() for d in docs)
    assert any(d.text == "Great work!" for d in docs)


def test_dry_run_lists_unknown_keys(tmp_path: Path, capsys):
    (tmp_path / "your_facebook_activity/posts").mkdir(parents=True)
    (tmp_path / "your_facebook_activity/posts/mystery_new_file.json"
     ).write_text('[{"weird_new_key": 1}]')
    FacebookParser(tmp_path).dry_run()
    out = capsys.readouterr().out
    assert "mystery_new_file.json" in out
    assert "weird_new_key" in out


def test_comment_ids_unique_when_entry_has_multiple_data_items(tmp_path: Path):
    import json
    (tmp_path / "your_facebook_activity/comments_and_reactions").mkdir(parents=True)
    payload = {"comments_v2": [{
        "timestamp": 1, "title": "x",
        "data": [
            {"comment": {"timestamp": 1, "comment": "first", "author": "Test User"}},
            {"comment": {"timestamp": 2, "comment": "second", "author": "Test User"}},
        ],
    }]}
    (tmp_path / "your_facebook_activity/comments_and_reactions/comments.json"
     ).write_text(json.dumps(payload))
    docs = list(FacebookParser(tmp_path).iter_documents())
    ids = [d.id for d in docs]
    assert len(ids) == len(set(ids)) == 2
