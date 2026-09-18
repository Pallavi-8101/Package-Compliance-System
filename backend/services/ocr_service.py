import os

# Disable problematic PIR / oneDNN paths
os.environ["FLAGS_enable_pir_api"] = "0"
os.environ["FLAGS_use_mkldnn"] = "0"

from paddleocr import PaddleOCR


ocr = PaddleOCR(
    lang="en",
    enable_mkldnn=False,
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False
)


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

        print("\n==============================")
        print("OCR DETECTED TEXT")
        print("==============================")

        if extracted:
            for text in extracted:
                print(text)
        else:
            print("No text detected.")

        print("==============================\n")

    except Exception as e:

        print("\n==============================")
        print("OCR ERROR")
        print("==============================")
        print(e)
        print("==============================\n")

    return extracted