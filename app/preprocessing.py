from io import BytesIO

import fitz
import numpy as np
from PIL import Image


def process_file(file_bytes: bytes, filename: str):
    filename = filename.lower()

    if filename.endswith((".jpg", ".jpeg", ".png")):
        return [file_bytes]

    if filename.endswith(".pdf"):
        pdf = fitz.open(stream=file_bytes, filetype="pdf")
        images = []

        for page in pdf:
            pix = page.get_pixmap()

            img_array = np.frombuffer(
                pix.samples,
                dtype=np.uint8
            ).reshape(
                pix.height,
                pix.width,
                pix.n
            )

            img = Image.fromarray(img_array)

            buffer = BytesIO()
            img.save(buffer, format="PNG")

            images.append(buffer.getvalue())

        return images

    raise ValueError("Unsupported file format")