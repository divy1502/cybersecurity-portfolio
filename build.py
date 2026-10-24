#!/usr/bin/env python3
"""Build dependency-free static website from posts/*.md."""
from pathlib import Path
from datetime import date
import re, html, shutil
ROOT=Path(__file__).parent
POSTS=ROOT/'posts'
OUT=ROOT/'site'
OUT.mkdir(exist_ok=True)

def esc(s): return html.escape(str(s), quote=True)
def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
def inline(s):
 s=esc(s)
 s=re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
 s=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s)
 s=re.sub(r'\[([^\]]+)\]\((https?://[^ )]+)\)',r'<a href="\2" target="_blank" rel="noopener">\1</a>',s)
 s=re.sub(r'\[([^\]]+)\]\(([^ )]+)\)',r'<a href="\2">\1</a>',s)
 return s

def markdown(s):
 lines=s.splitlines(); o=[]; para=[]; in_code=False; code=[]; in_list=False
 def flush():
  if para: o.append('<p>'+inline(' '.join(para))+'</p>');para.clear()
 for line in lines:
  if line.startswith('```'):
   flush()
   if in_list:o.append('</ul>');in_list=False
   if in_code:o.append('<pre><code>'+esc('\n'.join(code))+'</code></pre>');code=[];in_code=False
   else:in_code=True
   continue
  if in_code:code.append(line);continue
  if not line.strip():
   flush()
   if in_list:o.append('</ul>');in_list=False
   continue
  if line.startswith('#') and re.match(r'^#{1,4} ',line):
   flush()
   if in_list:o.append('</ul>');in_list=False
   n=len(line)-len(line.lstrip('#'));o.append(f'<h{n}>{inline(line[n:].strip())}</h{n}>');continue
  if line.startswith('- '):
   flush()
   if not in_list:o.append('<ul>');in_list=True
   o.append('<li>'+inline(line[2:])+'</li>');continue
  if line.startswith('> '):
   flush();o.append('<blockquote>'+inline(line[2:])+'</blockquote>');continue
  para.append(line.strip())
 flush()
 if in_list:o.append('</ul>')
 if in_code:o.append('<pre><code>'+esc('\n'.join(code))+'</code></pre>')
 return '\n'.join(o)

def load_posts():
 result=[]
 for file in POSTS.glob('*.md'):
  txt=file.read_text(encoding='utf8')
  if not txt.startswith('---\n'):continue
  _, head, body=txt.split('---',2)
  meta={}
  for line in head.strip().splitlines():
   if ':' in line:
    k,v=line.split(':',1);meta[k.strip()]=v.strip().strip('"\'')
  if not meta.get('title') or not re.fullmatch(r'\d{4}-\d{2}-\d{2}',meta.get('date','')):continue
  if meta.get('draft','false').lower()=='true':continue
  meta.update(body=body.strip(),slug=file.stem)
  result.append(meta)
 return sorted(result,key=lambda x:(x['date'],x['slug']),reverse=True)

nav=[('index.html','home'),('journal.html','journal'),('projects.html','projects'),('detections.html','detections'),('about.html','about')]
def layout(title,body,root='',active=''):
 links=''.join(f'<a class="{"active" if label==active else ""}" href="{root+href}">{label}</a>' for href,label in nav)
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#0B0F14"><meta name="description" content="Divy Brahmbhatt — cybersecurity, software projects, and a public learning journal."><title>{esc(title)} · Divy Brahmbhatt</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet"><link rel="stylesheet" href="{root}assets/style.css"></head><body><header class="site-header"><div class="container nav"><a class="brand" href="{root}index.html">divy@portfolio:<span>~$</span></a><nav aria-label="Main navigation">{links}</nav></div></header><main>{body}</main><footer class="footer"><div class="container footer-inner"><span>© {date.today().year} Divy Brahmbhatt</span><span>build in public · <a href="{root}journal.html">read the journey →</a></span></div></footer></body></html>'''

def section_header(n,k,title,desc=''):
 return f'<div class="eyebrow">// {n} {esc(k)}</div><h2>{esc(title)}</h2>'+ (f'<p class="muted intro">{esc(desc)}</p>' if desc else '')

def postrow(p,root=''):
 return f'<a class="entry" href="{root}journal/{esc(p["slug"])}.html"><span class="entry-date">{esc(p["date"])}</span><span class="entry-main"><strong>{esc(p["title"])}</strong><small>{esc(p.get("summary",""))}</small></span><span class="tag">{esc(p.get("category","journal"))}</span><span class="entry-arrow">↗</span></a>'

posts=load_posts()
latest=posts[0] if posts else None
latest_href='journal/'+latest['slug']+'.html' if latest else 'journal.html'
latest_name=latest['title'] if latest else 'First entry coming soon'
entries=''.join(postrow(p) for p in posts[:4]) or '<p class="muted">No published posts yet. Add a Markdown file to posts/ and run build.py.</p>'
status='''<aside class="status"><div class="panel-head"><span class="green-dot"></span> status.log <span class="panel-x">— □ ×</span></div><div class="status-body"><div><span class="key">building</span><strong>OVERR1DE security scanner</strong></div><div><span class="key">studying</span><strong>CompTIA Security+ (SY0-701)</strong></div><div><span class="key">latest case file</span><strong>Public learning journal</strong></div><div><span class="key">latest entry</span><a href="'''+latest_href+'''">'''+esc(latest_name)+''' ↗</a></div></div></aside>'''
projects=[('01','OVERR1DE','Security scanner and dashboard project. Building security tooling and documenting development decisions.','https://theoverr1de.com/','building'),('02','UIProbe','Compare Figma designs with live websites and investigate visual differences.','https://uiprobe.vercel.app/','building'),('03','Detection engineering lab','A place for Windows logs, alert logic, detection rules and experiments as they are completed.','','learning')]
def project_cards():
 x=''
 for n,name,desc,url,status in projects:
  link=f'<a href="{esc(url)}" target="_blank" rel="noopener">[ visit project ↗ ]</a>' if url else '<a href="detections.html">[ follow progress → ]</a>'
  x+=f'<article class="project"><div class="project-head"><span>PROJECT-{n}</span><span class="outlined">{status}</span></div><h3>{esc(name)}</h3><p>{esc(desc)}</p><div class="project-links">{link}</div></article>'
 return x
hero=f'''<section class="hero container"><div class="hero-copy"><div class="cmd">$ whoami</div><h1>Detection engineering, documented as I build it<span class="cursor">_</span></h1><p>CS student at Rutgers building detection tooling, a web security scanner, and a homelab. Every project gets a case file: what I built, what broke, and what I would change.</p><div class="buttons"><a class="button primary" href="{latest_href}">open latest case file</a><a class="button outline" href="projects.html">ls projects/</a></div></div>{status}</section>'''
home=hero+f'''<section class="band" id="writeups"><div class="container pad">{section_header('01','writeups','What I built, what broke')}<div class="entries">{entries}</div><p class="bottom-link"><a href="journal.html">view all journal entries →</a></p></div></section><section id="projects"><div class="container pad">{section_header('02','projects','Things that run')}<div class="cards">{project_cards()}</div></div></section><section class="band" id="roadmap"><div class="container pad">{section_header('03','roadmap','Where this is going','A plan, not a promise. Updated when something changes.')}<div class="steps"><div><b>PHASE 01 · NOW</b><h3>Fundamentals and first tools</h3><p>Security+ prep, hands-on detection experiments, and regular case files.</p></div><div><b>PHASE 02 · SPRING 2027</b><h3>Graduate, then Per Scholas</h3><p>Finish the CS degree at Rutgers and start the Per Scholas program.</p></div><div><b>PHASE 03 · THE THREAD</b><h3>AI and LLM security</h3><p>Prompt injection, LLM red-teaming, securing ML pipelines. One case file in every few.</p></div></div></div></section><section id="about"><div class="container pad about-mini">{section_header('04','about',"Hi, I'm Divy.")}<p>I'm a CS student at Rutgers. I'm working on detection engineering, cybersecurity tools, and practical software projects. This site documents what I learn, what breaks, and what I change along the way. <a href="about.html">More about me →</a></p></div></section>''' 
(OUT/'index.html').write_text(layout('Home',home,active='home'),encoding='utf8')
all_entries=''.join(postrow(p) for p in posts) or '<p class="muted">Your posts will appear here once you add one.</p>'
journal=f'''<section class="container page-head"><div class="eyebrow">// JOURNAL / THE PUBLIC LOG</div><h1>Everything I learn, <span class="gold">as it happens.</span></h1><p>Progress reports, technical notes, personal reflections, mistakes, and small wins. Chronological and written in my own words.</p><div class="terminal-note">$ ls -lt posts/ <span class="faint">// {len(posts)} published entries</span></div></section><section class="container journal-list"><div class="entries">{all_entries}</div></section>'''
(OUT/'journal.html').write_text(layout('Journal',journal,active='journal'),encoding='utf8')
proj=f'''<section class="container page-head"><div class="eyebrow">// PROJECTS</div><h1>Things that <span class="gold">run.</span></h1><p>Software and security projects I work on. Status indicates direction, not a claim of production readiness.</p></section><section class="container pad"><div class="cards">{project_cards()}</div></section>'''
(OUT/'projects.html').write_text(layout('Projects',proj,active='projects'),encoding='utf8')
detections='''<section class="container page-head"><div class="eyebrow">// DETECTION CATALOG</div><h1>Every rule, tested and written up.</h1><p>A working list of the detections I write: what behavior each one catches, which logs it needs, how I tested it, and what it gets wrong. Open any row for the full case file. Items shown are planned study topics, not completed detections.</p></section><section class="container pad"><div class="catalog-head"><span>DETECTION / STUDY TOPIC</span><span>TECHNIQUE</span><span>STATUS</span></div><div class="catalog-row"><b>Encoded PowerShell commands</b><span>T1059.001</span><span class="pill">planned</span></div><div class="catalog-row"><b>LSASS memory access</b><span>T1003.001</span><span class="pill">planned</span></div><div class="catalog-row"><b>New local user creation</b><span>T1136.001</span><span class="pill">planned</span></div><div class="catalog-row"><b>Suspicious scheduled tasks</b><span>T1053.005</span><span class="pill">planned</span></div><p class="muted">When an experiment is completed, add a full case file as a Markdown post with category: detection.</p><p><a href="journal.html">read published case files →</a></p></section>'''
(OUT/'detections.html').write_text(layout('Detections',detections,active='detections'),encoding='utf8')
about='''<section class="container page-head"><div class="eyebrow">$ cat about.md</div><h1>Hi, I'm <span class="gold">Divy.</span></h1><p>I'm a Computer Science student at Rutgers University–New Brunswick, working toward graduation in December 2026. I enjoy building software and exploring the security side of technology.</p></section><section class="container pad about-page"><h2>Why this website exists</h2><p>A resume can show outcomes, but it rarely shows the thinking behind them. I want a place to record what I'm learning, what doesn't work, what I improve, and why I made certain choices. Over time, this becomes the public record of my journey.</p><h2>What I'm working toward</h2><p>I'm developing practical skills in IT, networking, security analysis, and security engineering. My projects give me a way to practice and show what I can actually build.</p><h2>Find me</h2><p><a href="https://github.com/divy1502" target="_blank" rel="noopener">GitHub ↗</a> &nbsp; · &nbsp; <a href="https://theoverr1de.com/" target="_blank" rel="noopener">OVERR1DE ↗</a></p><p class="muted">Add your LinkedIn and preferred contact email here when ready.</p></section>'''
(OUT/'about.html').write_text(layout('About',about,active='about'),encoding='utf8')
(OUT/'journal').mkdir(exist_ok=True)
for p in posts:
 article=f'''<section class="article container"><a class="back" href="../journal.html">← cd ../journal</a><div class="eyebrow">LOG / {esc(p['category'] if 'category' in p else 'journal')} / {esc(p['date'])}</div><h1>{esc(p['title'])}</h1><p class="article-summary">{esc(p.get('summary',''))}</p><div class="article-meta"><span>published: {esc(p['date'])}</span><span>category: {esc(p.get('category','journal'))}</span></div><div class="prose">{markdown(p['body'])}</div><div class="article-end"><a href="../journal.html">← all entries</a><a href="../projects.html">projects →</a></div></section>'''
 (OUT/'journal'/f'{p["slug"]}.html').write_text(layout(p['title'],article,root='../',active='journal'),encoding='utf8')
(OUT/'assets').mkdir(exist_ok=True)
shutil.copy(ROOT/'assets'/'style.css',OUT/'assets'/'style.css')
print(f'Built {len(posts)} posts into {OUT}')
