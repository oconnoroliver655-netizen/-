from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Literal

from pydantic import BaseModel, EmailStr, Field


class LessonBase(BaseModel):
    title: str = Field(..., max_length=255)
    content: str
    duration_minutes: int = Field(..., ge=1, le=240)


class LessonCreate(LessonBase):
    course_id: int


class LessonRead(LessonBase):
    id: int
    course_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class CourseBase(BaseModel):
    title: str = Field(..., max_length=255)
    level: str = Field(..., max_length=50)
    description: Optional[str]


class CourseCreate(CourseBase):
    exam_id: int


class CourseRead(CourseBase):
    id: int
    exam_id: int
    created_at: datetime
    updated_at: datetime
    lessons: List[LessonRead] = []

    class Config:
        orm_mode = True


class ExamBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str]


class ExamCreate(ExamBase):
    pass


class ExamRead(ExamBase):
    id: int
    created_at: datetime
    updated_at: datetime
    courses: List[CourseRead] = []

    class Config:
        orm_mode = True


class StudyPlanBase(BaseModel):
    name: str
    goal: Optional[str]


class StudyPlanCreate(StudyPlanBase):
    lesson_ids: List[int] = []


class StudyPlanUpdate(StudyPlanBase):
    lesson_ids: Optional[List[int]] = None


class StudyPlanRead(StudyPlanBase):
    id: int
    user_id: int
    lessons: List[LessonRead] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., max_length=255)
    target_exam: Optional[str] = Field(None, max_length=100)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class DashboardSummary(BaseModel):
    total_courses: int
    total_lessons: int
    total_study_plans: int
    upcoming_lessons: List[LessonRead]


class SeedResponse(BaseModel):
    status: Literal["seeded", "already_seeded"]
    demo_user: Literal["created", "existing"]

