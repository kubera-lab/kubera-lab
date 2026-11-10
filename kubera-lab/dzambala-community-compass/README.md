# DZAMBALA Community Compass — London + Merton

A small, practical city-discovery prototype for finding **verified community, cultural, wellbeing, learning, volunteering and sport sources/events** in London, with a dedicated Merton view.

## What v0.2 does

- switches between **London + Merton** and **Merton only**;
- shows a verified **upcoming-event layer** from official/institutional sources;
- filters events by **Today**, **Tomorrow**, **Weekend**, **Free only** and category;
- hides ended events from the upcoming views and keeps them in an accessible **Past events (archive)** view;
- links every event to the original source and records when it was checked;
- keeps a separate verified-source directory with a transparent **Trust Score**;
- plots sources and events that have known coordinates on an OpenStreetMap/Leaflet map;
- validates event data, ISO timestamps, HTTPS provenance and deterministic duplicate fingerprints;
- runs the validators, event tests and date/archive tests in GitHub Actions.

## Event verification

`events.json` is a **manually verified seed layer**, not an automated scraper. The current seed was checked on **30 August 2026** against primary or institutional pages, including Merton Council and Bharatiya Vidya Bhavan.

Each event stores:

- start/end time with timezone offset;
- area/borough, venue and address;
- category and price state (`FREE`, `PAID`, `UNKNOWN`);
- organiser;
- original source URL and source type;
- verification date and status.

The browser marks an event as needing a recheck when its `checked_at` date is more than seven days old. That is a freshness warning, not a claim that the event is cancelled.

## Event lifecycle and archive

The page works out each event's lifecycle in the browser from its start/end time and the current London time (`compass-dates.js`):

| Lifecycle | Meaning | Shown in |
|---|---|---|
| Upcoming | starts later | Upcoming, Today, Tomorrow, Weekend |
| Happening now | started, not yet ended | Upcoming, Today (and Tomorrow/Weekend if it spans them) |
| Past event | ended; kept as a historical record | Past events (archive) only |
| Cancelled | the source itself reported a cancellation (`status: CANCELLED`) | Past events (archive) only |

- An ended event is **never** labelled cancelled; that label needs the source to say so.
- No record is deleted or rewritten when it ends: title, source link, organiser and verification date stay visible in the archive.
- The archive is sorted newest first and has its own button, so it works by keyboard and screen reader.
- When no upcoming event is listed, the page says so plainly, shows the date of the last check and links to the archive. It does not invent replacement events.
- Verification freshness (`checked_at` older than seven days) is shown separately and does not change the lifecycle.

## Trust Score for source hubs

The source-hub score is deliberately simple and visible:

- source authority: up to 40 points;
- freshness of verification: up to 30 points;
- direct official/source link: up to 20 points;
- local relevance: up to 10 points.

This is **not** a rating of a religion, community, teacher, organisation or worldview. It only describes how confidently the listing itself can be verified.

## Validation

From this folder:

```bash
python validate_data.py
python validate_events.py
python -m unittest -v test_events.py
TZ=Europe/London node --test test_dates.test.js
```

## Run locally

```bash
python -m http.server 8000
```

Then open `http://localhost:8000`.

## Status

`v0.2` implements a verified event layer, a past-events archive and deterministic validation/deduplication. **Automatic event ingestion, automatic re-verification, personal profiles, AI ranking and notifications are not claimed as implemented yet.**
