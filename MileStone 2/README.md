# 🏪 FranchiseOps AI

## Secure multi-user franchise intelligence with role-based operations.

> **Infosys Springboard Internship 7.0 | Batch 4 | Milestone 2**

🐍 **Python** · ⚡ **FastAPI** · 🗃️ **SQLite** · 🔐 **JWT** · 🛡️ **RBAC** · 🤖 **SQL Copilot** · ☁️ **Google Colab**

## ✨ About the project

**FranchiseOps AI** turns a single-user franchise operations dashboard into a secure multi-user platform. It combines the Milestone 1 authentication experience with six operational agents, a SQL-powered AI Copilot, user profiles, an Admin dashboard, and server-enforced role-based access control.

The platform helps franchise teams monitor staffing, outlet health, inventory, campaigns, customer sentiment, and audits — while ensuring each user sees only the data and actions appropriate for their role. 🚀

## 🌟 Key features

| 🔐 Authentication & Security | 🛡️ Access Control | 🤖 Operations Intelligence |
| :--- | :--- | :--- |
| Login, signup, logout and password reset | Five server-enforced roles | SQL-backed AI Copilot with safe queries |
| bcrypt/PBKDF2 password hashing | Store Manager outlet isolation | Six operational agent dashboards |
| JWT protected sessions | Protected API routes return 403 | SQL and returned-row count displayed |
| OTP and security-question recovery | Admin activity audit log | Follow-up prompts and spelling tolerance |
| Five-attempt account lockout | Locked tokens stop working immediately | Inventory, staffing, sentiment and audit insights |

## 🧭 User journey

```text
Sign Up ✨  →  Verify OTP 🔢  →  Secure Login 🔐  →  FranchiseOps Dashboard
                                                        │
                           ┌────────────────────────────┼────────────────────────────┐
                           ▼                            ▼                            ▼
                    👤 Profile                    🤖 AI Copilot               🏪 Agent dashboards
                           │                            │                            │
                  Change username/password     SQL-backed answers          Workforce · Outlets · Inventory
                                                                            Marketing · Sentiment · Audit
```

## 👥 Role-based access

| Role | What they can access | What they can do |
| :--- | :--- | :--- |
| 👑 **Admin** | All pages, Profile and Admin dashboard | Manage users, roles and outlet assignment; run agents; view audit log |
| 🏢 **Franchise Owner** | Copilot, all six agent pages and Profile | Run agents; cannot manage users |
| 🏪 **Store Manager** | Copilot, Workforce, Outlets, Inventory, Sentiment, Audit and Profile | View only the assigned outlet; cannot run agents |
| 👤 **Staff** | Copilot and Profile | Read permitted operational information only |
| 📋 **Auditor** | Copilot, all six agent pages and Profile | Read-only access across all outlets |

> 🛡️ Permissions are enforced by the FastAPI backend — not only hidden in the interface. Restricted routes return **403 Forbidden**, and denied requests are recorded in the activity log.

## 📊 The six operational agents

| Agent | Focus |
| :--- | :--- |
| 👥 **Workforce** | Staffing levels, attendance and attrition risk |
| 🏬 **Outlets** | Outlet health, performance and rankings |
| 📦 **Inventory** | Stock cover, reorder risk and purchase orders |
| 📣 **Marketing** | Campaign performance and ROI |
| 💬 **Sentiment** | Customer feedback and sentiment analysis |
| ✅ **Audit** | Compliance scores, findings and corrective action |

## 🤖 AI Copilot

The Copilot answers operational questions using validated, read-only SQL. Every database answer shows the SQL query and the number of returned rows. It also supports spelling correction, alternative wording, follow-up questions, empty-result handling, and polite unsupported-question suggestions.

### 💡 Try these questions

1. Which outlets are at highest risk?
2. Why is OUT-007 flagged?
3. Which outlet has the lowest CSAT?
4. How many staff does OUT-010 have?
5. List items below reorder level.
6. Which campaign has the best ROI?
7. Show negative reviews this week.
8. Which outlets need a reorder?
9. Show the lowest audit scores.
10. Which outlet has the highest attrition risk?
11. Show open critical tickets.
12. Compare outlet health scores.
13. Top 5 outlets by revenue.
14. How is inventory holding up?
15. What are the latest customer sentiment issues?

## 👤 Profile and Admin dashboard

### Profile

Each user can view their username, email, role, joined date and last login. Users can safely update their username and password after confirming their current password.

### Admin dashboard

- 📈 Total users, locked users and users-per-role KPI cards
- 👥 User table with account status and last-login information
- ➕ Add user with a strong temporary password
- 🔁 Promote or demote users
- 🔒 Lock or unlock accounts
- 🗑️ Delete an account with explicit confirmation
- 🏪 Assign a Store Manager to exactly one outlet
- 🧾 Latest 50 activity-log entries
- 🛑 Protection against self-lock/self-delete and removal of the final Admin

## 🎨 User experience

- Responsive desktop and mobile layout
- Clear loading indicators, success notifications and error messages
- Readable tables, KPI cards, charts and action forms
- 🌙 Persistent Dark mode / Light mode toggle
- Improved Copilot chat experience with saved conversations and SQL evidence

## 🧰 Tech stack

| Technology | Purpose |
| :--- | :--- |
| 🐍 **Python** | Application and business logic |
| ⚡ **FastAPI** | Secure REST API and server routes |
| 🗃️ **SQLite** | Users, operational data and audit logs |
| 🔐 **PyJWT** | Signed session tokens |
| 🔒 **bcrypt / PBKDF2** | Password hashing and verification |
| 📊 **Pandas, NumPy, scikit-learn** | Analytics and agent data processing |
| 🌐 **HTML, CSS, JavaScript** | Responsive single-page interface |
| ☁️ **Google Colab + ngrok** | Notebook execution and public access |

## ☁️ Run with Google Colab

1. Upload `Milestone2_FranchiseOps_Integrated.ipynb` to Google Colab.
2. Open **Colab Secrets** (the key icon) and add:
   - `JWT_SECRET` — required for JWT signing
   - `EMAIL_ADDRESS` and `EMAIL_PASSWORD` — optional, for OTP email delivery
   - `NGROK_AUTHTOKEN` — optional fallback public link
3. Choose **Runtime → Restart session**, then **Runtime → Run all**.
4. Wait for the launcher to finish and click **Open the app**.
5. If the Colab proxy link is unavailable, use the ngrok fallback link.

## 📸 Project screenshots

> Replace the placeholders below with your own GitHub image links after uploading screenshots to the repository or GitHub Issues.

### 🔐 Login and signup

<img width="1917" height="925" alt="image" src="https://github.com/user-attachments/assets/a94935cb-e290-4bf6-a53e-c9b31ea380ff" />

<img width="1917" height="928" alt="image" src="https://github.com/user-attachments/assets/25738bbb-0829-4657-bc96-fb2ddd2e1352" />


### 👤 Profile page

<img width="1917" height="928" alt="image" src="https://github.com/user-attachments/assets/8d9075a4-9296-4d65-8946-087e15fcb1b7" />


### 👑 Admin dashboard

<img width="1917" height="927" alt="image" src="https://github.com/user-attachments/assets/edf8831d-bf42-4ae2-b6e1-b7c051b7329b" />


### 🛡️ Role-based denial

<img width="1917" height="927" alt="image" src="https://github.com/user-attachments/assets/bb98068c-2719-4fe5-9249-cea474a452c1" />


### 🤖 AI Copilot

<img width="1917" height="926" alt="image" src="https://github.com/user-attachments/assets/f818db7a-471b-4517-8b6b-4f81e07d27d0" />


### 📊 Six agents

<img width="1917" height="928" alt="image" src="https://github.com/user-attachments/assets/c39fe38d-bc58-4ba4-999f-16aa5cab9680" />

<img width="1917" height="926" alt="image" src="https://github.com/user-attachments/assets/233cc3a2-5c83-431f-9350-7a83fdec3293" />

<img width="1917" height="930" alt="image" src="https://github.com/user-attachments/assets/3c661f7a-32b7-4403-be49-b52f64fc93cd" />

<img width="1917" height="927" alt="image" src="https://github.com/user-attachments/assets/71483911-87ff-49b4-a8f0-63e7626ce105" />

<img width="1917" height="927" alt="image" src="https://github.com/user-attachments/assets/0e9d42b6-051b-4b04-a8d1-9e2c22af55b6" />

<img width="1917" height="927" alt="image" src="https://github.com/user-attachments/assets/9542a6e1-6b53-47dc-b35c-8ddc1cf440ec" />

### 👥 Team Members
- Ajay D
- Akshita Pator
- Madhavi Katekhaye
## 🔒 Security reminder

🚫 Never upload `.env` files, databases, email app passwords, JWT secrets, OTP values, ngrok tokens, session cookies, or access tokens to GitHub.
