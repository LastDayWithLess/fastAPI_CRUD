from fastapi import FastAPI, Depends
from sqlalchemy import insert, select, update
from sqlalchemy.orm import Session
from classesModel import Worker, Resume
from database import get_db
from models import WorkerModel, ResumeModel
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

@app.post("/add_worker")
async def add_worker_in_db(worker: Worker, db: AsyncSession = Depends(get_db)):
    stmt = insert(WorkerModel).returning(WorkerModel.id, WorkerModel.username)

    result = await db.execute(stmt, [{"username": worker.username},])
    await db.commit()

    return {"result": dict(result.all())}

@app.post("/add_resume")
async def add_resume_in_db(resumes: List[Resume], db: AsyncSession = Depends(get_db)):
    stmt = insert(ResumeModel)

    resume_data = [
        {
            "title": resume.title,
            "compensation": resume.compensation,
            "worker_id": resume.worker_id,
            "create_at": resume.create_at 
        }
        for resume in resumes
    ]

    await db.execute(stmt, resume_data)
    await db.commit()

    return {"result": "ok"}

@app.put("/alter_worker/{id_worker}")
async def alter_worker_in_db(id_worker: int, worker: Worker, db: AsyncSession = Depends(get_db)):

    result = await db.execute(update(WorkerModel).where(WorkerModel.id == id_worker).values(username=worker.username).returning(WorkerModel.id, WorkerModel.username))

    if result is None:
        return {"error": "Worker not found"}

    await db.commit()
    res = result.first()
    
    return {"alter": {"id": res[0], "username": res[1]}}

@app.get('/get_workers')
async def get_workers_in_db(db: AsyncSession = Depends(get_db)):
    result = await db.scalars(select(WorkerModel))

    return result.all()

@app.get('/get_workers_and_resumes')
async def get_workers_and_resumes_in_db(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(WorkerModel.username, ResumeModel.title).join_from(WorkerModel, ResumeModel, WorkerModel.id == ResumeModel.worker_id))

    return [{"username": username, "resume": title} for username, title in result.all()]

