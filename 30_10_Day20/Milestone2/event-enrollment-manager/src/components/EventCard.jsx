function formatDate(dateString) {
  const [year, month, day] = dateString.split("-").map(Number);
  return new Date(year, month - 1, day).toLocaleDateString("en-IN", {
    day: "numeric",
    month: "short",
    year: "numeric"
  });
}

function formatTime(timeString) {
  const [hours, minutes] = timeString.split(":").map(Number);
  return new Date(2000, 0, 1, hours, minutes).toLocaleTimeString("en-IN", {
    hour: "numeric",
    minute: "2-digit"
  });
}

export default function EventCard({ event, availableSeats, onRegister }) {
  const isFull = availableSeats <= 0;

  return (
    <article className="event-card">
      <div className="event-card-top">
        <span className={`category-pill category-${event.category.toLowerCase().replaceAll(" ", "-")}`}>
          {event.category}
        </span>
        <span className={isFull ? "seat-status full" : "seat-status"}>
          {isFull ? "Fully booked" : `${availableSeats} seats left`}
        </span>
      </div>

      <div className="event-id">{event.id}</div>
      <h3>{event.title}</h3>

      <div className="event-meta">
        <div><span aria-hidden="true">▦</span> {formatDate(event.date)}</div>
        <div><span aria-hidden="true">◷</span> {formatTime(event.time)}</div>
      </div>

      <div className="capacity-row">
        <span>Available seats</span>
        <strong>{availableSeats} <span className="capacity-total">/ {event.capacity}</span></strong>
      </div>
      <div className="capacity-track" aria-label={`${availableSeats} of ${event.capacity} seats available`}>
        <div
          className="capacity-fill"
          style={{ width: `${Math.max(0, (availableSeats / event.capacity) * 100)}%` }}
        />
      </div>

      <button
        className={isFull ? "button button-disabled button-block" : "button button-primary button-block"}
        type="button"
        disabled={isFull}
        onClick={() => onRegister(event)}
      >
        {isFull ? "Registration closed" : "Register now"}
        {!isFull && <span aria-hidden="true">→</span>}
      </button>
    </article>
  );
}