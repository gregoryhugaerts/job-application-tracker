"""Module containing database models for job applications."""

from datetime import date

from flask_sqlalchemy_lite import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase

db = SQLAlchemy()


class Base(DeclarativeBase):
    pass


class Company(Base):
    """Represents a company.

    Attributes
    ----------
        id: The unique identifier for the company.
        name: The name of the company.

    """

    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)


class Application(Base):
    """Represents a job application.

    Attributes
    ----------
        id: The unique identifier for the application.
        company: The company the application is for.
        job_title: The title of the job being applied for.
        status: The current status of the application (default: 'Applied').
        applied_on: The date the application was submitted.
        notes: Optional notes about the application.

    """

    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
    )
    job_title: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False, default="Applied")
    applied_on: Mapped[date] = mapped_column(nullable=False)
    notes: Mapped[str] = mapped_column(nullable=True)

    company = relationship("Company", back_populates="applications")


Company.applications = relationship("Application", back_populates="company")
