with open('app/templates/student/portal.html', 'r', encoding='utf-8') as f:
    portal = f.read()

print('Current size:', len(portal))

# Replace the complex Jinja2 block with a simpler version
old_jinja = '''<script>
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

new_jinja = '''<script>
window.HS_USER = {
  id: {{ user.id }},
  name: {{ user.full_name | tojson }},
  grade: {{ user.grade or 7 }},
  school: {{ (user.school or 'F.D. Moon Middle School') | tojson }},
  xp: {{ user.xp or 0 }},
  cluster: {{ user.cluster | tojson if user.cluster else 'null' }},
  role: {{ user.role | tojson }}
};
window.HS_PROGRESS = {
  pre_done: {{ (progress.pre_done if progress else False) | tojson }},
  money_mod: {{ progress.money_mod if progress else 0 }},
  think_q: {{ progress.think_q if progress else 0 }},
  story_done: {{ (progress.story_done if progress else False) | tojson }},
  ai_mod: {{ progress.ai_mod if progress else 0 }},
  eng_done: {{ (progress.eng_done if progress else False) | tojson }},
  career_sparks_done: {{ (progress.career_sparks_done if progress else False) | tojson }},
  reflections: {{ (progress.reflections or {}) | tojson if progress else '{}' }}
};
</script>'''

if old_jinja in portal:
    portal = portal.replace(old_jinja, new_jinja)
    print('Jinja2 block replaced')
else:
    print('Old jinja block not found - checking what is there')
    idx = portal.find('window.HS_USER')
    if idx > 0:
        print('HS_USER context:', repr(portal[idx:idx+300]))
    else:
        print('HS_USER not found at all')

with open('app/templates/student/portal.html', 'w', encoding='utf-8') as f:
    f.write(portal)

print('Done, size:', len(portal))
