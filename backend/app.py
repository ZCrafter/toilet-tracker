from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.middleware.cors import CORSMiddleware
from .database import SessionLocal, engine, Base
from .models import Pee, Poo, Sum
from sqlalchemy.future import select
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_db():
    async with SessionLocal() as session:
        yield session

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

class PeeCreate(BaseModel):
    time: datetime
    location: str

class PooCreate(BaseModel):
    time: datetime
    location: str

class SumCreate(BaseModel):
    time: datetime
    vr: bool
    names: List[str]

@app.post("/pee")
async def create_pee(entry: PeeCreate, db: AsyncSession = Depends(get_db)):
    pee = Pee(**entry.dict())
    db.add(pee)
    await db.commit()
    return {"status": "ok"}

@app.post("/poo")
async def create_poo(entry: PooCreate, db: AsyncSession = Depends(get_db)):
    poo = Poo(**entry.dict())
    db.add(poo)
    await db.commit()
    return {"status": "ok"}

@app.post("/sum")
async def create_sum(entry: SumCreate, db: AsyncSession = Depends(get_db)):
    sum_entry = Sum(**entry.dict())
    db.add(sum_entry)
    await db.commit()
    return {"status": "ok"}

@app.get("/stats")
async def get_stats(db: AsyncSession = Depends(get_db)):
    result = {}
    for model, name in zip([Pee, Poo, Sum], ["pee", "poo", "sum"]):
        res = await db.execute(select(model))
        result[name] = [r.__dict__ for r in res.scalars().all()]
    return result
