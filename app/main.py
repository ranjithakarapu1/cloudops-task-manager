import os
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import select
from .database import Base, engine, get_db
from .models import Task
from .schemas import TaskCreate, TaskUpdate, TaskOut

APP_NAME = os.getenv("APP_NAME", "CloudOps Task Manager")
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "/mnt/shared/uploads"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# For a learning sample. For production, use Alembic migrations instead.
Base.metadata.create_all(bind=engine)

app = FastAPI(title=APP_NAME, version="1.0.0")

@app.get("/")
def root():
    return {"application": APP_NAME, "docs": "/docs", "health": "/health"}

@app.get("/health")
def health():
    # Keep this lightweight for the ALB liveness check.
    return {"status": "ok"}

@app.get("/ready")
def readiness(db: Session = Depends(get_db)):
    try:
        db.execute(select(1))
        return {"status": "ready", "database": "reachable"}
    except Exception:
        raise HTTPException(status_code=503, detail="database unavailable")

@app.post("/tasks", response_model=TaskOut, status_code=201)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    task = Task(title=payload.title, description=payload.description)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@app.get("/tasks", response_model=list[TaskOut])
def list_tasks(db: Session = Depends(get_db)):
    return db.scalars(select(Task).order_by(Task.id.desc())).all()

@app.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    return task

@app.patch("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    db.delete(task)
    db.commit()
    return None

@app.post("/uploads", status_code=201)
async def upload_file(file: UploadFile = File(...)):
    # Demo only: production code should validate file type/size, scan uploads,
    # and use generated object names rather than trusting user-supplied filenames.
    safe_name = Path(file.filename or "upload.bin").name
    destination = UPLOAD_DIR / safe_name
    content = await file.read()
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="file exceeds 10 MB lab limit")
    destination.write_bytes(content)
    return {"filename": safe_name, "bytes": len(content), "storage": str(destination)}
