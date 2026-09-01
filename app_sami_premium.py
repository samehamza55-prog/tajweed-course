from flask import Flask, render_template_string, send_file
import os

app = Flask(__name__)

@app.get("/khatm_sami.png")
def khatm_sami():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "khatm_sami-2.png")
    return send_file(path, mimetype="image/png")

PAGE = r'''<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#082a22">
<title>بوابة نتائج دورة التجويد | سامي</title>
<style>
:root{--g:#087b5b;--g2:#20c997;--deep:#082a22;--ink:#102c26;--muted:#70817c;--gold:#c49a45;--bg:#f4f8f6;--white:#fff;--line:#e1ebe6;--shadow:0 24px 70px rgba(8,42,34,.10)}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font-family:Tahoma,"Segoe UI",Arial,sans-serif;color:var(--ink);background:radial-gradient(circle at 5% 0,#d9f8ec 0,transparent 30%),radial-gradient(circle at 100% 7%,#eee7ff 0,transparent 27%),linear-gradient(135deg,#f8fbfa,#eef6f2);min-height:100vh}
body:before{content:"";position:fixed;inset:0;pointer-events:none;opacity:.25;background-image:radial-gradient(#087b5b 1px,transparent 1px);background-size:26px 26px;mask-image:linear-gradient(to bottom,black,transparent 65%)}
.wrap{max-width:1160px;margin:auto;padding:20px 15px 55px;position:relative}
.top{display:flex;justify-content:space-between;align-items:center;gap:14px;margin-bottom:18px;padding:13px 15px;border:1px solid #ffffffaa;border-radius:24px;background:#ffffffc9;backdrop-filter:blur(16px);box-shadow:0 12px 35px #123b3010}
.brand{display:flex;align-items:center;gap:12px}.logo{width:52px;height:52px;border-radius:17px;display:grid;place-items:center;color:white;font-size:25px;background:linear-gradient(145deg,#063f31,#12a875 60%,#d3ad58);box-shadow:0 12px 30px #087b5b30}.brand b{font-size:20px}.brand small{display:block;color:var(--muted);margin-top:4px}
.status{padding:9px 13px;border-radius:999px;background:#effaf5;border:1px solid #d5eee4;color:var(--g);font-size:12px;font-weight:900}
.layout{display:grid;grid-template-columns:1.55fr .8fr;gap:18px}.card{background:#fffffff0;border:1px solid #ffffff;outline:1px solid #deebe5;border-radius:30px;padding:25px;box-shadow:var(--shadow);backdrop-filter:blur(14px)}
.hero{min-height:450px;display:flex;flex-direction:column;justify-content:center;overflow:hidden;position:relative}.hero:after{content:"";position:absolute;width:300px;height:300px;border-radius:50%;left:-145px;bottom:-165px;background:linear-gradient(135deg,#d8f7e9,#fff1c4);opacity:.75}
.kicker{color:var(--g);font-weight:900;font-size:13px;letter-spacing:.2px}h1{font-size:46px;line-height:1.2;margin:10px 0 13px;max-width:760px}.lead{color:var(--muted);line-height:2;font-size:15px;max-width:720px}
.hero-pills{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}.pill{padding:8px 11px;border-radius:999px;background:#f4faf7;border:1px solid #dcece5;color:#2d6555;font-size:12px;font-weight:800}
.poem{margin-top:22px;padding:18px 20px;border-radius:20px;background:linear-gradient(135deg,#f1fbf6,#fffdf7);border:1px solid #d9ece4;line-height:2.05;color:#2b6656;font-size:14px;position:relative;z-index:1}.poem b{display:block;color:var(--g);margin-bottom:6px}
.login h2{margin:0 0 9px;font-size:23px}.hint{background:linear-gradient(135deg,#f7fbf9,#fff);border:1px solid var(--line);padding:14px;border-radius:17px;color:var(--muted);font-size:13px;line-height:1.85}
label{display:block;font-weight:900;font-size:13px;margin:16px 0 7px}input{width:100%;padding:14px 15px;border:1px solid #d5e2dc;border-radius:15px;background:#fff;font-size:16px;outline:0;transition:.2s}input:focus{border-color:var(--g);box-shadow:0 0 0 4px #087b5b12}
button{width:100%;border:0;border-radius:15px;padding:14px 16px;margin-top:10px;font-size:15px;font-weight:900;color:#fff;background:linear-gradient(135deg,#066c50,#18bd87);box-shadow:0 12px 25px #087b5b25;cursor:pointer;transition:.2s}button:hover{transform:translateY(-1px);filter:saturate(1.05)}button.secondary{background:#eff4f1;color:#29483f;box-shadow:none}button.link{background:transparent;color:var(--g);box-shadow:none;font-size:13px}
.hidden{display:none!important}.msg{margin-top:12px;padding:12px 14px;border-radius:15px;background:#effaf5;color:#176b53;font-size:13px;line-height:1.8}.error{background:#fff0f0;color:#a33d3d}
.student,.admin{margin-top:18px}.student-head,.admin-head{display:flex;align-items:center;justify-content:space-between;gap:12px}.student-head h2,.admin-head h2{margin:5px 0}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:18px}.stat{background:#fff;border:1px solid var(--line);border-radius:20px;padding:16px}.stat small{color:var(--muted)}.stat strong{display:block;font-size:27px;margin-top:5px}.green{color:var(--g)}.blue{color:#3f72d5}.gold{color:var(--gold)}
.section-title{margin:25px 0 11px;font-size:21px}.result{border:1px solid var(--line);border-radius:21px;padding:17px;margin-top:11px;background:#fff}.result-top{display:flex;justify-content:space-between;gap:12px;align-items:center}.result-title{font-weight:900}.date{color:var(--muted);font-size:12px;margin-top:5px}.score{font-size:28px;font-weight:900;color:var(--g);white-space:nowrap}
.bar{height:10px;border-radius:99px;background:#eaf0ed;overflow:hidden;margin:15px 0 8px}.bar i{display:block;height:100%;border-radius:99px;background:linear-gradient(90deg,#087b5b,#25d39a)}.meta{display:flex;justify-content:space-between;gap:8px;color:var(--muted);font-size:12px}.badge{background:#eaf8f2;color:var(--g);padding:6px 9px;border-radius:999px;font-weight:900}
.smart{margin-top:16px;border-radius:22px;padding:18px;background:linear-gradient(135deg,#102f28,#174d40);color:#effff9;border:1px solid #2e6f5d;box-shadow:0 18px 35px #0a312727}.smart small{color:#b9e8d7;font-weight:900}.smart h3{margin:7px 0;font-size:18px}.smart p{margin:0;color:#d9eee8;line-height:1.9;font-size:13px}
.stamp-wrap{display:flex;justify-content:center;align-items:center;margin:22px auto 5px;padding:13px;border-radius:24px;background:linear-gradient(135deg,#fbf8ee,#fff);border:1px solid #eadfbe;max-width:280px}.stamp{width:100%;max-width:240px;height:auto;display:block;filter:drop-shadow(0 10px 15px #6d572a22)}
.footer{text-align:center;color:#82918c;font-size:12px;margin-top:22px;line-height:1.9}.admin-table{overflow:auto;margin-top:12px}table{width:100%;border-collapse:separate;border-spacing:0;min-width:650px}th,td{padding:10px;border-bottom:1px solid var(--line);text-align:center;font-size:13px}th{background:#f7faf8;color:#61716c;font-size:12px}.admin input{padding:8px;font-size:13px}
.modal{position:fixed;inset:0;background:#09251d99;display:grid;place-items:center;padding:16px;z-index:10;backdrop-filter:blur(7px)}.modal .card{width:min(450px,100%);background:#fff}.divider{height:1px;background:var(--line);margin:20px 0}
@media(max-width:820px){.layout{grid-template-columns:1fr}.hero{min-height:auto}h1{font-size:34px}.stats{grid-template-columns:1fr}.top{align-items:flex-start}.status{display:none}.card{padding:20px;border-radius:24px}.result-top{align-items:flex-start}}
@media(max-width:480px){h1{font-size:30px}.brand b{font-size:17px}.logo{width:46px;height:46px}}
</style>
</head>
<body>
<main class="wrap">
<header class="top"><div class="brand"><div class="logo">✦</div><div><b>بوابة دورة التجويد</b><small>نتائج • متابعة • إنجاز</small></div></div><div class="status">● النظام جاهز وآمن</div></header>
<section class="layout">
<section class="card hero"><div class="kicker">مرحباً بك في بوابة نتائج دورة التجويد</div><h1>تعلّم، أتقن، وارتقِ في تلاوتك ✨</h1><div class="lead">بوابة أنيقة لمتابعة نتائج الطلاب، مصممة لتكون واضحة وسريعة على الهاتف، مع عرض جميل للتقدم والإنجازات.</div><div class="hero-pills"><span class="pill">🌿 متابعة مستمرة</span><span class="pill">📊 نتائج واضحة</span><span class="pill">🏆 إنجازك خطوة بخطوة</span></div><div class="poem"><b>🌿 أبيات جميلة في طريق التعلّم</b>تعلّم كتابَ اللهِ وامضِ بثقةٍ، فالعلمُ نورٌ والقلوبُ منارُ<br>واجعلْ تلاوتَكَ كلَّ يومٍ عادةً، فبها يطيبُ الوقتُ والأعمارُ</div></section>
<section class="card login"><div class="kicker">بوابة الطالب</div><h2>🔐 دخول الطالب</h2><div class="hint">أدخل كلمة المرور الخاصة بك، وستظهر نتائجك أنت فقط.</div><label>كلمة المرور</label><input id="pw" type="password" inputmode="numeric" autocomplete="off" placeholder="أدخل كلمة المرور" onkeydown="if(event.key==='Enter')studentLogin()"><button onclick="studentLogin()">عرض نتائجي ←</button><button class="link" onclick="openAdmin()">⚙ دخول المسؤول</button><div id="msg"></div><div class="divider"></div><div class="stamp-wrap"><img class="stamp" src="/khatm_sami.png" alt="ختم سامي والتوقيع"></div><div style="text-align:center;color:var(--muted);font-size:11px;margin-top:7px">ختم وتوقيع • سامي عدي</div></section>
</section>
<section id="student" class="card student hidden"></section><section id="admin" class="card admin hidden"></section>
<div class="footer">وفقك الله في علمك، وبارك لك في وقتك وجهدك 🌿<br><b>الإتقان هوية النجاح</b></div>
</main>
<div id="modal" class="modal hidden"><div class="card"><div class="kicker">صلاحيات خاصة</div><h2>⚙ دخول المسؤول</h2><label>رمز المسؤول</label><input id="apw" type="password" placeholder="رمز المسؤول" onkeydown="if(event.key==='Enter')adminLogin()"><button onclick="adminLogin()">دخول لوحة التحكم</button><button class="secondary" onclick="closeAdmin()">إلغاء</button><div id="amsg"></div></div></div>
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
 const pw=document.getElementById('pw').value.trim(),m=document.getElementById('msg');const s=state.find(x=>x.password===pw);
 if(!s){m.innerHTML='<div class="msg error">كلمة المرور غير صحيحة. حاول مرة أخرى.</div>';return}
 const total=s.scores.reduce((a,x)=>a+Number(x.score||0),0),max=s.scores.reduce((a,x)=>a+Number(x.max||0),0),pct=max?Math.round(total/max*100):0;
 const label=pct>=90?'مستوى مميز جداً 🏆':pct>=75?'مستوى ممتاز 🌟':pct>=60?'تقدم جميل 💚':'نحتاج مزيداً من التدريب 🌱';
 const advice=pct>=90?'أداء رائع! حافظ على المراجعة اليومية وواصل طريق الإتقان.':pct>=75?'مستواك جميل. ركّز على الأخطاء الصغيرة وستقترب أكثر من الإتقان.':'لا تستعجل النتيجة؛ المراجعة والمداومة تصنع الفرق. أنت قادر على التحسن بإذن الله.';
 const results=s.scores.map(x=>{const p=x.max?Math.round(x.score/x.max*100):0;const label2=p>=90?'ممتاز جداً':p>=75?'ممتاز':p>=60?'جيد جداً':p>=50?'جيد':'استمر بالتدريب';return `<div class="result"><div class="result-top"><div><div class="result-title">📘 ${esc(x.name)}</div><div class="date">📅 ${esc(x.date||'بدون تاريخ')}</div></div><div class="score">${x.score} / ${x.max}</div></div><div class="bar"><i style="width:${p}%"></i></div><div class="meta"><span>النسبة <b class="green">${p}%</b></span><span class="badge">${label2}</span></div></div>`}).join('');
 document.getElementById('student').classList.remove('hidden');document.getElementById('student').innerHTML=`<div class="student-head"><div><div class="kicker">السلام عليكم ورحمة الله وبركاته</div><h2>نتائج الطالب: <span class="green">${esc(s.name)}</span></h2></div><button class="secondary" onclick="logoutStudent()" style="width:auto">خروج</button></div><div class="stats"><div class="stat"><small>النسبة الإجمالية</small><strong class="green">${pct}%</strong></div><div class="stat"><small>المجموع الكلي</small><strong class="blue">${total} / ${max}</strong></div><div class="stat"><small>عدد الاختبارات</small><strong class="gold">${s.scores.length}</strong></div></div><div class="smart"><small>✦ المساعد الذكي للتقدم</small><h3>${label}</h3><p>${advice}</p></div><div class="section-title">نتائج الاختبارات</div>${results}<div class="msg">✨ أحسنت، استمر في المراجعة والتدريب؛ فالإتقان يأتي مع الصبر والمداومة.</div><div class="stamp-wrap"><img class="stamp" src="/khatm_sami.png" alt="ختم سامي والتوقيع"></div>`;
 document.getElementById('pw').value='';document.getElementById('student').scrollIntoView({behavior:'smooth'})
}
function logoutStudent(){document.getElementById('student').classList.add('hidden');window.scrollTo({top:0,behavior:'smooth'})}
function openAdmin(){document.getElementById('modal').classList.remove('hidden');document.getElementById('apw').focus()}
function closeAdmin(){document.getElementById('modal').classList.add('hidden');document.getElementById('apw').value='';document.getElementById('amsg').innerHTML=''}
function adminLogin(){if(document.getElementById('apw').value!==ADMIN){document.getElementById('amsg').innerHTML='<div class="msg error">رمز المسؤول غير صحيح.</div>';return}closeAdmin();renderAdmin()}
function renderAdmin(){
 let exams=state[0]?.scores?.map((x,i)=>({i,name:x.name,date:x.date,max:x.max}))||[];
 let rows=state.map((s,i)=>`<tr><td>${esc(s.id)}</td><td><b>${esc(s.name)}</b></td><td><input id="p${i}" value="${esc(s.password)}"></td>${exams.map(e=>`<td><input id="s${i}_${e.i}" type="number" min="0" max="${e.max}" step="0.5" value="${s.scores[e.i]?.score??0}"></td>`).join('')}</tr>`).join('');
 document.getElementById('admin').classList.remove('hidden');document.getElementById('admin').innerHTML=`<div class="admin-head"><div><div class="kicker">لوحة التحكم</div><h2>إدارة الطلاب والاختبارات والنتائج</h2></div><button class="secondary" onclick="document.getElementById('admin').classList.add('hidden')" style="width:auto">إغلاق</button></div><div class="msg">✓ تم تحميل البيانات بنجاح — عدّل العلامات ثم اضغط حفظ.</div><div class="stats"><div class="stat"><small>الطلاب</small><strong class="blue">${state.length}</strong></div><div class="stat"><small>الاختبارات</small><strong class="gold">${exams.length}</strong></div><div class="stat"><small>الحالة</small><strong class="green" style="font-size:18px">جاهز</strong></div></div><div class="admin-table"><table><thead><tr><th>الرقم</th><th>الطالب</th><th>كلمة المرور</th>${exams.map(e=>`<th>${esc(e.name)}<br>من ${e.max}</th>`).join('')}</tr></thead><tbody>${rows}</tbody></table></div><button onclick="saveAdmin()">💾 حفظ جميع التعديلات</button><div class="card" style="margin-top:17px"><h2>➕ إضافة اختبار جديد</h2><label>اسم الاختبار</label><input id="newName" placeholder="مثال: الاختبار الثاني"><label>التاريخ</label><input id="newDate" type="date"><label>العلامة الكاملة</label><input id="newMax" type="number" value="10" min="1"><button onclick="addExam()">إضافة الاختبار للجميع</button></div>`;document.getElementById('admin').scrollIntoView({behavior:'smooth'})
}
function saveAdmin(){let exams=state[0]?.scores?.length||0;state.forEach((s,i)=>{s.password=document.getElementById('p'+i).value.trim();for(let j=0;j<exams;j++){let v=document.getElementById(`s${i}_${j}`);if(v)s.scores[j].score=Math.max(0,Number(v.value)||0)}});save();alert('تم حفظ جميع التعديلات بنجاح ✓');renderAdmin()}
function addExam(){const name=document.getElementById('newName').value.trim()||`الاختبار ${state[0].scores.length+1}`;const date=document.getElementById('newDate').value;const max=Math.max(1,Number(document.getElementById('newMax').value)||10);state.forEach(s=>s.scores.push({name,date,score:0,max}));save();renderAdmin();alert('تمت إضافة الاختبار للجميع ✓')}
</script>
</body></html>'''

@app.get("/")
def home():
    return render_template_string(PAGE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
