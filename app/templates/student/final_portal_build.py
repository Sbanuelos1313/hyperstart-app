
# This script writes the complete portal HTML directly to the correct location
# It includes the full renderThink function which was missing from the source

import os

# First read the current source file
with open('grades-6-8-source.html', 'r', encoding='utf-8') as f:
    src = f.read()

print('Source size:', len(src))

# Fix the broken end of file
script_end = src.rfind('</script>')
src = src[:script_end + 9] + '\n</body>\n</html>'

# Extract parts
head_start = src.find('<head>') + 6
head_end = src.find('</head>')
head_content = src[head_start:head_end]

body_start = src.find('<body>') + 6
first_script = src.find('<script>', body_start)
body_html = src[body_start:first_script]

script_start = src.rfind('<script>') + 8
script_end = src.rfind('</script>')
script_content = src[script_start:script_end]

print('Script size:', len(script_content))

# Find and replace the init block
idx = script_content.rfind("showTab('home');")
block_start = script_content.rfind('\ninit();', 0, idx)
if block_start < 0:
    block_start = script_content.rfind('init();', 0, idx)
end = idx + len("showTab('home');")

new_init = """
init();
fetch('/student/api/me',{credentials:'include'})
.then(function(r){return r.json();})
.then(function(data){
  if(data&&data.id){
    student={id:data.id,name:data.name,grade:data.grade||7,school:data.school||'F.D. Moon Middle School',emoji:'\\u2728',color:'#f5c842',xp:data.xp||0,cluster:data.cluster||null,tab:'home'};
    var p=data.progress||{};
    answers={moneyMod:p.money_mod||0,thinkQ:p.think_q||0,aiMod:p.ai_mod||0,storyStarted:p.story_done||false,preAssessmentDone:p.pre_done||false,quizDone:p.career_sparks_done||false,clusterName:data.cluster||null,sparkScores:{},sparkCollected:[],sparkPhase:p.career_sparks_done?'done':'collect'};
    if(p.reflections)Object.assign(answers,p.reflections);
    var _ox=awardXP;
    awardXP=function(n){_ox(n);fetch('/student/api/progress',{method:'POST',credentials:'include',headers:{'Content-Type':'application/json'},body:JSON.stringify({cluster:student.cluster,xp:student.xp,xp_delta:n||0,money_mod:answers.moneyMod||0,think_q:answers.thinkQ||0,ai_mod:answers.aiMod||0,story_done:!!answers.storyStarted,eng_done:!!answers.engDone,module:'general'})}).catch(function(){});};
  }else{
    student=JSON.parse(JSON.stringify(PERSONAS.find(function(p){return p.id==='zara';})));
    answers={};
  }
  quizState={q:0,scores:{}};
  showTab('home');
}).catch(function(){
  student=JSON.parse(JSON.stringify(PERSONAS.find(function(p){return p.id==='zara';})));
  answers={};quizState={q:0,scores:{}};
  showTab('home');
});

// Export to window for onclick handlers
window.showTab=showTab;window.go=go;window.loginStudent=loginStudent;
window.collectCard=collectCard;window.loadCareerAI=loadCareerAI;
window.saveReflect=saveReflect;window.pickStory=pickStory;
window.pickInterest=pickInterest;window.selectPre=selectPre;
window.updateBudgetChallenge=updateBudgetChallenge;
window.clusterKey=clusterKey;window.awardXP=awardXP;
window.buildInterestGrid=buildInterestGrid;window.renderHome=renderHome;
"""

script_content = script_content[:block_start] + new_init + script_content[end:]

# Build the final portal - NO Jinja2, pure HTML with API fetch
portal = ('<!DOCTYPE html>\n<html lang="en">\n<head>\n'
    '<meta charset="UTF-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">\n'
    '<title>HyperStart</title>\n'
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,700;12..96,800&family=DM+Sans:wght@300;400;500&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">\n'
    + head_content + '\n</head>\n<body>\n'
    + body_html.rstrip()
    + '\n<script>\n' + script_content + '\n</script>\n'
    '</body>\n</html>')

# Write to correct location
out = 'app/templates/student/portal.html'
with open(out, 'w', encoding='utf-8') as f:
    f.write(portal)

print('Written:', len(portal), 'bytes')
print('Script tags:', portal.count('<script>'))
print('showTab:', "showTab('home')" in portal)
print('fetch /student/api/me:', "fetch('/student/api/me'" in portal)
print('window.showTab:', 'window.showTab=showTab' in portal)
print('renderThink:', 'function renderThink' in portal)
print('Last 80 chars:', repr(portal[-80:]))
print('DONE - now run: git add -f app/templates/student/portal.html && git commit -m "Complete portal rebuild" && git push origin main')
