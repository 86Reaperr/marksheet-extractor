from pydantic import BaseModel
from typing import List, Optional


class ExtractedField(BaseModel):
    value: Optional[str] = None
    confidence: float


class Subject(BaseModel):
    subject: ExtractedField
    max_marks_or_credits: ExtractedField
    obtained_marks_or_credits: ExtractedField
    grade: Optional[ExtractedField] = None


class CandidateDetails(BaseModel):
    name: ExtractedField
    father_name: Optional[ExtractedField] = None
    mother_name: Optional[ExtractedField] = None
    roll_no: Optional[ExtractedField] = None
    registration_no: Optional[ExtractedField] = None
    dob: Optional[ExtractedField] = None


class MarksheetResponse(BaseModel):
    candidate_details: CandidateDetails

    board_university: Optional[ExtractedField] = None
    institution: Optional[ExtractedField] = None
    exam_year: Optional[ExtractedField] = None

    overall_result: Optional[ExtractedField] = None
    overall_grade: Optional[ExtractedField] = None
    division: Optional[ExtractedField] = None

    issue_date: Optional[ExtractedField] = None
    issue_place: Optional[ExtractedField] = None

    subjects: List[Subject]