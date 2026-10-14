import os
from datetime import datetime, timezone
from typing import Annotated

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, StringConstraints
from pymongo import MongoClient

from search import mongo_filter, parse_query, rank
from seed_data import seed_database

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")

client = MongoClient(MONGO_URL, tz_aware=True)
notes = client["notes_app"]["notes"]

app = FastAPI(title="Notes API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class NoteIn(BaseModel):
    title: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)]
    body: str = Field(default="", max_length=100_000)


class NoteOut(BaseModel):
    id: str
    title: str
    body: str
    created_at: datetime
    updated_at: datetime


def to_out(doc: dict) -> NoteOut:
    return NoteOut(
        id=str(doc["_id"]),
        title=doc["title"],
        body=doc["body"],
        created_at=doc["created_at"],
        updated_at=doc["updated_at"],
    )


def parse_id(note_id: str) -> ObjectId:
    try:
        return ObjectId(note_id)
    except (InvalidId, TypeError):
        raise HTTPException(404, "Note not found")


@app.get("/api/notes", response_model=list[NoteOut])
def list_notes(q: str = Query(default="")):
    words = parse_query(q)
    docs = list(notes.find(mongo_filter(words)))
    return [to_out(d) for d in rank(docs, words)]


@app.post("/api/notes", response_model=NoteOut, status_code=201)
def create_note(data: NoteIn):
    now = datetime.now(timezone.utc)
    doc = {**data.model_dump(), "created_at": now, "updated_at": now}
    doc["_id"] = notes.insert_one(doc).inserted_id
    return to_out(doc)


@app.put("/api/notes/{note_id}", response_model=NoteOut)
def update_note(note_id: str, data: NoteIn):
    doc = notes.find_one_and_update(
        {"_id": parse_id(note_id)},
        {"$set": {**data.model_dump(), "updated_at": datetime.now(timezone.utc)}},
        return_document=True,
    )
    if doc is None:
        raise HTTPException(404, "Note not found")
    return to_out(doc)


@app.delete("/api/notes/{note_id}", status_code=204)
def delete_note(note_id: str):
    if notes.delete_one({"_id": parse_id(note_id)}).deleted_count == 0:
        raise HTTPException(404, "Note not found")
    return Response(status_code=204)


@app.post("/api/seed")
def trigger_seed():
    count = seed_database()
    return {"message": "Successfully seeded demo notes", "count": count}
