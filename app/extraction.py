from google import genai
from app.config import settings

from PIL import Image
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

    Required fields:

    candidate_details:
    - name
    - father_name
    - mother_name
    - roll_no
    - registration_no
    - dob

    Other fields:
    - board_university
    - institution
    - exam_year
    - overall_result
    - overall_grade
    - division
    - issue_date
    - issue_place

    subjects:
    - subject
    - max_marks_or_credits
    - obtained_marks_or_credits
    - grade

    Every field must have:
    {
      "value": "...",
      "confidence": 0.0
    }

    Confidence must be between 0 and 1.

    Return valid JSON only.
    """


def extract_marksheet_from_image(image_bytes):
    prompt = get_extraction_prompt()

    image = Image.open(io.BytesIO(image_bytes))

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt, image]
    )

    cleaned = response.text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(cleaned)
    except Exception:
        return {
            "raw_response": response.text
        }