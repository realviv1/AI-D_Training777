import { useMemo, useState } from "react";
import EventCard from "../components/EventCard";
import EventFilters from "../components/EventFilters";
import EmptyState from "../components/EmptyState";
import RegistrationModal from "../components/RegistrationModal";

export default function Events({ events, getAvailableSeats, registerUser }) {
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("All");
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [notice, setNotice] = useState("");

  const filteredEvents = useMemo(() => {
    const normalizedSearch = search.trim().toLowerCase();

    return events.filter((event) => {
      const matchesSearch = event.title.toLowerCase().includes(normalizedSearch);
      const matchesCategory = category === "All" || event.category === category;
      return matchesSearch && matchesCategory;
    });
  }, [events, search, category]);

  function handleRegistration(eventId, name, email) {
    const result = registerUser(eventId, name, email);
    if (result.success) {
      setNotice(result.message);
    }
    return result;
  }

  return (
    <main className="page-container">
      <section className="hero">
        <div className="hero-copy">
          <span className="eyebrow">LEARN SOMETHING NEW</span>
          <h1>Find your next <span>experience.</span></h1>
          <p>Small events. Fresh perspectives. Real connections. Find a session that sparks your curiosity.</p>
        </div>
        <div className="hero-art" aria-hidden="true">
          <div className="hero-orbit orbit-one" />
          <div className="hero-orbit orbit-two" />
          <div className="hero-spark">✳</div>
          <div className="hero-note">Make time<br />for what<br /><em>moves you.</em></div>
        </div>
      </section>

      <section className="section-heading">
        <div>
          <span className="eyebrow">WHAT'S HAPPENING</span>
          <h2>Upcoming events</h2>
          <p>Explore the programme and save your seat.</p>
        </div>
        <div className="event-count"><strong>{filteredEvents.length}</strong> {filteredEvents.length === 1 ? "event" : "events"} found</div>
      </section>

      <EventFilters
        search={search}
        onSearchChange={setSearch}
        category={category}
        onCategoryChange={setCategory}
      />

      {notice && (
        <div className="success-notice" role="status">
          <span aria-hidden="true">✓</span> {notice}
          <button type="button" onClick={() => setNotice("")} aria-label="Dismiss message">×</button>
        </div>
      )}

      {filteredEvents.length > 0 ? (
        <div className="event-grid">
          {filteredEvents.map((event) => (
            <EventCard
              key={event.id}
              event={event}
              availableSeats={getAvailableSeats(event.id)}
              onRegister={setSelectedEvent}
            />
          ))}
        </div>
      ) : (
        <EmptyState
          title="No events found"
          message="Try another title or choose a different category to see more events."
        />
      )}

      {selectedEvent && (
        <RegistrationModal
          event={selectedEvent}
          availableSeats={getAvailableSeats(selectedEvent.id)}
          onClose={() => setSelectedEvent(null)}
          onSubmit={handleRegistration}
        />
      )}
    </main>
  );
}