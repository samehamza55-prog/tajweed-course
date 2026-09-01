from flask import Flask, request, redirect, session, flash, render_template_string
import sqlite3
import os
from functools import wraps

DB = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "tajweed.db"
)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "tajweed-secret-2026")

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "4826")


# =========================
# DATABASE
# =========================

def db():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c


def init_db():
    c = db()

    c.executescript("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        password TEXT UNIQUE NOT NULL,
        active INTEGER DEFAULT 1
    );

    CREATE TABLE IF NOT EXISTS exams(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        max_score REAL DEFAULT 10,
        sort_order INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS scores(
        student_id INTEGER,
        exam_id INTEGER,
        score REAL,
        PRIMARY KEY(student_id, exam_id)
    );
    """)

    # الطلاب
    if c.execute("SELECT COUNT(*) FROM students").fetchone()[0] == 0:
        students = [
            ("إبراهيم عبد الماجد", "241"),
            ("آدم حمزة", "352"),
            ("حمد عادل", "463"),
            ("يحيى وجدي", "574"),
            ("عبد الرحمن علاء", "685"),
            ("تيم", "796")
        ]

        c.executemany(
            "INSERT INTO students(name,password) VALUES(?,?)",
            students
        )

    # الاختبار الأول
    if c.execute("SELECT COUNT(*) FROM exams").fetchone()[0] == 0:
        c.execute(
            "INSERT INTO exams(title,max_score,sort_order) VALUES(?,?,?)",
            ("الاختبار الأول", 10, 1)
        )

        sid = c.execute(
            "SELECT id FROM students WHERE name='تيم'"
        ).fetchone()[0]

        eid = c.execute(
            "SELECT id FROM exams LIMIT 1"
        ).fetchone()[0]

        c.execute(
            "INSERT INTO scores VALUES(?,?,?)",
            (sid, eid, 5)
        )

    c.commit()
    c.close()


# =========================
# ADMIN SECURITY
# =========================

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("admin"):
            return redirect("/admin/login")
        return f(*args, **kwargs)

    return wrapper


# =========================
# DESIGN
# =========================

CSS = """
<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, Tahoma, sans-serif;
    direction: rtl;
    background:
        radial-gradient(circle at top right, #dff7ed, transparent 35%),
        radial-gradient(circle at bottom left, #e8f0ff, transparent 35%),
        #f5f7fb;
    color: #172033;
}

.container {
    max-width: 1050px;
    margin: 30px auto;
    padding: 15px;
}

.box {
    background: rgba(255,255,255,.95);
    border-radius: 28px;
    padding: 30px;
    box-shadow: 0 15px 45px rgba(20,40,80,.10);
    border: 1px solid rgba(255,255,255,.8);
}

.login {
    max-width: 480px;
    margin: 70px auto;
    text-align: center;
}

.logo {
    width: 82px;
    height: 82px;
    border-radius: 24px;
    margin: 0 auto 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 42px;
    background: linear-gradient(135deg,#168f68,#0d6efd);
    color: white;
    box-shadow: 0 12px 25px rgba(13,110,253,.25);
}

h1 {
    margin: 8px 0;
    font-size: 30px;
}

h2 {
    margin-top: 10px;
}

.subtitle {
    color: #687386;
    line-height: 1.8;
}

input, button {
    font-family: inherit;
}

input {
    width: 100%;
    padding: 15px 16px;
    border-radius: 14px;
    border: 1px solid #d7deea;
    background: #fbfcfe;
    font-size: 17px;
    outline: none;
    margin: 7px 0;
}

input:focus {
    border-color: #168f68;
    box-shadow: 0 0 0 4px rgba(22,143,104,.10);
}

button {
    border: 0;
    padding: 14px 22px;
    border-radius: 14px;
    background: linear-gradient(135deg,#168f68,#0d6efd);
    color: white;
    font-size: 17px;
    font-weight: bold;
    cursor: pointer;
    margin-top: 8px;
}

button:hover {
    opacity: .92;
}

.btn-light {
    display: inline-block;
    padding: 11px 17px;
    border-radius: 12px;
    background: #eef2f7;
    color: #263143;
    text-decoration: none;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 15px;
    margin-bottom: 25px;
}

.welcome {
    color: #697586;
}

.stats {
    display: grid;
    grid-template-columns: repeat(3,1fr);
    gap: 15px;
    margin: 20px 0;
}

.stat {
    padding: 20px;
    border-radius: 20px;
    background: linear-gradient(135deg,#f8fffc,#f1f6ff);
    border: 1px solid #e3eaf3;
    text-align: center;
}

.stat .number {
    font-size: 30px;
    font-weight: bold;
    margin: 7px 0;
}

.exam {
    margin: 15px 0;
    padding: 22px;
    border-radius: 22px;
    background: white;
    border: 1px solid #e5eaf1;
    box-shadow: 0 7px 20px rgba(20,40,80,.05);
}

.exam-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
}

.exam-title {
    font-size: 19px;
    font-weight: bold;
}

.score {
    font-size: 26px;
    font-weight: bold;
    color: #168f68;
}

.progress {
    height: 11px;
    background: #e9eef4;
    border-radius: 30px;
    overflow: hidden;
    margin-top: 15px;
}

.progress-bar {
    height: 100%;
    border-radius: 30px;
    background: linear-gradient(90deg,#168f68,#0d6efd);
}

.percent {
    margin-top: 9px;
    color: #687386;
    font-size: 14px;
}

.admin-card {
    padding: 20px;
    background: #f8fafc;
    border-radius: 20px;
    margin: 18px 0;
    border: 1px solid #e4e9f0;
}

.table-wrap {
    overflow-x: auto;
}

table {
    width: 100%;
    border-collapse: collapse;
    min-width: 650px;
}

th, td {
    padding: 12px 8px;
    border-bottom: 1px solid #e7ebf1;
    text-align: center;
}

th {
    background: #f5f7fa;
}

.small-input {
    width: 85px;
    text-align: center;
}

.flash {
    background: #fff0f0;
    color: #c62828;
    padding: 12px;
    border-radius: 12px;
    margin-top: 15px;
}

.success {
    background: #ecfdf5;
    color: #087f5b;
}

.footer {
    text-align: center;
    color: #8a94a6;
    margin-top: 25px;
    font-size: 13px;
}

@media(max-width:700px) {

    .container {
        margin: 10px auto;
        padding: 10px;
    }

    .box {
        padding: 20px 15px;
        border-radius: 22px;
    }

    .login {
        margin: 35px auto;
    }

    h1 {
        font-size: 25px;
    }

    .stats {
        grid-template-columns: 1fr;
    }

    .header {
        flex-direction: column;
        align-items: stretch;
        text-align: center;
    }

    .exam-top {
        align-items: flex-start;
    }

}

</style>
"""


# =========================
# STUDENT LOGIN
# =========================

LOGIN = CSS + """
<div class="container">

<div class="box login">

<div class="logo">📖</div>

<h1>بوابة نتائج دورة التجويد</h1>

<p class="subtitle">
مرحباً بك 🌿<br>
أدخل كلمة المرور الخاصة بك للاطلاع على نتائجك
</p>

<form method="post">

<input
name="password"
inputmode="numeric"
placeholder="🔐 كلمة المرور"
autocomplete="off"
autofocus
required
>

<button type="submit">
عرض نتائجي 📊
</button>

</form>

{% for m in get_flashed_messages() %}
<div class="flash">{{m}}</div>
{% endfor %}

<div style="margin-top:20px">
<a class="btn-light" href="/admin/login">
👨‍💼 دخول المسؤول
</a>
</div>

<div class="footer">
دورة التجويد • بوابة النتائج
</div>

</div>
</div>
"""


# =========================
# STUDENT RESULTS
# =========================

RESULT = CSS + """
<div class="container">

<div class="box">

<div class="header">

<div>
<h1>السلام عليكم 🌿</h1>
<div class="welcome">
نتائج الطالب: <strong>{{s.name}}</strong>
</div>
</div>

<a class="btn-light" href="/logout">
خروج
</a>

</div>


<div class="stats">

<div class="stat">
<div>عدد الاختبارات</div>
<div class="number">{{total_exams}}</div>
</div>

<div class="stat">
<div>المجموع</div>
<div class="number">{{total_score}} / {{total_max}}</div>
</div>

<div class="stat">
<div>النسبة</div>
<div class="number">{{overall}}%</div>
</div>

</div>


<h2>📚 نتائج الاختبارات</h2>

{% for r in rows %}

<div class="exam">

<div class="exam-top">

<div class="exam-title">
{{r.title}}
</div>

{% if r.score is none %}

<div style="color:#8a94a6">
لم تُرصد
</div>

{% else %}

<div class="score">
{{r.score}} / {{r.max_score}}
</div>

{% endif %}

</div>


{% if r.score is not none %}

{% set p = ((r.score / r.max_score) * 100) if r.max_score else 0 %}

<div class="progress">
<div class="progress-bar" style="width:{{p}}%"></div>
</div>

<div class="percent">
النتيجة: {{p|round(1)}}%
</div>

{% endif %}

</div>

{% endfor %}


{% if not rows %}

<div class="exam" style="text-align:center">
لا توجد اختبارات حتى الآن.
</div>

{% endif %}


<div class="footer">
وفقكم الله وبارك في علمكم 🌸
</div>

</div>
</div>
"""


# =========================
# ADMIN LOGIN
# =========================

ADMIN_LOGIN = CSS + """
<div class="container">

<div class="box login">

<div class="logo">👨‍💼</div>

<h1>لوحة المسؤول</h1>

<p class="subtitle">
أدخل كلمة مرور المسؤول
</p>

<form method="post">

<input
type="password"
name="password"
placeholder="🔐 كلمة مرور المسؤول"
required
>

<button type="submit">
دخول لوحة التحكم
</button>

</form>

{% for m in get_flashed_messages() %}
<div class="flash">{{m}}</div>
{% endfor %}

<br>

<a class="btn-light" href="/">
العودة للطلاب
</a>

</div>
</div>
"""


# =========================
# ADMIN DASHBOARD
# =========================

ADMIN = CSS + """
<div class="container">

<div class="box">

<div class="header">

<div>
<h1>👨‍💼 لوحة تحكم دورة التجويد</h1>
<div class="welcome">
إدارة الطلاب والاختبارات والنتائج
</div>
</div>

<a class="btn-light" href="/admin/logout">
خروج
</a>

</div>


<div class="admin-card">

<h2>➕ إضافة اختبار جديد</h2>

<form method="post" action="/admin/add-exam">

<input
name="title"
placeholder="اسم الاختبار، مثال: الاختبار الثاني"
required
>

<input
name="max_score"
type="number"
step="0.5"
min="1"
value="10"
placeholder="العلامة الكاملة"
required
>

<button>
إضافة الاختبار
</button>

</form>

</div>


<div class="admin-card">

<h2>📊 إدخال العلامات</h2>

<form method="post" action="/admin/save">

<div class="table-wrap">

<table>

<tr>

<th>الطالب</th>

{% for e in exams %}

<th>
{{e.title}}
<br>
<small>من {{e.max_score}}</small>
</th>

{% endfor %}

</tr>


{% for s in students %}

<tr>

<td>
<strong>{{s.name}}</strong>
</td>

{% for e in exams %}

<td>

<input
class="small-input"
name="score_{{s.id}}_{{e.id}}"
value="{{scores.get((s.id,e.id),'')}}"
type="number"
min="0"
max="{{e.max_score}}"
step="0.5"
>

</td>

{% endfor %}

</tr>

{% endfor %}

</table>

</div>

<button>
💾 حفظ جميع العلامات
</button>

</form>

</div>


<div class="admin-card">

<h2>👨‍🎓 بيانات الطلاب</h2>

{% for s in students %}

<form
class="admin-card"
method="post"
action="/admin/student/{{s.id}}"
>

<strong>{{s.name}}</strong>

<input
name="name"
value="{{s.name}}"
placeholder="اسم الطالب"
required
>

<input
name="password"
value="{{s.password}}"
placeholder="كلمة المرور"
required
>

<button>
حفظ بيانات الطالب
</button>

</form>

{% endfor %}

</div>


<div class="footer">
بوابة نتائج دورة التجويد
</div>

</div>
</div>
"""


# =========================
# STUDENT LOGIN ROUTE
# =========================

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        password = request.form.get("password", "").strip()

        c = db()

        s = c.execute(
            """
            SELECT * FROM students
            WHERE password=? AND active=1
            """,
            (password,)
        ).fetchone()

        c.close()

        if s:
            session.clear()
            session["student_id"] = s["id"]
            return redirect("/result")

        flash("كلمة المرور غير صحيحة ❌")

    return render_template_string(LOGIN)


# =========================
# RESULTS
# =========================

@app.route("/result")
def result():

    if not session.get("student_id"):
        return redirect("/")

    c = db()

    s = c.execute(
        "SELECT * FROM students WHERE id=?",
        (session["student_id"],)
    ).fetchone()

    rows = c.execute(
        """
        SELECT
            e.title,
            e.max_score,
            sc.score
        FROM exams e
        LEFT JOIN scores sc
            ON sc.exam_id=e.id
            AND sc.student_id=?
        ORDER BY e.sort_order, e.id
        """,
        (session["student_id"],)
    ).fetchall()

    c.close()

    total_score = 0
    total_max = 0

    for r in rows:
        if r["score"] is not None:
            total_score += r["score"]

        total_max += r["max_score"]

    overall = round(
        (total_score / total_max) * 100,
        1
    ) if total_max else 0

    return render_template_string(
        RESULT,
        s=s,
        rows=rows,
        total_exams=len(rows),
        total_score=total_score,
        total_max=total_max,
        overall=overall
    )


# =========================
# STUDENT LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# =========================
# ADMIN LOGIN
# =========================

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        password = request.form.get("password", "")

        if password == ADMIN_PASSWORD:

            session["admin"] = True

            return redirect("/admin")

        flash("كلمة مرور المسؤول غير صحيحة ❌")

    return render_template_string(ADMIN_LOGIN)


# =========================
# ADMIN DASHBOARD
# =========================

@app.route("/admin")
@admin_required
def admin():

    c = db()

    students = c.execute(
        "SELECT * FROM students ORDER BY id"
    ).fetchall()

    exams = c.execute(
        "SELECT * FROM exams ORDER BY sort_order,id"
    ).fetchall()

    scores = {
        (r["student_id"], r["exam_id"]): r["score"]
        for r in c.execute("SELECT * FROM scores")
    }

    c.close()

    return render_template_string(
        ADMIN,
        students=students,
        exams=exams,
        scores=scores
    )


# =========================
# ADD EXAM
# =========================

@app.post("/admin/add-exam")
@admin_required
def add_exam():

    title = request.form.get("title", "").strip()

    try:
        max_score = float(
            request.form.get("max_score", "10")
        )
    except:
        max_score = 10

    if not title:
        return redirect("/admin")

    c = db()

    order = c.execute(
        "SELECT COALESCE(MAX(sort_order),0)+1 FROM exams"
    ).fetchone()[0]

    c.execute(
        """
        INSERT INTO exams(title,max_score,sort_order)
        VALUES(?,?,?)
        """,
        (title, max_score, order)
    )

    c.commit()
    c.close()

    return redirect("/admin")


# =========================
# SAVE SCORES
# =========================

@app.post("/admin/save")
@admin_required
def save():

    c = db()

    for key, value in request.form.items():

        if key.startswith("score_") and value.strip() != "":

            try:
                _, sid, eid = key.split("_")

                score = float(value)

                exam = c.execute(
                    "SELECT max_score FROM exams WHERE id=?",
                    (eid,)
                ).fetchone()

                if exam and 0 <= score <= exam["max_score"]:

                    c.execute(
                        """
                        INSERT INTO scores
                        VALUES(?,?,?)
                        ON CONFLICT(student_id,exam_id)
                        DO UPDATE SET score=excluded.score
                        """,
                        (
                            int(sid),
                            int(eid),
                            score
                        )
                    )

            except:
                pass

    c.commit()
    c.close()

    return redirect("/admin")


# =========================
# UPDATE STUDENT
# =========================

@app.post("/admin/student/<int:sid>")
@admin_required
def student(sid):

    name = request.form.get("name", "").strip()
    password = request.form.get("password", "").strip()

    if name and password:

        c = db()

        try:

            c.execute(
                """
                UPDATE students
                SET name=?, password=?
                WHERE id=?
                """,
                (name, password, sid)
            )

            c.commit()

        except sqlite3.IntegrityError:
            pass

        c.close()

    return redirect("/admin")


# =========================
# ADMIN LOGOUT
# =========================

@app.route("/admin/logout")
def admin_logout():

    session.pop("admin", None)

    return redirect("/")


# =========================
# START
# =========================

init_db()

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(
            os.environ.get("PORT", 5000)
        )
    )
