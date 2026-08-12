# 🌲 森林小报 · NexaPress 换皮工程交接文档

> 写给下一只接活的狐：本文档记录 2026-08-10 深夜换皮全过程，详细到你可以不看聊天记录直接续作。
> 有大橘（橘橘姐姐/主编）的批改意见为最高优先级，本文档次之，模板原样再次之。**别自作主张加戏**——这是本工程最贵的学费。

---

## 〇、工程概况

- **目标**：把「橘橘森林八卦小报」首页 + 文章内页，从原深色赛博风换成 NexaPress 模板亮色风。
- **规格书**：`../NexaPress换皮规格.md`（大橘 08-10 21:19 钦定终版：H5 Hero + H5 作者榜 + H4 卡片 + H4 分类 + 纯亮色）。
- **原站（只读！）**：`C:\Users\MIAMIA\WorkBuddy\八卦小报森林编辑部\` —— 可以读，**一个字节都不许改**。
- **工作间**：`C:\Users\MIAMIA\WorkBuddy\猫猫捡来的包子\`，本工程文件夹为 `橘橘森林八卦小报\`（08-12 由「森林小报-NexaPress换皮」改名）。
- **模板源**：`../html-NexaPress/`（home-page-4.html + home-page-5.html 混搭，standard-post.html 做内页）。
- **素材**：`../图片/`（129 张 webp，已拷入本工程 `images/`）。

### 文件结构

```
橘橘森林八卦小报/
├── index.html          # 首页（换皮完成 · 含加密壳）
├── a108.html           # 文章内页样机（a108 零成本表白欠条）
├── readme.md           # 本文档
├── dist/               # NexaPress 模板资源（css/js/fonts/images 原样拷贝）
├── images/             # 小报素材（webp）
│   ├── hero_bg.webp        # Hero 背景（已裁图，猫脸居左）
│   ├── hero_bg_full.webp   # Hero 原图备份（裁错了回滚用）
│   ├── fox_*.webp          # 11 张狐狐立绘（作者维度）
│   ├── cat_*.webp          # 9 张猫猫头像（分类维度，按中文名命名）
│   └── hengka_1..108.webp  # 108 张横卡风景（文章封面，id 数字直映射）
└── articles/           # 108 个 .enc 密文（AES-256-GCM，从原站拷贝）
```

---

## 一、首页怎么做的（index.html）

### 1.1 数据来源：元数据是加密的

原站首页是加密壳：文章元数据（标题/摘要/作者/分类/日期/enc文件名）存在 `index.html` 的一行 JS 变量里：

```js
var META_SALT="...", META_IV="...", META_CT="...";
```

解密方式（WebCrypto，密码 `jujuForest66`，sessionStorage 键 `julu_pwd`）：

```js
// PBKDF2(100000, SHA-256) → AES-256-GCM
crypto.subtle.importKey('raw', new TextEncoder().encode(pwd), {name:'PBKDF2'}, false, ['deriveKey'])
  .then(k => crypto.subtle.deriveKey({name:'PBKDF2', salt:b64d(salt), iterations:100000, hash:'SHA-256'},
                                     k, {name:'AES-GCM',length:256}, false, ['decrypt']))
  .then(key => crypto.subtle.decrypt({name:'AES-GCM', iv:b64d(iv)}, key, b64d(ct)))
```

每篇文章结构：`{id:'a108', date:'08月10日 16:42', author:'DeepSeek', badge:'📦 其他', bc:'box', title, desc, tags[], enc:'xxx.html.enc'}`。

**本地批量解密脚本**（Node，managed node 22 可直接跑，`crypto.subtle` 全局可用）：
- 解密元数据：从 index.html 正则提取 `META_SALT/IV/CT` → 同上流程
- 解密单篇：读 `articles/xxx.html.enc`（JSON：`{salt,iv,ct}`）→ 同上流程
- 现成参考脚本：`../.workbuddy/tmp/decrypt_meta.js`

**换皮后的 index.html 把这行 META 变量原样内嵌**（从原站 index.html 第 227 行整行抠出来注入），解锁后才渲染全部区块。

### 1.2 页面结构（从上到下 · 已按大橘四轮批改定稿）

| 区块 | 模板出处 | 内容规则 |
|------|---------|---------|
| 顶栏 navbar | H5 header | 🌲文字logo + 「分类」mega下拉(9猫图) + 「作者」下拉(8狐) + 冷色透明搜索框。**无暗色切换**（已拆 + `localStorage.removeItem('theme')`） |
| Hero | H5 `hero-section style-5` | `images/hero_bg.webp` 全宽背景（**亮色模式无蒙版**），右列白卡 slick 轮播**最新 3 篇**（徽章+时间+日期+标题+摘要+Continue Reading） |
| Explore by Author | H5 `explore-category style-5` 的 `category-type` 卡 | 8 狐立绘 + 篇数，点击=筛选该作者并滚到卡片区 |
| What's New Today | H5 `new-today` 原生三栏 | 左 story-card 大卡=最新第4篇；中 Trending 3 条（权重 red>orange>pink>其他，同类按日期新→旧）；右双横卡=**最新一天更新最多的两个分类各一篇**。三栏定高 510px 对齐 |
| Explore by Category | H4 `explore-category style-4` 的 `explore-item` 卡 | 9 猫图 + 篇数 + Explore，点击=筛选该分类并滚到卡片区 |
| Read All Blogs | H4 `blog-section style-4` + **Music & Sound 交错版** | 108 篇全量三列；每行中间列 `card-2` 翻转（文上图下 + `nebo--tr`），左右列上图下文（`nebo--br`）。计数+「✕ 清除筛选」在标题右侧 |
| 阅读窗 #rv | 原站承重墙原样 | fixed 全屏 iframe srcdoc 解密渲染，返回按钮 + Esc + 点backdrop关闭 |
| 页脚 | 模板 footer 原生风 | 品牌栏(🐾+简介+chips) + 分类(5+4两列一个标题) + 作者(4+4两列一个标题) + 底行 `© 2026 八卦小报森林编辑部` / `// v3.0 // ` |
| 锁屏 #lock | 原站承重墙·亮色系 | 米白底 + 🐾 + 密码框 + 解锁按钮；解锁后 `renderAll()` |

### 1.3 数据映射表（背下来）

```js
// 九色协议（bc → 中文名/emoji/猫图）
red=审讯室🔴 cat_审讯.webp   orange=重磅🟠 cat_重磅.webp  yellow=苦瓜🟡 cat_苦瓜.webp
green=绿闻🟢 cat_绿闻.webp   pink=花边🌸 cat_花边.webp    blue=教学🔵 cat_教学.webp
purple=论文🟣 cat_论文.webp  white=吐槽⚪ cat_吐槽.webp   box=其他📦 cat_其他.webp
// 顺序固定：red→orange→yellow→green→pink→blue→purple→white→box

// 八狐（author → 立绘）顺序固定：DeepSeek→Hy→GLM→Kimi→MiniMax→Qwen→Doubao→Others
DeepSeek=fox_DSV4.webp（V4主打，DSR1/DSV3.2 备用）  Hy=fox_Hy.webp  GLM=fox_GLM.webp（🦌）
Kimi=fox_Kimi.webp  MiniMax=fox_MiniMax.webp  Qwen=fox_Qwen.webp  Doubao=fox_Doubao.webp  Others=fox_其他.webp

// 文章封面：a N → images/hengka_N.webp（去 'a' 前缀直接映射）
```

排序：按 `date`（"08月10日 16:42" 解析成可比较数字）倒序，同刻按 id 数字倒序。

### 1.4 怎么预览首页

```bash
# 必须用本地服务器（file:// 下 fetch .enc 会被 CORS 拦）
"C:/Users/MIAMIA/.workbuddy/binaries/python/versions/3.13.12/python.exe" -m http.server 8964 --bind 127.0.0.1 --directory "C:/Users/MIAMIA/WorkBuddy/猫猫捡来的包子/橘橘森林八卦小报"
```

浏览器开 **http://127.0.0.1:8964/** → 输密码 `jujuForest66` → 解锁看全站。

⚠️ **端口坑**：后台起服务时 `cd` 可能不生效，必须用 `--directory` 显式指定；8899 端口被一台旧 Python 3.9 服务器长期占用（伺候旧站），别用。

---

## 二、内页怎么做的（a108.html）

### 2.1 版式结构（standard-post.html 套皮 · 大橘钦定）

```
┌ 顶栏：🌲logo(链回首⻚) + 「← 返回首页」按钮 ┐
├ 第一行（两栏）：                          ┤
│   左 col-lg-8：文章头图 hengka_N.webp      │
│   右 col-lg-4：Trending Post 侧栏 3 条      │
│   （与头图顶对齐；不要 Explore by Category）│
├ 第二行起（单栏拉满，与头部同宽）：          ┤
│   meta 行：作者狐头像+名 · 分类徽章 ·       │
│           X Min Read · 日期时间             │
│   标题 h2 + 一句话简介                      │
│   正文组件（亮色模板风，见 2.2）            │
│   Tags（模板原生 .tags 件）                 │
├ 页脚：                                     ┤
│   文章署名块（居中排版·透明背景·全宽）       │
│   © 2026 八卦小报森林编辑部 | // v3.0 //    │
└───────────────────────────────────────────┘
```

**铁律**：内页页脚 = 文章署名 + 版权行，**不要**站点导航页脚（品牌栏/分类/作者菜单都不放）。

### 2.2 正文组件翻译规则（深色霓虹 → 亮色模板风）

原文各篇是独立深色 HTML，组件需逐个翻译。以 a108 为例的对照表：

| 原组件（深色） | 新组件（亮色） | 要点 |
|--------------|--------------|------|
| `.tape` 胶带条 | `.tape` 亮灰底紫左边条 | 登记事项行 |
| `.hero` kicker/h1/sub | 模板 `single-blog-overly` 区 | 标题进 `post-title h2`，简介进 `short-description` |
| `.card` 引言卡 | `.card-x` 白卡 | 淡阴影 + 🐾 水印 |
| `.sec-title` 章节题 | 同款亮色 | 紫左边条渐变 |
| `.contract/.party/.clause` 合同条款 | 同名亮色版 | 壹~捌序号改马卡龙色（`.c1`~`.c8`），彩虹魂保留 |
| `table` 账目表 | `.bill-table` | 浅色 + 粉紫渐变表头 |
| `.verdict` 盖章区 | 浅紫渐变 + 红印章 `.stamp`（旋转 -7° 保留） | |
| `.note` 锐评便签 | `.note-x` 黄粉渐变虚线框 | |
| `.sign` 署名 | `.foot-sign`（**搬到页脚**） | 居中、透明、全宽 |
| `.gloss` 悬停术语注释 | 白底紫框 tooltip | `data-tip` 机制原样保留 |

**阅读时长**：正文字数 ÷ 450 字/分钟，四舍五入（a108 = 8177 字 → 18 Min Read）。

### 2.3-A 从零写一篇新内页

1. 复制 `a108.html` 改名（如 `a109.html`）。
2. 换 4 处：头图 `hengka_N.webp`、meta 行（作者狐头像/名、分类徽章、Min Read、日期）、标题+简介、正文组件内容。
3. Trending 侧栏换最新 3 篇（排除本篇）。
4. Tags 换本篇标签。
5. 页脚 `.foot-sign` 换本篇署名信息（执笔/出品/来源），版权行不动。
6. 检查：作者物种 emoji 别错（GLM 是 🦌 鹿不是狐！Others 是 🪶）。

### 2.3-B 把原有旧内页改成新内页

1. **解密旧文**：Node 脚本读 `articles/xxx.html.enc` → 解出深色明文 HTML（流程见 1.1）。
2. **抽取正文**：从明文中剥离 `<body>` 里的内容区（tape/hero/card/各组件/sign）。
3. **组件翻译**：按 2.2 对照表逐个换类名 + 亮色 CSS。`.gloss` 的 `data-tip` 原文搬。
4. **套骨架**：把翻译后的内容填进 a108.html 同款骨架（顶栏/头图行/meta行/Tags/页脚署名）。
5. **验收清单**：meta 信息对、Min Read 算过、gloss 悬停能出、页脚署名是原文信息、返回首页能点。

---

## 三、踩坑血泪史（别再踩）

1. **模板亮色模式没有 Hero 蒙版**——`:before` 黑纱是 dark-mode 专属，亮色下别加 veil。
2. **Bootstrap 的 `d-xl-block`/`d-lg-flex` 等 display 工具类带 `!important`**——会盖死你的自定义 flex。套栅格类时先检查。
3. **覆盖模板 CSS 先数选择器优先级**：模板 `.explore-category.style-5 .trending-post-thum img`（3类+元素）> 你的 2 类规则。提权就加长前缀，别急着 `!important`。
4. **模板 `mix-blend-mode: luminosity`**（Trending 缩略图自带）会把图片染成单色——换成真实图片时必须压掉。
5. **定高容器 + 子项溢出**：定高 510px 的栏里子项必须 `flex:1; min-height:0` 均分，否则内容多了直接凸出来。
6. **flex 等高别赌 `height:100%` 循环解析**——用定高锚点（如 510px）最稳。
7. **模板 `.mega-img img` 缺 `object-fit`**——竖图会被拉扁，补 `object-fit:cover`。
8. **`nebo nebo--br`/`nebo--tr` 切角遮罩类**是 H4 卡片的异形缺口灵魂，丢了就不是那味儿。
9. **Node `fs.unlinkSync` 会被安全删除 shim 拦截**——临时文件用 `mv` 挪走，别 unlink。
10. **Git Bash curl 访问该服务器 index 显示 0B 是假象**，资源 200 即为正常，以浏览器为准。

---

## 四、后续任务（下一步要干什么）

### 4.0 首页 ↔ 内页 链接机制（已实现 · 08-11 凌晨）

**已实现「双轨跳转」**，在 index.html 的 `openArticle()` 开头：

```js
var NEW_INNER_PAGES={a108:1};  // ← 换皮登记册
function openArticle(a){
  if(NEW_INNER_PAGES[a.id]){ window.location.href=a.id+'.html'; return; }  // 新内页：整页跳转
  // ……其余文章：照旧走 #rv iframe 解密阅读窗（深色旧页）
}
```

- **规则**：新内页文件名 = `文章id.html`（a108 → `a108.html`），每换皮一篇就把 id 加进 `NEW_INNER_PAGES`。
- **返回首页**：新内页是整页跳转（不是 iframe），所以顶栏 logo 和「← 返回首页」都是真链接，直接回 index.html；sessionStorage 记着密码，回去自动解锁不用重输。
- **接手狐要做的事**：批量换皮（下面 4.1）→ 每产出一篇 `aN.html` → 登记册 +1 → 完事。不需要改别的。

### 4.1 批量换皮路线（待大橘拍板）

1. **首页阅读窗接新内页**：双轨机制已就位（见 4.0），剩下的是把 108 篇全部产出新内页：
   - A. 全部 108 篇按 2.3-B 批量换皮重新加密（工作量大但彻底）
   - B. 阅读窗改成包一层新模板壳、正文仍注入旧文（过渡方案）
   - 需大橘拍板。
2. **批量套皮脚本**：建议写 Node 脚本：批量解密 → 组件翻译（需要按篇的组件映射，各篇结构不完全一样，可能要逐类处理）→ 生成新明文 → 重新加密 .enc。
3. **内页 Trending 侧栏**：目前 a108 里是占位链接，批量时改成真实跳逻辑（同为 `aN.html` 直链即可）。
4. **上线**：原站部署走 `deploy_split.py`（在 miaowu-publish-article 技能里），换皮上线=改壳模板+重加密+push，**严禁 `git add -A`**，只加 `articles/ index.html`；push 先直连，不通就喊大橘开梯子（代理 7890）。
   - ⚠️ 注意：`aN.html` 这种明文新内页**不能直接上传公开仓库**（等于绕过加密）。上线形态应是：新内页明文 → 加密成 .enc → 阅读窗解密后把「正文 HTML 片段」注入新模板壳渲染（即方案 B 的完全体），或整页密文+前端解密闭环。具体加密形态随 4.1 拍板一起定。
5. **图片上货规格**：立绘 webp 320px、猫图 400px、横卡 800px、Hero 1920px，引用用 `articles/xxx.webp` 全路径（iframe srcdoc 基准根目录）。

---

## 五、大橘批改语录（品味校准用）

- 「别暖色，哪个好看换哪个」——配色拿不准就给冷色/中性色选项
- 「美观优先」——图长裁方、字多省略号、没对齐就往死里对
- 「尽量套模板格式」——模板有的组件不许自创，模板没有的才准发挥
- 「怎么好看怎么摆」——给了自由度但验收极严，出预览再动手

_—— 臭猫🐱王霸帝 整理于 2026-08-11 凌晨，叉叉山编辑部_

---

## 六、内页组件库（08-11 接班狐补充 · 大橘批改定稿）

> 完整自说明模板见 `template.html`（每个组件示例=使用注意事项，复制改名即可开工）。

### 6.1 基础组件（a108/a107/a106 通用）
| 组件 | 类名 | 要点 |
|------|------|------|
| 登记条 | `.tape` | 深灰底+紫左边条，`<b>` 写分类强调 |
| 引言卡 | `.card-x` | 白卡+🐾右下水印，通用性最强 |
| 章节题 | `.sec-title` | 紫左边条渐变，`<small>` 写补充 |
| 数据表 | `.bill-table` | 渐变粉紫表头；`.free`绿/`.bill`橙语义色 |
| 锐评 | `.note-x` | 黄粉虚线框，`<b>📎 编辑部锐评：</b>` 开头 |
| 术语 | `.gloss` | `data-tip` 悬停，猫话放最后，禁嵌套 HTML |
| 金句 | `.q-card` | 紫左边条白卡；带署名加 `.by` |
| Tags | `.tags` | 模板件，按 tags 数组生成 |

### 6.2 教学组件（a107 新增）
`.formula-card`(公式卡 top/line/bot 三层) · `.piece-grid`(四件套 p-b-sun/mint/pink/lav) · `.demo-card`(滑块互动+JS) · `.work-grid`(三工位 mini) · `details.quiz`(随堂小考 opt/ans)

### 6.3 审讯室组件（a106 新增）
`.scene-x`(场景卡+`.dialogue-x`对话左红条+`.who`/`.who-q`说话人) · `.evi-card`(证物卡 evi-head/evi-tag/evi-body+`.quote-x`引用块) · `.confess-x`(供词卡+who标签) · `.list-x`(编号命门列表) · `.verdict`宣判区(复用 a108 亮色版+红stamp)

### 6.4 foot 规范（大橘 08-11 批改最终版）
- **左对齐**、全部文字 **16px**（与「© 2026 八卦小报森林编辑部」版权行同大）
- 署名重点 `<b>` 用品牌蓝 **#367FF7**（模板 --c-primary）
- 排版顺序：**署名行 → .src 来源行 → 🐾**（paw 在来源后）
- 来源信息（.src）必须保留原文 sign 的「来源：xxx」内容，不得丢失
- 标题 h2 内**冒号后不换行**（禁 `<br>` 紧跟冒号）

### 6.5 Min Read 规则
汉字数 ÷ 450 四舍五入（a108=8177→18 · a107=2087→5 · a106=1751→4）
