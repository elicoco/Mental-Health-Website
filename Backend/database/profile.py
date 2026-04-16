import os
import secrets
import string
from dotenv import load_dotenv
from Backend.custom.customclasses import Snackbar
from Backend.database.creating_tables import close_database, start_database
from Backend.email.email import send_email
from Backend.login_signup.hash import verify_password, hash_password, hash_key
from Backend.login_signup.signup import password_strong

load_dotenv()
BASE_URL = os.getenv('BASE_URL', 'http://127.0.0.1:5000')

green  = "#4CAF50"
red    = "#F44336"
orange = "#FBC02D"


def get_user_profile(username: str) -> dict:
    cursor, conn = start_database()
    cursor.execute('''SELECT username, email, first_name, last_name, email_verified_bool
                      FROM Users WHERE username = %s''', (username,))
    row = cursor.fetchone()
    close_database(cursor, conn)
    if not row:
        return {}
    return {
        'username':           row[0],
        'email':              row[1],
        'first_name':         row[2],
        'last_name':          row[3],
        'email_verified_bool': row[4],
    }


def update_name(username: str, first_name: str, last_name: str) -> Snackbar:
    if not first_name.strip() or not last_name.strip():
        return Snackbar(need_snackbar=True, colour=orange, message="Name fields cannot be empty")
    cursor, conn = start_database()
    cursor.execute('''UPDATE Users SET first_name = %s, last_name = %s WHERE username = %s''',
                   (first_name.strip(), last_name.strip(), username))
    conn.commit()
    close_database(cursor, conn)
    return Snackbar(need_snackbar=True, colour=green, message="Name updated")


def update_username(old_username: str, new_username: str) -> Snackbar:
    new_username = new_username.strip()
    if not new_username:
        return Snackbar(need_snackbar=True, colour=orange, message="Username cannot be empty")
    if new_username == old_username:
        return Snackbar(need_snackbar=True, colour=orange, message="That's already your username")
    cursor, conn = start_database()
    cursor.execute('SELECT id FROM Users WHERE username = %s', (new_username,))
    if cursor.fetchone():
        close_database(cursor, conn)
        return Snackbar(need_snackbar=True, colour=orange, message="Username already taken")
    cursor.execute('UPDATE Users SET username = %s WHERE username = %s', (new_username, old_username))
    conn.commit()
    close_database(cursor, conn)
    return Snackbar(need_snackbar=True, colour=green, message="Username updated")


def update_password(username: str, current_password: str, new_password: str) -> Snackbar:
    cursor, conn = start_database()
    cursor.execute('SELECT encrypted_password FROM Users WHERE username = %s', (username,))
    row = cursor.fetchone()
    if not row or not verify_password(current_password, row[0]):
        close_database(cursor, conn)
        return Snackbar(need_snackbar=True, colour=orange, message="Current password is incorrect")
    if not password_strong(new_password):
        close_database(cursor, conn)
        return Snackbar(need_snackbar=True, colour=orange,
                        message="New password must be at least 8 characters with a letter, number and symbol")
    cursor.execute('UPDATE Users SET encrypted_password = %s WHERE username = %s',
                   (hash_password(new_password), username))
    conn.commit()
    close_database(cursor, conn)
    return Snackbar(need_snackbar=True, colour=green, message="Password updated")


def resend_verification_email(username: str) -> Snackbar:
    cursor, conn = start_database()
    cursor.execute('SELECT email FROM Users WHERE username = %s', (username,))
    row = cursor.fetchone()
    if not row:
        close_database(cursor, conn)
        return Snackbar(need_snackbar=True, colour=orange, message="User not found")
    email = row[0]
    key = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(40))
    body = f'''Thank you for using Zen Log.
To verify your email please click the link {BASE_URL}/emailverification/{key}'''
    cursor.execute('UPDATE Users SET hashed_email_verification_key = %s WHERE username = %s',
                   (hash_key(key), username))
    conn.commit()
    close_database(cursor, conn)
    try:
        send_email(subject="Verify your Zen Log email", body=body, to=email)
        return Snackbar(need_snackbar=True, colour=green, message="Verification email sent")
    except Exception:
        return Snackbar(need_snackbar=True, colour=orange, message="Failed to send email, please try again later")


def delete_account(username: str, password: str) -> Snackbar:
    cursor, conn = start_database()
    cursor.execute('SELECT encrypted_password FROM Users WHERE username = %s', (username,))
    row = cursor.fetchone()
    if not row or not verify_password(password, row[0]):
        close_database(cursor, conn)
        return Snackbar(need_snackbar=True, colour=orange, message="Incorrect password")
    cursor.execute('DELETE FROM Users WHERE username = %s', (username,))
    conn.commit()
    close_database(cursor, conn)
    return Snackbar(need_snackbar=True, colour=green, message="Account deleted")
