import streamlit as st
import fitz  # PyMuPDF
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
st.set_page_config(page_title="GR ATS RESUME EXPERT")
st.header("ATS TRACKING SYSTEM")

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        pdf_text = ""
        with fitz.open(uploaded_file) as doc:
            for page in doc:
                pdf_text += page.get_text()

        return pdf_text
    else:
        raise FileNotFoundError("No file uploaded")

@st.cache
def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_text, pdf_content, prompt])
    return response.text

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

input_text = st.text_area("JOB DESCRIPTION:")
uploaded_file = st.file_uploader("UPLOAD YOUR RESUME (PDF)..", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell me About the Resume")
submit3 = st.button("Percentage match")

input_prompt1 = """
You are an experienced Technical Human Resource Manager, your task is to review the provided resume against the job description.
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality,
your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
the job description. First, the output should come as a percentage, then keywords missing, and lastly final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt1)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume") 

if submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt3)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")
