from src.database.config import supabase
import bcrypt


# Hash password before storing it
def hash_pass(pwd):
    return bcrypt.hashpw(
        pwd.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


# Verify entered password against stored hash
def check_pass(pwd, hashed):
    if not pwd or not hashed:
        return False

    try:
        return bcrypt.checkpw(
            pwd.encode("utf-8"),
            hashed.encode("utf-8")
        )
    except (ValueError, TypeError):
        return False


# Check whether a teacher already exists
def check_teacher_exists(username):
    response = (
        supabase.table("teachers")
        .select("username")
        .eq("username", username.strip())
        .limit(1)
        .execute()
    )

    return bool(response.data)


# Register a new teacher
def create_teacher(username, password, name):
    username = username.strip()
    name = name.strip()

    if not username or not password or not name:
        raise ValueError("All fields are required.")

    if check_teacher_exists(username):
        raise ValueError("Username already taken.")

    data = {
        "username": username,
        "password": hash_pass(password),
        "name": name
    }

    response = (
        supabase.table("teachers")
        .insert(data)
        .execute()
    )

    return response.data


# Authenticate a teacher
def teacher_login(username, password):
    if not username or not password:
        return None

    response = (
        supabase.table("teachers")
        .select("teacher_id, username, password, name")
        .eq("username", username.strip())
        .limit(1)
        .execute()
    )

    if not response.data:
        return None

    teacher = response.data[0]

    if check_pass(password, teacher.get("password", "")):
        return {
            "teacher_id": teacher["teacher_id"],
            "username": teacher["username"],
            "name": teacher["name"]
        }

    return None


# Get all students
def get_all_students():
    response = (
        supabase.table("students")
        .select("*")
        .execute()
    )

    return response.data or []


# Create a student
def create_student(new_name, face_embedding=None, voice_embedding=None):
    data = {
        "name": new_name,
        "face_embedding": face_embedding,
        "voice_embedding": voice_embedding
    }

    response = (
        supabase.table("students")
        .insert(data)
        .execute()
    )

    return response.data


# Create a subject
def create_subject(subject_code, subject_name, section, teacher_id):
    data = {
        "subject_code": subject_code,
        "name": subject_name,
        "section": section,
        "teacher_id": teacher_id
    }

    response = (
        supabase.table("subjects")
        .insert(data)
        .execute()
    )

    return response.data


# Get subjects belonging to a teacher
def get_teacher_subjects(teacher_id):
    response = supabase.table('subjects').select("*, subject_students(count), attendance_logs(timestamp)").eq("teacher_id", teacher_id).execute()
    subjects = response.data or []


    for sub in subjects:
        sub['total_students'] = sub.get("subject_students", [{}])[0].get('count', 0) if sub.get('subject_students') else 0
        attendance = sub.get('attendance_logs', [])
        unique_sessions = len(set(log['timestamp'] for log in attendance))
        sub['total_classes'] = unique_sessions


        sub.pop('subject_students', None)
        sub.pop('attendance_logs', None)

    return subjects


def enroll_student_to_subject(student_id, subject_id):
    data = {"student_id": student_id, "subject_id": subject_id}
    response =supabase.table('subject_students').insert(data).execute()
    return response.data

def unenroll_student_to_subject(student_id, subject_id):
    response = supabase.table('subject_students').delete().eq("student_id",student_id).eq("subject_id",subject_id).execute()
    return response.data


def get_student_subjects(student_id):
    response = supabase.table('subject_students').select('*,subjects(*)').eq('student_id',student_id).execute()
    return response.data

def get_student_attendance(student_id):
    response = supabase.table('attendance_logs').select('*,subjects(*)').eq('student_id',student_id).execute()
    return response.data

def create_attendance(logs):
    response = supabase.table("attendance_logs").insert(logs).execute()
    return response.data

