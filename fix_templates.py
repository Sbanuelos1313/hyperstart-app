import os

os.makedirs('app/templates/admin', exist_ok=True)
os.makedirs('app/templates/student', exist_ok=True)

templates = {}

templates['app/templates/landing.html'] = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>HyperStart — STEM/STEAM Pathways</title>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,800&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:"DM Sans",sans-serif;background:#0a0e1a;color:#f0f4ff;min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:40px 20px;text-align:center;}
body::before{content:"";position:fixed;inset:0;background:radial-gradient(ellipse 60% 50% at 50% 0%,rgba(245,200,66,0.06),transparent 60%);pointer-events:none;}
.hero{max-width:560px;position:relative;z-index:1;}
.title{font-family:"Bricolage Grotesque",sans-serif;font-size:clamp(36px,8vw,56px);font-weight:800;line-height:1.1;margin-bottom:12px;}
.title span{color:#f5c842;}
.sub{font-size:16px;color:#8b95b0;line-height:1.65;margin-bottom:32px;}
.pills{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-bottom:32px;}
.pill{padding:6px 14px;border-radius:20px;font-size:12px;font-weight:600;text-transform:uppercase;}
.p1{background:rgba(45,212,191,0.1);color:#2dd4bf;border:1px solid rgba(45,212,191,0.3);}
.p2{background:rgba(245,200,66,0.1);color:#f5c842;border:1px solid rgba(245,200,66,0.3);}
.p3{background:rgba(167,139,250,0.1);color:#a78bfa;border:1px solid rgba(167,139,250,0.3);}
.cta{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;}
.btn{padding:14px 32px;border-radius:8px;font-family:"DM Sans",sans-serif;font-size:16px;font-weight:700;cursor:pointer;border:none;text-decoration:none;display:inline-block;}
.btn-gold{background:#f5c842;color:#0a0e1a;}
.btn-out{background:transparent;color:#f0f4ff;border:1px solid rgba(255,255,255,0.15);}
</style>
</head>
<body>
<div class="hero">
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="72" height="72" style="margin:0 auto 20px">
    <rect width="100" height="100" rx="22" fill="#111827"/>
    <rect x="16" y="18" width="21" height="64" rx="10" fill="#5b8ecf"/>
    <rect x="63" y="18" width="21" height="64" rx="10" fill="#9b6a7a"/>
    <rect x="16" y="40" width="68" height="20" rx="10" fill="#f5c842"/>
  </svg>
  <div class="title">Hyper<span>Start</span></div>
  <div class="sub">STEM/STEAM career pathways for grades 6-8.<br>Discover your match. Build real skills. See your future.</div>
  <div class="pills">
    <span class="pill p1">Northeast OKC</span>
    <span class="pill p2">Millwood</span>
    <span class="pill p1">F.D. Moon</span>
    <span class="pill p3">Classen SAS</span>
    <span class="pill p2">2026-27</span>
  </div>
  <div class="cta">
    <a href="/auth/login" class="btn btn-gold">Start My Journey &rarr;</a>
    <a href="/admin/dashboard" class="btn btn-out">Admin Dashboard</a>
  </div>
</div>
</body>
</html>'''

templates['app/templates/login.html'] = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sign In - HyperStart</title>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,800&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:"DM Sans",sans-serif;background:#0a0e1a;color:#f0f4ff;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px;}
.box{background:#111827;border:1px solid rgba(255,255,255,0.07);border-radius:20px;padding:36px;max-width:420px;width:100%;}
.logo{text-align:center;margin-bottom:28px;}
.logo-title{font-family:"Bricolage Grotesque",sans-serif;font-size:28px;font-weight:800;margin-top:12px;}
.logo-title span{color:#f5c842;}
.logo-sub{font-size:13px;color:#8b95b0;margin-top:4px;}
.tabs{display:flex;margin-bottom:24px;border:1px solid rgba(255,255,255,0.07);border-radius:8px;overflow:hidden;}
.tab{flex:1;padding:10px;text-align:center;font-size:13px;font-weight:600;cursor:pointer;background:transparent;color:#8b95b0;border:none;}
.tab.active{background:#f5c842;color:#0a0e1a;}
.field{margin-bottom:16px;}
label{font-size:12px;font-weight:600;color:#8b95b0;text-transform:uppercase;letter-spacing:.06em;display:block;margin-bottom:6px;}
input,select{width:100%;padding:12px 15px;background:#1a2235;border:1px solid rgba(255,255,255,0.07);border-radius:8px;color:#f0f4ff;font-family:"DM Sans",sans-serif;font-size:15px;outline:none;}
input:focus,select:focus{border-color:#f5c842;}
.btn{width:100%;padding:13px;background:#f5c842;color:#0a0e1a;border:none;border-radius:8px;font-family:"DM Sans",sans-serif;font-size:15px;font-weight:700;cursor:pointer;margin-top:8px;}
.error{background:rgba(251,113,133,0.1);border:1px solid rgba(251,113,133,0.3);border-radius:8px;padding:10px 14px;font-size:13px;color:#fb7185;margin-bottom:16px;}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:12px;}
</style>
</head>
<body>
<div class="box">
  <div class="logo">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="52" height="52" style="margin:auto;display:block">
      <rect width="100" height="100" rx="22" fill="#0a0e1a"/>
      <rect x="16" y="18" width="21" height="64" rx="10" fill="#5b8ecf"/>
      <rect x="63" y="18" width="21" height="64" rx="10" fill="#9b6a7a"/>
      <rect x="16" y="40" width="68" height="20" rx="10" fill="#f5c842"/>
    </svg>
    <div class="logo-title">Hyper<span>Start</span></div>
    <div class="logo-sub">STEM/STEAM Career Pathways &middot; Grades 6-8</div>
  </div>
  <div class="tabs">
    <button class="tab active" id="tab-login" onclick="switchTab(\'login\')">Sign In</button>
    <button class="tab" id="tab-register" onclick="switchTab(\'register\')">New Student</button>
  </div>
  {% if error %}<div class="error">{{ error }}</div>{% endif %}
  <form id="form-login" action="/auth/login" method="POST">
    <div class="field"><label>Email</label><input type="email" name="email" placeholder="your@email.com" required></div>
    <div class="field"><label>Password</label><input type="password" name="password" placeholder="&bull;&bull;&bull;&bull;&bull;&bull;&bull;&bull;" required></div>
    <button type="submit" class="btn">Sign In &rarr;</button>
  </form>
  <form id="form-register" action="/auth/register" method="POST" style="display:none">
    <div class="field"><label>Full Name</label><input type="text" name="full_name" placeholder="Your name" required></div>
    <div class="field"><label>Email</label><input type="email" name="email" placeholder="your@email.com" required></div>
    <div class="field"><label>Password</label><input type="password" name="password" placeholder="Create a password" required minlength="6"></div>
    <div class="grid2">
      <div class="field"><label>Grade</label>
        <select name="grade" required>
          <option value="6">6th Grade</option>
          <option value="7">7th Grade</option>
          <option value="8">8th Grade</option>
        </select>
      </div>
      <div class="field"><label>Zip Code</label><input type="text" name="zip_code" placeholder="73111" maxlength="5"></div>
    </div>
    <div class="field"><label>School</label>
      <select name="school" required>
        <option value="">Select your school</option>
        <option value="F.D. Moon Middle School">F.D. Moon Middle School</option>
        <option value="Classen SAS">Classen SAS</option>
        <option value="Millwood Public Schools">Millwood Public Schools</option>
      </select>
    </div>
    <button type="submit" class="btn">Create Account &rarr;</button>
  </form>
</div>
<script>
function switchTab(t){
  document.getElementById("form-login").style.display=t==="login"?"block":"none";
  document.getElementById("form-register").style.display=t==="register"?"block":"none";
  document.getElementById("tab-login").className="tab"+(t==="login"?" active":"");
  document.getElementById("tab-register").className="tab"+(t==="register"?" active":"");
}
</script>
</body>
</html>'''

templates['app/templates/base.html'] = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{% block title %}HyperStart{% endblock %}</title>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,800&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">
{% block extra_styles %}{% endblock %}
</head>
<body>
{% block body %}{% endblock %}
<script>{% block scripts %}{% endblock %}</script>
</body>
</html>'''

templates['app/templates/student/portal.html'] = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>HyperStart - {{ user.full_name }}</title>
<script>
window.HS_USER = {
  id: {{ user.id }},
  name: "{{ user.full_name }}",
  grade: {{ user.grade or 7 }},
  school: "{{ user.school or 'F.D. Moon Middle School' }}",
  xp: {{ user.xp or 0 }},
  cluster: {{ ('"%s"' % user.cluster) if user.cluster else 'null' }},
  role: "{{ user.role }}"
};
window.HS_PROGRESS = {
  pre_done: {{ 'true' if (progress and progress.pre_done) else 'false' }},
  money_mod: {{ progress.money_mod if progress else 0 }},
  think_q: {{ progress.think_q if progress else 0 }},
  story_done: {{ 'true' if (progress and progress.story_done) else 'false' }},
  ai_mod: {{ progress.ai_mod if progress else 0 }},
  eng_done: {{ 'true' if (progress and progress.eng_done) else 'false' }},
  career_sparks_done: {{ 'true' if (progress and progress.career_sparks_done) else 'false' }},
  reflections: {{ progress.reflections | tojson if (progress and progress.reflections) else '{}' }}
};
</script>
<style>
body{margin:0;padding:40px;font-family:"DM Sans",sans-serif;background:#0a0e1a;color:#f0f4ff;text-align:center;}
.welcome{font-family:"Bricolage Grotesque",sans-serif;font-size:32px;font-weight:800;margin-bottom:12px;}
.welcome span{color:#f5c842;}
.sub{color:#8b95b0;margin-bottom:32px;}
.btn{padding:14px 28px;background:#f5c842;color:#0a0e1a;border:none;border-radius:8px;font-size:16px;font-weight:700;cursor:pointer;text-decoration:none;display:inline-block;margin:8px;}
.btn-out{background:transparent;color:#f0f4ff;border:1px solid rgba(255,255,255,0.2);}
.info{background:#111827;border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:20px;max-width:400px;margin:24px auto;text-align:left;}
.info p{font-size:13px;color:#8b95b0;margin:4px 0;}
.info strong{color:#f0f4ff;}
</style>
</head>
<body>
<div class="welcome">Hey, <span>{{ user.full_name.split()[0] }}.</span> &#128075;</div>
<div class="sub">Your STEM/STEAM journey starts here. &mdash; {{ user.grade }}th Grade &middot; {{ user.school }}</div>
<div class="info">
  <p><strong>XP Earned:</strong> {{ user.xp }}</p>
  <p><strong>Career Match:</strong> {{ user.cluster or "Not yet matched" }}</p>
  <p><strong>Pre-Assessment:</strong> {{ "Complete" if (progress and progress.pre_done) else "Pending" }}</p>
  <p><strong>Life & Money:</strong> Module {{ (progress.money_mod or 0) + 1 }} of 5</p>
  <p><strong>AI Literacy:</strong> Module {{ (progress.ai_mod or 0) + 1 }} of 4</p>
</div>
<a href="/auth/logout" class="btn btn-out">Sign Out</a>
<p style="color:#8b95b0;font-size:13px;margin-top:24px;">Full interactive portal coming soon. Progress is being tracked.</p>
</body>
</html>'''

for path, content in templates.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Written: {path}')

print('All templates done.')
