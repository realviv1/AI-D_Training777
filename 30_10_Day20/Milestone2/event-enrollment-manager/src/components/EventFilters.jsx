const CATEGORIES = ["All", "Technology", "Arts", "Life Skills"];

export default function EventFilters({
  search,
  onSearchChange,
  category,
  onCategoryChange
}) {
  return (
    <div className="filters">
      <label className="search-box">
        <span className="search-icon" aria-hidden="true">⌕</span>
        <span className="sr-only">Search events by title</span>
        <input
          type="search"
          placeholder="Search events by title..."
          value={search}
          onChange={(event) => onSearchChange(event.target.value)}
        />
      </label>

      <label className="category-select">
        <span className="sr-only">Filter by category</span>
        <select value={category} onChange={(event) => onCategoryChange(event.target.value)}>
          {CATEGORIES.map((item) => (
            <option key={item} value={item}>{item === "All" ? "All categories" : item}</option>
          ))}
        </select>
      </label>
    </div>
  );
}