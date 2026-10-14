import { useEffect, useState } from "react";
import { listNotes, createNote, updateNote, deleteNote } from "./api";

const EMPTY_NOTE = { id: null, title: "", body: "" };

function formatDate(iso) {
  if (!iso) return "";
  return new Date(iso).toLocaleDateString(undefined, {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

// Counts distinct search words appearing in title to visualize ranking rule
function getTitleMatchCount(title, query) {
  if (!query.trim() || !title) return 0;
  const words = Array.from(new Set(query.toLowerCase().split(/\s+/).filter(Boolean)));
  const lowerTitle = title.toLowerCase();
  return words.filter((w) => lowerTitle.includes(w)).length;
}

export default function App() {
  const [query, setQuery] = useState("");
  const [notes, setNotes] = useState([]);
  const [draft, setDraft] = useState(EMPTY_NOTE);
  const [version, setVersion] = useState(0);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  // Load notes whenever query changes (debounced 200ms) or after save/delete
  useEffect(() => {
    let cancelled = false;
    const timer = setTimeout(async () => {
      try {
        const data = await listNotes(query);
        if (!cancelled) {
          setNotes(data || []);
          setError("");

          // Default selection to first note if none selected
          if (data && data.length > 0) {
            setDraft((prev) => (prev.id ? prev : data[0]));
          }
        }
      } catch {
        if (!cancelled) setError("Could not reach backend API at http://localhost:8000");
      }
    }, 200);

    return () => {
      cancelled = true;
      clearTimeout(timer);
    };
  }, [query, version]);

  const reload = () => setVersion((v) => v + 1);

  async function handleSave(e) {
    e.preventDefault();
    if (!draft.title.trim()) return;

    try {
      const payload = { title: draft.title.trim(), body: draft.body };
      const saved = draft.id
        ? await updateNote(draft.id, payload)
        : await createNote(payload);

      setDraft(saved);
      setError("");
      setMessage("Note saved successfully.");
      setTimeout(() => setMessage(""), 3000);
      reload();
    } catch {
      setError("Failed to save the note. Make sure title is provided.");
    }
  }

  async function handleDelete() {
    if (!draft.id || !window.confirm("Are you sure you want to delete this note?")) return;

    try {
      await deleteNote(draft.id);
      setDraft(EMPTY_NOTE);
      setError("");
      setMessage("Note deleted.");
      setTimeout(() => setMessage(""), 3000);
      reload();
    } catch {
      setError("Failed to delete note.");
    }
  }

  const isSearching = query.trim().length > 0;
  const canSave = draft.title.trim().length > 0;

  return (
    <div className="app-container">
      {/* Sidebar: Search and Notes List */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <div className="header-title-row">
            <h1 className="app-title">Notes</h1>
            <span className="notes-count">{notes.length} {notes.length === 1 ? "note" : "notes"}</span>
          </div>

          <div className="search-bar-row">
            <input
              type="text"
              className="search-input"
              placeholder="Search notes (e.g. 'FastAPI React')..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              aria-label="Search notes"
              autoComplete="off"
            />
            {query && (
              <button
                type="button"
                className="clear-search-btn"
                onClick={() => setQuery("")}
                aria-label="Clear search"
              >
                ×
              </button>
            )}
            <button
              type="button"
              className="btn btn-primary new-btn"
              onClick={() => setDraft(EMPTY_NOTE)}
              title="Create a new note"
            >
              + New
            </button>
          </div>
        </div>

        {error && <div className="sidebar-alert error-alert">{error}</div>}

        <ul className="notes-list">
          {notes.map((note) => {
            const titleMatches = isSearching ? getTitleMatchCount(note.title, query) : 0;
            const isSelected = note.id === draft.id;

            return (
              <li key={note.id}>
                <button
                  type="button"
                  className={`note-card ${isSelected ? "active" : ""}`}
                  onClick={() => setDraft({ id: note.id, title: note.title, body: note.body })}
                >
                  <div className="note-card-top">
                    <span className="note-title">{note.title}</span>
                    {isSearching && (
                      <span
                        className={`rank-badge ${titleMatches > 0 ? "title-match" : "body-match"}`}
                        title={`${titleMatches} search word(s) in title`}
                      >
                        {titleMatches > 0 ? `${titleMatches} in title` : "body match"}
                      </span>
                    )}
                  </div>
                  <span className="note-snippet">{note.body || "No additional text"}</span>
                  <span className="note-date">{formatDate(note.updated_at)}</span>
                </button>
              </li>
            );
          })}

          {notes.length === 0 && (
            <li className="empty-message">
              {isSearching
                ? "No notes contain all of those search words."
                : "No notes yet. Click '+ New' to create one."}
            </li>
          )}
        </ul>
      </aside>

      {/* Main Area: Note Editor */}
      <main className="editor">
        {message && <div className="editor-alert success-alert">{message}</div>}

        <form onSubmit={handleSave} className="editor-form">
          <input
            className="title-input"
            placeholder="Title"
            value={draft.title}
            onChange={(e) => setDraft({ ...draft, title: e.target.value })}
            maxLength={200}
            aria-label="Note Title"
          />

          <textarea
            className="body-input"
            placeholder="Write your note here..."
            value={draft.body}
            onChange={(e) => setDraft({ ...draft, body: e.target.value })}
            aria-label="Note Body"
          />

          <div className="editor-actions">
            <button
              type="submit"
              className="btn btn-primary"
              disabled={!canSave}
            >
              Save note
            </button>
            {draft.id && (
              <button
                type="button"
                className="btn btn-danger"
                onClick={handleDelete}
              >
                Delete note
              </button>
            )}
          </div>
        </form>
      </main>
    </div>
  );
}
