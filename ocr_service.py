from paddleocr import PaddleOCR

# OCR engine
ocr = PaddleOCR(lang="en")


def extract_text(image_path):
    """
    Extract text from a package image.
    Returns a list of detected text lines.
    """

    extracted = []

    try:
        result = ocr.predict(image_path)

        for page in result:

            if not hasattr(page, "json"):
                continue

            data = page.json

            if isinstance(data, dict):
                data = data.get("res", data)

            texts = data.get("rec_texts", [])

            for text in texts:
                if text and text.strip():
                    extracted.append(text.strip())

    except Exception as e:
        print("OCR Error:", e)

    return extracted