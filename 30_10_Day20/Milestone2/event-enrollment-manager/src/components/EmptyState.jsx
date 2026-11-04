function EmptyState({ title, message }) {
  return (
    <div className="empty-state">
      <div className="empty-icon">⌕</div>

      <h3>{title || "No events found"}</h3>

      <p>
        {message ||
          "Try changing your search or category filter to find an event."}
      </p>
    </div>
  );
}

export default EmptyState;