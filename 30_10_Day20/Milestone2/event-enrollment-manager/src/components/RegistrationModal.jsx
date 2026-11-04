import { useEffect, useState } from "react";

function formatDate(dateString) {
  const [year, month, day] = dateString.split("-").map(Number);
  return new Date(year, month - 1, day).toLocaleDateString("en-IN", {
    day: "numeric",
    month: "long",
    year: "numeric"
  });
}

export default function RegistrationModal({
  event,
  availableSeats,
  onClose,
  onSubmit
}) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    function handleKeyDown(keyEvent) {
      if (keyEvent.key === "Escape") onClose();
    }
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [onClose]);

  function handleSubmit(formEvent) {
    formEvent.preventDefault();
    setError("");

    const result = onSubmit(event.id, name, email);
    if (!result.success) {
      setError(result.message);
      return;
    }
    onClose();
  }

  return (
    <div className="modal-backdrop" onMouseDown={(e) => {
      if (e.target === e.currentTarget) onClose();
    }}>
      <section className="modal" role="dialog" aria-modal="true" aria-labelledby="modal-title">
        <div className="modal-heading">
          <div>
            <span className="eyebrow">EVENT ENROLLMENT</span>
            <h2 id="modal-title">Reserve your place</h2>
          </div>
          <button className="icon-button" type="button" onClick={onClose} aria-label="Close dialog">×</button>
        </div>

        <div className="selected-event">
          <span className="selected-event-label">YOU'RE REGISTERING FOR</span>
          <strong>{event.title}</strong>
          <span>{formatDate(event.date)} · {event.time} · {availableSeats} seats available</span>
        </div>

        <form onSubmit={handleSubmit} noValidate>
          <label className="form-label" htmlFor="attendee-name">Full name</label>
          <input
            id="attendee-name"
            className="form-input"
            type="text"
            autoComplete="name"
            placeholder="Enter your full name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />

          <label className="form-label" htmlFor="attendee-email">Email address</label>
          <input
            id="attendee-email"
            className="form-input"
            type="email"
            autoComplete="email"
            placeholder="you@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          {error && <p className="form-error" role="alert">{error}</p>}

          <div className="modal-actions">
            <button className="button button-secondary" type="button" onClick={onClose}>Cancel</button>
            <button className="button button-primary" type="submit">Confirm registration <span aria-hidden="true">→</span></button>
          </div>
        </form>
        <p className="privacy-note">Your registration is saved in this browser.</p>
      </section>
    </div>
  );
}