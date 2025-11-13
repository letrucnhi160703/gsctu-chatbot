import zipfile
from bs4 import BeautifulSoup
from docx import Document
import PyPDF2
import io
import sys
import os

ZIP_PATH = "dataset/gs.ctu.edu.vn.zip"
OUTPUT_PATH = "dataset/processed_data.txt"


def extract_txt(data):
    return data.decode("utf-8", errors="ignore")

def extract_docx(data):
    file_stream = io.BytesIO(data)
    doc = Document(file_stream)
    return "\n".join(para.text for para in doc.paragraphs)

def extract_pdf(data):
    text = []
    reader = PyPDF2.PdfReader(io.BytesIO(data))
    for page in reader.pages:
        t = page.extract_text()
        if t:
            text.append(t)
    return "\n".join(text)

def extract_html(data):
    soup = BeautifulSoup(data.decode("utf-8", errors="ignore"), "html.parser")
    raw = soup.get_text("\n")

    lines = raw.splitlines()
    cleaned = [line.strip() for line in lines if line.strip()]
    return "\n".join(cleaned)


def main():
    if not os.path.exists(ZIP_PATH):
        print("Cannot find ZIP file:", ZIP_PATH)
        sys.exit(1)

    output = open(OUTPUT_PATH, "w", encoding="utf-8")
    count = 0

    with zipfile.ZipFile(ZIP_PATH, "r") as z:
        for name in z.namelist():

            ext = name.lower()

            if ext.endswith(".html") or ext.endswith(".htm"):
                filetype = "HTML"
            elif ext.endswith(".txt"):
                filetype = "TXT"
            elif ext.endswith(".pdf"):
                filetype = "PDF"
            elif ext.endswith(".docx"):
                filetype = "DOCX"
            else:
                continue

            count += 1
            print(f"[{count}] Processing: {name} ({filetype})")

            data = z.read(name)

            try:
                if filetype == "HTML":
                    text = extract_html(data)
                elif filetype == "TXT":
                    text = extract_txt(data)
                elif filetype == "PDF":
                    text = extract_pdf(data)
                elif filetype == "DOCX":
                    text = extract_docx(data)
                else:
                    continue

                output.write(f"\n===== FILE: {name} =====\n{text}\n")

            except Exception as e:
                print("Error when reading file:", name, e)

            if count == 10:
                break

    output.close()
    print("------------------ Total processed files:", count)
    print("------------------ Output file:", OUTPUT_PATH)


if __name__ == "__main__":
    main()
