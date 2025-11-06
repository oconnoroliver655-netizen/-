from __future__ import annotations

from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import auth, models, schemas
from .auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_db,
    get_password_hash,
)
from .database import Base, engine
from .seed import seed_basic_data

Base.metadata.create_all(bind=engine)

app = FastAPI(title="English Exam Learning Platform API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/auth/register", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if auth.get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        target_exam=user.target_exam,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/auth/login", response_model=schemas.Token)
def login(form_data: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.email, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token = create_access_token({"sub": user.email})
    return schemas.Token(access_token=access_token)


@app.get("/users/me", response_model=schemas.UserRead)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user


@app.post("/exams", response_model=schemas.ExamRead, status_code=status.HTTP_201_CREATED)
def create_exam(exam: schemas.ExamCreate, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    db_exam = models.Exam(name=exam.name, description=exam.description)
    db.add(db_exam)
    db.commit()
    db.refresh(db_exam)
    return db_exam


@app.get("/exams", response_model=List[schemas.ExamRead])
def list_exams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    exams = db.query(models.Exam).offset(skip).limit(limit).all()
    return exams


@app.post("/courses", response_model=schemas.CourseRead, status_code=status.HTTP_201_CREATED)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    exam = db.query(models.Exam).filter(models.Exam.id == course.exam_id).first()
    if exam is None:
        raise HTTPException(status_code=404, detail="Exam not found")
    db_course = models.Course(
        exam_id=course.exam_id,
        title=course.title,
        level=course.level,
        description=course.description,
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


@app.get("/courses", response_model=List[schemas.CourseRead])
def list_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    courses = db.query(models.Course).offset(skip).limit(limit).all()
    return courses


@app.post("/lessons", response_model=schemas.LessonRead, status_code=status.HTTP_201_CREATED)
def create_lesson(lesson: schemas.LessonCreate, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    course = db.query(models.Course).filter(models.Course.id == lesson.course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    db_lesson = models.Lesson(
        course_id=lesson.course_id,
        title=lesson.title,
        content=lesson.content,
        duration_minutes=lesson.duration_minutes,
    )
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson


@app.get("/lessons", response_model=List[schemas.LessonRead])
def list_lessons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    lessons = db.query(models.Lesson).offset(skip).limit(limit).all()
    return lessons


@app.post("/study-plans", response_model=schemas.StudyPlanRead, status_code=status.HTTP_201_CREATED)
def create_study_plan(
    study_plan: schemas.StudyPlanCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_plan = models.StudyPlan(user_id=current_user.id, name=study_plan.name, goal=study_plan.goal)
    if study_plan.lesson_ids:
        lessons = db.query(models.Lesson).filter(models.Lesson.id.in_(study_plan.lesson_ids)).all()
        if len(lessons) != len(set(study_plan.lesson_ids)):
            raise HTTPException(status_code=404, detail="One or more lessons not found")
        db_plan.lessons.extend(lessons)
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan


@app.patch("/study-plans/{plan_id}", response_model=schemas.StudyPlanRead)
def update_study_plan(
    plan_id: int,
    payload: schemas.StudyPlanUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_plan = (
        db.query(models.StudyPlan)
        .filter(models.StudyPlan.id == plan_id, models.StudyPlan.user_id == current_user.id)
        .first()
    )
    if db_plan is None:
        raise HTTPException(status_code=404, detail="Study plan not found")

    if payload.name is not None:
        db_plan.name = payload.name
    if payload.goal is not None:
        db_plan.goal = payload.goal
    if payload.lesson_ids is not None:
        lessons = db.query(models.Lesson).filter(models.Lesson.id.in_(payload.lesson_ids)).all()
        if len(lessons) != len(set(payload.lesson_ids)):
            raise HTTPException(status_code=404, detail="One or more lessons not found")
        db_plan.lessons = lessons

    db.commit()
    db.refresh(db_plan)
    return db_plan


@app.get("/study-plans", response_model=List[schemas.StudyPlanRead])
def list_study_plans(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    plans = (
        db.query(models.StudyPlan)
        .filter(models.StudyPlan.user_id == current_user.id)
        .all()
    )
    return plans


@app.get("/dashboard/summary", response_model=schemas.DashboardSummary)
def dashboard_summary(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    total_courses = db.query(models.Course).count()
    total_lessons = db.query(models.Lesson).count()
    total_study_plans = (
        db.query(models.StudyPlan)
        .filter(models.StudyPlan.user_id == current_user.id)
        .count()
    )
    upcoming_lessons = (
        db.query(models.Lesson)
        .join(models.StudyPlan.lessons)
        .filter(models.StudyPlan.user_id == current_user.id)
        .order_by(models.Lesson.created_at.desc())
        .limit(5)
        .all()
    )
    return schemas.DashboardSummary(
        total_courses=total_courses,
        total_lessons=total_lessons,
        total_study_plans=total_study_plans,
        upcoming_lessons=upcoming_lessons,
    )


@app.post("/seed/basic", response_model=schemas.SeedResponse, status_code=status.HTTP_201_CREATED)
def seed_basic(_: models.User = Depends(get_current_user)):
    """Seed the database with default demo content so beginners can explore the API."""
    result = seed_basic_data()
    return result.as_payload()

