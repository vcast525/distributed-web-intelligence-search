import { useEffect, useMemo, useState } from "react";
import "./App.css";

const API_BASE_URL = "http://127.0.0.1:8000/api/v1";

function App() {
  const [query, setQuery] = useState("");
  const [sourceFilter, setSourceFilter] = useState("all");
  const [results, setResults] = useState([]);
  const [sources, setSources] = useState([]);
  const [totalResults, setTotalResults] = useState(null);
  const [isSearching, setIsSearching] = useState(false);
  const [isLoadingSources, setIsLoadingSources] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [statusMessage, setStatusMessage] = useState("");

  const selectedSource = useMemo(() => {
    if (sourceFilter === "all") {
      return null;
    }

    return sources.find((source) => source.url === sourceFilter) || null;
  }, [sourceFilter, sources]);

  const visibleResults = useMemo(() => {
    if (selectedSource) {
      return [
        {
          url: selectedSource.url,
          title: selectedSource.title || "Untitled Source",
          clean_text:
            "This indexed source is available in the platform. Use keyword search to retrieve relevance-ranked content from Elasticsearch.",
          score: null,
        },
      ];
    }

    return results;
  }, [selectedSource, results]);

  async function loadSources(showMessage = false) {
    setIsLoadingSources(true);
    setErrorMessage("");

    try {
      const response = await fetch(`${API_BASE_URL}/sources`);

      if (!response.ok) {
        throw new Error("Unable to load sources.");
      }

      const data = await response.json();
      setSources(data.sources || []);

      if (showMessage) {
        setStatusMessage("Sources refreshed successfully.");
      }
    } catch (error) {
      setErrorMessage("Unable to load indexed sources.");
    } finally {
      setIsLoadingSources(false);
    }
  }

  async function handleSearch() {
    if (!query.trim()) {
      setErrorMessage("Please enter a search term.");
      return;
    }

    setIsSearching(true);
    setErrorMessage("");
    setStatusMessage("");
    setSourceFilter("all");

    try {
      const response = await fetch(
        `${API_BASE_URL}/search?q=${encodeURIComponent(query)}`
      );

      if (!response.ok) {
        throw new Error("Search request failed.");
      }

      const data = await response.json();

      setResults(data.results || []);
      setTotalResults(data.total_results);
      setStatusMessage("Search completed successfully.");
    } catch (error) {
      setErrorMessage("Unable to retrieve search results.");
      setResults([]);
      setTotalResults(null);
    } finally {
      setIsSearching(false);
    }
  }

  function handleSourceChange(event) {
    const selectedValue = event.target.value;

    setSourceFilter(selectedValue);
    setErrorMessage("");

    if (selectedValue === "all") {
      setStatusMessage("Showing all indexed sources.");
    } else {
      setResults([]);
      setTotalResults(null);
      setStatusMessage("Source selected.");
    }
  }

  function handleClearSearch() {
    setQuery("");
    setErrorMessage("");
    setStatusMessage("Search field cleared.");
  }

  function handleClearResults() {
    setResults([]);
    setTotalResults(null);
    setSourceFilter("all");
    setErrorMessage("");
    setStatusMessage("Search results cleared.");
  }

  async function handleDeleteSource(source) {
    const confirmed = window.confirm(
      `Delete this indexed source?\n\n${source.title || source.url}\n\nThis removes it from MongoDB and Elasticsearch.`
    );

    if (!confirmed) {
      return;
    }

    setIsDeleting(true);
    setErrorMessage("");
    setStatusMessage("");

    try {
      const response = await fetch(
        `${API_BASE_URL}/sources/${source.document_id}`,
        {
          method: "DELETE",
        }
      );

      if (!response.ok) {
        throw new Error("Delete request failed.");
      }

      await response.json();

      setSources((currentSources) =>
        currentSources.filter(
          (currentSource) => currentSource.document_id !== source.document_id
        )
      );

      setResults((currentResults) =>
        currentResults.filter((result) => result.url !== source.url)
      );

      if (sourceFilter === source.url) {
        setSourceFilter("all");
      }

      setStatusMessage("Source deleted successfully.");
    } catch (error) {
      setErrorMessage("Unable to delete source.");
    } finally {
      setIsDeleting(false);
    }
  }

  useEffect(() => {
    loadSources();
  }, []);

  return (
    <main className="app-shell">
      <section className="hero-section">
        <p className="eyebrow">Distributed Web Intelligence</p>
        <h1>APEX Financial Intelligence</h1>
        <p className="hero-copy">
          Search indexed web intelligence collected through a distributed
          ingestion, crawling, processing, storage, and indexing pipeline.
        </p>
      </section>

      <section className="workspace-heading">
        <p className="eyebrow">Intelligence Workspace</p>
        <h2>Explore indexed intelligence</h2>
        <p>
          Use keyword search and source filtering to explore crawled, processed, and indexed intelligence content.
        </p>
      </section>

      <section className="search-panel">
        <div className="panel-header">
          <div>
            <p className="section-label">Query Workspace</p>
            <h2>Find indexed content</h2>
          </div>
          <span className="status-pill">Backend Connected</span>
        </div>

        <div className="search-row">
          <input
            type="text"
            placeholder="Enter a keyword to search indexed intelligence..."
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter") {
                handleSearch();
              }
            }}
          />
          <button type="button" onClick={handleSearch} disabled={isSearching}>
            {isSearching ? "Searching..." : "Search"}
          </button>
          <button
            type="button"
            className="secondary-button"
            onClick={handleClearSearch}
          >
            Clear Search
          </button>
          <button
            type="button"
            className="secondary-button"
            onClick={handleClearResults}
          >
            Clear Results
          </button>
        </div>

        <div className="filter-row">
          <label htmlFor="source-filter">View Source</label>
          <select
            id="source-filter"
            value={sourceFilter}
            onChange={handleSourceChange}
          >
            <option value="all">All indexed sources</option>
            {sources.map((source) => (
              <option key={source.document_id} value={source.url}>
                {source.name || source.title || source.url}
              </option>
            ))}
          </select>
        </div>

        {errorMessage && <p className="error-text">{errorMessage}</p>}
        {statusMessage && <p className="success-text">{statusMessage}</p>}

        {totalResults !== null && !selectedSource && (
          <p className="helper-text">
            {visibleResults.length} visible result
            {visibleResults.length === 1 ? "" : "s"} shown from{" "}
            {totalResults} total result{totalResults === 1 ? "" : "s"} for{" "}
            <strong>{query}</strong>.
          </p>
        )}
      </section>

      <section className="results-panel">
        <div className="panel-header compact-header">
          <div>
            <p className="section-label">Results</p>
            <h2>
              {selectedSource
                ? "Selected source"
                : totalResults === null
                ? "Ready to search"
                : `${visibleResults.length} result${
                    visibleResults.length === 1 ? "" : "s"
                  } shown`}
            </h2>
          </div>
        </div>

        {visibleResults.length === 0 && totalResults === null && !selectedSource && (
          <div className="result-card">
            <h3>Search indexed intelligence</h3>
            <p>
              Enter a keyword above or select an indexed source to view content
              that has been crawled, processed, stored, and indexed.
            </p>
          </div>
        )}

        {totalResults !== null && visibleResults.length === 0 && !selectedSource && (
          <div className="result-card">
            <h3>No visible results</h3>
            <p>
              Try a different keyword or select an indexed source from the
              dropdown.
            </p>
          </div>
        )}

        {visibleResults.map((result) => (
          <article className="result-card" key={result.url}>
            <p className="result-url">{result.url}</p>
            <h3>{result.title || "Untitled Result"}</h3>
            <p>{result.clean_text?.slice(0, 360)}...</p>
            {result.score === null ? (
              <span className="score-pill">Indexed Source</span>
            ) : (
              <span className="score-pill">
                Relevance Score: {result.score?.toFixed(2)}
              </span>
            )}
          </article>
        ))}
      </section>

      <section className="workspace-heading source-library-heading">
        <p className="eyebrow">Source Library</p>
        <h2>Manage the intelligence source repository</h2>
        <p>
          Review the approved sources available to the APEX platform and manage indexed source records.
        </p>
      </section>

      <section className="source-panel">
        <div className="panel-header compact-header">
          <div>
              <p className="section-label">Source Repository</p>
              <h2>{sources.length} indexed source{sources.length === 1 ? "" : "s"}</h2>
          </div>
          <button
            type="button"
            className="secondary-button"
            onClick={() => loadSources(true)}
            disabled={isLoadingSources}
          >
            {isLoadingSources ? "Refreshing..." : "Refresh Sources"}
          </button>
        </div>

        <div className="source-grid">
          {sources.length === 0 && (
            <div className="empty-state">
              No indexed sources found. Add sources through the ingestion API.
            </div>
          )}

          {sources.map((source) => (
            <article className="source-card" key={source.document_id}>
              <div>
                <p className="source-title">{source.name || source.title || "Untitled Source"}</p>
                <p className="source-url">{source.url}</p>
              </div>

              <div className="source-meta">
                <span>Status: {source.processing_status || "unknown"}</span>
                <span>Index: {source.indexing_status || "unknown"}</span>
                <span>HTTP: {source.status_code || "N/A"}</span>
              </div>

              <button
                type="button"
                className="danger-button"
                onClick={() => handleDeleteSource(source)}
                disabled={isDeleting}
              >
                Delete Source
              </button>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}

export default App;