from functools import wraps
from flask import session, redirect, url_for, flash

def student_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        # belum login
        if 'user_id' not in session:
            flash('Silakan login dulu!')
            return redirect(url_for('user.login'))

        # 🔥 FIX: pakai user_role
        if session.get('user_role') != 'Student':
            flash('Akses hanya untuk mahasiswa!')
            return redirect(url_for('user.dashboard'))

        return f(*args, **kwargs)
    return wrapper

def teacher_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        if 'user_id' not in session:
            return redirect(url_for('user.login'))

        if session.get('user_role') != 'Teacher':
            return redirect(url_for('user.dashboard'))

        return f(*args, **kwargs)
    return wrapper