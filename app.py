"""FranchiseOps AI – Login / Signup (Streamlit). Run: streamlit run app.py"""
import streamlit as st
import db, auth, ui, home

st.set_page_config(page_title="FranchiseOps AI", page_icon="🏪", layout="wide")
ui.inject_css()
db.init_db(); auth.seed_admin()

S = st.session_state
S.setdefault("token", None)
S.setdefault("pending", None)   # {"email":..., "purpose": "signup"|"login"}
S.setdefault("dev_otp", None)

def current_session():
    return auth.decode_token(S.token) if S.token else None

def start_otp(email, purpose):
    sent, dev = auth.send_otp(email, purpose)
    S.pending = {"email": email, "purpose": purpose}
    S.dev_otp = dev
    if sent: st.toast("OTP sent to your email 📧")

def logout():
    S.token = None; S.pending = None; S.dev_otp = None

# ---------------- Authenticated area ----------------
def app_shell(sess):
    role_label = sess["role"].replace("_", " ").title()
    with st.sidebar:
        st.markdown("### 🏪 FranchiseOps AI")
        st.markdown(f"**{sess['name']}**")
        st.markdown(f'<span class="badge">{role_label}</span>'
                    + (f' <span class="badge">{sess["outlet"]}</span>' if sess.get("outlet") else ""),
                    unsafe_allow_html=True)
        st.divider()

    # Role-based module visibility
    modules = [("🏠 Home Dashboard", "staff"), ("🤖 AI Copilot / Chatbot", "staff"),
               ("📈 Performance Dashboard", "outlet_manager"), ("📦 Inventory Dashboard", "outlet_manager"),
               ("👥 Workforce Dashboard", "outlet_manager"), ("📣 Marketing ROI", "outlet_manager"),
               ("✅ Compliance Audit", "outlet_manager"), ("💬 Customer Feedback", "staff"),
               ("🏆 Executive Dashboard", "executive"), ("⚙️ Admin", "admin")]
    allowed = [m for m, lvl in modules if auth.has_role(sess, lvl)]
    with st.sidebar:
        page = st.radio("Modules", allowed, label_visibility="collapsed")
        st.divider()
        st.button("Logout", on_click=logout, use_container_width=True)

    ui.hero(page.split(" ", 1)[1], f"Welcome back, {sess['name'].split()[0]} 👋")
    if page.endswith("Home Dashboard"):
        home.render(sess)
    else:
        st.info("🚧 This module is coming next. Authentication and role-based access are working.")

# ---------------- OTP screen ----------------
def otp_screen():
    _, mid, _ = st.columns([1, 1.6, 1])
    with mid:
        _otp_card()

def _otp_card():
    p = S.pending
    ui.hero("🔐 Verify it's you", "Enter the one-time code we just sent.")
    st.subheader("🔐 Enter verification code")
    st.caption(f"We sent a 6-digit code to **{p['email']}**. It expires in 5 minutes.")
    if S.dev_otp:
        st.warning(f"DEV MODE (email not configured) – your OTP is **{S.dev_otp}**")
    code = st.text_input("6-digit OTP", max_chars=6)
    c1, c2, c3 = st.columns(3)
    if c1.button("Verify", type="primary", use_container_width=True):
        ok, msg = auth.verify_otp(p["email"], p["purpose"], code)
        if ok:
            if p["purpose"] == "signup":
                db.mark_verified(p["email"])
                S.pending = None; S.dev_otp = None
                st.success("Email verified! You can now log in."); st.rerun()
            else:
                S.token = auth.create_token(db.get_user(p["email"]))
                S.pending = None; S.dev_otp = None; st.rerun()
        else:
            st.error(msg)
    if c2.button("Resend", use_container_width=True):
        start_otp(p["email"], p["purpose"]); st.rerun()
    if c3.button("Cancel", use_container_width=True):
        S.pending = None; S.dev_otp = None; st.rerun()

# ---------------- Login / Signup ----------------
def auth_screen():
    _, mid, _ = st.columns([1, 1.6, 1])
    with mid:
        _auth_card()

def _auth_card():
    ui.hero("🏪 FranchiseOps AI", "Transforming franchise operations into intelligent, data-driven decisions.",
            ["Performance", "Inventory", "Workforce", "Marketing", "Audits", "Feedback"])
    tab_login, tab_signup = st.tabs(["Login", "Sign up"])

    with tab_login:
        with st.form("login_form"):
            email = st.text_input("Email")
            pw = st.text_input("Password", type="password")
            go = st.form_submit_button("Login", type="primary", use_container_width=True)
        if go:
            status, msg, user = auth.login(email, pw)
            if status == "ok":
                S.token = auth.create_token(user); st.rerun()
            elif status == "otp":
                start_otp(user["email"], "login"); st.rerun()
            elif status == "unverified":
                st.warning(msg); start_otp(user["email"], "signup"); st.rerun()
            else:
                st.error(msg)

    with tab_signup:
        with st.form("signup_form"):
            name = st.text_input("Full name")
            email = st.text_input("Email", key="su_email")
            c1, c2 = st.columns(2)
            role = c1.selectbox("Role", auth.SIGNUP_ROLES,
                                format_func=lambda r: r.replace("_", " ").title())
            outlet = c2.text_input("Outlet (optional)")
            pw = st.text_input("Password", type="password", key="su_pw",
                               help="8+ chars, upper, lower and a digit")
            pw2 = st.text_input("Confirm password", type="password")
            go = st.form_submit_button("Create account", type="primary", use_container_width=True)
        if go:
            ok, msg = auth.signup(name, email, pw, pw2, role, outlet)
            if ok:
                start_otp(email.strip().lower(), "signup"); st.rerun()
            else:
                st.error(msg)

# ---------------- Router ----------------
sess = current_session()
if sess:
    app_shell(sess)
elif S.pending:
    otp_screen()
else:
    S.token = None
    auth_screen()