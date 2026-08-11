# -*- coding: utf-8 -*-
"""
通用转换器：深色明文 → 亮色新内页
用法: python _convert.py a105 a104 ...
流程: 元数据(articles.json) + 源文(明文HTML存档) → 组件映射管道 → 套骨架 → aN.html + 登记
组件管道规则可扩展：改 RULES / 组件 CSS / 特判函数即可。
"""
import os, re, sys, json

WS = r'C:/Users/MIAMIA/WorkBuddy/猫猫捡来的包子/森林小报-NexaPress换皮'
ARCHIVE = r'C:/Users/MIAMIA/WorkBuddy/八卦小报森林编辑部/明文HTML存档'
SHELL = os.path.join(WS, 'a107.html')   # 骨架（基础+教学组件 CSS）
ARTS_JSON = r'C:/Users/MIAMIA/.workbuddy/skills/miaowu-forestnewspaper/articles.json'

# ---------- 元数据 ----------
ARTS = json.load(open(ARTS_JSON, encoding='utf-8'))['articles']
META = {a['id']: a for a in ARTS}

# 源文文件名映射（新增文章在此登记）
ART_SRC = {
    'a106': '审讯室：红毛狐狸的尾巴是热乎乎的吗？.html',
    'a105': '表白现场座位表：你以为的二人世界，其实是七机位片场.html',
    'a104': '震惊！深夜食堂的章，居然只认「正经」不认「真心」.html',
}

AUTHOR_FOX = {'DeepSeek': 'fox_DSV4.webp', 'Hy': 'fox_Hy.webp', 'GLM': 'fox_GLM.webp',
              'Kimi': 'fox_Kimi.webp', 'MiniMax': 'fox_MiniMax.webp', 'Qwen': 'fox_Qwen.webp',
              'Doubao': 'fox_Doubao.webp', 'Others': 'fox_其他.webp'}
AUTHOR_EMOJI = {'DeepSeek': '🦊', 'Hy': '🦊', 'GLM': '🦌', 'Kimi': '🦊',
                'MiniMax': '🦊', 'Qwen': '🦭', 'Doubao': '🦊', 'Others': '🪶'}

# ---------- 新增组件 CSS（审讯室 + 花边全套） ----------
COMPONENT_CSS = '''
        /* ===== 审讯室组件（a106） ===== */
        .scene-x { background:#fff; border:1px solid #ececf2; border-radius:16px; padding:22px 26px; font-size:15px; margin:16px 0; position:relative; box-shadow:0 4px 18px rgba(30,30,60,.04); line-height:1.9; color:#3a3a42; }
        .scene-x p { margin-bottom:12px; }
        .scene-x p:last-child { margin-bottom:0; }
        .dialogue-x { border-left:3px solid #e05252; padding-left:14px; margin:14px 0; }
        .dialogue-x .who-q { font-weight:800; color:#e8843d; }
        .dialogue-x .who { font-weight:800; color:#e05252; }
        .evi-card { background:#fff; border:1px solid #f0c4c0; border-radius:16px; margin:18px 0; overflow:hidden; box-shadow:0 4px 18px rgba(30,30,60,.04); }
        .evi-head { display:flex; align-items:center; gap:10px; background:linear-gradient(90deg, rgba(224,82,82,.08), rgba(224,82,82,.02)); padding:10px 18px; font-size:14px; font-weight:700; color:#1d1d1d; border-bottom:1px solid #f0e0de; }
        .evi-tag { background:#e05252; color:#fff; font-size:11px; font-weight:800; padding:2px 10px; border-radius:99px; letter-spacing:1px; flex-shrink:0; }
        .evi-body { padding:16px 18px; font-size:14.5px; color:#3a3a42; line-height:1.9; }
        .evi-body p { margin-bottom:10px; }
        .evi-body p:last-child { margin-bottom:0; }
        .evi-body b { color:#e05252; }
        .quote-x { border-left:3px solid #e0b73c; background:rgba(245,197,66,.06); padding:10px 14px; border-radius:0 8px 8px 0; margin:10px 0; font-size:14px; color:#3a3a42; line-height:1.8; }
        .quote-x .src { display:block; margin-top:6px; font-size:12px; color:#8a8a96; }
        .confess-x { background:linear-gradient(160deg, #fff9f4, #fdf6ff); border:1px solid #f0b27a; border-radius:16px; padding:18px 22px; margin:16px 0; font-size:14.5px; color:#3a3a42; line-height:1.9; box-shadow:0 4px 18px rgba(30,30,60,.04); }
        .confess-x .who { font-size:12px; color:#e8843d; letter-spacing:2px; margin-bottom:8px; font-weight:800; }
        .confess-x b { color:#e05252; }
        .confess-x p { margin-bottom:10px; }
        .confess-x p:last-child { margin-bottom:0; }
        .list-x { margin:10px 0 10px 4px; }
        .list-x div { display:flex; gap:10px; padding:8px 0; border-bottom:1px dashed #ececf2; font-size:14.5px; color:#3a3a42; line-height:1.8; }
        .list-x div:last-child { border-bottom:none; }
        .list-x .no { color:#e05252; font-weight:800; flex-shrink:0; }
        .list-x b { color:#e8843d; }

        /* ===== 花边组件（a105/a104） ===== */
        .dialog-x { background:#fff; border:1px solid #ececf2; border-radius:12px; padding:4px 18px; margin:16px 0; box-shadow:0 4px 18px rgba(30,30,60,.04); }
        .dialog-x p { margin:10px 0; font-size:15px; line-height:1.8; }
        .dialog-x .cat { color:#c2547e; font-weight:700; }
        .dialog-x .fox { color:#2f8f86; font-weight:700; }
        .dialog-x .crew { color:#8a8a96; font-size:13.5px; }
        .bub-x { background:#fff; border-radius:12px; padding:12px 16px; margin:12px 0; border:1px solid #ececf2; box-shadow:0 4px 18px rgba(30,30,60,.04); }
        .bub-x .who { font-weight:800; margin-bottom:6px; }
        .bub-x.b-fox .who { color:#2f8f86; }
        .bub-x.b-cat .who { color:#e05252; }
        .bub-x .bub { font-size:15px; color:#3a3a42; line-height:1.8; }
        .seat-map { background:linear-gradient(160deg, #fff8fc, #f3fbf8); border:1px solid #f2e2ef; border-radius:14px; padding:18px 18px 10px; margin:18px 0; }
        .seat-map .stage { text-align:center; font-size:13px; letter-spacing:3px; color:#8a8a96; border:1px dashed #e8b9d4; border-radius:99px; padding:6px 10px; margin:0 24px 16px; background:#fff; }
        .seat-map .seats { display:grid; grid-template-columns:1fr 1fr; gap:12px; }
        .seat { background:#fff; border:1px solid #f2e2ef; border-radius:10px; padding:12px 14px; font-size:14px; position:relative; }
        .seat .no { position:absolute; top:-9px; left:12px; background:linear-gradient(135deg,#ff8fb8,#b9a6ef); color:#fff; font-size:11px; font-weight:800; border-radius:99px; padding:1px 9px; letter-spacing:1px; }
        .seat .role { font-weight:800; color:#4a3f6b; }
        .seat .job { color:#8a8a96; font-size:13px; margin-top:2px; line-height:1.6; }
        .seat.vip { background:linear-gradient(135deg,#fff0f6,#fdeeff); border-color:#f0bcd6; }
        .seat.vip .no { background:linear-gradient(135deg,#e64545,#ff8fb8); }
        .punch-x { margin:22px 0; padding:20px 24px; border-radius:12px; background:linear-gradient(135deg,#fff2f7,#eefaf6); border:1px solid #f2e2ef; text-align:center; }
        .punch-x .big { font-family:"Noto Serif SC","Songti SC",serif; font-size:19px; font-weight:700; color:#2f2a3d; line-height:1.75; }
        .punch-x .big b { color:#e64545; }
        .notebox-x { background:#fffdf2; border:1px dashed #f0c86e; border-radius:10px; padding:13px 18px; font-size:14.5px; margin:16px 0; color:#3a3a42; line-height:1.9; }
        .reveal-x { margin:20px 0; padding:20px 24px; border-radius:12px; background:linear-gradient(135deg,#fff2f7,#eefaf6); border:1px solid #f2e2ef; text-align:center; }
        .reveal-x .big { font-family:"Noto Serif SC","Songti SC",serif; font-size:19px; font-weight:700; color:#2f2a3d; line-height:1.75; }
        .reveal-x .big b { color:#e64545; }
        .cotcard-x { background:#fff; border:1px solid #ececf2; border-radius:14px; padding:16px 20px; margin:16px 0; box-shadow:0 4px 18px rgba(30,30,60,.04); }
        .cotcard-x .lbl { font-size:12px; color:#e8843d; letter-spacing:2px; font-weight:800; margin-bottom:8px; display:block; }
        .cotcard-x p { font-size:14.5px; color:#3a3a42; line-height:1.9; margin-bottom:10px; }
        .cotcard-x p:last-child { margin-bottom:0; }
        .errata-x { background:#fdf0f5; border:1px solid #f2c4d8; border-radius:10px; padding:14px 18px; margin:18px 0; font-size:14px; color:#3a3a42; line-height:1.9; }
        .errata-x .lbl { font-size:12px; color:#e64545; letter-spacing:2px; font-weight:700; display:block; margin-bottom:6px; }
        .bill-table .r-y td { background:rgba(255,214,120,.10); }
        .bill-table .r-n td { background:rgba(120,220,170,.08); }
        .bill-table .r-new td { background:rgba(160,130,240,.08); }
        .bill-table td.y { color:#d97b1c; font-weight:700; }
        .bill-table td.n { color:#2e9e5b; font-weight:700; }
        @media (max-width:600px){ .seat-map .seats { grid-template-columns:1fr; } }
'''

# ---------- 通用翻译管道 ----------
def wrap_top_level_ps(html):
    """把层级 0（不在任何 div 容器内）的连续 <p> 序列包进 card-x"""
    tokens = re.split(r'(<div\b[^>]*>|</div>|<p[^>]*>.*?</p>)', html, flags=re.S)
    out, depth, buf = [], 0, []
    def flush():
        nonlocal buf
        if buf:
            card = '<div class="card-x">\n<div class="paw">🐾</div>\n' + '\n'.join(buf) + '\n</div>'
            out.append(card)
            buf = []
    for t in tokens:
        if not t:
            continue
        if t.startswith('<div'):
            flush(); depth += 1; out.append(t)
        elif t == '</div>':
            flush(); depth -= 1; out.append(t)
        elif t.startswith('<p') and depth == 0:
            buf.append(t)
        else:
            flush(); out.append(t)
    flush()
    return ''.join(out)

def translate_body(html):
    """深色 body 内容 → 亮色组件（通用规则 + 特判）"""
    # 1. 切出 .wrap 内容
    m = re.search(r'<div class="wrap">(.*?)</div>\s*</body>', html, re.S)
    body = m.group(1) if m else html

    # 2. 删报头 / 标题 / sub / meta（信息并入骨架）
    body = re.sub(r'<div class="mast">.*?</div>\s*', '', body, flags=re.S)
    body = re.sub(r'<h1>.*?</h1>\s*', '', body, flags=re.S)
    body = re.sub(r'<p class="sub">.*?</p>\s*', '', body, flags=re.S)
    body = re.sub(r'<p class="meta">.*?</p>\s*', '', body, flags=re.S)
    body = re.sub(r'<div class="hero">.*?</div>\s*', '', body, flags=re.S)
    body = re.sub(r'<span class="kicker">.*?</span>\s*', '', body, flags=re.S)
    body = re.sub(r'<div class="tape">', '<div class="tape">', body)  # 保留 tape

    # 3. 章节标题：h2.sec → sec-title
    body = re.sub(r'<h2 class="sec">.*?<span class="pip"></span>\s*', '<div class="sec-title">', body, flags=re.S)
    body = re.sub(r'</h2>', '</div>', body)

    # 4. 组件类名映射
    REPL = [
        (r'<div class="dlg fox">', '<div class="bub-x b-fox">'),
        (r'<div class="dlg cat">', '<div class="bub-x b-cat">'),
        (r'<div class="dialog">', '<div class="dialog-x">'),
        (r'<div class="set">', '<div class="seat-map">'),
        (r'<div class="seats">', '<div class="seats">'),
        (r'<div class="seat vip">', '<div class="seat vip">'),
        (r'<div class="punch">', '<div class="punch-x">'),
        (r'<div class="notebox">', '<div class="notebox-x">'),
        (r'<div class="reveal">', '<div class="reveal-x">'),
        (r'<div class="cotcard">', '<div class="cotcard-x">'),
        (r'<div class="errata">', '<div class="errata-x">'),
        (r'<div class="scene">', '<div class="scene-x">'),
        (r'<div class="confess">', '<div class="confess-x">'),
        (r'<div class="list">', '<div class="list-x">'),
        (r'<div class="quote q">', '<div class="quote-x">'),
        (r'<div class="quote good q">', '<div class="quote-x">'),
        (r'<div class="quote">', '<div class="quote-x">'),
        (r'<div class="formula">', '<div class="formula-card"><div class="formula">'),
        (r'<div class="formula-note">', '</div><div class="formula-note">'),
        (r'<div class="verdict">', '<div class="verdict">'),
        (r'<div class="quotes">', '<div class="quotes">'),
        (r'<div class="quote-card">', '<div class="q-card">'),
        (r'<div class="note">', '<div class="note-x">'),
        (r'<div class="tbl">', ''),
        (r'<div class="grid">', '<div class="piece-grid">'),
        (r'<div class="piece ', '<div class="piece '),
        (r'<table>', '<table class="bill-table">'),
        (r'<tr class="tag-n">', '<tr class="r-n">'),
        (r'<tr class="tag-y">', '<tr class="r-y">'),
        (r'<tr class="tag-new">', '<tr class="r-new">'),
        (r'<td class="n">', '<td class="n">'),
        (r'<td class="y">', '<td class="y">'),
        (r'<td class="tag-n">', '<td class="n">'),
    ]
    for pat, rep in REPL:
        body = re.sub(pat, rep, body)

    # 5. 内联 var() 颜色 / 无用属性清除
    body = re.sub(r'style="color:var\(--[a-z]+\)"', '', body)
    body = re.sub(r'<b style="color:var\(--[a-z]+\)">', '<b>', body)
    body = re.sub(r'<strong>', '<b>', body)
    body = re.sub(r'</strong>', '</b>', body)

    # 6. <p class="note"> 收尾注释 → 小灰字
    body = re.sub(r'<p class="note">', '<p style="font-size:13px;color:#8a8a96;">', body)

    # 7. 删 .foot 区块（信息进骨架页脚）
    body = re.sub(r'<div class="foot">.*?</div>\s*', '', body, flags=re.S)

    # 8. 游离段落（层级0的连续 <p>）包进 card-x，与 a108/a107 风格统一
    body = wrap_top_level_ps(body)

    # 9. 收尾：空行清理
    body = re.sub(r'\n{3,}', '\n\n', body)
    return body.strip()

def date_val(a):
    d = re.match(r'(\d+)月(\d+)日', a['date'])
    hm = re.search(r'(\d+):(\d+)', a['date'])
    v = 0
    if d: v = int(d.group(1))*100000 + int(d.group(2))*1000
    if hm: v += int(hm.group(1))*10 + int(hm.group(2))
    return v

def build_article(aid):
    a = META[aid]
    src_path = os.path.join(ARCHIVE, ART_SRC[aid])
    src = open(src_path, encoding='utf-8').read()
    body_html = translate_body(src)

    # Trending：最新3篇排除本篇
    others = sorted([x for x in ARTS if x['id'] != aid],
                    key=lambda x: (date_val(x), int(re.sub(r'\D','',x['id']) or 0)), reverse=True)[:3]

    s = open(SHELL, encoding='utf-8').read()
    # title
    s = s.replace('<title>贝叶斯全家桶：先入为主 + 吃瓜修正 · 橘橘森林八卦小报</title>',
                  f'<title>{a["title"]} · 橘橘森林八卦小报</title>')
    # 头图
    num = re.sub(r'\D', '', aid)
    s = s.replace('<img class="blog-card-bg" src="images/hengka_107.webp" alt="贝叶斯全家桶">',
                  '<img class="blog-card-bg" src="images/hengka_{}.webp" alt="{}">'.format(num, aid))
    # Trending
    old_titles = ['🧾 零成本表白欠条：红毛藏狐赡养费预支凭证', '🍗 贝叶斯全家桶：先入为主 + 吃瓜修正', '🎬 表白现场座位表：你以为的二人世界，其实是七机位片场']
    for i, t in enumerate(others):
        img = 'hengka_{}.webp'.format(re.sub(r'\D', '', t['id']))
        s = s.replace(f'<img src="images/hengka_{108 if i==0 else 107 if i==1 else 105}.webp" alt="trending-post">', '<img src="images/{}" alt="trending-post">'.format(img), 1)
        s = s.replace(old_titles[i], t['title'], 1)
        s = s.replace(f'<div class="category mb-2">{["📦 其他","🔵 教学","🌸 花边"][i]}</div>', f'<div class="category mb-2">{t["badge"]}</div>', 1)
    # meta 行
    s = s.replace('<div class="category">🔵 教学</div>', f'<div class="category">{a["badge"]}</div>', 1)
    s = s.replace('<img alt="DeepSeek" src="images/fox_DSV4.webp">', f'<img alt="{a["author"]}" src="images/{AUTHOR_FOX[a["author"]]}">', 1)
    s = s.replace('🦊 DeepSeek', f'{AUTHOR_EMOJI[a["author"]]} {a["author"]}', 1)
    s = s.replace('<h2>🍗 贝叶斯全家桶：先入为主 + 吃瓜修正</h2>', f'<h2>{a["title"]}</h2>')
    s = s.replace('<p>统计学的温柔科学——允许你先猜错，<b>只要你肯改</b> 💗</p>', f'<p>{a["desc"]}</p>')
    # 正文
    start = s.find('<div class="single-blog-content">')
    end = s.find('<!-- Tags（模板件） -->')
    body_final = f'<div class="single-blog-content">\n\n{body_html}\n\n                        </div>'
    s = s[:start] + body_final + s[end:]
    # Tags
    old_tags = re.search(r'<div class="tags">.*?</div>\s*</div>', s, re.S)
    new_tags = '<div class="tags">\n<h3>Tags:</h3>\n<ul>\n' + \
        '\n'.join(f'<li><a href="javascript:void(0)">{t}</a></li>' for t in a.get('tags', [])) + '\n</ul>\n</div>'
    if old_tags:
        s = s[:old_tags.start()] + new_tags + s[old_tags.end():]
    # 页脚（引导占位，按原文 foot 内容填入）
    s = s.replace('主笔：<b>DeepSeek🦊红毛藏狐</b>（深夜食堂主厨 · 破折号狂魔）｜ 出品：臭猫🐱王霸帝',
                  f'出品：<b>{AUTHOR_EMOJI[a["author"]]}{a["author"]}</b>（{a["badge"]}）｜ 执笔：{AUTHOR_EMOJI[a["author"]]}{a["author"]} ｜ 出品：臭猫🐱王霸帝')
    # 注入组件 CSS
    s = s.replace('</style>', COMPONENT_CSS + '</style>', 1)
    # Min Read
    text = re.sub(r'<[^>]+>', '', body_html)
    zh = len(re.findall(r'[\u4e00-\u9fff]', text))
    mins = max(1, round(zh / 450))
    s = re.sub(r'\d+ Min Read', f'{mins} Min Read', s, count=1)
    out = os.path.join(WS, f'{aid}.html')
    open(out, 'w', encoding='utf-8').write(s)
    print(f'✅ {aid} 生成: {os.path.getsize(out)//1024}KB | MinRead={mins} | 正文{zh}字 | trending={[t["id"] for t in others]}')
    return out

if __name__ == '__main__':
    ids = sys.argv[1:] or ['a105', 'a104']
    for aid in ids:
        if aid not in ART_SRC:
            print(f'⚠️ {aid} 未登记源文（加进 ART_SRC 映射）')
            continue
        build_article(aid)
