"""Utility helpers to populate the database with demo content.

This module is used both by the API endpoints and the command-line quickstart
script so that beginners can get a working dataset without understanding the
full backend stack.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

from . import models
from .auth import get_password_hash
from .database import Base, DEFAULT_SQLITE_PATH, engine, session_scope


DEMO_USER_EMAIL = "demo@student.local"
DEMO_USER_PASSWORD = "English123!"
DEMO_USER_NAME = "Demo Learner"


@dataclass
class SeedResult:
    created_content: bool
    created_user: bool

    def as_payload(self) -> Dict[str, str]:
        status = "seeded" if self.created_content else "already_seeded"
        user_status = "created" if self.created_user else "existing"
        return {"status": status, "demo_user": user_status}


def _ensure_learning_content() -> bool:
    """Insert demo exams/courses/lessons if the database is empty."""
    with session_scope() as session:
        if session.query(models.Exam).count() > 0:
            return False

        cet4 = models.Exam(name="CET-4", description="College English Test Band 4")
        ielts = models.Exam(
            name="IELTS", description="International English Language Testing System"
        )
        session.add_all([cet4, ielts])
        session.flush()

        cet_course = models.Course(
            exam_id=cet4.id,
            title="CET-4 Core Vocabulary",
            level="intermediate",
            description="Cover the must-know vocabulary for CET-4 with spaced repetition",
        )
        ielts_course = models.Course(
            exam_id=ielts.id,
            title="IELTS Writing Task 2",
            level="advanced",
            description="Argumentative essay techniques and model answers",
        )
        session.add_all([cet_course, ielts_course])
        session.flush()

        session.add_all(
            [
                models.Lesson(
                    course_id=cet_course.id,
                    title="Vocabulary Set 1",
                    content="20 high-frequency CET-4 words with example sentences.",
                    duration_minutes=20,
                ),
                models.Lesson(
                    course_id=ielts_course.id,
                    title="Essay Structure Overview",
                    content="How to structure an IELTS Writing Task 2 essay effectively.",
                    duration_minutes=25,
                ),
            ]
        )
    return True


def _ensure_demo_user() -> bool:
    with session_scope() as session:
        existing = (
            session.query(models.User).filter(models.User.email == DEMO_USER_EMAIL).first()
        )
        if existing:
            return False

        user = models.User(
            email=DEMO_USER_EMAIL,
            full_name=DEMO_USER_NAME,
            hashed_password=get_password_hash(DEMO_USER_PASSWORD),
            target_exam="CET-4",
        )
        session.add(user)
    return True


def seed_basic_data() -> SeedResult:
    """Create the database schema and populate demo data if needed."""
    Base.metadata.create_all(bind=engine)
    created_content = _ensure_learning_content()
    created_user = _ensure_demo_user()
    return SeedResult(created_content=created_content, created_user=created_user)


def print_summary(result: SeedResult) -> None:
    db_path = Path(DEFAULT_SQLITE_PATH)
    print("📚 数据库位置:", db_path)
    if result.created_content:
        print("✅ 已写入示例考试、课程和课时数据。")
    else:
        print("ℹ️ 检测到数据库已有学习内容，未重复写入。")

    if result.created_user:
        print("✅ 创建了演示账号，方便直接登录体验。")
    else:
        print("ℹ️ 演示账号已存在，保留原有密码。")

    print("\n演示账号信息：")
    print(f"  邮箱: {DEMO_USER_EMAIL}")
    print(f"  初始密码: {DEMO_USER_PASSWORD}")


def cli_main() -> None:
    parser = argparse.ArgumentParser(
        description="创建示例数据，帮助初学者快速体验后端接口",
    )
    parser.add_argument(
        "--silent",
        action="store_true",
        help="仅进行数据写入，不打印说明。",
    )
    args = parser.parse_args()

    result = seed_basic_data()
    if not args.silent:
        print_summary(result)


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    cli_main()
