# FaceVPlus — AI-Powered Face & Voice Attendance System

FaceVPlus is an AI-powered attendance management system designed to simplify classroom attendance using facial recognition and optional voice-based identification. Built with Python and Streamlit, the application provides separate teacher and student interfaces, subject enrollment, attendance analysis, and attendance record management.

## ✨ Features

- **Face Recognition:** Identify registered students using facial embeddings.
- **AI Attendance:** Analyze classroom photos captured through a camera or uploaded by a teacher.
- **Teacher Dashboard:** Manage subjects and initiate attendance analysis.
- **Student Dashboard:** Log in using facial recognition and view enrolled subjects and attendance statistics.
- **Subject Enrollment:** Allow students to enroll in available subjects and unenroll when necessary.
- **Attendance Tracking:** Record attendance status, timestamps, and the source photos used for identification.
- **Optional Voice Enrollment:** Capture voice samples during student registration for voice-based identification.
- **Supabase Integration:** Store student profiles, teacher information, subject enrollments, and attendance records.
- **Interactive Interface:** Built with Streamlit, with custom styling and reusable UI components.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Interactive web application |
| OpenCV / NumPy | Image processing |
| dlib / face-recognition models | Facial detection and embeddings |
| scikit-learn | Face classification |
| Supabase | Database and backend services |
| Pillow | Image handling |
| Pandas | Attendance data processing |
| Voice-processing pipeline | Optional voice embedding generation |

## 📁 Project Structure

```text
FaceVPlus/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── src/
│   ├── components/
│   │   ├── header.py
│   │   ├── footer.py
│   │   ├── subject_card.py
│   │   ├── dialog_enroll.py
│   │   └── dialog_add_photoes.py
│   │
│   ├── database/
│   │   ├── config.py
│   │   └── db.py
│   │
│   ├── pipelines/
│   │   ├── face_pipeline.py
│   │   └── voice_pipeline.py
│   │
│   ├── screens/
│   │   ├── student_screen.py
│   │   └── teacher_screen.py
│   │
│   └── ui/
│       └── base_layout.py
│
└── .streamlit/
    └── secrets.toml
```

*The tree illustrates the project's main modules. Adjust filenames to match your actual repository.*

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/FaceVPlus.git
cd FaceVPlus
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Some facial-recognition dependencies, especially `dlib`, may require compatible Python versions, build tools, or additional system libraries.

### 4. Configure Supabase

Create a project in [Supabase](https://supabase.com/) and configure your database tables to match the application's queries and schema.

Create `.streamlit/secrets.toml` in your project directory:

```toml
SUPABASE_URL = "YOUR_SUPABASE_PROJECT_URL"
SUPABASE_KEY = "YOUR_SUPABASE_API_KEY"
```

Replace the placeholders with your actual credentials. The key names must match those used by your database configuration code.

**Security:** Never commit `secrets.toml`, database passwords, or private API keys to GitHub.

### 5. Run the application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal, usually:

`http://localhost:8501`

## 🧑‍🏫 How It Works

### Teacher workflow

1. Log in to the teacher dashboard.
2. Create or select a subject.
3. Add classroom photos using the camera or file uploader.
4. Run facial recognition on the collected photos.
5. Compare detected student IDs against the students enrolled in the selected subject.
6. Review the attendance results and associated photo sources.
7. Save attendance records through the application's attendance-recording workflow.

### Student workflow

1. Open the student portal.
2. Capture a face image using the camera.
3. The system attempts to identify the registered student.
4. New students can register their name and facial features.
5. Students can optionally provide a voice sample during registration.
6. After login, students can view their enrolled subjects and attendance statistics.

## 🧠 Face Recognition Pipeline

The face-recognition pipeline processes an image to identify registered students.

1. **Image capture:** Obtain an image from the camera or uploaded files.
2. **Face detection:** Detect faces in the image.
3. **Feature extraction:** Generate facial embeddings for detected faces.
4. **Classification:** Compare or classify embeddings using the trained recognition model.
5. **Identity matching:** Associate recognized identities with student records.
6. **Attendance evaluation:** Match detected students against the selected subject's enrollment records.

The system's accuracy depends on image quality, lighting, camera position, model configuration, and the quality of the enrolled facial samples.

## 🎙️ Voice Recognition

FaceVPlus includes a voice-processing pipeline and supports optional voice enrollment during registration.

The voice pipeline can generate voice embeddings from audio samples. A complete voice-based attendance workflow also requires reliable speaker matching, suitable thresholds, and integration with attendance recording.

## 🗄️ Database

Supabase provides the backend database for application records.

The application currently references tables such as:

- `students` — student profiles and recognition data.
- `teachers` — teacher accounts.
- `subject_students` — student-to-subject enrollment relationships.
- Attendance records — student attendance status, subject, and timestamp.

Use the actual table names and column definitions from your Supabase schema when configuring a new environment.

## ☁️ Deployment

FaceVPlus can be deployed using [Streamlit Community Cloud](https://share.streamlit.io/).

1. Push the project to GitHub.
2. Ensure `requirements.txt` contains compatible dependencies.
3. Create a new Streamlit app.
4. Select the repository, branch, and `app.py` entrypoint.
5. Add the required Supabase secrets in the app settings.
6. Deploy and test the application.

Native dependencies such as `dlib` may need extra configuration. Test the face-recognition and audio pipelines in the deployment environment before using the application in a classroom.

## 🔐 Privacy and Security

FaceVPlus processes facial images, facial embeddings, and potentially voice data. These are sensitive biometric data.

- Protect student and teacher records with appropriate database access policies.
- Never expose private Supabase credentials in frontend code or public repositories.
- Obtain appropriate consent before collecting biometric information.
- Restrict access to attendance records.
- Define secure retention and deletion policies for biometric samples.
- Test authentication and authorization before public deployment.

## 🛣️ Future Improvements

- Complete voice-based attendance identification.
- Add attendance reports and downloadable summaries.
- Provide subject-wise and date-wise attendance analytics.
- Add attendance correction and teacher review workflows.
- Introduce stronger authentication and role-based access control.
- Improve recognition performance in crowded classrooms.
- Add configurable duplicate detection and attendance verification.
- Improve deployment reliability and automated testing.

## 🤝 Contributing

Contributions, bug reports, and feature suggestions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a pull request describing your improvements.

## 📄 License

Choose a license for your project before distributing it publicly. If you intend to publish it as open source, you can add an appropriate license file, such as the MIT License, after deciding on the terms.

---

**FaceVPlus — Making classroom attendance smarter with AI.**
