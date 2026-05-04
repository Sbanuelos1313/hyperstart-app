{% extends "base.html" %}
{% block title %}HyperStart{% endblock %}
{% block extra_styles %}
<style>
body{display:flex;flex-direction:column;min-height:100vh;align-items:center;justify-content:center;padding:40px 20px;text-align:center;}
body::before{content:'';position:fixed;inset:0;background:radial-gradient(ellipse 60% 50% at 50% 0%,rgba(245,200,66,0.06),transparent 60%);pointer-events:none;}
.hero{max-width:560px;position:relative;z-index:1;}
.hero-logo{margin:0 auto 20px;}
.hero-title{font-family:'Bricolage Grotesque',sans-serif;font-size:clamp(36px,8vw,56px);font-weight:800;line-height:1.1;margin-bottom:12px;}
.hero-title span{color:var(--gold);}
.hero-sub{font-size:16px;color:var(--muted);line-height:1.65;margin-bottom:32px;max-width:420px;margin-left:auto;margin-right:auto;}
.pills{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-bottom:32px;}
.pill{padding:6px 14px;border-radius:20px;font-size:12px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;}
.p-teal{background:var(--teal-d);color:var(--teal);border:1px solid rgba(45,212,191,.3);}
.p-gold{background:var(--gold-d);color:var(--gold);border:1px solid rgba(245,200,66,.3);}
.p-violet{background:var(--violet-d);color:var(--violet);border:1px solid rgba(167,139,250,.3);}
.cta-row{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;}
</style>
{% endblock %}
{% block body %}
<div class="hero">
  <svg class="hero-logo" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="72" height="72">
    <rect width="100" height="100" rx="22" fill="#111827"/>
    <rect width="100" height="100" rx="22" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="2"/>
    <rect x="16" y="18" width="21" height="64" rx="10" fill="#5b8ecf"/>
    <rect x="63" y="18" width="21" height="64" rx="10" fill="#9b6a7a"/>
    <rect x="16" y="40" width="68" height="20" rx="10" fill="#f5c842"/>
  </svg>
  <div class="hero-title">Hyper<span>Start</span></div>
  <div class="hero-sub">
    STEM/STEAM career pathways for grades 6–8.<br>
    Discover your match. Build real skills. See your future.
  </div>
  <div class="pills">
    <span class="pill p-teal">Northeast OKC</span>
    <span class="pill p-gold">Millwood</span>
    <span class="pill p-teal">F.D. Moon</span>
    <span class="pill p-violet">Classen SAS</span>
    <span class="pill p-gold">2026–27</span>
  </div>
  <div class="cta-row">
    <a href="/login" class="btn btn-gold" style="font-size:16px;padding:14px 32px">Start My Journey →</a>
    <a href="/admin/dashboard" class="btn btn-out">Admin Dashboard</a>
  </div>
</div>
{% endblock %}
