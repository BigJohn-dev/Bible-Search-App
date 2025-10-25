import React, { useState } from "react";
import "./SearchBar.css";

function SearchBar({ onSearch }) {
    const [query, setQuery] = useState("");

    const handleSubmit = (e) => {
        e.preventDefault();
        if (query.trim()) {
        onSearch(query);
        }
    };

    return (
        <div className="Search-section">
            <form className="search-bar" onSubmit={handleSubmit}>
            <input
                type="text"
                value={query}
                placeholder="Search by verse or reference (e.g. John 3:16)"
                onChange={(e) => setQuery(e.target.value)}
            />
            <button type="submit">Search</button>
        </form>
        </div>
    );
}

export default SearchBar;
