/**
 * Sends an HTTP request to the backend API.
 * Automatically prepends `/api`, includes default headers, and parses JSON responses.
 *
 * @param {string} path - The endpoint path relative to `/api` (e.g., '/notes').
 * @param {RequestInit} [options={}] - Standard fetch options (method, headers, body, etc.).
 * @returns {Promise<any>} Resolves to parsed JSON response, or null if response status is 204 (No Content).
 * @throws {Error} Throws an error if the HTTP response status is not ok (outside 200-299).
 */
async function request(path, options = {}) {
  const res = await fetch(`/api${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) throw new Error(`Request failed (${res.status})`);
  return res.status === 204 ? null : res.json();
}

/**
 * Retrieves a list of notes from the server, optionally filtered and ranked by a search query.
 *
 * @param {string} [q=""] - Optional search query to filter notes by title and body keywords.
 * @returns {Promise<Array<{id: string, title: string, body: string, created_at: string, updated_at: string}>>} Array of matching note objects.
 */
export const listNotes = (q) => request(`/notes?q=${encodeURIComponent(q || "")}`);

/**
 * Creates a new note in the database.
 *
 * @param {{title: string, body?: string}} note - The note payload containing title and optional body.
 * @returns {Promise<{id: string, title: string, body: string, created_at: string, updated_at: string}>} The newly created note object.
 */
export const createNote = (note) =>
  request("/notes", { method: "POST", body: JSON.stringify(note) });

/**
 * Updates an existing note by its unique identifier.
 *
 * @param {string} id - The ID of the note to update.
 * @param {{title: string, body?: string}} note - The updated note data (title and body).
 * @returns {Promise<{id: string, title: string, body: string, created_at: string, updated_at: string}>} The updated note object.
 */
export const updateNote = (id, note) =>
  request(`/notes/${id}`, { method: "PUT", body: JSON.stringify(note) });

/**
 * Permanently deletes a note by its unique identifier.
 *
 * @param {string} id - The ID of the note to delete.
 * @returns {Promise<null>} Resolves to null upon successful deletion (status 204).
 */
export const deleteNote = (id) => request(`/notes/${id}`, { method: "DELETE" });

/**
 * Triggers the database seeding endpoint with sample demo notes.
 *
 * @returns {Promise<{message: string, count: number}>} Confirmation message and count of seeded notes.
 */
export const seedNotes = () => request("/seed", { method: "POST" });

