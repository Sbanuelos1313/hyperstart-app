import os

with open('app/templates/student/portal.html', 'r', encoding='utf-8') as f:
    portal = f.read()

print('Original size:', len(portal))

# 1. Add HS_USER injection in <head> before </head>
hs_user_script = '''
<script>
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
</script>
</head>'''

portal = portal.replace('</head>', hs_user_script, 1)
print('After HS_USER inject:', len(portal))

# 2. Replace the old static init with HS_USER-aware version
old_init = """// Load real user data from server
init();
student = {
  id: '{{ user.id }}',"""

# Check if the old template-style init is present
if old_init in portal:
    print('Old template init found - replacing')
    # Find from "// Load real user data" to "showTab('home');"
    start = portal.find('// Load real user data from server\ninit();')
    end = portal.find("showTab('home');", start) + len("showTab('home');")
    old_block = portal[start:end]
    
    new_init = """init();

// Use real server data if available
if(typeof window.HS_USER !== 'undefined' && window.HS_USER.id) {
  student = {
    id: window.HS_USER.id,
    name: window.HS_USER.name,
    grade: window.HS_USER.grade || 7,
    school: window.HS_USER.school || 'F.D. Moon Middle School',
    emoji: String.fromCodePoint(0x1F31F),
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
    sparkScores: {},
    sparkCollected: [],
    sparkPhase: p.career_sparks_done ? 'done' : 'collect'
  };
  if(p.reflections) { Object.assign(answers, p.reflections); }
  window.saveToServer = function(module, xpDelta) {
    fetch('/student/api/progress', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        cluster: student.cluster, xp: student.xp, xp_delta: xpDelta || 0,
        money_mod: answers.moneyMod || 0, think_q: answers.thinkQ || 0,
        ai_mod: answers.aiMod || 0, story_done: !!answers.storyStarted,
        eng_done: !!answers.engDone, module: module || 'general',
        reflections: Object.fromEntries(
          Object.entries(answers).filter(function(e){ return e[0].startsWith('reflect_') || e[0].startsWith('aiReflect_'); })
        )
      })
    }).catch(function(){});
  };
  var _origXP = awardXP;
  awardXP = function(n) { _origXP(n); window.saveToServer('xp', n); };
} else {
  student = JSON.parse(JSON.stringify(PERSONAS.find(function(p){return p.id==='zara';})));
  answers = {};
}
quizState = {q:0,scores:{}};
showTab('home');"""
    
    portal = portal[:start] + new_init + portal[end:]
    print('New init injected')

else:
    # Find the old non-template init
    old_static = "init();\nstudent=JSON.parse(JSON.stringify(PERSONAS.find(function(p){return p.id==='zara';})));\nanswers={};quizState={q:0,scores:{}};\nshowTab('home');"
    
    if old_static in portal:
        print('Static init found - replacing')
    else:
        # Find saveToServer block
        start = portal.rfind('\n\n// Override awardXP')
        if start < 0:
            start = portal.rfind("showTab('home');")
            # Back up to find beginning of init block
            start = portal.rfind('\ninit();', 0, start)
        end = portal.find("showTab('home');", start) + len("showTab('home');")
        print('Found init block at:', start, 'to', end)
        old_block = portal[start:end]
        print('Old block preview:', repr(old_block[:100]))

        new_init = """
init();

if(typeof window.HS_USER !== 'undefined' && window.HS_USER.id) {
  student = {
    id: window.HS_USER.id,
    name: window.HS_USER.name,
    grade: window.HS_USER.grade || 7,
    school: window.HS_USER.school || 'F.D. Moon Middle School',
    emoji: String.fromCodePoint(0x1F31F),
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
  if(p.reflections) { Object.assign(answers, p.reflections); }
  window.saveToServer = function(module, xpDelta) {
    fetch('/student/api/progress', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        cluster: student.cluster, xp: student.xp, xp_delta: xpDelta || 0,
        money_mod: answers.moneyMod || 0, think_q: answers.thinkQ || 0,
        ai_mod: answers.aiMod || 0, story_done: !!answers.storyStarted,
        eng_done: !!answers.engDone, module: module || 'general',
        reflections: Object.fromEntries(
          Object.entries(answers).filter(function(e){ return e[0].startsWith('reflect_') || e[0].startsWith('aiReflect_'); })
        )
      })
    }).catch(function(){});
  };
  var _origXP = awardXP;
  awardXP = function(n) { _origXP(n); window.saveToServer('xp', n); };
} else {
  student = JSON.parse(JSON.stringify(PERSONAS.find(function(p){return p.id==='zara';})));
  answers = {};
}
quizState = {q:0,scores:{}};
showTab('home');"""

        portal = portal[:start] + new_init + portal[end:]
        print('Init replaced')

with open('app/templates/student/portal.html', 'w', encoding='utf-8') as f:
    f.write(portal)

print('Final size:', len(portal))
print('HS_USER present:', 'window.HS_USER' in portal)
print('Done!')
