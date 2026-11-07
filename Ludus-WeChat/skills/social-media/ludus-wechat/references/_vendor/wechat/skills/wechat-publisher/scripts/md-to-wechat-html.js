#!/usr/bin/env node
/**
 * Markdown → 公众号HTML 转换脚本
 * 
 * 将 Markdown 文章转为公众号兼容的HTML，自动应用视觉风格。
 * 使用前需先用工具将正文图片上传到微信图床。
 *
 * Usage:
 *   node md-to-wechat-html.js --input article.md --output article.html [--style daily|warm|professional|lively]
 * 
 * 如果不指定 --style，默认使用日报风（daily）。
 * --style 也可以传写作风格编号（1-8），会自动映射到对应视觉风格。
 */

const fs = require('fs');
const path = require('path');
const { getVisualStyle, getStyleByName } = require('./visual-styles.js');

function parseArgs() {
  const args = process.argv.slice(2);
  const opts = {};
  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--input': opts.input = args[++i]; break;
      case '--output': opts.output = args[++i]; break;
      case '--style': opts.style = args[++i]; break;
      case '--title': opts.title = args[++i]; break;
    }
  }
  return opts;
}

/**
 * 将 Markdown 文本转为公众号 HTML
 */
function convert(markdown, style) {
  const C = style.colors;
  const isPlainList = style.listStyle === 'plain';
  const sepStyle = style.separatorStyle || 'hr';

  let html = '';
  const lines = markdown.split('\n');
  let inCodeBlock = false;
  let listTag = null;

  function closeList() {
    if (listTag) {
      html += `</${listTag}>\n`;
      listTag = null;
    }
  }

  for (let i = 0; i < lines.length; i++) {
    let line = lines[i];
    const trimmed = line.trim();
    const isListLine = !isPlainList && (
      trimmed.startsWith('- ') ||
      trimmed.startsWith('▸ ') ||
      /^\d+\.\s+/.test(trimmed)
    );
    if (!inCodeBlock && !isListLine) closeList();

    // 代码块
    if (line.trim().startsWith('```')) {
      if (inCodeBlock) {
        html += '</code></pre>\n';
        inCodeBlock = false;
      } else {
        html += '<pre style="margin:3px 0;padding:12px;background:#f4f4f5;border-radius:8px;font-size:14px;line-height:1.6;overflow-x:auto;"><code style="background:transparent;color:#333;padding:0;font-size:14px;">';
        inCodeBlock = true;
      }
      continue;
    }

    if (inCodeBlock) {
      html += line.replace(/</g, '&lt;').replace(/>/g, '&gt;') + '\n';
      continue;
    }

    // 空行
    if (line.trim() === '') {
      continue;
    }

    // 水平分割线
    if (/^---/.test(line.trim())) {
      if (sepStyle === 'none') {
        // 不渲染任何分割线，跳过
        continue;
      } else {
        html += '<hr style="border:none;border-top:1px solid #eee;margin:8px 0;" />\n';
      }
      continue;
    }

    // 引用块
    if (line.trim().startsWith('> ')) {
      const content = line.trim().substring(2);
      html += `<blockquote style="margin:3px 0;padding:12px 18px;background:${C.bg};border-left:${style.blockquoteBorder};color:#555;font-style:italic;">${inlineConvert(content, C, isPlainList)}</blockquote>\n`;
      continue;
    }

    // 无序列表
    if (line.trim().startsWith('- ') || line.trim().startsWith('▸ ')) {
      const content = line.trim().replace(/^[-▸]\s*/, '');
      if (isPlainList) {
        // ▸ 作为普通段落（无缩进、无圆点）
        html += `<p style="margin:3px 0;font-size:16px;line-height:1.75;color:${C.text};">▸ ${inlineConvert(content, C, isPlainList)}</p>\n`;
      } else {
        // 标准列表
        if (listTag !== 'ul') {
          closeList();
          html += '<ul style="margin:3px 0;padding-left:20px;list-style-type:disc;">\n';
          listTag = 'ul';
        }
        html += `<li style="margin:2px 0;font-size:16px;line-height:1.75;color:${C.text};">${inlineConvert(content, C, isPlainList)}</li>\n`;
      }
      continue;
    }

    // 有序列表：只识别“数字 + 点 + 空格”，避免把“1、”和“2026.05.01”误判为列表
    if (/^\d+\.\s+/.test(line.trim())) {
      if (listTag !== 'ol') {
        closeList();
        html += '<ol style="margin:3px 0;padding-left:20px;">\n';
        listTag = 'ol';
      }
      const content = line.trim().replace(/^\d+\.\s+/, '');
      html += `<li style="margin:2px 0;font-size:16px;line-height:1.75;color:${C.text};">${inlineConvert(content, C, isPlainList)}</li>\n`;
      continue;
    }

    // 标题
    if (/^##\s/.test(line)) {
      const text = inlineConvert(line.replace(/^##\s+/, ''), C, isPlainList);
      const hasBorder = style.headingBorder !== 'none';
      html += `<h2 style="font-size:20px;font-weight:bold;color:${C.title};margin-top:15px;margin-bottom:5px;${hasBorder ? 'padding-left:12px;border-left:' + style.headingBorder + ';' : ''}">${text}</h2>\n`;
      continue;
    }
    if (/^###\s/.test(line)) {
      const text = inlineConvert(line.replace(/^###\s+/, ''), C, isPlainList);
      html += `<h3 style="font-size:17px;font-weight:bold;color:${C.subtitle};margin-top:12px;margin-bottom:3px;">${text}</h3>\n`;
      continue;
    }

    // 图片
    const imgMatch = line.match(/!\[(.*?)\]\((.*?)\)/);
    if (imgMatch) {
      html += `<p style="text-align:center;margin:3px 0;"><img src="${imgMatch[2]}" style="max-width:100%;display:block;margin:0 auto;border-radius:12px;" alt="${imgMatch[1]}"/></p>\n`;
      continue;
    }

    // 正文段落
    html += `<p style="margin:3px 0;font-size:16px;line-height:1.75;color:${C.text};">${inlineConvert(line, C, isPlainList)}</p>\n`;
  }

  closeList();
  return html;
}

/**
 * 行内格式转换（加粗、链接、行内代码等）
 */
function inlineConvert(text, C, isPlainBold) {
  // 转义HTML
  text = text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

  // 图片标记（行内）
  text = text.replace(/!\[(.*?)\]\((.*?)\)/g, '<img src="$2" style="max-width:100%;border-radius:8px;" alt="$1"/>');

  // 加粗+颜色标记：**【关键词】** → 品牌蓝加粗
  text = text.replace(/\*\*【(.+?)】\*\*/g, `<strong style="color:${C.accent};">【$1】</strong>`);

  // 链接
  text = text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" style="color:' + C.accent + ';text-decoration:none;">$1</a>');

  // 加粗
  // isPlainBold=true（日报风）：纯黑色加粗，简洁风格
  // isPlainBold=false（其他风格）：品牌蓝加粗突显关键词
  if (isPlainBold) {
    text = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  } else {
    text = text.replace(/\*\*(.+?)\*\*/g, `<strong style="color:${C.accent};">$1</strong>`);
  }

  // 行内代码
  text = text.replace(/`([^`]+)`/g, '<code style="background:#f4f4f5;color:#c0392b;padding:1px 4px;border-radius:3px;font-size:14px;">$1</code>');

  return text;
}

// ======== 主入口 ========
function main() {
  const opts = parseArgs();
  if (!opts.input || !opts.output) {
    console.log(JSON.stringify({
      usage: 'node md-to-wechat-html.js --input article.md --output article.html [--style daily|warm|professional|lively|1-8] [--title "标题"]'
    }, null, 2));
    process.exit(0);
  }

  // 读取markdown
  const content = fs.readFileSync(path.resolve(opts.input), 'utf8');

  // 确定视觉风格
  let style;
  const styleArg = opts.style || 'daily';
  if (/^[1-8]$/.test(styleArg)) {
    style = getVisualStyle(parseInt(styleArg));
  } else {
    style = getStyleByName(styleArg);
  }

  const C = style.colors;
  const noSummary = style.summaryBorder === 'none';

  if (noSummary) {
    // 日报风：不生成摘要引导块，全文直接转换
    let html = convert(content, style);
    const outputPath = path.resolve(opts.output);
    fs.writeFileSync(outputPath, html, 'utf8');
    console.log(JSON.stringify({
      success: true,
      style: style.name,
      input: opts.input,
      output: outputPath,
      size: `${(html.length / 1024).toFixed(1)}KB`
    }, null, 2));
  } else {
    // 其他风格：自动提取首段为摘要引导块
    const lines = content.split('\n');
    let digest = '';
    for (const line of lines) {
      const trimmed = line.trim();
      if (trimmed && !trimmed.startsWith('#') && !trimmed.startsWith('---') && !trimmed.startsWith('>')) {
        digest = trimmed.substring(0, 120);
        break;
      }
    }

    let html = `<section style="margin:10px 0 15px;padding:15px 20px;background:${C.bg};border-left:${style.summaryBorder};font-size:15px;color:#555;line-height:1.6;">\n${digest}\n</section>\n\n`;
    const bodyContent = content.split('\n').slice(lines.indexOf(digest) + 1).join('\n');
    html += convert(bodyContent, style);

    const outputPath = path.resolve(opts.output);
    fs.writeFileSync(outputPath, html, 'utf8');
    console.log(JSON.stringify({
      success: true,
      style: style.name,
      input: opts.input,
      output: outputPath,
      size: `${(html.length / 1024).toFixed(1)}KB`
    }, null, 2));
  }
}

main();
