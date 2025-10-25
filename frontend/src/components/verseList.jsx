import React from "react";
import "./VerseList.css";

function VerseList({ verses, loading }) {
    if (loading) return <p className="loading">Searching...</p>;

    if (!verses.length) return <p className="no-results">No results found.</p>;

    return (
        <div className="verse-list">
        {verses.map((v, index) => (
            <div key={index} className="verse-card">
            <h4>{v.reference}</h4>
            <p>{v.text}</p>
            </div>
        ))}
        </div>
    );
}

export default VerseList;
