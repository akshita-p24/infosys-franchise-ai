"""Auth logic: bcrypt passwords, OTP via Gmail SMTP, JWT sessions, role checks."""
import os, re, time, hmac, hashlib, secrets, smtplib
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage
import bcrypt, jwt
import db

JWT_SECRET = os.getenv("JWT_SECRET", "dev-only-secret-change-me")
OTP_SECRET = os.getenv("OTP_SECRET", "dev-only-otp-secret")
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_APP_PASSWORD = os.getenv("SMTP_APP_PASSWORD", "")
REQUIRE_LOGIN_OTP = os.getenv("REQUIRE_LOGIN_OTP", "false").lower() == "true"
DEV_SHOW_OTP = os.getenv("DEV_SHOW_OTP", "true").lower() == "true"

OTP_TTL = 300          # 5 min
OTP_MAX_ATTEMPTS = 5
SESSION_HOURS = 8

# Roles a person may pick at signup. 'admin' is never self-assignable.
SIGNUP_ROLES = ["staff", "outlet_manager", "executive"]
ROLE_LEVEL = {"staff": 1, "outlet_manager": 2, "executive": 3, "admin": 4}

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

# ---------- passwords ----------
def hash_password(pw: str) -> bytes:
    return bcrypt.hashpw(pw.encode(), bcrypt.gensalt())

def check_password(pw: str, pw_hash: bytes) -> bool:
    return bcrypt.checkpw(pw.encode(), pw_hash)

def validate_password(pw: str):
    if len(pw) < 8: return "Password must be at least 8 characters."
    if not re.search(r"[A-Z]", pw): return "Add at least one uppercase letter."
    if not re.search(r"[a-z]", pw): return "Add at least one lowercase letter."
    if not re.search(r"\d", pw): return "Add at least one digit."
    return None

# ---------- OTP ----------
def _hash_otp(email, otp):
    return hmac.new(OTP_SECRET.encode(), f"{email.lower()}:{otp}".encode(), hashlib.sha256).hexdigest()

def _send_email(to, subject, body) -> bool:
    if not (SMTP_USER and SMTP_APP_PASSWORD):
        return False
    msg = EmailMessage()
    msg["From"], msg["To"], msg["Subject"] = SMTP_USER, to, subject
    msg.set_content(body)
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15) as s:
            s.login(SMTP_USER, SMTP_APP_PASSWORD)
            s.send_message(msg)
        return True
    except Exception:
        return False

def send_otp(email, purpose):
    """Returns (sent_by_email: bool, dev_otp: str|None)."""
    otp = f"{secrets.randbelow(10**6):06d}"
    db.save_otp(email, purpose, _hash_otp(email, otp), time.time() + OTP_TTL)
    sent = _send_email(email, "FranchiseOps AI – your verification code",
                       f"Your one-time code is {otp}. It expires in {OTP_TTL//60} minutes.\n"
                       "If you didn't request this, ignore this email.")
    return sent, (otp if (not sent and DEV_SHOW_OTP) else None)

def verify_otp(email, purpose, otp):
    row = db.get_otp(email, purpose)
    if not row: return False, "No code requested. Please request a new one."
    if time.time() > row["expires_at"]:
        db.delete_otp(email, purpose); return False, "Code expired. Request a new one."
    if row["attempts"] >= OTP_MAX_ATTEMPTS:
        db.delete_otp(email, purpose); return False, "Too many attempts. Request a new code."
    if not hmac.compare_digest(row["otp_hash"], _hash_otp(email, otp.strip())):
        db.bump_otp_attempts(email, purpose); return False, "Incorrect code."
    db.delete_otp(email, purpose)
    return True, "OK"

# ---------- signup / login ----------
def signup(name, email, password, confirm, role, outlet):
    name, email = name.strip(), email.strip().lower()
    if not name: return False, "Name is required."
    if not EMAIL_RE.match(email): return False, "Enter a valid email."
    err = validate_password(password)
    if err: return False, err
    if password != confirm: return False, "Passwords do not match."
    if role not in SIGNUP_ROLES: return False, "Invalid role."
    existing = db.get_user(email)
    if existing and existing["is_verified"]:
        return False, "An account with this email already exists."
    if existing:  # unverified leftover – let them retry
        db.delete_user(email)
    db.create_user(name, email, hash_password(password), role, outlet.strip() or None, verified=0)
    return True, "Account created. Verify your email with the OTP."

def login(email, password):
    """Returns (status, message, user). status: ok | otp | fail | unverified"""
    user = db.get_user(email.strip().lower())
    # same message for unknown email / wrong password (avoids user enumeration)
    if not user or not check_password(password, user["password_hash"]):
        return "fail", "Invalid email or password.", None
    if not user["is_verified"]:
        return "unverified", "Please verify your email first.", user
    if REQUIRE_LOGIN_OTP:
        return "otp", "OTP required.", user
    return "ok", "Welcome back!", user

# ---------- JWT session ----------
def create_token(user) -> str:
    now = datetime.now(timezone.utc)
    payload = {"sub": user["email"], "name": user["name"], "role": user["role"],
               "outlet": user["outlet"], "iat": now, "exp": now + timedelta(hours=SESSION_HOURS)}
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def decode_token(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except jwt.PyJWTError:
        return None

# ---------- role-based access ----------
def has_role(session: dict, min_role: str) -> bool:
    return ROLE_LEVEL.get(session.get("role"), 0) >= ROLE_LEVEL[min_role]

def seed_admin():
    email = os.getenv("ADMIN_EMAIL", "admin@franchiseops.ai")
    pw = os.getenv("ADMIN_PASSWORD", "Admin@12345")
    if not db.get_user(email):
        db.create_user("Administrator", email, hash_password(pw), "admin", None, verified=1)