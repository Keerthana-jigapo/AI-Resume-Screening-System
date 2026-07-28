from utils import extract_text, calculate_similarity

resume_path = "resumes/resume1.pdf"

# Resume text
resume_text = extract_text(resume_path)

# Job Description text
with open("job_description.txt", "r", encoding="utf-8") as file:
    job_description = file.read()

# Print both texts
print("===== Resume Text =====")
print(resume_text)

print("\n===== Job Description =====")
print(job_description)

# Calculate similarity
score = calculate_similarity(resume_text, job_description)

print("\n===== Resume Matching Result =====")
print(f"Matching Score: {score:.2f}%")