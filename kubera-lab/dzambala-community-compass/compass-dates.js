/* DZAMBALA Community Compass — event date logic.
 * Pure functions (no DOM, no network) so they can be tested with fixed clocks.
 * Used by index.html in the browser and by test_dates.test.js under Node.
 *
 * Three separate facts about an event, never mixed:
 *   lifecycle    — from the dates and the recorded status: upcoming | ongoing | past | cancelled
 *   verification — how long ago the listing was checked against its source (checked_at)
 *   status       — what the source said at the last check (CURRENT = not cancelled, CANCELLED)
 * An event that has ended is "past" (historical), not "cancelled": cancellation needs evidence.
 */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.CompassDates = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  const DAY_MS = 86400000;
  const RECHECK_AFTER_DAYS = 7;

  function startOfDay(d) { const x = new Date(d); x.setHours(0, 0, 0, 0); return x; }
  function addDays(d, n) { const x = new Date(d); x.setDate(x.getDate() + n); return x; }

  function upcomingWeekend(now) {
    const daysUntilSaturday = (6 - now.getDay() + 7) % 7;
    const saturday = startOfDay(addDays(now, daysUntilSaturday));
    return [saturday, startOfDay(addDays(saturday, 2))];
  }

  function lifecycle(item, now) {
    if (item.status === 'CANCELLED') return 'cancelled';
    const start = new Date(item.start), end = new Date(item.end);
    if (end < now) return 'past';
    if (start <= now) return 'ongoing';
    return 'upcoming';
  }

  /* Does the event belong to the chosen time view?
   * upcoming/today/tomorrow/weekend never include ended or cancelled events;
   * archive shows every event that has ended (and cancelled ones, labelled as such). */
  function matchesTime(item, mode, now) {
    const state = lifecycle(item, now);
    if (mode === 'archive') return state === 'past' || state === 'cancelled';
    if (state === 'past' || state === 'cancelled') return false;
    const start = new Date(item.start), end = new Date(item.end);
    if (mode === 'upcoming') return true;
    if (mode === 'today') return start < startOfDay(addDays(now, 1));
    if (mode === 'tomorrow') return start < startOfDay(addDays(now, 2)) && end >= startOfDay(addDays(now, 1));
    if (mode === 'weekend') { const [sat, mon] = upcomingWeekend(now); return end >= sat && start < mon; }
    return false;
  }

  function verification(item, now) {
    const checked = new Date(`${item.checked_at}T00:00:00`);
    const ageDays = Math.floor((startOfDay(now) - checked) / DAY_MS);
    return { ageDays, stale: ageDays > RECHECK_AFTER_DAYS, checkedAt: item.checked_at };
  }

  /* Most recent checked_at in the list (YYYY-MM-DD strings sort as dates), or null. */
  function lastChecked(items) {
    return items.reduce((latest, x) => (!latest || x.checked_at > latest ? x.checked_at : latest), null);
  }

  function sortForView(items, mode) {
    const byStart = (a, b) => new Date(a.start) - new Date(b.start);
    return [...items].sort(mode === 'archive' ? (a, b) => byStart(b, a) : byStart);
  }

  return { RECHECK_AFTER_DAYS, startOfDay, addDays, upcomingWeekend, lifecycle, matchesTime, verification, lastChecked, sortForView };
});
