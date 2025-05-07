from flask import Flask, render_template, request
from resume_extractor import extract_resume_text
from groq_client import analyze_resume_with_groq
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        resume_file = request.files['resume']
        job_description = request.form['job_description']

        if resume_file and allowed_file(resume_file.filename):
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
            resume_file.save(resume_path)

            resume_text = extract_resume_text(resume_path)
            if not resume_text:
                return "Failed to extract text from the resume."

            result = analyze_resume_with_groq(resume_text, job_description)

            return render_template('index.html', result=result)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
