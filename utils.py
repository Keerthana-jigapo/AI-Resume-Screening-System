import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract_text(pdf_path):
    text = ""

    with pdfplumber.open(pdf_path) as pdf:
        print("Pages:", len(pdf.pages))

        for page in pdf.pages:
            page_text = page.extract_text()

            # If normal extraction fails, try extracting words
            if not page_text:
                words = page.extract_words()
                page_text = " ".join([w["text"] for w in words])

            if page_text:
                text += page_text + "\n"

    return text.strip()


def calculate_similarity(resume_text, job_description):
    documents = [resume_text, job_description]

    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(documents)

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    return similarity[0][0] * 100