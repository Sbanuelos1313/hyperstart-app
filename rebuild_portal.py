import os, re

# Read the source grades-6-8 file
# We need to find it - check common locations
source_paths = [
    r'C:\dev\ChronosAI\Software_applications\hyperstart\grades-6-8.html',
    r'C:\dev\ChronosAI\hyperstart\grades-6-8.html', 
    r'C:\Users\sbanu\Downloads\hyperstart-grades-6-8.html',
]

src = None
for p in source_paths:
    if os.path.exists(p):
        src = p
        print('Found source:', p)
        break

if not src:
    print('Source not found in expected locations')
    print('Checking Downloads...')
    dl = os.path.expanduser('~/Downloads')
    for f in os.listdir(dl):
        if 'grades' in f.lower() or 'hyperstart' in f.lower():
            print(' Found:', f)
    exit()

with open(src, 'r', encoding='utf-8') as f:
    html = f.read()

print('Source size:', len(html))

# Extract head content (styles)
head_start = html.find('<head>') + 6
head_end = html.find('</head>')
head_content = html[head_start:head_end]

# Extract body content  
body_start = html.find('<body>') + 6
body_end = html.rfind('</body>')
body_content = html[body_start:body_end]

# Build the Jinja2 data injection block
jinja_block = '''<script>
window.HS_USER = {
  id: {{ user.id }},
  name: "{{ user.full_name }}",
  grade: {{ user.grade or 7 }},
  school: "{{ user.school or 'F.D. Moon Middle School' }}",
  xp: {{ user.xp or 0 }},
  cluster: {% if user.cluster %}"{{ user.cluster }}"{% else %}null{% endif %},
  role: "{{ user.role }}"
};
window.HS_PROGRESS = {
  pre_done: {% if progress and progress.pre_done %}true{% else %}false{% endif %},
  money_mod: {{ progress.money_mod if progress else 0 }},
  think_q: {{ progress.think_q if progress else 0 }},
  story_done: {% if progress and progress.story_done %}true{% else %}false{% endif %},
  ai_mod: {{ progress.ai_mod if progress else 0 }},
  eng_done: {% if progress and progress.eng_done %}true{% else %}false{% endif %},
  career_sparks_done: {% if progress and progress.career_sparks_done %}true{% else %}false{% endif %},
  reflections: {{ progress.reflections | tojson if (progress and progress.reflections) else '{}' }}
};
</script>'''

# Find and replace the static init at the bottom of body_content
new_init = """
// Initialize with real server data
init();
if(typeof window.HS_USER !== 'undefined' && window.HS_USER.id) {
  student = {
    id: window.HS_USER.id,
    name: window.HS_USER.name,
    grade: window.HS_USER.grade || 7,
    school: window.HS_USER.school || 'F.D. Moon Middle School',
    emoji: '\\u2728',
    color: '#f5c842',
    xp: window.HS_USER.xp || 0,
    cluster: window.HS_USER.cluster || null,
    tab: 'home'
  };
  var p = window.HS_PROGRESS || {};
  answers = {
    moneyMod: p.money_mod || 0,
    thinkQ: p.think_q || 0,
    aiMod: p.ai_mod || 0,
    storyStarted: p.story_done || false,
    preAssessmentDone: p.pre_done || false,
    quizDone: p.career_sparks_done || false,
    clusterName: window.HS_USER.cluster || null,
    sparkScores: {}, sparkCollected: [],
    sparkPhase: p.career_sparks_done ? 'done' : 'collect'
  };
  if(p.reflections) Object.assign(answers, p.reflections);
  window.saveToServer = function(mod, xp) {
    fetch('/student/api/progress', {method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({cluster:student.cluster,xp:student.xp,xp_delta:xp||0,
        money_mod:answers.moneyMod||0,think_q:answers.thinkQ||0,ai_mod:answers.aiMod||0,
        story_done:!!answers.storyStarted,eng_done:!!answers.engDone,module:mod||'general',
        reflections:Object.fromEntries(Object.entries(answers).filter(function(e){return e[0].startsWith('reflect_')||e[0].startsWith('aiReflect_');}))
      })
    }).catch(function(){});
  };
  var _ox=awardXP; awardXP=function(n){_ox(n);window.saveToServer('xp',n);};
} else {
  student=JSON.parse(JSON.stringify(PERSONAS.find(function(p){return p.id==='zara';})));
  answers={};
}
quizState={q:0,scores:{}};
showTab('home');
"""

# Replace old init patterns
old_patterns = [
    "init();\nstudent=JSON.parse(JSON.stringify(PERSONAS.find(function(p){return p.id==='zara';})));\nanswers={};quizState={q:0,scores:{}};\nshowTab('home');",
    "init();\nstudent=JSON.parse(JSON.stringify(PERSONAS.find(p=>p.id==='zara')));\nanswers={};quizState={q:0,scores:{}};\nshowTab('home');",
]

replaced = False
for old in old_patterns:
    if old in body_content:
        body_content = body_content.replace(old, new_init)
        print('Replaced old init pattern')
        replaced = True
        break

if not replaced:
    # Find the last showTab('home') and replace surrounding block
    idx = body_content.rfind("showTab('home');")
    if idx > 0:
        # Find start of init block
        block_start = body_content.rfind('\ninit();', 0, idx)
        if block_start < 0:
            block_start = idx - 500
        end = idx + len("showTab('home');")
        body_content = body_content[:block_start] + new_init + body_content[end:]
        print('Replaced init block by position')

# Build final portal
portal = '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">\n<title>HyperStart</title>\n<link rel="preconnect" href="https://fonts.googleapis.com">\n<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,700;12..96,800&family=DM+Sans:wght@300;400;500&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">\n' + jinja_block + '\n' + head_content + '\n</head>\n<body>' + body_content + '</body>\n</html>'

out_path = 'app/templates/student/portal.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(portal)

print('Written:', len(portal), 'bytes')
print('HS_USER present:', 'window.HS_USER' in portal)
print('showTab home present:', "showTab('home')" in portal)
print('Done! Now run: git add app/templates/student/portal.html && git commit -m "Full portal rewrite" && git push origin main')
