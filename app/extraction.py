from google import genai
from app.config import settings

from PIL import Image
from fastapi import HTTPException

import io
import json

client = genai.Client(api_key=settings.GEMINI_API_KEY)


def test_gemini():
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Reply with exactly: Gemini connection successful"
    )
    return response.text


def get_extraction_prompt():
    return """
    Extract all information from this marksheet.

    Return ONLY valid JSON.

    Required schema:

    {
      "candidate_details": {
        "name": {"value":"","confidence":0},
        "father_name": {"value":"","confidence":0},
        "mother_name": {"value":"","confidence":0},
        "roll_no": {"value":"","confidence":0},
        "registration_no": {"value":"","confidence":0},
        "dob": {"value":"","confidence":0},
        "exam_year": {"value":"","confidence":0},
        "board_university": {"value":"","confidence":0},
        "institution": {"value":"","confidence":0}
      },

      "subjects": [
        {
          "subject": {"value":"","confidence":0},
          "max_marks_or_credits": {"value":"","confidence":0},
          "obtained_marks_or_credits": {"value":"","confidence":0},
          "grade": {"value":"","confidence":0}
        }
      ],

      "overall_result": {"value":"","confidence":0},
      "overall_grade": {"value":"","confidence":0},
      "division": {"value":"","confidence":0},

      "issue_date": {"value":"","confidence":0},
      "issue_place": {"value":"","confidence":0}
    }

    Rules:
    - Every field must contain value and confidence.
    - Confidence must be between 0 and 1.
    - If a field is missing:
      {"value": null, "confidence": 0.0}
    - Never assign confidence above 0.2 when value is null.
    - Return JSON only.
    """
    

def extract_marksheet_from_image(image_bytes):

    try:
        image = Image.open(io.BytesIO(image_bytes))
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid or corrupted image file"
        )

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                get_extraction_prompt(),
                image
            ]
        )
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Gemini API Error: {str(e)}"
        )

    cleaned = (
        response.text
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    try:
        return json.loads(cleaned)

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Gemini returned invalid JSON",
                "raw_response": response.text
            }
        )