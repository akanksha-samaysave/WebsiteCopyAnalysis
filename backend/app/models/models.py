from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Website(Base):
    __tablename__ = "websites"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True)
    domain = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    analyses = relationship("Analysis", back_populates="website", cascade="all, delete-orphan")
    screenshots = relationship("Screenshot", back_populates="website", cascade="all, delete-orphan")


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, index=True)
    website_id = Column(Integer, ForeignKey("websites.id"), index=True)
    status = Column(String, default="pending")  # pending, processing, completed, failed
    raw_html = Column(Text, nullable=True)
    visible_text = Column(Text, nullable=True)
    sections = Column(JSON, nullable=True)
    analysis_metadata = Column("metadata", JSON, nullable=True)
    error_message = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    website = relationship("Website", back_populates="analyses")
    scores = relationship("Score", back_populates="analysis", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="analysis", cascade="all, delete-orphan")
    report = relationship("Report", back_populates="analysis", uselist=False, cascade="all, delete-orphan")


class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"), index=True)
    category = Column(String)  # design, messaging, trust, clarity, conversion, ux
    score = Column(Float)
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    analysis = relationship("Analysis", back_populates="scores")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"), index=True)
    priority = Column(String)  # High, Medium, Low
    title = Column(String)
    description = Column(Text)
    reasoning = Column(Text)
    category = Column(String)  # copywriting, ux, trust, design, conversion
    created_at = Column(DateTime, default=datetime.utcnow)

    analysis = relationship("Analysis", back_populates="recommendations")


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"), index=True)
    pdf_path = Column(String, nullable=True)
    csv_path = Column(String, nullable=True)
    generated_at = Column(DateTime, default=datetime.utcnow)

    analysis = relationship("Analysis", back_populates="report")


class Screenshot(Base):
    __tablename__ = "screenshots"

    id = Column(Integer, primary_key=True, index=True)
    website_id = Column(Integer, ForeignKey("websites.id"), index=True)
    file_path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    website = relationship("Website", back_populates="screenshots")
