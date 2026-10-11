from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import Assessment, AssessmentResult, Base, RegulatoryVersion, Regulation


def test_orm_schema_and_relationships_create_in_sqlite():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        regulation = Regulation(id="REG-1", name="Synthetic standard", issuer="Demo issuer", jurisdiction="India")
        version = RegulatoryVersion(id="VER-1", regulation=regulation, version="v1")
        assessment = Assessment(id="ASMT-1", scope="Reporting", status="completed", mode="rules")
        result = AssessmentResult(id="RES-1", assessment_id="ASMT-1", result={"verified": False})
        session.add_all([regulation, version, assessment, result])
        session.commit()
        assert session.get(Regulation, "REG-1").versions[0].version == "v1"
        assert session.get(AssessmentResult, "RES-1").result["verified"] is False
