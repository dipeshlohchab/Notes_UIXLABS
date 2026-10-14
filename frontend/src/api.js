async function request(path, options = {}) {
  const res = await fetch(`/api${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) throw new Error(`Request failed (${res.status})`);
  return res.status === 204 ? null : res.json();
}

export const listNotes = (q) => request(`/notes?q=${encodeURIComponent(q)}`);
export const createNote = (note) =>
  request("/notes", { method: "POST", body: JSON.stringify(note) });
export const updateNote = (id, note) =>
  request(`/notes/${id}`, { method: "PUT", body: JSON.stringify(note) });
export const deleteNote = (id) => request(`/notes/${id}`, { method: "DELETE" });
export const seedNotes = () => request("/seed", { method: "POST" });
