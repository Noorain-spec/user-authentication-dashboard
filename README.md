<img width="968" height="310" alt="image" src="https://github.com/user-attachments/assets/bf9a6c0e-7e10-4552-8619-d96cb20ac48d" /># user-authentication-dashboard

Problem Statement:
Build a User Authentication Dashboard with session-based login, registration, and role-based access. It simulates a basic admin panel where users can log in, and only admins can manage users.

flask_auth_dashboard/
 │
├── app.py
├── models.py
├── forms.py (optional, or use raw HTML forms)
├── templates/
 │   ├── layout.html
 │   ├── login.html
 │   ├── register.html
 │   ├── dashboard.html
 │   ├── admin_panel.html
 │
 └── static/
    └── style.css

        Features	                         Tech Stack	                                 Implemented routes: 
        USER-AUTH	                           Flask	                                       Login: /
                Register	                   Sqlite+ redis(session storage)	               Register: /register
                Login	                       Jinjal template	                             Dashboard: /dashboard
                Logout	                     Html+boostrap	
                Password hashing
                Session-mgmt
        RBAC
                Admin/Regular user
                Admin dashboard
        User mgmt (admin only)
                View all users
                Promote/demote user
                Delete user
        Security
                Pwd hashing
                Login protection with session expiry
                Secure cookie
	
Level-1 add-ons ideas:
(after basic login/register app)

Center elements	                           UI (CSS/ html) 	                   Done
Session expiry after 10 min	               Session management & security	     Done
Flash messages	                           UX and Flask feature familiarity	   Done
Flask-Login integration	                   Cleaner auth handling 	
User profile page	                         User context & routing	
Deploy to Render/Heroku/ Railway	         Deployment 	

Problems Faced:
	1. redirecting but not able to see flash messages ----> (tried using "error" in meantime problem solves)
		a. Checked html page for get_flashed_messages() code block
		b. Use redirect after flash, don’t user render_template (it will clear flash messages)
		c. Have secret_key defined
		d. No session.clear() or session.pop(...) after flash/before rendering
		e. Added test route to test
		f. Cookies disabled in your browser/ Some browser extension or proxy interfering
		g. | Method              | Use case                      | Pros                              | Cons                                       |
		| ------------------- | ----------------------------- | --------------------------------- | ------------------------------------------ |
		| Flash + Redirect    | Show message after redirect   | Clean PRG pattern, persistent msg | Needs session/cookie support               |
		| Render with context | Show message without redirect | Simple, immediate feedback        | Refresh resubmits form                     |
		| Client-side JS      | Validate before submit        | Great UX, instant feedback        | Not secure, server validation still needed |
Solution:
Type in layout.html form ---> massages instead of messages

	2. session not expiring  ---> typo in config
		a. app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=2)
		b. If want to redirect instead of rendering on session expiry (so that refresh won’t resubmit form)
Solution:
Missed --> app.config['SESSION_FILE_DIR'] = './flask_session'
Without setting SESSION_FILE_DIR, Flask-Session won't store the session on disk, and session behavior can become unpredictable — especially with expiration.

Code:
app = Flask(__name__)
app.secret_key = 'my-secret-key'

# Server-side session configuration
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = os.path.join(app.root_path, 'flask_session')
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=2)
app.config['SESSION_REFRESH_EACH_REQUEST'] = False

Session(app)

Level-2 add-ons ideas:

Add Flask-WTF forms for CSRF protection	
Auto-login after registration	
session to expire based on absolute time only (even if the user is active)	---> Nope ( idle expire is prefered)
Use Flask-Login for cleaner session management	
Flask-Session to store the session server-side (instead of cookies)? That can help with flash message consistency too	--->  Done (implemented to solve above prblm-1)


Level-3 add-ons ideas:

Add forgot password policy		
Custom "session expired" blocking popup		
Parallel users login support		
Instead of session caching try cookies		

Workflow	status
Register --> login --> userpage(user dashboard) ---> click logout (redirect to login page)	---> Done
Login (no user in db) ---> register ---> login …	---> Done
Register (user exist) ---> user already exist flash message stay on same page (try again)	---> Done
Login(wrng creds) ---> login page (flash error message wrng creds)	---> Done
Login --> idle window(+2mins)[should expire] ----> redirect to login [with flash message]	---> Done
Login(admin creds) ---> admin dashboard ---> admin panel (user mgmt board)	---> Done
Admin ---> promote/demote (edit)users; create user; delete user [ newly admins cant edit original 'admin' user ]	---> Done
	
	
	

Improvements:
	1. After registration need flash success category message --- done
	2. Auto log out after session expire with given time 
		a. Can the dashboard page automatically expire and redirect the user when their session expires — without requiring manual refresh?
	Yes, that's possible — with JavaScript on the frontend. Flask (being a backend framework) can only act when a request comes in. But with a little help from JS, we can proactively check and redirect.
	Caveat
	This approach is frontend only — if the user:
		• Leaves the tab idle
		• Or puts the computer to sleep
	The JS timer may not trigger precisely.
	3. Session when didn’t expire was active even after restart of app. ----> Session caching concept 
		a. When you restarted Flask:
			• The session cookie (session ID) was sent again with your browser request.
			• Flask checked the session backend (filesystem in your case) and found the saved session still valid.
			• So, it restored the previous session, and you saw the dashboard page as if still logged in.
		b. clear all sessions every time the app starts — useful in development, not in production
	4. Auto clear expired sessions from disk ( can work on this using docker ) ---> Session caching concept
		a. Expired sessions are not automatically deleted from disk. So over time, old session files pile up — especially in development.
		b. Can use cleanup script manually trigger / use redis. 
		c. Redis or Memcached as the session store
		Why?
			• Expired sessions are automatically purged
			• Faster and scalable
			• No file system cleanup required
	5. When direct /dashboard don’t say session expired --> redirect to login
	6. Parallel users login support
	7. Add forgot password policy
	8. Auto login after Registration
	9. Custom "session expired" blocking popup
