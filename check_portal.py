
# This script writes the full portal template directly into the repo
# Run from: C:\dev\ChronosAI\hyperstart-app-fresh

import urllib.request, os

# Read the portal template we built
portal_url = "https://raw.githubusercontent.com/Sbanuelos1313/hyperstart-app/main/app/templates/student/portal.html"

# We'll build it from scratch here
styles = """<style>
:root{--bg:#0a0e1a;--surf:#111827;--surf2:#1a2235;--border:rgba(255,255,255,0.07);--border-hi:rgba(255,255,255,0.14);--gold:#f5c842;--gold-d:rgba(245,200,66,0.1);--teal:#2dd4bf;--teal-d:rgba(45,212,191,0.1);--violet:#a78bfa;--violet-d:rgba(167,139,250,0.1);--coral:#fb7185;--coral-d:rgba(251,113,133,0.1);--green:#4ade80;--green-d:rgba(74,222,128,0.1);--amber:#fb923c;--text:#f0f4ff;--muted:#8b95b0;--r:14px;--r-sm:8px}
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'DM Sans',sans-serif;background:var(--bg);color:var(--text);min-height:100vh;font-size:15px;overflow:hidden;}
</style>"""

# The full portal is too large to write inline - let's just fix the init section
# by reading the current portal and patching it

try:
    with open('app/templates/student/portal.html', 'r', encoding='utf-8') as f:
        portal = f.read()
    print('Current portal size:', len(portal))
    
    # Check if HS_USER injection is present
    if 'window.HS_USER' in portal:
        print('HS_USER already present')
    else:
        print('HS_USER NOT present - need to add')
    
    # Check what init looks like
    idx = portal.rfind("showTab('home')")
    if idx > 0:
        print('showTab home at:', idx)
        print('Context:', repr(portal[max(0,idx-300):idx+20]))
    else:
        print('showTab home NOT found')
        
except Exception as e:
    print('Error:', e)
