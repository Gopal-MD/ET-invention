from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Regulation(TimestampMixin, Base):
    __tablename__ = "regulations"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    issuer: Mapped[str] = mapped_column(String(255), nullable=False)
    jurisdiction: Mapped[str] = mapped_column(String(80), nullable=False)
    versions: Mapped[list["RegulatoryVersion"]] = relationship(back_populates="regulation", cascade="all, delete-orphan")


class RegulatoryVersion(TimestampMixin, Base):
    __tablename__ = "regulatory_versions"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    regulation_id: Mapped[str] = mapped_column(ForeignKey("regulations.id"), index=True)
    version: Mapped[str] = mapped_column(String(80), nullable=False)
    source_document_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime)
    effective_at: Mapped[datetime | None] = mapped_column(DateTime)
    regulation: Mapped[Regulation] = relationship(back_populates="versions")
    chunks: Mapped[list["DocumentChunk"]] = relationship(back_populates="version", cascade="all, delete-orphan")
    __table_args__ = (UniqueConstraint("regulation_id", "version"),)


class DocumentChunk(TimestampMixin, Base):
    __tablename__ = "document_chunks"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    version_id: Mapped[str] = mapped_column(ForeignKey("regulatory_versions.id"), index=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    source_location: Mapped[str] = mapped_column(String(120), nullable=False)
    page: Mapped[int | None] = mapped_column(Integer)
    embedding: Mapped[list[float] | None] = mapped_column(JSON)
    version: Mapped[RegulatoryVersion] = relationship(back_populates="chunks")


class BusinessUnit(TimestampMixin, Base):
    __tablename__ = "business_units"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(160), unique=True, nullable=False)


class Obligation(TimestampMixin, Base):
    __tablename__ = "obligations"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    version_id: Mapped[str | None] = mapped_column(ForeignKey("regulatory_versions.id"), index=True)
    statement: Mapped[str] = mapped_column(Text, nullable=False)
    source_chunk_id: Mapped[str | None] = mapped_column(ForeignKey("document_chunks.id"))
    applicability: Mapped[str] = mapped_column(String(40), default="Needs Review")
    review_status: Mapped[str] = mapped_column(String(40), default="Needs review")
    confidence: Mapped[float | None] = mapped_column()


class Policy(TimestampMixin, Base):
    __tablename__ = "policies"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    text: Mapped[str] = mapped_column(Text, default="")


class Control(TimestampMixin, Base):
    __tablename__ = "orm_controls"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    owner: Mapped[str] = mapped_column(String(160), nullable=False)
    status: Mapped[str] = mapped_column(String(60), nullable=False)
    effectiveness: Mapped[str] = mapped_column(String(80), nullable=False)


class EvidenceDocument(TimestampMixin, Base):
    __tablename__ = "evidence_documents"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    control_id: Mapped[str | None] = mapped_column(ForeignKey("orm_controls.id"))
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    review: Mapped[str] = mapped_column(Text, default="")


class Assessment(TimestampMixin, Base):
    __tablename__ = "assessments"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    scope: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(40), nullable=False)
    mode: Mapped[str] = mapped_column(String(80), nullable=False)
    stage_events: Mapped[list["AgentRunEvent"]] = relationship(back_populates="assessment", cascade="all, delete-orphan")


class AssessmentResult(TimestampMixin, Base):
    __tablename__ = "assessment_results"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    assessment_id: Mapped[str] = mapped_column(ForeignKey("assessments.id"), index=True)
    obligation_id: Mapped[str | None] = mapped_column(ForeignKey("obligations.id"))
    result: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)


class Gap(TimestampMixin, Base):
    __tablename__ = "orm_gaps"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    obligation_id: Mapped[str | None] = mapped_column(ForeignKey("obligations.id"))
    control_id: Mapped[str | None] = mapped_column(ForeignKey("orm_controls.id"))
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    severity: Mapped[str] = mapped_column(String(30), nullable=False)
    risk_score: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)


class RiskAssessment(TimestampMixin, Base):
    __tablename__ = "risk_assessments"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    gap_id: Mapped[str] = mapped_column(ForeignKey("orm_gaps.id"), index=True)
    impact: Mapped[int] = mapped_column(Integer, nullable=False)
    likelihood: Mapped[int] = mapped_column(Integer, nullable=False)
    criticality: Mapped[int] = mapped_column(Integer, nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    formula_version: Mapped[str] = mapped_column(String(30), default="v1")


class RemediationPlan(TimestampMixin, Base):
    __tablename__ = "remediation_plans"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    gap_id: Mapped[str] = mapped_column(ForeignKey("orm_gaps.id"), index=True)
    action: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(40), default="Proposed")
    owner: Mapped[str] = mapped_column(String(160), nullable=False)


class RemediationAction(TimestampMixin, Base):
    __tablename__ = "remediation_actions"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    plan_id: Mapped[str] = mapped_column(ForeignKey("remediation_plans.id"), index=True)
    action: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(40), default="Proposed")


class AgentRun(TimestampMixin, Base):
    __tablename__ = "agent_runs"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    agent: Mapped[str] = mapped_column(String(120), nullable=False)
    status: Mapped[str] = mapped_column(String(40), nullable=False)
    model: Mapped[str | None] = mapped_column(String(120))
    error: Mapped[str | None] = mapped_column(Text)
    events: Mapped[list["AgentRunEvent"]] = relationship(back_populates="run", cascade="all, delete-orphan")


class AgentRunEvent(TimestampMixin, Base):
    __tablename__ = "agent_run_events"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    run_id: Mapped[str | None] = mapped_column(ForeignKey("agent_runs.id"), index=True)
    assessment_id: Mapped[str | None] = mapped_column(ForeignKey("assessments.id"), index=True)
    stage: Mapped[str] = mapped_column(String(120), nullable=False)
    status: Mapped[str] = mapped_column(String(40), nullable=False)
    output: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    run: Mapped[AgentRun | None] = relationship(back_populates="events")
    assessment: Mapped[Assessment | None] = relationship(back_populates="stage_events")


class AuditEvent(TimestampMixin, Base):
    __tablename__ = "orm_audit_events"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    actor: Mapped[str] = mapped_column(String(120), nullable=False)
    event: Mapped[str] = mapped_column(String(160), nullable=False)
    record_id: Mapped[str] = mapped_column(String(64), nullable=False)
    outcome: Mapped[str] = mapped_column(String(80), nullable=False)
    event_metadata: Mapped[dict[str, Any]] = mapped_column("metadata", JSON, default=dict)


class ReviewDecision(TimestampMixin, Base):
    __tablename__ = "review_decisions"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    record_id: Mapped[str] = mapped_column(String(64), index=True)
    decision: Mapped[str] = mapped_column(String(50), nullable=False)
    reviewer: Mapped[str] = mapped_column(String(120), nullable=False)
    comment: Mapped[str] = mapped_column(Text, default="")


class ApplicationSetting(TimestampMixin, Base):
    __tablename__ = "application_settings"
    key: Mapped[str] = mapped_column(String(120), primary_key=True)
    value: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
