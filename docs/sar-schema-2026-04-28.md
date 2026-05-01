# Facebook SAR Schema Snapshot — 2026-04-28

This is the schema observed in the Meta "Download Your Information" export
`facebook-***REDACTED***-28_04_2026-NTH22s5t`. **Meta changes this schema
without notice.** Re-run `turbo-invention ingest --dry-run --source <path>`
against any new export and update the parser before processing.

## Top-level folders
- `ads_information/`
- `apps_and_websites_off_of_facebook/`
- `connections/`
- `docs/`
- `logged_information/`
- `personal_information/`
- `preferences/`
- `security_and_login_information/`
- `your_facebook_activity/`

## v0.1 parser targets
- `your_facebook_activity/posts/your_posts__check_ins__photos_and_videos_*.json` — list of post entries; text at `entry.data[].post`.
- `your_facebook_activity/comments_and_reactions/comments.json` — dict with `comments_v2` list; text at `entry.data[].comment.comment`.

## Known-but-not-yet-parsed (future PRs)
messages, groups, events, marketplace, pages, stories, search history.
