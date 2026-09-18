import os
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract


def extract_text(image_path):
    """
    Extract text from a package image using Tesseract OCR.

    The function returns a list of detected text lines.
    It does not require OpenCV, PaddleOCR, or PaddlePaddle.
    """

    extracted = []

    try:
        # Check whether the image exists
        if not os.path.exists(image_path):
            print("\n==============================")
            print("OCR ERROR")
            print("==============================")
            print(f"Image not found: {image_path}")
            print("==============================\n")
            return extracted

        # Open image
        image = Image.open(image_path)

        # Convert to RGB
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Make the image larger for better OCR
        width, height = image.size

        if width < 1500:
            scale = 1500 / width
            new_width = int(width * scale)
            new_height = int(height * scale)
            image = image.resize(
                (new_width, new_height),
                Image.Resampling.LANCZOS
            )

        # Convert to grayscale
        gray = image.convert("L")

        # Improve contrast
        contrast = ImageEnhance.Contrast(gray)
        gray = contrast.enhance(1.5)

        # Slightly sharpen the image
        gray = gray.filter(ImageFilter.SHARPEN)

        # Run Tesseract OCR
        text = pytesseract.image_to_string(
            gray,
            lang="eng",
            config="--psm 6"
        )

        # Convert OCR output into clean lines
        for line in text.splitlines():
            line = line.strip()

            if line:
                extracted.append(line)

        # Print OCR result in terminal
        print("\n==============================")
        print("OCR DETECTED TEXT")
        print("==============================")

        if extracted:
            for line in extracted:
                print(line)
        else:
            print("No text detected.")

        print("==============================\n")

    except Exception as e:
        print("\n==============================")
        print("OCR ERROR")
        print("==============================")
        print(str(e))
        print("==============================\n")

    return extracted
