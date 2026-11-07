#!/usr/bin/env node
/**
 * 微信公众号草稿箱API自动上传工具
 *
 * @package  wechat-publisher
 * @author   magicx (original skill)
 * @license  ISC
 *
 * 功能：
 * 1. 通过微信API将文章上传到公众号草稿箱
 * 2. 支持HTML格式内容
 * 3. 自动获取 access_token 并提交草稿
 *
 * 使用方式：
 *   node upload-draft.js --appid <appid> --secret <secret> --html <文件路径> --title "标题"
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// ======== 配置 ========
const DEFAULT_CONFIG_FILE = path.join(__dirname, '.wechat-config.json');

// ======== 参数解析 ========
function parseArgs() {
  const args = process.argv.slice(2);
  const opts = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--appid') opts.appid = args[++i];
    else if (args[i] === '--secret') opts.secret = args[++i];
    else if (args[i] === '--html') opts.html = args[++i];
    else if (args[i] === '--title') opts.title = args[++i];
    else if (args[i] === '--author') opts.author = args[++i];
    else if (args[i] === '--digest') opts.digest = args[++i];
    else if (args[i] === '--source-url') opts.sourceUrl = args[++i];
    else if (args[i] === '--config') opts.config = args[++i];
    else if (args[i] === '--save-config') opts.saveConfig = true;
    else if (args[i] === '--help' || args[i] === '-h') {
      console.log(`
微信公众号草稿箱API上传工具

用法:
  node upload-draft.js --html <文件> --title <标题> [选项]

参数:
  --appid <id>       公众号AppID（也可用环境变量 WECHAT_APPID）
  --secret <secret>  公众号AppSecret（也可用环境变量 WECHAT_APP_SECRET）
  --html <path>      HTML文章文件路径
  --title <title>    文章标题
  --author <name>    文章作者（默认读取配置或 WECHAT_AUTHOR）
  --digest <text>    摘要（可选）
  --source-url <url> 原文链接（可选）
  --config <path>    配置文件路径（默认 scripts/.wechat-config.json）
  --save-config      保存AppID/Secret/作者到本地配置
  -h, --help         显示帮助

首次使用:
  1. 登录公众号后台 → 设置与开发 → 基本配置
  2. 获取AppID和AppSecret
  3. 运行: node upload-draft.js --appid xxx --secret xxx --save-config
  4. 以后只需: node upload-draft.js --html 文章.html --title "标题"
      `);
      process.exit(0);
    }
  }
  return opts;
}

// ======== 配置管理 ========
function loadConfig(configPath) {
  if (!fs.existsSync(configPath)) return {};
  try {
    return JSON.parse(fs.readFileSync(configPath, 'utf8'));
  } catch (e) {
    return {};
  }
}

function saveConfig(configPath, config) {
  fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
  console.log(`✅ 配置已保存到 ${configPath}`);
}

// ======== 微信API调用 ========
function httpsRequest(url, method = 'GET', data = null) {
  return new Promise((resolve, reject) => {
    const urlObj = new URL(url);
    const options = {
      hostname: urlObj.hostname,
      path: urlObj.pathname + urlObj.search,
      method: method,
      headers: {
        'Content-Type': 'application/json'
      }
    };

    if (data) {
      const payload = JSON.stringify(data);
      options.headers['Content-Length'] = Buffer.byteLength(payload);
    }

    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(body);
          if (result.errcode && result.errcode !== 0) {
            reject(new Error(`API错误 ${result.errcode}: ${result.errmsg}`));
          } else {
            resolve(result);
          }
        } catch (e) {
          reject(new Error('响应解析失败: ' + body));
        }
      });
    });

    req.on('error', reject);
    if (data) req.write(JSON.stringify(data));
    req.end();
  });
}

// 获取access_token
async function getAccessToken(appid, secret) {
  console.log('🔑 正在获取access_token...');
  const url = `https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=${appid}&secret=${secret}`;
  const result = await httpsRequest(url);
  console.log(`✅ access_token获取成功（有效期7200秒）`);
  return result.access_token;
}

// 新增草稿
async function addDraft(accessToken, title, author, content, digest, sourceUrl) {
  console.log('📝 正在上传草稿到公众号...');

  const url = `https://api.weixin.qq.com/cgi-bin/draft/add?access_token=${accessToken}`;
  const data = {
    articles: [{
      title: title,
      author: author || '',
      digest: digest || '',
      content: content,
      content_source_url: sourceUrl || '',
      need_open_comment: 0,
      only_fans_can_comment: 0
    }]
  };

  const result = await httpsRequest(url, 'POST', data);
  console.log(`✅ 草稿上传成功！media_id: ${result.media_id}`);
  console.log(`📱 请在公众号后台 → 内容与互动 → 草稿箱 中查看`);
  return result.media_id;
}

// ======== 主流程 ========
async function main() {
  const opts = parseArgs();
  const configPath = path.resolve(opts.config || process.env.WECHAT_CONFIG || DEFAULT_CONFIG_FILE);
  const savedConfig = loadConfig(configPath);

  // 合并配置：命令行 > 环境变量 > 配置文件
  const appid = opts.appid || process.env.WECHAT_APPID || savedConfig.appid;
  const secret = opts.secret || process.env.WECHAT_APP_SECRET || savedConfig.secret;
  const author = opts.author || process.env.WECHAT_AUTHOR || savedConfig.author || '';

  if (!appid || !secret) {
    console.log('❌ 缺少AppID或AppSecret');
    console.log('   首次使用请运行: node upload-draft.js --appid xxx --secret xxx --save-config');
    console.log('   或设置环境变量 WECHAT_APPID / WECHAT_APP_SECRET');
    console.log('   或使用 --help 查看帮助');
    process.exit(1);
  }

  if (!opts.html || !opts.title) {
    console.log('❌ 缺少必要参数');
    console.log('   使用方式: node upload-draft.js --html <文件> --title <标题>');
    console.log('   使用 --help 查看完整帮助');
    process.exit(1);
  }

  // 保存配置
  if (opts.saveConfig) {
    saveConfig(configPath, { ...savedConfig, appid, secret, ...(author ? { author } : {}) });
  }

  // 读取HTML文件
  const htmlPath = path.resolve(opts.html);
  if (!fs.existsSync(htmlPath)) {
    console.log(`❌ 文件不存在: ${htmlPath}`);
    process.exit(1);
  }

  let htmlContent = fs.readFileSync(htmlPath, 'utf8');

  // 如果是完整HTML，提取body内容
  const bodyMatch = htmlContent.match(/<body[^>]*>([\s\S]*)<\/body>/i);
  if (bodyMatch) {
    htmlContent = bodyMatch[1];
  }

  console.log(`📄 已读取文章: ${htmlPath} (${(htmlContent.length / 1024).toFixed(1)}KB)`);

  // 检查内容大小
  if (htmlContent.length > 2000000) { // 2MB
    console.log('❌ 文章内容超过2MB限制');
    process.exit(1);
  }

  try {
    // 1. 获取access_token
    const accessToken = await getAccessToken(appid, secret);

    // 2. 上传草稿
    const mediaId = await addDraft(accessToken, opts.title, author, htmlContent, opts.digest, opts.sourceUrl);

    console.log('\n🎉 上传完成！');
    console.log(`📱 请在公众号后台查看草稿并发布`);
    console.log(`💡 提示：如需上传封面图，请先在公众号后台手动上传到素材库`);

  } catch (e) {
    console.error('❌ 上传失败:', e.message);
    process.exit(1);
  }
}

main().catch(console.error);
