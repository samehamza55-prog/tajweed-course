from flask import Flask, render_template_string
import os

app = Flask(__name__)

PAGE = r"""<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#0b8f68">
<title>بوابة نتائج دورة التجويد</title>
<style>
:root{--g:#07865f;--g2:#17bd87;--dark:#122a25;--muted:#71827d;--bg:#f4f8f6;--line:#e4ece8;--white:#fff;--gold:#b88728}
*{box-sizing:border-box}
body{margin:0;font-family:Tahoma,"Segoe UI",Arial,sans-serif;color:var(--dark);
background:radial-gradient(circle at 5% 0,#dff8ed 0,transparent 27%),
radial-gradient(circle at 100% 5%,#eee7ff 0,transparent 25%),var(--bg);min-height:100vh}
.wrap{max-width:1080px;margin:auto;padding:22px 15px 50px}
.top{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px}
.brand{display:flex;align-items:center;gap:11px}.logo{width:48px;height:48px;border-radius:16px;
display:grid;place-items:center;color:white;font-size:24px;background:linear-gradient(135deg,#056d50,#1bc791);
box-shadow:0 12px 28px #087f5b2b}.brand b{font-size:19px}.brand small{display:block;color:var(--muted);margin-top:3px}
.status{background:#fff;border:1px solid #dce9e3;border-radius:999px;padding:9px 13px;color:var(--g);font-size:12px;font-weight:800}
.layout{display:grid;grid-template-columns:1.45fr .78fr;gap:17px}
.card{background:#fffffff2;border:1px solid var(--line);border-radius:26px;padding:24px;box-shadow:0 18px 50px #163b2e0d}
.hero{min-height:340px;display:flex;flex-direction:column;justify-content:center;overflow:hidden;position:relative}
.hero:before{content:"";position:absolute;width:190px;height:190px;border-radius:50%;background:#dff7ec;left:-75px;bottom:-85px}
.kicker{color:var(--g);font-weight:900;font-size:13px}
h1{font-size:42px;line-height:1.25;margin:9px 0 12px;max-width:700px}
.lead{color:var(--muted);line-height:1.95;font-size:15px;max-width:690px}
.poem{margin-top:22px;padding:17px 19px;border-radius:18px;background:linear-gradient(135deg,#f0fbf6,#fbfdfc);
border:1px solid #d8eee5;line-height:2;color:#256552;font-size:14px}
.poem b{display:block;color:var(--g);margin-bottom:5px}
.login h2{margin:0 0 9px;font-size:22px}
.hint{background:#f7faf8;border:1px solid var(--line);padding:13px;border-radius:15px;color:var(--muted);font-size:13px;line-height:1.8}
label{display:block;font-weight:800;font-size:13px;margin:16px 0 7px}
input{width:100%;padding:14px 15px;border:1px solid #d5e1dc;border-radius:14px;background:#fff;font-size:16px;outline:0}
input:focus{border-color:var(--g);box-shadow:0 0 0 4px #07865f12}
button{width:100%;border:0;border-radius:14px;padding:13px 16px;margin-top:10px;font-size:15px;font-weight:900;
color:white;background:linear-gradient(135deg,#067b59,#16bd86);box-shadow:0 10px 22px #07865f22;cursor:pointer}
button.secondary{background:#f0f5f2;color:#29443c;box-shadow:none}
button.link{background:transparent;color:var(--g);box-shadow:none;font-size:13px}
.hidden{display:none!important}
.msg{margin-top:12px;padding:12px;border-radius:14px;background:#effaf5;color:#176b53;font-size:13px}
.error{background:#fff0f0;color:#a33d3d}
.student{margin-top:17px}
.student-head{display:flex;align-items:center;justify-content:space-between;gap:10px}
.student-head h2{margin:4px 0}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:11px;margin-top:17px}
.stat{background:#fff;border:1px solid var(--line);border-radius:19px;padding:16px}
.stat small{color:var(--muted)}.stat strong{display:block;font-size:27px;margin-top:5px}
.green{color:var(--g)}.blue{color:#3f72d5}.gold{color:var(--gold)}
.section-title{margin:23px 0 11px;font-size:21px}
.result{border:1px solid var(--line);border-radius:20px;padding:16px;margin-top:11px;background:#fff}
.result-top{display:flex;justify-content:space-between;gap:12px;align-items:center}
.result-title{font-weight:900}.date{color:var(--muted);font-size:12px;margin-top:5px}
.score{font-size:27px;font-weight:900;color:var(--g);white-space:nowrap}
.bar{height:9px;border-radius:99px;background:#eaf0ed;overflow:hidden;margin:15px 0 8px}
.bar i{display:block;height:100%;border-radius:99px;background:linear-gradient(90deg,#07865f,#22c993)}
.meta{display:flex;justify-content:space-between;gap:8px;color:var(--muted);font-size:12px}
.badge{background:#eaf8f2;color:var(--g);padding:6px 9px;border-radius:999px;font-weight:900}
.footer{text-align:center;color:#82918c;font-size:12px;margin-top:23px}
.admin{margin-top:17px}.admin-head{display:flex;justify-content:space-between;align-items:center;gap:10px}
.admin-table{overflow:auto;margin-top:12px}table{width:100%;border-collapse:separate;border-spacing:0;min-width:650px}
th,td{padding:10px;border-bottom:1px solid var(--line);text-align:center;font-size:13px}th{background:#f7faf8;color:#61716c;font-size:12px}
.admin input{padding:8px;font-size:13px}
.modal{position:fixed;inset:0;background:#09251d88;display:grid;place-items:center;padding:16px;z-index:10}
.modal .card{width:min(450px,100%);background:#fff}
@media(max-width:800px){.layout{grid-template-columns:1fr}h1{font-size:32px}.hero{min-height:auto}.stats{grid-template-columns:1fr}.top{align-items:flex-start}.status{display:none}}
</style>
</head>
<body>
<main class="wrap">
<header class="top">
  <div class="brand"><div class="logo">✦</div><div><b>دورة التجويد</b><small>بوابة النتائج والمتابعة</small></div></div>
  <div class="status">● النظام جاهز</div>
</header>

<section class="layout">
  <section class="card hero">
    <div class="kicker">مرحباً بك في بوابة دورة التجويد</div>
    <h1>تعلّم، أتقن، وارتقِ في تلاوتك</h1>
    <div class="lead">تابع نتائجك بسهولة، وشاهد تقدّمك في الاختبارات بواجهة رايقة وسريعة ومناسبة للجوال.</div>
    <div class="poem">
      <b>🌿 أبيات جميلة في طريق التعلّم</b>
      تعلّم كتابَ اللهِ وامضِ بثقةٍ، فالعلمُ نورٌ والقلوبُ منارُ<br>
      واجعلْ تلاوتَكَ كلَّ يومٍ عادةً، فبها يطيبُ الوقتُ والأعمارُ
    </div>
  </section>

  <section class="card login">
    <h2>🔐 دخول الطالب</h2>
    <div class="hint">أدخل كلمة المرور الخاصة بك، وستظهر نتائجك أنت فقط.</div>
    <label>كلمة المرور</label>
    <input id="pw" type="password" inputmode="numeric" autocomplete="off" placeholder="أدخل كلمة المرور"
           onkeydown="if(event.key==='Enter')studentLogin()">
    <button onclick="studentLogin()">عرض نتائجي ←</button>
    <button class="link" onclick="openAdmin()">⚙ دخول المسؤول</button>
    <div id="msg"></div>
  </section>
</section>

<section id="student" class="card student hidden"></section>
<section id="admin" class="card admin hidden"></section>
<div class="footer">وفقك الله في علمك، وبارك لك في وقتك وجهدك 🌿</div>
</main>

<div id="modal" class="modal hidden">
 <div class="card">
   <h2>⚙ دخول المسؤول</h2>
   <label>رمز المسؤول</label>
   <input id="apw" type="password" placeholder="رمز المسؤول" onkeydown="if(event.key==='Enter')adminLogin()">
   <button onclick="adminLogin()">دخول لوحة التحكم</button>
   <button class="secondary" onclick="closeAdmin()">إلغاء</button>
   <div id="amsg"></div>
 </div>
</div>

<script>
const INITIAL=[
{id:'S001',name:'إبراهيم عبد الماجد',password:'241',scores:[{name:'الاختبار الأول',date:'2026-08-17',score:9.5,max:10}]},
{id:'S002',name:'آدم حمزة',password:'352',scores:[{name:'الاختبار الأول',date:'2026-08-17',score:7.5,max:10}]},
{id:'S003',name:'حمد عادل',password:'463',scores:[{name:'الاختبار الأول',date:'2026-08-17',score:9.5,max:10}]},
{id:'S004',name:'يحيى وجدي',password:'574',scores:[{name:'الاختبار الأول',date:'2026-08-17',score:6,max:10}]},
{id:'S005',name:'عبد الرحمن علاء',password:'685',scores:[{name:'الاختبار الأول',date:'2026-08-17',score:5,max:10}]},
{id:'S006',name:'تيم',password:'796',scores:[{name:'الاختبار الأول',date:'2026-08-17',score:5,max:10}]}
];
const ADMIN='4826';
let state=JSON.parse(localStorage.getItem('tajweed_state')||'null')||INITIAL;
const esc=s=>String(s??'').replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
function save(){localStorage.setItem('tajweed_state',JSON.stringify(state))}
function studentLogin(){
 const pw=document.getElementById('pw').value.trim(),m=document.getElementById('msg');
 const s=state.find(x=>x.password===pw);
 if(!s){m.innerHTML='<div class="msg error">كلمة المرور غير صحيحة. حاول مرة أخرى.</div>';return}
 const total=s.scores.reduce((a,x)=>a+Number(x.score||0),0);
 const max=s.scores.reduce((a,x)=>a+Number(x.max||0),0);
 const pct=max?Math.round(total/max*100):0;
 const results=s.scores.map(x=>{
   const p=x.max?Math.round(x.score/x.max*100):0;
   const label=p>=90?'ممتاز جداً':p>=75?'ممتاز':p>=60?'جيد جداً':p>=50?'جيد':'استمر بالتدريب';
   return `<div class="result"><div class="result-top"><div><div class="result-title">📘 ${esc(x.name)}</div><div class="date">📅 ${esc(x.date||'بدون تاريخ')}</div></div><div class="score">${x.score} / ${x.max}</div></div><div class="bar"><i style="width:${p}%"></i></div><div class="meta"><span>النسبة <b class="green">${p}%</b></span><span class="badge">${label}</span></div></div>`
 }).join('');
 document.getElementById('student').classList.remove('hidden');
 document.getElementById('student').innerHTML=`<div class="student-head"><div><div class="kicker">السلام عليكم ورحمة الله وبركاته</div><h2>نتائج الطالب: <span class="green">${esc(s.name)}</span></h2></div><button class="secondary" onclick="logoutStudent()" style="width:auto">خروج</button></div>
 <div class="stats"><div class="stat"><small>النسبة الإجمالية</small><strong class="green">${pct}%</strong></div><div class="stat"><small>المجموع الكلي</small><strong class="blue">${total} / ${max}</strong></div><div class="stat"><small>عدد الاختبارات</small><strong class="gold">${s.scores.length}</strong></div></div>
 <div class="section-title">نتائج الاختبارات</div>${results}
 <div class="msg">✨ أحسنت، استمر في المراجعة والتدريب؛ فالإتقان يأتي مع الصبر والمداومة.</div>`;
 document.getElementById('pw').value='';document.getElementById('student').scrollIntoView({behavior:'smooth'});
}
function logoutStudent(){document.getElementById('student').classList.add('hidden');window.scrollTo({top:0,behavior:'smooth'})}
function openAdmin(){document.getElementById('modal').classList.remove('hidden');document.getElementById('apw').focus()}
function closeAdmin(){document.getElementById('modal').classList.add('hidden');document.getElementById('apw').value='';document.getElementById('amsg').innerHTML=''}
function adminLogin(){if(document.getElementById('apw').value!==ADMIN){document.getElementById('amsg').innerHTML='<div class="msg error">رمز المسؤول غير صحيح.</div>';return}closeAdmin();renderAdmin()}
function renderAdmin(){
 let exams=state[0]?.scores?.map((x,i)=>({i,name:x.name,date:x.date,max:x.max}))||[];
 let rows=state.map((s,i)=>`<tr><td>${esc(s.id)}</td><td><b>${esc(s.name)}</b></td><td><input id="p${i}" value="${esc(s.password)}"></td>${exams.map(e=>`<td><input id="s${i}_${e.i}" type="number" min="0" max="${e.max}" step="0.5" value="${s.scores[e.i]?.score??0}"></td>`).join('')}</tr>`).join('');
 document.getElementById('admin').classList.remove('hidden');
 document.getElementById('admin').innerHTML=`<div class="admin-head"><div><div class="kicker">لوحة التحكم</div><h2>إدارة الطلاب والاختبارات والنتائج</h2></div><button class="secondary" onclick="document.getElementById('admin').classList.add('hidden')" style="width:auto">إغلاق</button></div>
 <div class="msg">✓ تم تحميل البيانات بنجاح — عدّل العلامات ثم اضغط حفظ.</div>
 <div class="stats"><div class="stat"><small>الطلاب</small><strong class="blue">${state.length}</strong></div><div class="stat"><small>الاختبارات</small><strong class="gold">${exams.length}</strong></div><div class="stat"><small>الحالة</small><strong class="green" style="font-size:18px">جاهز</strong></div></div>
 <div class="admin-table"><table><thead><tr><th>الرقم</th><th>الطالب</th><th>كلمة المرور</th>${exams.map(e=>`<th>${esc(e.name)}<br>من ${e.max}</th>`).join('')}</tr></thead><tbody>${rows}</tbody></table></div>
 <button onclick="saveAdmin()">💾 حفظ جميع التعديلات</button>
 <div class="card" style="margin-top:17px"><h2>➕ إضافة اختبار جديد</h2><label>اسم الاختبار</label><input id="newName" placeholder="مثال: الاختبار الثاني"><label>التاريخ</label><input id="newDate" type="date"><label>العلامة الكاملة</label><input id="newMax" type="number" value="10" min="1"><button onclick="addExam()">إضافة الاختبار للجميع</button></div>`;
 document.getElementById('admin').scrollIntoView({behavior:'smooth'});
}
function saveAdmin(){
 let exams=state[0]?.scores?.length||0;
 state.forEach((s,i)=>{s.password=document.getElementById('p'+i).value.trim();for(let j=0;j<exams;j++){let v=document.getElementById(`s${i}_${j}`);if(v)s.scores[j].score=Math.max(0,Number(v.value)||0)}});save();alert('تم حفظ جميع التعديلات بنجاح ✓');renderAdmin()
}
function addExam(){
 const name=document.getElementById('newName').value.trim()||`الاختبار ${state[0].scores.length+1}`;
 const date=document.getElementById('newDate').value;const max=Math.max(1,Number(document.getElementById('newMax').value)||10);
 state.forEach(s=>s.scores.push({name,date,score:0,max}));save();renderAdmin();alert('تمت إضافة الاختبار للجميع ✓')
}
</script>
</body></html>"""

@app.get("/")
def home():
    return render_template_string(PAGE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
