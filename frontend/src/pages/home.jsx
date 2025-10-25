import React, { useState } from "react";
import SearchBar from "../components/searchBar";
import VerseList from "../components/verseList";
import "./home.css";

function Home() {
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleSearch = async (query) => {
        setLoading(true);
        setError("");

        try {
        const response = await fetch(
            `http://127.0.0.1:5000/search?q=${encodeURIComponent(query)}`
            // `http://127.0.0.1:5000/search?q=${(query)}`
        );

        if (!response.ok) throw new Error("Server error");

        const data = await response.json();
        setResults(data.results || []);
        } catch (err) {
        console.error("Error:", err);
        setError("Something went wrong. Please try again.");
        } finally {
        setLoading(false);
        }
    };

    return (
        <div className="home-container">
        <h1>Bible Search (KJV)</h1>
        <SearchBar onSearch={handleSearch} />
        {error && <p className="error">{error}</p>}
        <VerseList verses={results} loading={loading} />
        </div>
    );
}

export default Home;
