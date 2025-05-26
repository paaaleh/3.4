from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import Base, Student
from database import engine, SessionLocal
from crud import *

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/students/", response_model=List[dict])
def read_students(db: Session = Depends(get_db)):
    students = get_all_students(db)
    return [s.__dict__ for s in students]

@app.get("/students/by_faculty/{faculty}", response_model=List[dict])
def students_by_faculty(faculty: str, db: Session = Depends(get_db)):
    return [s.__dict__ for s in get_students_by_faculty(db, faculty)]

@app.get("/students/unique_courses", response_model=List[str])
def unique_courses(db: Session = Depends(get_db)):
    return [c[0] for c in get_unique_courses(db)]

@app.get("/students/avg_grade_by_faculty", response_model=List[dict])
def avg_grade_by_faculty(db: Session = Depends(get_db)):
    return [{"faculty": f, "average_grade": round(avg, 2)} for f, avg in get_average_grade_by_faculty(db)]

@app.get("/students/low_grades/{course}", response_model=List[dict])
def students_with_low_grades(course: str, db: Session = Depends(get_db)):
    return [s.__dict__ for s in get_students_with_low_grade(db, course)]

@app.put("/students/{student_id}", response_model=dict)
def update_student_record(student_id: int, updates: dict, db: Session = Depends(get_db)):
    student = update_student(db, student_id, updates)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student.__dict__

@app.delete("/students/{student_id}", response_model=dict)
def delete_student_record(student_id: int, db: Session = Depends(get_db)):
    student = delete_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student.__dict__
