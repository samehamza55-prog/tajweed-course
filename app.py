from flask import Flask, request, redirect, url_for, session, flash, render_template_string
import sqlite3, os
from functools import wraps

DB=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tajweed.db')
app=Flask(__name__)
app.secret_key=os.environ.get('SECRET_KEY','tajweed-secret-2026')
ADMIN_PASSWORD=os.environ.get('ADMIN_PASSWORD','4826')

def db():
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c

def init_db():
    c=db(); c.executescript('''CREATE TABLE IF NOT EXISTS students(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT UNIQUE NOT NULL,password TEXT UNIQUE NOT NULL,active INTEGER DEFAULT 1);CREATE TABLE IF NOT EXISTS exams(id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT NOT NULL,max_score REAL DEFAULT 10,sort_order INTEGER DEFAULT 0);CREATE TABLE IF NOT EXISTS scores(student_id INTEGER,exam_id INTEGER,score REAL,PRIMARY KEY(student_id,exam_id));''')
    if c.execute('SELECT COUNT(*) FROM students').fetchone()[0]==0:
        c.executemany('INSERT INTO students(name,password) VALUES(?,?)',[('إبراهيم عبد الماجد','241'),('آدم حمزة','352'),('حمد عادل','463'),('يحيى وجدي','574'),('عبد الرحمن علاء','685'),('تيم','796')])
    if c.execute('SELECT COUNT(*) FROM exams').fetchone()[0]==0:
        c.execute('INSERT INTO exams(title,max_score,sort_order) VALUES(?,?,?)',('الاختبار الأول',10,1)); sid=c.execute("SELECT id FROM students WHERE name='تيم'").fetchone()[0]; eid=c.execute('SELECT id FROM exams LIMIT 1').fetchone()[0]; c.execute('INSERT INTO scores VALUES(?,?,?)',(sid,eid,5))
    c.commit(); c.close()

def admin_required(f):
    @wraps(f)
    def w(*a,**k): return f(*a,**k) if session.get('admin') else redirect('/admin/login')
    return w

CSS='''<style>body{font-family:Arial,sans-serif;background:#f5f7fb;margin:0;color:#18212f;direction:rtl}.box{max-width:900px;margin:40px auto;background:white;padding:28px;border-radius:20px;box-shadow:0 8px 30px #0001}h1,h2{text-align:center}input,button{font-size:18px;padding:12px;border-radius:10px;border:1px solid #ccd3df;margin:5px}button{background:#1769aa;color:white;border:0;cursor:pointer}.login{text-align:center;max-width:420px}.login input{width:85%}.ok{color:#087f5b;font-weight:bold}.muted{color:#667085}.table{width:100%;border-collapse:collapse;margin-top:20px}.table th,.table td{padding:9px;border-bottom:1px solid #eee;text-align:center}.card{background:#f8fafc;padding:15px;border-radius:14px;margin:12px 0}.logout{display:inline-block;margin:5px;padding:9px 14px;background:#eee;border-radius:9px;color:#222;text-decoration:none}</style>'''

LOGIN=CSS+'''<div class="box login"><h1>بوابة نتائج دورة التجويد</h1><p class="muted">أدخل كلمة المرور للاطلاع على نتائجك</p><form method="post"><input name="password" inputmode="numeric" placeholder="كلمة المرور" autofocus><br><button>عرض النتائج</button></form><p><a href="/admin/login">دخول المسؤول</a></p>{% for m in get_flashed_messages() %}<p style="color:#c00">{{m}}</p>{% endfor %}</div>'''
RESULT=CSS+'''<div class="box"><h1>نتائج الطالب: {{s.name}}</h1><table class="table"><tr><th>الاختبار</th><th>العلامة</th><th>من</th></tr>{% for r in rows %}<tr><td>{{r.title}}</td><td>{% if r.score is none %}—{% else %}{{r.score}}{% endif %}</td><td>{{r.max_score}}</td></tr>{% endfor %}</table><p style="text-align:center"><a class="logout" href="/logout">خروج</a></p></div>'''
ADMINLOGIN=CSS+'''<div class="box login"><h1>دخول المسؤول</h1><form method="post"><input name="password" type="password" placeholder="كلمة مرور المسؤول"><br><button>دخول</button></form>{% for m in get_flashed_messages() %}<p style="color:#c00">{{m}}</p>{% endfor %}</div>'''
ADMIN=CSS+'''<div class="box"><h1>لوحة تحكم دورة التجويد</h1><p class="muted">أضف اختبارات مستقبلية وعدّل العلامات وكلمات المرور.</p><form method="post" action="/admin/add-exam" class="card"><h3>إضافة اختبار</h3><input name="title" placeholder="مثال: الاختبار الثاني" required><input name="max_score" type="number" step="0.5" value="10" required><button>إضافة الاختبار</button></form><form method="post" action="/admin/save"><table class="table"><tr><th>الطالب</th>{% for e in exams %}<th>{{e.title}}<br><small>من {{e.max_score}}</small></th>{% endfor %}</tr>{% for s in students %}<tr><td>{{s.name}}<br><small>كلمة: {{s.password}}</small></td>{% for e in exams %}<td><input style="width:70px" name="score_{{s.id}}_{{e.id}}" value="{{scores.get((s.id,e.id),'')}}" type="number" min="0" step="0.5"></td>{% endfor %}</tr>{% endfor %}</table><button>حفظ كل العلامات</button></form><h2>بيانات الطلاب</h2>{% for s in students %}<form class="card" method="post" action="/admin/student/{{s.id}}"><input name="name" value="{{s.name}}"><input name="password" value="{{s.password}}"><button>حفظ بيانات الطالب</button></form>{% endfor %}<p style="text-align:center"><a class="logout" href="/admin/logout">خروج</a></p></div>'''

@app.route('/',methods=['GET','POST'])
def login():
    if request.method=='POST':
        c=db(); s=c.execute('SELECT * FROM students WHERE password=? AND active=1',(request.form.get('password','').strip(),)).fetchone(); c.close()
        if s: session['student_id']=s['id']; return redirect('/result')
        flash('كلمة المرور غير صحيحة')
    return render_template_string(LOGIN)
@app.route('/result')
def result():
    if not session.get('student_id'): return redirect('/')
    c=db(); s=c.execute('SELECT * FROM students WHERE id=?',(session['student_id'],)).fetchone(); rows=c.execute('SELECT e.title,e.max_score,sc.score FROM exams e LEFT JOIN scores sc ON sc.exam_id=e.id AND sc.student_id=? ORDER BY e.sort_order,e.id',(session['student_id'],)).fetchall(); c.close(); return render_template_string(RESULT,s=s,rows=rows)
@app.route('/logout')
def logout(): session.clear(); return redirect('/')
@app.route('/admin/login',methods=['GET','POST'])
def admin_login():
    if request.method=='POST':
        if request.form.get('password','')==ADMIN_PASSWORD: session['admin']=True; return redirect('/admin')
        flash('رمز المسؤول غير صحيح')
    return render_template_string(ADMINLOGIN)
@app.route('/admin')
@admin_required
def admin():
    c=db(); students=c.execute('SELECT * FROM students ORDER BY id').fetchall(); exams=c.execute('SELECT * FROM exams ORDER BY sort_order,id').fetchall(); scores={(r['student_id'],r['exam_id']):r['score'] for r in c.execute('SELECT * FROM scores')}; c.close(); return render_template_string(ADMIN,students=students,exams=exams,scores=scores)
@app.post('/admin/add-exam')
@admin_required
def add_exam():
    title=request.form.get('title','').strip(); mx=float(request.form.get('max_score','10') or 10); c=db(); order=c.execute('SELECT COALESCE(MAX(sort_order),0)+1 FROM exams').fetchone()[0]; c.execute('INSERT INTO exams(title,max_score,sort_order) VALUES(?,?,?)',(title,mx,order)); c.commit(); c.close(); return redirect('/admin')
@app.post('/admin/save')
@admin_required
def save():
    c=db()
    for k,v in request.form.items():
        if k.startswith('score_') and v!='':
            _,sid,eid=k.split('_'); c.execute('INSERT INTO scores VALUES(?,?,?) ON CONFLICT(student_id,exam_id) DO UPDATE SET score=excluded.score',(int(sid),int(eid),float(v)))
    c.commit(); c.close(); return redirect('/admin')
@app.post('/admin/student/<int:sid>')
@admin_required
def student(sid):
    c=db(); c.execute('UPDATE students SET name=?,password=? WHERE id=?',(request.form.get('name','').strip(),request.form.get('password','').strip(),sid)); c.commit(); c.close(); return redirect('/admin')
@app.route('/admin/logout')
def alogout(): session.pop('admin',None); return redirect('/')

init_db()
if __name__=='__main__': app.run(host='0.0.0.0',port=int(os.environ.get('PORT',5000)))
