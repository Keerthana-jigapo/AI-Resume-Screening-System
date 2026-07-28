import streamlit as st
from utils import extract_text, calculate_similarity
import tempfile
import os
from fpdf import FPDF
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Resume Screening System", page_icon="📄", layout="wide")

st.title("📊 Resume Analysis")

uploaded_resume = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

job_description = st.text_area(
    "Enter Job Description",
    height=250
)

if st.button("Analyze Resume"):

    if uploaded_resume is not None and job_description.strip() != "":

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_resume.read())
            temp_path = temp_file.name

        resume_text = extract_text(temp_path)

        score = calculate_similarity(resume_text, job_description)

        st.success(f"Matching Score : {score:.2f}%")

        st.progress(int(score))

        skills = [
            "Python",
            "SQL",
            "Machine Learning",
            "Power BI",
            "Excel",
            "Communication",
            "Statistics"
        ]

        matched = []
        missing = []

        resume_lower = resume_text.lower()

        for skill in skills:
            if skill.lower() in resume_lower:
                matched.append(skill)
            else:
                missing.append(skill)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("✅ Matched Skills")

            if matched:
                for skill in matched:
                    st.success(skill)
            else:
                st.error("No Matched Skills")

        with col2:
            st.subheader("❌ Missing Skills")

            if missing:
                for skill in missing:
                    st.error(skill)
            else:
                st.success("No Missing Skills 🎉")

        st.subheader("📈 Skills Distribution")

        fig, ax = plt.subplots(figsize=(5,5))

        ax.pie(
            [len(matched), len(missing)],
            labels=["Matched","Missing"],
            autopct="%1.1f%%",
            startangle=90,
            colors=["green","red"]
        )

        ax.axis("equal")

        st.pyplot(fig)

        st.subheader("💡 Suggestions")

        if missing:
            st.info("Improve your resume by adding these skills:")
            for skill in missing:
                st.write("👉", skill)
        else:
            st.success("Excellent! Your resume contains all required skills.")

        st.subheader("🏆 Final Result")

        if score >= 80:
            st.success("⭐⭐⭐⭐⭐ Excellent Match")
        elif score >= 60:
            st.success("⭐⭐⭐⭐ Good Match")
        elif score >= 40:
            st.warning("⭐⭐⭐ Average Match")
        else:
            st.error("⭐ Low Match")

        # ---------------- PDF REPORT ----------------

        pdf = FPDF()
        pdf.add_page()

        pdf.set_font("Arial", "B", 16)
        pdf.cell(190, 10, "ATS Resume Report", ln=True)

        pdf.set_font("Arial", "", 12)
        pdf.cell(190, 10, f"Matching Score : {score:.2f}%", ln=True)

        pdf.ln(5)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(190, 10, "Matched Skills", ln=True)

        pdf.set_font("Arial", "", 12)
        for skill in matched:
            pdf.cell(190, 8, "- " + skill, ln=True)

        pdf.ln(5)

        pdf.set_font("Arial", "B", 12)
        pdf.cell(190, 10, "Missing Skills", ln=True)

        pdf.set_font("Arial", "", 12)

        if missing:
            for skill in missing:
                pdf.cell(190, 8, "- " + skill, ln=True)
        else:
            pdf.cell(190, 8, "No Missing Skills", ln=True)

        pdf.ln(5)

        pdf.set_font("Arial", "B", 12)
        pdf.cell(190, 10, "Final Result", ln=True)

        pdf.set_font("Arial", "", 12)

        if score >= 80:
            pdf.cell(190, 8, "Excellent Match", ln=True)
        elif score >= 60:
            pdf.cell(190, 8, "Good Match", ln=True)
        elif score >= 40:
            pdf.cell(190, 8, "Average Match", ln=True)
        else:
            pdf.cell(190, 8, "Low Match", ln=True)

        pdf.output("ATS_Report.pdf")

        with open("ATS_Report.pdf", "rb") as file:
            st.download_button(
                label="📄 Download ATS Report",
                data=file,
                file_name="ATS_Report.pdf",
                mime="application/pdf"
            )

        os.remove(temp_path)

    else:
        st.warning("Please upload resume and enter job description.")