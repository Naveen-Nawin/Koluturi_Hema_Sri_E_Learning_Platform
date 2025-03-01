from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Secret key for session management

# Dummy Data for Users & Courses
users = {
    "admin": "password123",
    "naveen": "naveen@123",
    "sri": "sri@123",
    "lokesh": "lokesh@123",
    "kalyani": "kalyani@123"
}

courses = [
    {"id": 1, "title": "Python for Beginners", "progress": 50},
    {"id": 2, "title": "Web Development with Flask", "progress": 75},
    {"id": 3, "title": "Cybersecurity Basics", "progress": 20}
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    student = {"name": session.get('user', 'Guest')}
    return render_template('dashboard.html', courses=courses, student=student)

@app.route('/courses')
def courses_page():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('courses.html', courses=courses)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    student = {"name": session.get('user', 'Guest')}

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        return redirect(url_for('home'))

    return render_template('contact.html', student=student)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid Credentials')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return render_template('signup.html', error='Username already exists')
        users[username] = password  # Add new user
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
