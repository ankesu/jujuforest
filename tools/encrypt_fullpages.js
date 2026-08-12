/* 整页密文批量加密：v3明文/aN.html → articles/aN.html.enc
 * 格式对齐原站：{salt, iv, ct} base64，PBKDF2(100000, sha256) + AES-256-GCM
 * 预处理：① 路径 ../xxx → xxx（srcdoc 基准=站点根） ② 注入返回按钮关闭阅读窗 JS
 * 不修改 v3明文 原件（只读）
 * 08-12 起存放于 tools/，ROOT 指向工程根（本文件上一级）
 */
const fs = require('fs');
const crypto = require('crypto');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const SRC_DIR = path.join(ROOT, 'v3明文');
const OUT_DIR = path.join(ROOT, 'articles');
const PWD = 'jujuForest66';

// 返回按钮关闭阅读窗 JS（注入 </body> 前；iframe 内调 parent.closeReader，直开则正常跳首页）
const CLOSE_JS = `\n<script>\n(function(){document.addEventListener('click',function(e){\nvar a=e.target&&e.target.closest?e.target.closest('a'):null;\nif(a&&(a.getAttribute('href')==='index.html'||a.getAttribute('href')==='./index.html')){\ne.preventDefault();\ntry{if(window.parent&&window.parent.closeReader){window.parent.closeReader();return;}}catch(_){}\nwindow.location.href='index.html';\n}});})();\n</script>\n`;

// 页面不透明背景（srcdoc 渲染时 body 透明会让主页透出导致双导航条重叠）
const BG_CSS = `\n<style>html,body{background:#f5f6fa!important;min-height:100vh}</style>\n`;

function encrypt(plain) {
  const salt = crypto.randomBytes(16);
  const iv = crypto.randomBytes(12);
  const key = crypto.pbkdf2Sync(PWD, salt, 100000, 32, 'sha256');
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
  const enc = Buffer.concat([cipher.update(plain, 'utf8'), cipher.final()]);
  const tag = cipher.getAuthTag();
  return JSON.stringify({
    salt: salt.toString('base64'),
    iv: iv.toString('base64'),
    ct: Buffer.concat([enc, tag]).toString('base64')
  });
}

const files = fs.readdirSync(SRC_DIR).filter(f => /^a\d+\.html$/.test(f)).sort((a, b) => {
  return parseInt(a.match(/\d+/)[0]) - parseInt(b.match(/\d+/)[0]);
});
console.log('待加密:', files.length, '篇');

let ok = 0, fail = [];
for (const f of files) {
  try {
    let s = fs.readFileSync(path.join(SRC_DIR, f), 'utf8');
    // ① 路径修正：src/href/url 后的 ../ 去掉
    s = s.replace(/(src|href)="\.\.\//g, '$1="');
    s = s.replace(/url\(\.\.\//g, 'url(');
    // ② 注入不透明背景（防主页透出双导航）+ 关闭阅读窗 JS
    s = s.replace('</head>', BG_CSS + '</head>');
    s = s.replace('</body>', CLOSE_JS + '</body>');
    // ③ 加密
    const outName = f.replace('.html', '.html.enc');
    fs.writeFileSync(path.join(OUT_DIR, outName), encrypt(s), 'utf8');
    ok++;
  } catch (e) {
    fail.push(f + ':' + e.message);
  }
}
console.log('✅ 加密完成:', ok, '篇 | 失败:', fail.length ? fail.join(',') : '无');
