from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import sqlite3
import hashlib
import os
from datetime import datetime
import re

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'  # IMPORTANT: Change this for production!
# For production, use: app.secret_key = os.environ.get('SECRET_KEY') or 'very-secure-random-key-here'

# Database configuration
DATABASE = 'instance/database.db'

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with tables"""
    with app.app_context():
        conn = get_db_connection()
        
        # Create tables
        conn.executescript('''
            CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                color TEXT DEFAULT '#3498db',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                question_text TEXT NOT NULL,
                code_answer TEXT NOT NULL,
                difficulty TEXT DEFAULT 'Medium',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (subject_id) REFERENCES subjects (id) ON DELETE CASCADE
            );
            
            CREATE TABLE IF NOT EXISTS admin_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        
        # Check if admin user exists, if not create default admin
        admin = conn.execute('SELECT * FROM admin_users WHERE username = ?', ('admin',)).fetchone()
        if not admin:
            # Default password: 'admin123' (change this!)
            password_hash = hashlib.sha256('admin123'.encode()).hexdigest()
            conn.execute('INSERT INTO admin_users (username, password_hash) VALUES (?, ?)', 
                        ('admin', password_hash))
        
        # Add sample subjects if none exist
        subjects = conn.execute('SELECT COUNT(*) as count FROM subjects').fetchone()
        if subjects['count'] == 0:
            sample_subjects = [
                ('AJP', 'Advanced Java Programming', '#e74c3c'),
                ('DSV', 'Data Structures and Visualization', '#2ecc71'),
                ('DAA', 'Design and Analysis of Algorithms', '#f39c12'),
                ('DBMS', 'Database Management Systems', '#9b59b6'),
                ('Web Tech', 'Web Technologies', '#1abc9c')
            ]
            
            for name, desc, color in sample_subjects:
                conn.execute('INSERT INTO subjects (name, description, color) VALUES (?, ?, ?)',
                           (name, desc, color))
        
        conn.commit()
        conn.close()

# Routes
@app.route('/')
def home():
    """Homepage with subject containers"""
    conn = get_db_connection()
    subjects = conn.execute('SELECT * FROM subjects ORDER BY name').fetchall()
    conn.close()
    return render_template('home.html', subjects=subjects)

@app.route('/subject/<int:subject_id>')
def subject_questions(subject_id):
    """Show all questions for a specific subject"""
    conn = get_db_connection()
    subject = conn.execute('SELECT * FROM subjects WHERE id = ?', (subject_id,)).fetchone()
    if not subject:
        flash('Subject not found!', 'error')
        return redirect(url_for('home'))
    
    questions = conn.execute('''
        SELECT * FROM questions 
        WHERE subject_id = ? 
        ORDER BY created_at DESC
    ''', (subject_id,)).fetchall()
    
    conn.close()
    return render_template('subject_questions.html', subject=subject, questions=questions)

@app.route('/question/<int:question_id>')
def question_detail(question_id):
    """Show detailed view of a specific question"""
    conn = get_db_connection()
    question = conn.execute('''
        SELECT q.*, s.name as subject_name, s.color as subject_color
        FROM questions q
        JOIN subjects s ON q.subject_id = s.id
        WHERE q.id = ?
    ''', (question_id,)).fetchone()
    
    if not question:
        flash('Question not found!', 'error')
        return redirect(url_for('home'))
    
    conn.close()
    return render_template('question_detail.html', question=question)

@app.route('/debug-helper')
def debug_helper():
    """AI Debug Helper page"""
    return render_template('debug_helper.html')

@app.route('/about')
def about():
    """About Me page"""
    return render_template('about.html')

@app.route('/api/debug', methods=['POST'])
def api_debug():
    """API endpoint for debug assistance"""
    data = request.get_json()
    code = data.get('code', '').strip()
    error = data.get('error', '').strip()
    
    # Simple rule-based debugging (placeholder for AI)
    suggestions = analyze_code_issues(code, error)
    
    return jsonify({
        'success': True,
        'suggestions': suggestions
    })

def analyze_code_issues(code, error):
    """Simple rule-based code analysis"""
    suggestions = []
    
    if error:
        error_lower = error.lower()
        
        # Common Python errors
        if 'indentation' in error_lower:
            suggestions.append("🔍 **Indentation Error**: Check your code indentation. Python requires consistent indentation (use 4 spaces or tabs consistently).")
        
        elif 'syntax' in error_lower:
            suggestions.append("🔍 **Syntax Error**: Check for missing colons (:), parentheses, or brackets. Make sure all opening brackets have closing ones.")
        
        elif 'name' in error_lower and 'not defined' in error_lower:
            suggestions.append("🔍 **NameError**: Variable or function not defined. Make sure you've declared the variable before using it.")
        
        elif 'index' in error_lower and 'out of range' in error_lower:
            suggestions.append("🔍 **IndexError**: You're trying to access an array/list element that doesn't exist. Check your array bounds.")
        
        elif 'key' in error_lower:
            suggestions.append("🔍 **KeyError**: Dictionary key not found. Use .get() method or check if key exists before accessing.")
        
        elif 'import' in error_lower:
            suggestions.append("🔍 **ImportError**: Module not found. Make sure the module is installed and spelled correctly.")
    
    if code:
        code_lower = code.lower()
        
        # Code quality suggestions
        if 'print(' not in code_lower and 'printf' not in code_lower:
            suggestions.append("💡 **Tip**: Add print statements to debug your code and see intermediate values.")
        
        if 'for' in code_lower or 'while' in code_lower:
            suggestions.append("💡 **Loop Tip**: Make sure your loops have proper exit conditions to avoid infinite loops.")
        
        if 'def' in code_lower:
            suggestions.append("💡 **Function Tip**: Test your functions with different inputs to ensure they work correctly.")
    
    # Default suggestions if no specific issues found
    if not suggestions:
        suggestions = [
            "🔍 **General Debug Tips**:",
            "• Read error messages carefully - they usually tell you exactly what's wrong",
            "• Check line numbers mentioned in errors",
            "• Use print() statements to see what values your variables have",
            "• Make sure all imports are at the top of your file",
            "• Check for typos in variable and function names",
            "💡 **Best Practices**:",
            "• Use meaningful variable names",
            "• Add comments to explain complex logic",
            "• Test your code with different inputs",
            "• Break complex problems into smaller functions"
        ]
    
    return suggestions

# Admin routes
@app.route('/admin')
def admin_login():
    """Admin login page"""
    if 'admin_logged_in' in session:
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_login.html')

@app.route('/admin/login', methods=['POST'])
def admin_login_post():
    """Handle admin login"""
    username = request.form['username']
    password = request.form['password']
    
    conn = get_db_connection()
    admin = conn.execute(
        'SELECT * FROM admin_users WHERE username = ?', (username,)
    ).fetchone()
    conn.close()
    
    if admin and admin['password_hash'] == hashlib.sha256(password.encode()).hexdigest():
        session['admin_logged_in'] = True
        session['admin_username'] = username
        flash('Login successful!', 'success')
        return redirect(url_for('admin_dashboard'))
    else:
        flash('Invalid credentials!', 'error')
        return redirect(url_for('admin_login'))

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    subjects = conn.execute('SELECT * FROM subjects ORDER BY name').fetchall()
    questions = conn.execute('''
        SELECT q.*, s.name as subject_name 
        FROM questions q 
        JOIN subjects s ON q.subject_id = s.id 
        ORDER BY q.created_at DESC 
        LIMIT 10
    ''').fetchall()
    
    stats = {
        'total_subjects': len(subjects),
        'total_questions': conn.execute('SELECT COUNT(*) as count FROM questions').fetchone()['count']
    }
    
    conn.close()
    return render_template('admin_dashboard.html', subjects=subjects, questions=questions, stats=stats)

@app.route('/admin/subjects/add', methods=['GET', 'POST'])
def admin_add_subject():
    """Add new subject"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        name = request.form['name'].strip()
        description = request.form['description'].strip()
        color = request.form['color']
        
        if name:
            conn = get_db_connection()
            try:
                conn.execute('INSERT INTO subjects (name, description, color) VALUES (?, ?, ?)',
                           (name, description, color))
                conn.commit()
                flash('Subject added successfully!', 'success')
                return redirect(url_for('admin_dashboard'))
            except sqlite3.IntegrityError:
                flash('Subject name already exists!', 'error')
            finally:
                conn.close()
        else:
            flash('Subject name is required!', 'error')
    
    return render_template('admin_add_subject.html')

@app.route('/admin/subjects/edit/<int:subject_id>', methods=['GET', 'POST'])
def admin_edit_subject(subject_id):
    """Edit subject"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    subject = conn.execute('SELECT * FROM subjects WHERE id = ?', (subject_id,)).fetchone()
    
    if not subject:
        flash('Subject not found!', 'error')
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        name = request.form['name'].strip()
        description = request.form['description'].strip()
        color = request.form['color']
        
        if name:
            try:
                conn.execute('UPDATE subjects SET name = ?, description = ?, color = ? WHERE id = ?',
                           (name, description, color, subject_id))
                conn.commit()
                flash('Subject updated successfully!', 'success')
                return redirect(url_for('admin_dashboard'))
            except sqlite3.IntegrityError:
                flash('Subject name already exists!', 'error')
        else:
            flash('Subject name is required!', 'error')
    
    conn.close()
    return render_template('admin_edit_subject.html', subject=subject)

@app.route('/admin/subjects/delete/<int:subject_id>')
def admin_delete_subject(subject_id):
    """Delete subject"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    conn.execute('DELETE FROM subjects WHERE id = ?', (subject_id,))
    conn.commit()
    conn.close()
    
    flash('Subject deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/questions/add', methods=['GET', 'POST'])
def admin_add_question():
    """Add new question"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    subjects = conn.execute('SELECT * FROM subjects ORDER BY name').fetchall()
    
    if request.method == 'POST':
        subject_id = request.form['subject_id']
        title = request.form['title'].strip()
        question_text = request.form['question_text'].strip()
        code_answer = request.form['code_answer'].strip()
        difficulty = request.form['difficulty']
        
        if subject_id and title and question_text and code_answer:
            conn.execute('''
                INSERT INTO questions (subject_id, title, question_text, code_answer, difficulty) 
                VALUES (?, ?, ?, ?, ?)
            ''', (subject_id, title, question_text, code_answer, difficulty))
            conn.commit()
            flash('Question added successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('All fields are required!', 'error')
    
    conn.close()
    return render_template('admin_add_question.html', subjects=subjects)

@app.route('/admin/questions/edit/<int:question_id>', methods=['GET', 'POST'])
def admin_edit_question(question_id):
    """Edit question"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    question = conn.execute('SELECT * FROM questions WHERE id = ?', (question_id,)).fetchone()
    subjects = conn.execute('SELECT * FROM subjects ORDER BY name').fetchall()
    
    if not question:
        flash('Question not found!', 'error')
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        subject_id = request.form['subject_id']
        title = request.form['title'].strip()
        question_text = request.form['question_text'].strip()
        code_answer = request.form['code_answer'].strip()
        difficulty = request.form['difficulty']
        
        if subject_id and title and question_text and code_answer:
            conn.execute('''
                UPDATE questions 
                SET subject_id = ?, title = ?, question_text = ?, code_answer = ?, difficulty = ? 
                WHERE id = ?
            ''', (subject_id, title, question_text, code_answer, difficulty, question_id))
            conn.commit()
            flash('Question updated successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('All fields are required!', 'error')
    
    conn.close()
    return render_template('admin_edit_question.html', question=question, subjects=subjects)

@app.route('/admin/questions/delete/<int:question_id>')
def admin_delete_question(question_id):
    """Delete question"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    conn.execute('DELETE FROM questions WHERE id = ?', (question_id,))
    conn.commit()
    conn.close()
    
    flash('Question deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    # Create instance directory if it doesn't exist
    os.makedirs('instance', exist_ok=True)
    init_db()
    app.run(debug=True)
