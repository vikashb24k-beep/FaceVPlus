
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
        .eq("username", username)
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
    username = username.strip()

    if not username or not password:
        return None

    response = (
        supabase.table("teachers")
        .select("username, password, name")
        .eq("username", username)
        .limit(3)
        .execute()
    )

    if not response.data:
        return None

    teacher = response.data[0]

    if check_pass(password, teacher.get("password", "")):
        # Return teacher details, excluding the password hash
        return {
            "username": teacher["username"],
            "name": teacher["name"]
        }

    return None


def get_all_students():
    response = supabase.table('students').select('*').execute()
    return response.data

def create_student(new_name, face_embedding=None, voice_embedding=None):
    data = {'name': new_name, 'face_embedding':face_embedding, "voice_embedding": voice_embedding}
    response = supabase.table('students').insert(data).execute()
    return response.data

