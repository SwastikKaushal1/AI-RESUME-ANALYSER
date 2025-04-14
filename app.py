import streamlit as st
import spacy
import pdfplumber
import docx
import re


st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

st.sidebar.title("👤 Developer Info")
st.sidebar.markdown("""
**Made by:** Swastik Kaushal  
📧 [Email](mailto:your_email@example.com)  
🌐 [GitHub](https://github.com/SwastikKaushal1)  
💼 [LinkedIn](https://www.linkedin.com/in/your-link/)
""")



nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text() or ''
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return '\n'.join([para.text for para in doc.paragraphs])

def analyze_resume(text):
    doc = nlp(text)
    word_count = len([token.text for token in doc if not token.is_punct])
    grammar_errors = len([token for token in doc if token.pos_ == "X"])

    skills = [
        'python', 'java', 'c++', 'javascript', 'html', 'css', 'sql',
        'machine learning', 'deep learning', 'data science', 'data analysis',
        'tensorflow', 'pandas', 'numpy', 'matplotlib', 'power bi',
        'excel', 'react', 'node.js', 'flask', 'django', 'api development',
        'git', 'github', 'docker', 'kubernetes', 'cloud computing',
        'aws', 'azure', 'gcp', 'linux',
        'communication', 'teamwork', 'leadership', 'problem solving',
        'critical thinking', 'time management', 'adaptability',
        'creativity', 'collaboration', 'attention to detail',
        'project management', 'agile', 'scrum', 'kanban',
        'business analysis', 'product management',
        'jira', 'trello', 'notion', 'tableau', 'lookml', 'postman',
        'figma', 'photoshop', 'illustrator', 'vs code', 'slack'
    ]

    found_skills = [skill for skill in skills if skill.lower() in text.lower()]
    sections = ['education', 'experience', 'projects', 'skills', 'certifications']
    found_sections = [s for s in sections if re.search(s, text, re.IGNORECASE)]

    score = 0
    score += min(10, word_count // 30)
    score += 20 if grammar_errors <= 3 else 10
    score += (len(found_skills) / len(skills)) * 30
    score += 10 if word_count > 200 else 5
    score += (len(found_sections) / len(sections)) * 30

    suggestions = []
    if grammar_errors > 3:
        suggestions.append("🔠 Too many grammar issues.")
    if word_count < 150:
        suggestions.append("📄 Resume is too short.")
    if len(found_skills) < 3:
        suggestions.append("💼 Add more relevant skills.")
    if len(found_sections) < 4:
        suggestions.append("🧩 Add missing sections (Education, Experience, etc.)")

    return {
        "Word Count": word_count,
        "Grammar Errors": grammar_errors,
        "Skills Found": found_skills,
        "Sections Found": found_sections,
        "Suggestions": suggestions,
        "Score": int(score)
    }

st.title("📄 AI Resume Analyzer")

uploaded_file = st.file_uploader("Upload your Resume (.pdf or .docx)", type=["pdf", "docx"])

if uploaded_file:
    try:
        if uploaded_file.type == "application/pdf":
            resume_text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            resume_text = extract_text_from_docx(uploaded_file)
        else:
            st.error("Unsupported file format.")
            resume_text = ""

        if resume_text.strip():
            results = analyze_resume(resume_text)

            st.subheader("🧮 Resume Score")
            st.progress(results["Score"])
            st.success(f"Your Resume Score: **{results['Score']} / 100**")

            st.subheader("📊 Resume Stats")
            st.write(f"**Word Count**: {results['Word Count']}")
            st.write(f"**Grammar Issues**: {results['Grammar Errors']}")

            st.subheader("✅ Skills Detected")
            st.info(", ".join(results["Skills Found"]) or "No matching skills detected.")

            st.subheader("🧩 Sections Detected")
            st.info(", ".join(results["Sections Found"]) or "No standard sections found.")

            st.subheader("💡 Suggestions")
            for tip in results["Suggestions"]:
                st.warning(tip)
        else:
            st.error("Couldn't extract any text from the uploaded file.")

    except Exception as e:
        st.error(f"Error while processing your resume: {e}")
