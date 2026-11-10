// Run: TZ=Europe/London node --test test_dates.test.js
// Every test uses a fixed "now" — no dependency on today's date.
'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const D = require('./compass-dates.js');

const ev = (start, end, extra = {}) => ({ id: 'e', title: 'Event', start, end, status: 'CURRENT', checked_at: '2026-08-30', ...extra });
const at = (iso) => new Date(iso);

// Tuesday 10 Nov 2026, 15:00 London (GMT, +00:00)
const NOW = at('2026-11-10T15:00:00Z');

test('runs in the London time zone (the site audience)', () => {
  assert.equal(new Date('2026-07-01T12:00:00Z').getTimezoneOffset(), -60, 'set TZ=Europe/London');
});

test('lifecycle: upcoming, ongoing, past, cancelled', () => {
  assert.equal(D.lifecycle(ev('2026-11-12T10:00:00Z', '2026-11-12T12:00:00Z'), NOW), 'upcoming');
  assert.equal(D.lifecycle(ev('2026-11-10T14:00:00Z', '2026-11-10T16:00:00Z'), NOW), 'ongoing');
  assert.equal(D.lifecycle(ev('2026-09-01T18:30:00+01:00', '2026-09-01T19:30:00+01:00'), NOW), 'past');
  assert.equal(D.lifecycle(ev('2026-11-12T10:00:00Z', '2026-11-12T12:00:00Z', { status: 'CANCELLED' }), NOW), 'cancelled');
});

test('an ended event is past, never cancelled (cancellation needs the source to say so)', () => {
  const ended = ev('2026-09-05T10:00:00+01:00', '2026-09-05T22:00:00+01:00');
  assert.equal(D.lifecycle(ended, NOW), 'past');
  assert.equal(ended.status, 'CURRENT', 'data is not relabelled');
});

test('upcoming view excludes ended and cancelled events, keeps ongoing ones', () => {
  assert.equal(D.matchesTime(ev('2026-09-01T18:30:00+01:00', '2026-09-01T19:30:00+01:00'), 'upcoming', NOW), false);
  assert.equal(D.matchesTime(ev('2026-11-12T10:00:00Z', '2026-11-12T12:00:00Z', { status: 'CANCELLED' }), 'upcoming', NOW), false);
  assert.equal(D.matchesTime(ev('2026-11-10T14:00:00Z', '2026-11-10T16:00:00Z'), 'upcoming', NOW), true);
  assert.equal(D.matchesTime(ev('2026-11-20T10:00:00Z', '2026-11-20T12:00:00Z'), 'upcoming', NOW), true);
});

test('today: excludes an event that ended this morning, includes later today and ongoing', () => {
  assert.equal(D.matchesTime(ev('2026-11-10T09:00:00Z', '2026-11-10T11:00:00Z'), 'today', NOW), false);
  assert.equal(D.matchesTime(ev('2026-11-10T18:00:00Z', '2026-11-10T20:00:00Z'), 'today', NOW), true);
  assert.equal(D.matchesTime(ev('2026-11-09T10:00:00Z', '2026-11-11T10:00:00Z'), 'today', NOW), true);
  assert.equal(D.matchesTime(ev('2026-11-11T09:00:00Z', '2026-11-11T11:00:00Z'), 'today', NOW), false);
});

test('today uses the London day, also in British Summer Time', () => {
  const lateSummerEvening = at('2026-09-01T22:30:00Z'); // 23:30 BST on 1 Sep
  const startsJustAfterMidnight = ev('2026-09-02T00:15:00+01:00', '2026-09-02T02:00:00+01:00'); // 2 Sep London
  assert.equal(D.matchesTime(startsJustAfterMidnight, 'today', lateSummerEvening), false);
  assert.equal(D.matchesTime(startsJustAfterMidnight, 'tomorrow', lateSummerEvening), true);
});

test('tomorrow and weekend never show ended events', () => {
  assert.equal(D.matchesTime(ev('2026-11-11T09:00:00Z', '2026-11-11T11:00:00Z'), 'tomorrow', NOW), true);
  assert.equal(D.matchesTime(ev('2026-11-12T09:00:00Z', '2026-11-12T11:00:00Z'), 'tomorrow', NOW), false);
  assert.equal(D.matchesTime(ev('2026-11-14T11:00:00Z', '2026-11-14T17:00:00Z'), 'weekend', NOW), true);
  const saturdayAfternoon = at('2026-11-14T16:00:00Z');
  assert.equal(D.matchesTime(ev('2026-11-14T09:00:00Z', '2026-11-14T12:00:00Z'), 'weekend', saturdayAfternoon), false);
});

test('archive keeps past and cancelled events, newest first; never upcoming ones', () => {
  const items = [
    ev('2026-09-01T18:30:00+01:00', '2026-09-01T19:30:00+01:00', { id: 'a' }),
    ev('2026-09-20T11:00:00+01:00', '2026-09-20T16:00:00+01:00', { id: 'b' }),
    ev('2026-11-20T10:00:00Z', '2026-11-20T12:00:00Z', { id: 'future' }),
    ev('2026-11-21T10:00:00Z', '2026-11-21T12:00:00Z', { id: 'cancelled', status: 'CANCELLED' }),
  ];
  const archive = D.sortForView(items.filter((x) => D.matchesTime(x, 'archive', NOW)), 'archive');
  assert.deepEqual(archive.map((x) => x.id), ['cancelled', 'b', 'a']);
});

test('verification age is separate from lifecycle', () => {
  const recent = ev('2026-11-20T10:00:00Z', '2026-11-20T12:00:00Z', { checked_at: '2026-11-08' });
  const old = ev('2026-11-20T10:00:00Z', '2026-11-20T12:00:00Z', { checked_at: '2026-08-30' });
  assert.deepEqual([D.verification(recent, NOW).stale, D.verification(old, NOW).stale], [false, true]);
  assert.equal(D.lifecycle(old, NOW), 'upcoming', 'a stale check does not make an event past or cancelled');
});

test('the real seed list: all 8 records kept, all historical on 10 Nov 2026, none upcoming', () => {
  const seed = JSON.parse(fs.readFileSync(path.join(__dirname, 'events.json'), 'utf8'));
  assert.equal(seed.length, 8);
  assert.equal(seed.filter((x) => D.matchesTime(x, 'upcoming', NOW)).length, 0);
  assert.equal(seed.filter((x) => D.matchesTime(x, 'archive', NOW)).length, 8);
  assert.ok(seed.every((x) => x.source_url.startsWith('https://')), 'source links kept');
  assert.equal(D.lastChecked(seed), '2026-08-30');
});
