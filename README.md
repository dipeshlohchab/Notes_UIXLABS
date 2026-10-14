# Searchable Notes App

A full-stack, personal notes application built with **FastAPI**, **React (Vite)**, and **MongoDB**, featuring live case-insensitive multi-word search and title-priority ranking.

---

## 1. Project Overview & Architecture

### Tech Stack
- **Frontend**: React 18, Vite, Vanilla CSS with CSS custom properties (Dark theme design system).
- **Backend**: FastAPI (Python 3.10+), Pydantic v2 schemas, PyMongo driver, Uvicorn ASGI server.
- **Database**: MongoDB (`mongodb://localhost:27017`), Database: `notes_app`, Collection: `notes`.
- **Testing**: Pytest for algorithmic unit tests.

### Project Structure
```
notes-app/
├── backend/
│   ├── main.py          # FastAPI application, CORS, and REST API endpoints
│   ├── search.py        # Query parsing, MongoDB filter builder, and ranking algorithm
│   ├── seed_data.py     # Database seeder populating ~50 realistic test notes
│   ├── test_search.py   # Automated unit tests for search parsing, filtering & ranking
│   └── requirements.txt # Python dependencies (fastapi, uvicorn, pymongo, pytest, httpx)
├── frontend/
│   ├── src/
│   │   ├── App.jsx      # Main React application component (state, search, layout)
│   │   ├── api.js       # API client for backend communication
│   │   ├── main.jsx     # React DOM entry point
│   │   └── styles.css   # Modern dark-mode styling and responsive layout
│   ├── index.html       # Single Page Application HTML shell
│   ├── package.json     # Node scripts and dependencies
│   └── vite.config.js   # Vite configuration with `/api` reverse proxy to port 8000
└── README.md            # Complete documentation
```

---

## 2. Core Requirements & Implementation

### Requirement 1: Create, Edit, and Delete Notes with a Title and Body
- **Creation**: Users enter a `title` and `body` and click **Save note** (or `+ New` to start fresh). Calls `POST /api/notes`.
- **Editing**: Selecting any note populates the editor with its existing data. Edits are saved with `PUT /api/notes/{id}`.
- **Deletion**: Existing notes display a **Delete note** button that prompts confirmation and calls `DELETE /api/notes/{id}`.
- **Validation**:
  - `title`: Mandatory, 1–200 characters, whitespace-stripped.
  - `body`: Optional text up to 100,000 characters.
  - Timestamps: `created_at` and `updated_at` are automatically recorded in UTC.

### Requirement 2: Search Without Case Sensitivity
- Handled in `backend/search.py`:
  - `parse_query(q)` lowercases all input words: e.g. `"React FASTAPI"` $\to$ `["react", "fastapi"]`.
  - In MongoDB, regex filters use `{"$options": "i"}`.
  - Consequently, `fastapi`, `FASTAPI`, and `FastApi` yield identical matches.

### Requirement 3: Return Notes Containing Every Search Word Anywhere in Title or Body
- Strict **AND** logic across words:
  - If a user searches `fastapi react`, every returned note must contain *both* `fastapi` and *both* `react` (either in the title or the body).
  - Built dynamically in `backend/search.py` via `mongo_filter()`:
    ```python
    {"$and": [
        {"$or": [
            {"title": {"$regex": re.escape(word), "$options": "i"}},
            {"body": {"$regex": re.escape(word), "$options": "i"}},
        ]}
        for word in words
    ]}
    ```

### Requirement 4: Ranking by Number of Distinct Search Words in Title, Then by Recency
- Handled in `backend/search.py` via `rank()`:
  - **Criterion 1 (Primary)**: Count of distinct search keywords that appear in `note["title"]` (descending).
  - **Criterion 2 (Tiebreaker)**: Most recently updated (`updated_at` descending).
  - Empty queries return all notes ordered by `updated_at` descending (most recent first).
  - **UI Visualizer**: The frontend displays a badge on each note card during search:
    - `[X in title]` (highlighted in emerald) when keywords match in the title.
    - `[body match]` when keywords appear only in the note body.

---

## 3. REST API Reference

Base URL: `http://localhost:8000` (or `http://localhost:5173/api` via Vite proxy).

| Method | Endpoint | Description | Request Body | Response | Status |
|:---|:---|:---|:---|:---|:---:|
| `GET` | `/api/notes?q={query}` | Search and list notes | None | Array of `NoteOut` objects | `200 OK` |
| `POST` | `/api/notes` | Create a new note | `{"title": str, "body": str}` | Created `NoteOut` object | `201 Created` |
| `PUT` | `/api/notes/{id}` | Update an existing note | `{"title": str, "body": str}` | Updated `NoteOut` object | `200 OK` |
| `DELETE`| `/api/notes/{id}` | Delete a note by ID | None | None | `204 No Content` |
| `POST` | `/api/seed` | Seed ~50 sample notes | None | `{"message": str, "count": int}` | `200 OK` |

### Note Schema
```json
{
  "id": "6acf12a8bf9d4fc2cd3ae670",
  "title": "FastAPI Performance Optimization & Async Best Practices",
  "body": "When building high-throughput APIs with FastAPI, ensure connection pooling...",
  "created_at": "2026-10-13T09:05:00Z",
  "updated_at": "2026-10-14T09:05:00Z"
}
```

---

## 4. Setup & Running Locally

### Prerequisites
1. **Python 3.10+**
2. **Node.js 18+** & npm
3. **MongoDB** running locally on port `27017`

### Step 1: Start MongoDB
Ensure the MongoDB daemon is active:
```bash
# Verify connection
mongosh --eval "db.adminCommand('ping')"
```

### Step 2: Run the Backend
```bash
cd backend

# Create and activate virtual environment (optional but recommended)
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start backend server
uvicorn main:app --reload --port 8000
```
- API is running at: `http://localhost:8000`
- Interactive Swagger docs: `http://localhost:8000/docs`

### Step 3: Run the Frontend
```bash
cd frontend

# Install npm dependencies
npm install

# Start Vite dev server
npm run dev
```
- Application is live at: `http://localhost:5173`

---

## 5. Seeding Demo Notes

The repository includes a seeding script with **52 realistic, categorized notes** (covering software architecture, backend engineering, frontend frameworks, book summaries, productivity, and lifestyle).

To seed or reset the database at any time:
```bash
cd backend
python seed_data.py
```
Or send a `POST` request to `/api/seed`:
```bash
curl -X POST http://localhost:8000/api/seed
```

---

## 6. Running Tests

Automated tests cover all search parsing, filtering, and ranking requirements:
```bash
cd backend
pytest
```

### Test Coverage Breakdown (`test_search.py`):
1. `test_parse_query_lowercases_and_dedupes`: Confirms whitespace stripping, lowercasing, and word deduplication.
2. `test_filter_requires_every_word`: Confirms MongoDB `$and` contains a sub-filter for every distinct query word.
3. `test_filter_escapes_regex_characters`: Ensures special regex symbols like `c++` or `node.js` are escaped safely.
4. `test_title_score_counts_distinct_words`: Tests count of distinct keywords matching note title.
5. `test_rank_by_title_matches_then_recency`: Tests multi-tier sort: notes with 2 title matches rank above 1 title match, with ties broken by recency.

---

## 7. How to Explain This Project (Interview / Review Cheatsheet)

When presenting this project, walk through these three concise points:

1. **Architecture**: 
   *"It is a clean full-stack application. The frontend is built in React 18 with Vite, using a responsive two-column layout. The backend is a FastAPI microservice communicating with MongoDB. Vite proxies `/api` calls directly to FastAPI."*
2. **Search Logic (`backend/search.py`)**:
   *"When a query like `fastapi react` is entered, we lowercase and split it into distinct words. MongoDB uses an `$and` condition of `$or` regex filters to ensure every word exists in either the title or body, satisfying case-insensitivity and strict AND matching."*
3. **Ranking Heuristic**:
   *"Matching notes are sorted in Python using a compound key: first by the count of distinct query words in the title in descending order, and second by the `updated_at` timestamp in descending order. In the UI, a badge clearly highlights how many words matched in the title vs body."*
