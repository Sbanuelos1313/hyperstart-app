import os

with open('grades-6-8-source.html', 'r', encoding='utf-8') as f:
    html = f.read()

print('Source size:', len(html))

# Find showTab home
idx = html.rfind("showTab('home');")
print('showTab home at:', idx)
if idx > 0:
    print('Context:', repr(html[max(0,idx-200):idx+20]))

# Find head content
head_start = html.find('<head>') + 6
head_end = html.find('</head>')
head_content = html[head_start:head_end]

# Find body content
body_start = html.find('<body>') + 6
body_end = html.rfind('</body>')
body_content = html[body_start:body_end]

print('Head size:', len(head_content))
print('Body size:', len(body_content))

# Jinja2 data injection
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

new_init = '''
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
        reflections:Object.fromEntries(Object.entries(answers).filter(function(e){
          return e[0].startsWith('reflect_')||e[0].startsWith('aiReflect_');
        }))
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
'''

# Find and replace the init block
idx = body_content.rfind("showTab('home');")
if idx > 0:
    # Find beginning of init block
    block_start = body_content.rfind('\ninit();', 0, idx)
    if block_start < 0:
        block_start = body_content.rfind('init();', 0, idx)
    end = idx + len("showTab('home');")
    print('Replacing from', block_start, 'to', end)
    body_content = body_content[:block_start] + new_init + body_content[end:]
    print('Init replaced')
else:
    print('ERROR: showTab home not found in body!')

# Build portal
portal = ('<!DOCTYPE html>\n<html lang="en">\n<head>\n'
    '<meta charset="UTF-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">\n'
    '<title>HyperStart</title>\n'
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,700;12..96,800&family=DM+Sans:wght@300;400;500&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">\n'
    + jinja_block + '\n'
    + head_content + '\n</head>\n<body>'
    + body_content + '</body>\n</html>')

out = 'app/templates/student/portal.html'
with open(out, 'w', encoding='utf-8') as f:
    f.write(portal)

print('Written:', len(portal), 'bytes')
print('HS_USER:', 'window.HS_USER' in portal)
print('showTab home:', "showTab('home')" in portal)
print('DONE - now commit and push')
