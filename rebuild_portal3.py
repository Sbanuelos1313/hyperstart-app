
with open('grades-6-8-source.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find body content
body_start = html.find('<body>') + 6
body_end = html.rfind('</body>')
body_content = html[body_start:body_end]

# Find head content  
head_start = html.find('<head>') + 6
head_end = html.find('</head>')
head_content = html[head_start:head_end]

# Replace the static init with API-based data loading
old_init = "init();\nstudent=JSON.parse(JSON.stringify(PERSONAS.find(function(p){return p.id==='zara';})));\nanswers={};quizState={q:0,scores:{}};\nshowTab('home');"

new_init = """
init();

// Load real user data from server API
fetch('/student/api/me', {credentials: 'include'})
  .then(function(r) { return r.json(); })
  .then(function(data) {
    if(data && data.id) {
      student = {
        id: data.id,
        name: data.name,
        grade: data.grade || 7,
        school: data.school || 'F.D. Moon Middle School',
        emoji: '\\u2728',
        color: '#f5c842',
        xp: data.xp || 0,
        cluster: data.cluster || null,
        tab: 'home'
      };
      var p = data.progress || {};
      answers = {
        moneyMod: p.money_mod || 0,
        thinkQ: p.think_q || 0,
        aiMod: p.ai_mod || 0,
        storyStarted: p.story_done || false,
        preAssessmentDone: p.pre_done || false,
        quizDone: p.career_sparks_done || false,
        clusterName: data.cluster || null,
        sparkScores: {}, sparkCollected: [],
        sparkPhase: p.career_sparks_done ? 'done' : 'collect'
      };
      if(p.reflections) Object.assign(answers, p.reflections);

      // Override awardXP to save to server
      var _ox = awardXP;
      awardXP = function(n) {
        _ox(n);
        fetch('/student/api/progress', {
          method: 'POST', credentials: 'include',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({
            cluster: student.cluster, xp: student.xp, xp_delta: n || 0,
            money_mod: answers.moneyMod || 0, think_q: answers.thinkQ || 0,
            ai_mod: answers.aiMod || 0, story_done: !!answers.storyStarted,
            eng_done: !!answers.engDone, module: 'general'
          })
        }).catch(function(){});
      };
    } else {
      // Fallback to demo persona
      student = JSON.parse(JSON.stringify(PERSONAS.find(function(p){return p.id==='zara';})));
      answers = {};
    }
    quizState = {q:0, scores:{}};
    showTab('home');
  })
  .catch(function() {
    // If API fails, use demo
    student = JSON.parse(JSON.stringify(PERSONAS.find(function(p){return p.id==='zara';})));
    answers = {};
    quizState = {q:0, scores:{}};
    showTab('home');
  });
"""

if old_init in body_content:
    body_content = body_content.replace(old_init, new_init)
    print('Init replaced with API approach')
else:
    # Try finding by position
    idx = body_content.rfind("showTab('home');")
    block_start = body_content.rfind('\ninit();', 0, idx)
    if block_start < 0:
        block_start = body_content.rfind('init();', 0, idx)
    end = idx + len("showTab('home');")
    body_content = body_content[:block_start] + new_init + body_content[end:]
    print('Init replaced by position')

# Build portal - NO Jinja2 templating at all, just pure HTML
portal = ('<!DOCTYPE html>\n<html lang="en">\n<head>\n'
    '<meta charset="UTF-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">\n'
    '<title>HyperStart</title>\n'
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,700;12..96,800&family=DM+Sans:wght@300;400;500&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">\n'
    + head_content + '\n</head>\n<body>'
    + body_content + '</body>\n</html>')

with open('app/templates/student/portal.html', 'w', encoding='utf-8') as f:
    f.write(portal)

print('Written:', len(portal), 'bytes')
print('showTab home:', "showTab('home')" in portal)
print('fetch /student/api/me:', "fetch('/student/api/me'" in portal)
print('No Jinja2:', '{{' not in portal and '{%' not in portal)
print('DONE')
