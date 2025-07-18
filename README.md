# User Authentication Dashboard

## Problem Statement
Build a User Authentication Dashboard with session-based login, registration, and role-based access. It simulates a basic admin panel where users can log in, and only admins can manage users.

## Project Structure
flask_auth_dashboard/
│
├── app.py
├── models.py
├── forms.py (optional, or use raw HTML forms)
├── templates/
│ ├── layout.html
│ ├── login.html
│ ├── register.html
│ ├── dashboard.html
│ ├── admin_panel.html
│
└── static/
└── style.css


## Features & Tech Stack

| Features               | Tech Stack                          | Implemented Routes           |
|------------------------|-------------------------------------|------------------------------|
| **User Authentication** | Flask                               | Login: `/`                   |
| - Register             | SQLite + Redis (session storage)    | Register: `/register`        |
| - Login                | Jinja templates                     | Dashboard: `/dashboard`      |
| - Logout               | HTML + Bootstrap                    |                              |
| - Password hashing      |                                     |                              |
| - Session management    |                                     |                              |
| **RBAC**               |                                     |                              |
| - Admin/Regular user    |                                     |                              |
| - Admin dashboard       |                                     |                              |
| **User Management** (admin only) |                              |                              |
| - View all users        |                                     |                              |
| - Promote/demote user   |                                     |                              |
| - Delete user           |                                     |                              |
| **Security**           |                                     |                              |
| - Password hashing      |                                     |                              |
| - Login protection with session expiry |                     |                              |
| - Secure cookie         |                                     |                              |

## Level-1 Add-ons (Implemented)
- [x] Center elements (UI)
- [x] Session expiry after 10 minutes
- [x] Flash messages
-  Flask-Login integration
-  User profile page
-  Deploy to Render/Heroku/Railway (TODO)

## Level-2 Add-ons Ideas

- [ ] Add Flask-WTF forms for CSRF protection
- [ ] Auto-login after registration
- [ ] Absolute time session expiry *(Note: Idle expiry preferred instead)*
- [ ] Use Flask-Login for cleaner session management
- [x] Flask-Session for server-side storage *(Implemented to solve flash message issues)*

## Level-3 Add-ons Ideas

- [ ] Forgot password policy
- [ ] Custom "session expired" blocking popup
- [ ] Parallel users login support
- [ ] Cookie-based sessions (alternative to session caching)

## Workflow Status

- [x] Register → Login → User Dashboard → Logout → Redirect to login
- [x] Login (no user) → Register → Login
- [x] Register (existing user) → Show "user exists" flash message
- [x] Login (wrong credentials) → Show error message
- [x] Login → Idle (2+ mins) → Auto redirect to login with flash
- [x] Login (admin) → Admin Dashboard → User Management Panel
- [x] Admin functions:
  - Promote/demote users
  - Create users
  - Delete users
  *(Note: New admins can't edit original 'admin' user)*

## Implemented Improvements

1. [x] Flash success message after registration
2. Auto logout after session expiry
   - *Frontend solution:* JavaScript can auto-redirect when session expires
   - *Caveat:* JS timer may not trigger if tab is idle or computer sleeps
3. Session persistence after app restart (session caching behavior)
   - *Mechanism:* Session ID in cookie → Flask checks backend → Restores valid session
   - *Dev option:* Clear all sessions on app start (not for production)
4. Session cleanup needed:
   - [ ] Automatic cleanup of expired sessions from disk
   - *Solutions:*
     - Manual cleanup scripts
     - Redis/Memcached advantages:
       - Auto-purge expired sessions
       - Better performance
       - No filesystem cleanup needed
5. [x] Direct `/dashboard` access now properly redirects to login
6. [ ] Parallel users login support
7. [ ] Forgot password policy
8. [ ] Auto login after registration
9. [ ] Custom "session expired" popup

## Problems Faced & Solutions

### 1. Redirecting but not able to see flash messages
**Solution:** Typo in layout.html - used `massages` instead of `messages`

**Debugging Steps:**
- Checked HTML page for `get_flashed_messages()` code block
- Used redirect after flash, not `render_template`
- Verified secret_key was defined
- Ensured no `session.clear()` or `session.pop()` after flash
- Added test route to verify
- Checked for browser cookie issues

**Comparison Table:**
| Method              | Use Case                      | Pros                              | Cons                                       |
|---------------------|-------------------------------|-----------------------------------|--------------------------------------------|
| Flash + Redirect    | Show message after redirect   | Clean PRG pattern, persistent msg | Needs session/cookie support               |
| Render with context | Show message without redirect | Simple, immediate feedback       | Refresh resubmits form                     |
| Client-side JS      | Validate before submit        | Great UX, instant feedback       | Not secure, server validation still needed |

### 2. Session not expiring
**Solution:** Typo in config - missed `SESSION_FILE_DIR`

**Code Fix:**
```python
app = Flask(__name__)
app.secret_key = 'my-secret-key'

# Server-side session configuration
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = os.path.join(app.root_path, 'flask_session')
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=2)
app.config['SESSION_REFRESH_EACH_REQUEST'] = False

Session(app)

