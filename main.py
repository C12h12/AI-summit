from pdf_utils import extract_text_from_pdf
from interview import run_interview
import re
import google.generativeai as genai

# --- Gemini API Setup ---
GEMINI_API_KEY = "AIzaSyA55uoaiy3m6myLQDuDH5uiMlqA9WlHEQs"
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-1.5-flash-latest')

def generate_resources(major, weak_topics):
    topic_str = "; ".join(weak_topics) if weak_topics else major
    recom_prompt = (
        f"You are a helpful AI for interview preparation. The candidate needs to improve in these areas: {topic_str}.\n"
        f"For the field of {major}, provide 3 to 5 high-quality, up-to-date resources most relevant to these topics.\n"
        f"Return ONLY the URLs, one per line, with no titles, descriptions, or extra text."
    )
    resources = []
    try:
        resp = gemini_model.generate_content([{"role": "user", "parts": [recom_prompt]}])
        text = resp.text.strip()

        # Split into lines and keep only lines that look like URLs
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("http://") or line.startswith("https://"):
                resources.append(line)
    except Exception as e:
        print("Resource generation error:", e)

    return resources



# --- Main ---
resume_path = "C:\\Users\\Chaitanya\\Desktop\\Resume\\Chaitanya_Thakre.pdf"
job_desc_path = "C:\\Users\\Chaitanya\\Desktop\\full_stack_developer_job_description.txt"

resume_text = extract_text_from_pdf(resume_path)
job_desc_text = extract_text_from_pdf(job_desc_path)

level = input("Select interview difficulty (easy/moderate/experienced): ").lower()
type = input("Select Type of interview (HR/Technical): ").lower()

if input("Start the interview? (y/n): ").lower() in ["y", "yes", "ye"]:
    results = run_interview(level, type, job_desc_text, resume_text)

    weak_topics = results.get("weak_topics", [])
    major = "Full Stack Development"  # can be extracted dynamically if needed

    resources = generate_resources(major, weak_topics)

    if resources:
        print("\n📚 Recommended URLs:")
        for url in resources:
            print(url)  # plain URL, not clickable
    else:
        print("\nNo additional resources generated.")



else:
    print("Interview canceled.")
