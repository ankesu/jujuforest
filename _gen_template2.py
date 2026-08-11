# -*- coding: utf-8 -*-
"""重新生成 template.html：全组件使用说明书（基础+教学+审讯室+花边 26 组件）"""
import os, re

WS = r'C:/Users/MIAMIA/WorkBuddy/猫猫捡来的包子/森林小报-NexaPress换皮'
s = open(os.path.join(WS, 'a105.html'), encoding='utf-8').read()

# ===== 补 .q-card .by =====
old = '.q-card { background:#fff; border-left:4px solid #c8aef0; border-radius:0 14px 14px 0; padding:14px 18px; font-size:14.5px; font-weight:600; color:#3a3a42; line-height:1.8; box-shadow:0 4px 18px rgba(30,30,60,.04); }'
new = old + '\n        .q-card .by { display:block; margin-top:6px; font-size:12px; color:#8a8a96; font-weight:400; }'
assert old in s
s = s.replace(old, new)

# ===== title / 头图 / trending / meta =====
s = s.replace('<title>🎬 表白现场座位表：你以为的二人世界，其实是七机位片场 · 橘橘森林八卦小报</title>',
              '<title>🧾 内页模板使用说明书 组件示例即注意事项 · 橘橘森林八卦小报</title>')
s = s.replace('<img class="blog-card-bg" src="images/hengka_105.webp" alt="a105">',
              '<img class="blog-card-bg" src="images/hengka_107.webp" alt="模板">')
# trending → 模板导航（容器整体替换）
def extract_container(html, marker):
    i = html.find(marker)
    j = html.rfind('<div', 0, i)
    depth, k = 0, j
    while k < len(html):
        if html.startswith('<div', k): depth += 1; k += 4
        elif html.startswith('</div>', k): depth -= 1; k += 6
        else: k += 1
        if depth == 0: break
    return html[j:k], j, k
def nav_row(img, cat, title):
    return ('<div class="border-bottom-row">\n'
            '                                <div class="right-side">\n'
            '                                    <div class="trending-post-thum trending-post-thum-1">\n'
            f'                                        <img src="images/{img}" alt="trending-post">\n'
            '                                    </div>\n'
            '                                </div>\n'
            '                                <div class="left-side">\n'
            f'                                    <div class="category mb-2">{cat}</div>\n'
            '                                    <div class="trending-post-right">\n'
            '                                        <a href="javascript:void(0)">\n'
            f'                                            <h4 class="h5">{title}</h4>\n'
            '                                        </a>\n'
            '                                    </div>\n'
            '                                </div>\n'
            '                            </div>')
new_tr = ('<div class="trending-post in-sidebar fade-animation show">\n'
          '                            <h4>Trending Post</h4>\n'
          + nav_row('hengka_107.webp', '📦 模板', '🧾 组件速查：26 件套四分类（基础/教学/审讯室/花边）')
          + nav_row('hengka_106.webp', '📦 模板', '🖼️ 素材规格：头图 hengka_N / 作者狐图 / 分类猫图')
          + nav_row('hengka_105.webp', '📦 模板', '📏 样式规范：foot 左对齐 16px / 标题禁冒号后换行')
          + '\n                        </div>')
old_tr, tj, tk = extract_container(s, 'trending-post in-sidebar')
s = s[:tj] + new_tr + s[tk:]
# meta 行
s = s.replace('<div class="category">🌸 花边</div>', '<div class="category">📦 其他</div>', 1)
s = s.replace('<img alt="Kimi" src="images/fox_Kimi.webp">', '<img alt="DeepSeek" src="images/fox_DSV4.webp">', 1)
s = s.replace('🦊 Kimi', '🦊 DeepSeek', 1)
s = s.replace('<h2>🎬 表白现场座位表：你以为的二人世界，其实是七机位片场</h2>',
              '<h2>🧾 内页模板使用说明书 组件示例即注意事项</h2>')
# short-description 容器整体替换为引导语
sd_m = re.search(r'<div class="short-description">.*?</div>', s, re.S)
assert sd_m, 'short-description 未找到'
s = s.replace(sd_m.group(0), '<div class="short-description"><p>使用时复制本文件改名，按写作内容的需要来选择合适的模块，逐块替换。每个组件示例的正文 = 该组件的使用注意事项。</p></div>')

# ===== 正文：全组件教学 =====
start = s.find('<div class="single-blog-content">')
end = s.find('<!-- Tags（模板件） -->')
assert start != -1 and end != -1

BODY = '''<div class="single-blog-content">

                            <div class="tape">📦 模板使用 · 组件说明 <b>| 使用方法</b>：复制本文件改名 → 按内容需求挑组件 → 逐块替换示例文本。组件 CSS 已全部内置，删掉没用到的也不影响。</div>

                            <div class="card-x">
                                <div class="paw">🐾</div>
                                <p><b>一页看懂全部组件。</b>本模板按「基础 / 教学 / 审讯室 / 花边」四大类排列，每个组件的示例内容就是它的写法说明。正文区共 <b>26 个组件</b>：基础 8 + 教学 5 + 审讯室 5 + 花边 8。挑你要的抄，没用的组件直接删。</p>
                            </div>

                            <div class="sec-title">📦 一、基础组件 <small>所有文章通用 · 08-11 定稿</small></div>

                            <div class="card-x">
                                <div class="paw">🐾</div>
                                <p><b>tape 登记条</b>：文章类型登记行。写法 <b>&lt;div class="tape"&gt;🔵 教学 · 深夜食堂特辑 &lt;b&gt;💗 马卡龙限定&lt;/b&gt;&lt;/div&gt;</b>。&lt;b&gt; 里写分类强调词，放正文最顶部。</p>
                            </div>
                            <div class="card-x">
                                <div class="paw">🐾</div>
                                <p><b>card-x 引言卡</b>：白卡 + 右下 🐾 水印。段落用 &lt;p&gt;，重点用 &lt;b&gt;，术语用 <span class="gloss" data-tip="这就是活例句：data-tip 写悬停文案，猫话放最后，禁嵌套 HTML">gloss</span>。90% 的段落内容都用它装。</p>
                            </div>
                            <div class="sec-title">✏️ sec-title 章节标题 <small>紫左边条 + 渐变背景</small></div>
                            <div class="card-x">
                                <div class="paw">🐾</div>
                                <p>写法：<b>&lt;div class="sec-title"&gt;🍰 标题文字 &lt;small&gt;补充说明&lt;/small&gt;&lt;/div&gt;</b>。每个章节前必放，&lt;small&gt; 放英文缩写或注释。</p>
                            </div>
                            <div class="sec-title">📋 bill-table 数据表 <small>账目 / 对照 / 卷宗</small></div>
                            <table class="bill-table">
                                <tr><th>组件</th><th>语义色</th><th>说明</th></tr>
                                <tr><td>th 表头</td><td>渐变粉紫</td><td>首行 th 自动渐变 + 加粗</td></tr>
                                <tr><td>td 首列</td><td class="free">绿色 .free</td><td>首列自动加粗；免费/放行用 .free</td></tr>
                                <tr><td>td 其他</td><td class="bill">橙色 .bill</td><td>计费/贴条用 .bill；审讯室表格行可加 r-y/r-n/r-new</td></tr>
                            </table>
                            <div class="sec-title">💬 quotes 金句墙 <small>紫边白卡 · 可带署名</small></div>
                            <div class="quotes">
                                <div class="q-card">「金句 = 主题浓缩。每条一句 .q-card。」<span class="by">—— 署名用 .by，可选</span></div>
                            </div>
                            <div class="note-x">
                                <div class="paw">🐾</div>
                                <b>📎 note-x 编辑部锐评：</b>固定格式 &lt;b&gt;📎 编辑部锐评：&lt;/b&gt; 开头 + 毒舌总结。放金句墙之后、Tags 之前。
                            </div>
                            <div class="sec-title">🏷️ tags 标签 <small>模板件</small></div>
                            <div class="card-x">
                                <div class="paw">🐾</div>
                                <p>&lt;div class="tags"&gt; 内 &lt;ul&gt;&lt;li&gt;&lt;a&gt; 每篇按 tags 数组生成（转换脚本自动做）。</p>
                            </div>

                            <div class="sec-title">🧮 二、教学组件 <small>a107 贝叶斯篇新增 · 论文/教学文用</small></div>
                            <div class="formula-card">
                                <div class="formula">
                                    P(A | B) = <span class="frac"><span class="top">P(B | A) × P(A)</span><span class="line"></span><span class="bot">P(B)</span></span>
                                </div>
                            </div>
                            <div class="formula-note">formula-card 公式卡：白卡居中，分数用 .frac 三层（top/line/bot），下方 .formula-note 写变量说明。</div>
                            <div class="piece-grid">
                                <div class="piece p-b-sun"><span class="tag">PRIOR</span><h4>🍰 piece-grid</h4><p>四件套 2×2：p-b-sun 金 / p-b-mint 绿 / p-b-pink 粉 / p-b-lav 紫。</p><p class="miao">猫话：.tag 英文缩写 + .miao 猫话</p></div>
                                <div class="piece p-b-mint"><span class="tag">LIKELY</span><h4>🍬 何时用</h4><p>并列概念拆解（贝叶斯四件套/博弈要素）。</p><p class="miao">猫话：并排对比就用它</p></div>
                                <div class="piece p-b-pink"><span class="tag">EVID.</span><h4>🍓 结构</h4><p>.tag → h4 → p → .miao 四层，内容别超 4 行。</p><p class="miao">猫话：卡就是卡</p></div>
                                <div class="piece p-b-lav"><span class="tag">POST.</span><h4>🍮 坑</h4><p>移动端自动 1 列；别塞表格/滑块。</p><p class="miao">猫话：别当仓库</p></div>
                            </div>
                            <div class="demo-card">
                                <h4>demo-card 互动卡：白卡绿边框 + 滑块 + 实时结果。</h4>
                                <p class="case">滑块 id（prior/likeli）必须和 &lt;/body&gt; 前 JS 的 getElementById 一致；.verdict-mini 显示结果。</p>
                                <div class="ctl"><label>🍰 示例滑块 <b id="vPrior">50%</b></label><input type="range" id="prior" min="5" max="95" value="50"></div>
                                <div class="bar-row"><span class="lb">先验</span><div class="bar"><div class="fill" id="barPrior" style="background:#b9bcc9;width:50%"></div></div><b id="nPrior">50%</b></div>
                                <div class="arrow">💡 观察到新证据 ↓</div>
                                <div class="bar-row"><span class="lb">后验</span><div class="bar"><div class="fill" id="barPost" style="background:linear-gradient(90deg,#ff9db5,#c8aef0);width:50%"></div></div><b id="nPost">50%</b></div>
                                <div class="verdict-mini" id="verdict">JS 更新这里</div>
                            </div>
                            <div class="work-grid">
                                <div class="mini"><div class="ico">📧</div><h4>work-grid</h4><p>三工位 3 列：.ico emoji + h4 + p。</p><div class="form">.form 放公式</div></div>
                                <div class="mini"><div class="ico">🏥</div><h4>何时用</h4><p>「三个场景/三种工位」三分结构。</p><div class="form">P(场景 | 组件)</div></div>
                                <div class="mini"><div class="ico">🎮</div><h4>坑</h4><p>移动端 1 列；别塞长文。</p><div class="form">min-height</div></div>
                            </div>
                            <details class="quiz">
                                <summary>quiz 随堂小考怎么写？</summary>
                                <div class="opt">A. 随便 div<br>B. <b>details.quiz + summary 题目 + .opt 选项 + .ans 答案</b><br>C. 跳过</div>
                                <div class="ans">✅ B。正确答案在 .opt 用 &lt;b&gt; 标（自动粉 #ff6b96），.ans 以 ✅ 开头。</div>
                            </details>

                            <div class="sec-title">🔴 三、审讯室组件 <small>a106 温度案新增 · 场景/证物/供词</small></div>
                            <div class="scene-x">
                                <p><b>scene-x 场景卡</b>：白卡装审讯场景/对话。对话行加 <b>.dialogue-x</b>（红左条），说话人用 <b>.who-q</b>（主审橙）/.who（被告红）：</p>
                                <p class="dialogue-x"><span class="who-q">主审橘橘：</span>「交代吧。」</p>
                                <p class="dialogue-x"><span class="who">红毛：</span>「……我招。」</p>
                            </div>
                            <div class="evi-card">
                                <div class="evi-head"><span class="evi-tag">证物 ①</span> evi-card 证物卡：红边卡 + 标签头 + 正文</div>
                                <div class="evi-body">
                                    <p>evi-head 里放 <b>.evi-tag</b>（红标签）+ 标题；evi-body 正文，<b>&lt;b&gt;</b> 自动红。</p>
                                    <div class="quote-x">quote-x 引用块：金左条 + 淡黄底，引用证词/文档。<span class="src">—— .src 写来源</span></div>
                                </div>
                            </div>
                            <div class="confess-x">
                                <div class="who">confess-x 供词卡（橙渐变卡）</div>
                                <p>.who 标签写供述人；正文 &lt;p&gt;，<b>&lt;b&gt;</b> 自动红。放「当庭供述/终极供词」。</p>
                            </div>
                            <div class="list-x">
                                <div><span class="no">①</span> <span><b>list-x 编号列表</b>：红编号 + 虚线分隔，放「两条命门/三条铁律」。</span></div>
                                <div><span class="no">②</span> <span>每行 div 结构：&lt;span class="no"&gt;编号&lt;/span&gt; + &lt;span&gt;内容&lt;/span&gt;。</span></div>
                            </div>

                            <div class="sec-title">🌸 四、花边组件 <small>a104/a105 新增 · 对话/座位/语录</small></div>
                            <div class="dialog-x">
                                <p><b>dialog-x 对话卡</b>（白卡）：说话人用 <b>.cat</b>（橘粉）/ .fox（青）/ .crew（灰旁白）。</p>
                                <p><span class="cat">橘橘：</span>「你到底爱不爱我？」</p>
                                <p><span class="fox">红毛：</span>「爱。」</p>
                                <p><span class="crew">——画面外同期声——</span></p>
                            </div>
                            <div class="bub-x b-fox"><p class="who">bub-x 气泡对话（fox 青 / cat 红）</p><div class="bub">「.who 写说话人，.bub 写内容——聊天气泡风。」</div></div>
                            <div class="bub-x b-cat"><p class="who">橘橘🐱（拍桌）</p><div class="bub">「那为什么有的盖有的不盖？」</div></div>
                            <div class="seat-map">
                                <div class="stage">▲ seat-map 座位表：stage 舞台行 + seats 网格 + seat 卡 ▲</div>
                                <div class="seats">
                                    <div class="seat vip"><span class="no">1号位</span><div class="role">🦊 seat.vip 主角位</div><div class="job">.no 编号徽章 + .role 角色名 + .job 职责说明；vip 位粉色渐变。</div></div>
                                    <div class="seat"><span class="no">2号位</span><div class="role">📁 普通位</div><div class="job">2×2 网格自动排，移动端变 1 列。</div></div>
                                </div>
                            </div>
                            <div class="punch-x">
                                <div class="big">punch-x 金句卡：居中大字 + 粉绿渐变底。<br><b>&lt;b&gt; 自动红，收尾炸点专用。</b></div>
                            </div>
                            <div class="notebox-x">
                                <b>notebox-x 语录盒</b>（黄虚线）：放主编语录/实操指南。「💡 提示：……」
                            </div>
                            <div class="reveal-x">
                                <div class="big">reveal-x 大揭示卡：同 punch 样式，<br><b>放「三态档案/终极结论」这类大揭秘。</b></div>
                            </div>
                            <div class="cotcard-x">
                                <span class="lbl">cotcard-x 笑料卡（办公室速记）</span>
                                <p>.lbl 标签 + 段落。放「本场最佳笑料/幕后彩蛋」——审讯之外的人味。</p>
                            </div>
                            <div class="errata-x">
                                <span class="lbl">📌 errata-x 修订记录</span>
                                <p>v1「xxx」——被反例击穿，作废。<br>v2「xxx」——成立，保留。<br>编辑部规矩：事实比面子大。</p>
                            </div>

                        </div>'''

s = s[:start] + BODY + s[end:]

# ===== Tags =====
old_tags = re.search(r'<div class="tags">.*?</div>\s*</div>', s, re.S)
new_tags = '''<div class="tags">
                                <h3>Tags:</h3>
                                <ul>
                                    <li><a href="javascript:void(0)">模板</a></li>
                                    <li><a href="javascript:void(0)">内页</a></li>
                                    <li><a href="javascript:void(0)">组件</a></li>
                                    <li><a href="javascript:void(0)">使用说明书</a></li>
                                </ul>
                            </div>'''
if old_tags:
    s = s[:old_tags.start()] + new_tags + s[old_tags.end():]

# ===== 页脚（引导式，防照抄） =====
old_sign = '出品：<b>Kimi🦊纯黑色蓝狐</b>（侦探 · 编制外）｜ 2026-08-10'
assert old_sign in s, 'foot 署名未匹配'
s = s.replace(old_sign, '主笔：<b>DeepSeek🦊红毛藏狐</b>（深夜食堂主厨 · 破折号狂魔）｜ 出品：臭猫🐱王霸帝')
src_m = re.search(r'<div class="src">.*?</div>', s, re.S)
if src_m:
    s = s.replace(src_m.group(0), '<div class="src">这里填写各种补充信息，例如样式来源：NexaPress 模板（home-page-4/5 + standard-post）· 本模板即使用说明书，复制改名即可开工——注意 DeepSeek 的位置要改为你自己的狐名和信息</div>')

open(os.path.join(WS, 'template.html'), 'w', encoding='utf-8').write(s)
print('template.html v2 生成:', os.path.getsize(os.path.join(WS, 'template.html'))//1024, 'KB')
