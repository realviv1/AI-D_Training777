import EmptyState from "../components/EmptyState";

function formatDate(dateString) {
  if (!dateString) return "Date unavailable";
  const [year, month, day] = dateString.split("-").map(Number);
  return new Date(year, month - 1, day).toLocaleDateString("en-IN", {
    day: "numeric",
    month: "short",
    year: "numeric"
  });
}

export default function Registrations({
  events,
  registrations,
  cancelRegistration
}) {
  const rows = registrations.map((registration) => {
    const event = events.find((item) => item.id === registration.eventId);
    return { ...registration, event };
  });

  return (
    <main className="page-container registrations-page">
      <section className="section-heading registrations-heading">
        <div>
          <span className="eyebrow">YOUR EVENT ACTIVITY</span>
          <h1>Registrations</h1>
          <p>All your active event reservations, in one place.</p>
        </div>
        <div className="registration-summary">
          <strong>{registrations.length}</strong>
          <span>active {registrations.length === 1 ? "registration" : "registrations"}</span>
        </div>
      </section>

      {rows.length === 0 ? (
        <EmptyState
          title="No registrations yet"
          message="Your event reservations will appear here. Browse upcoming events and reserve your first seat."
        />
      ) : (
        <div className="table-card">
          <div className="table-topline">
            <div>
              <h2>Active reservations</h2>
              <p>Manage or cancel your event bookings.</p>
            </div>
          </div>
          <div className="table-scroll">
            <table>
              <thead>
                <tr>
                  <th>Attendee</th>
                  <th>Email address</th>
                  <th>Event</th>
                  <th>Event date</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((registration) => (
                  <tr key={registration.id}>
                    <td data-label="Attendee">
                      <div className="attendee-cell">
                        <span className="avatar">{registration.name.trim().charAt(0).toUpperCase()}</span>
                        <strong>{registration.name}</strong>
                      </div>
                    </td>
                    <td data-label="Email address">{registration.email}</td>
                    <td data-label="Event">{registration.event?.title || "Unknown event"}</td>
                    <td data-label="Event date">{formatDate(registration.event?.date)}</td>
                    <td data-label="Action">
                      <button
                        className="button button-cancel"
                        type="button"
                        onClick={() => cancelRegistration(registration.id)}
                      >
                        Cancel
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </main>
  );
}