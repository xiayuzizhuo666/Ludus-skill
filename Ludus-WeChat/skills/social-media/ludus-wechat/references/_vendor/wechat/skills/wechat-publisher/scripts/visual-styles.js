/**
 * 微信公众号视觉排版风格配置
 * 
 * 每种风格定义一套配色方案，对应不同的文章调性。
 * 在发布时通过 --visual <风格名> 指定。
 */

const VISUAL_STYLES = {
  // ═══════════════════════════════════════
  // 风格 A: 日报风（默认）
  // 适用：⑥资讯日报主义
  // 特点：参考无界灵脑脑机科技日刊排版，简洁干净
  // ═══════════════════════════════════════
  daily: {
    name: '日报风',
    colors: {
      accent: '#0EA5E9',       // 品牌蓝 - 关键词/金句
      data: '#f59e0b',         // 橙 - 数据/数字
      danger: '#ef4444',       // 红 - 警示
      growth: '#10b981',       // 绿 - 增长
      text: '#333333',         // 正文
      title: '#111111',        // 标题
      bg: '#f7f8fa',           // 引用/摘要背景
      border: '#0EA5E9',       // 边框
      muted: '#999999',        // 辅助文字
      subtitle: '#666666',     // 子标题
    },
    // 标题边框（'none' = 无左边框）
    headingBorder: 'none',
    // 引用块
    blockquoteBorder: '4px solid #0EA5E9',
    // 摘要块（'none' = 不生成摘要引导块）
    summaryBorder: 'none',
    // 分割线样式：'none' = 无分割线
    separatorStyle: 'none',
    // 列表样式：'plain' = ▸ 作为普通段落
    listStyle: 'plain',
  },

  // ═══════════════════════════════════════
  // 风格 B: 温暖风
  // 适用：①情感共鸣主义、⑦情感叙事文风
  // 特点：暖色系，柔和，适合讲故事
  // ═══════════════════════════════════════
  warm: {
    name: '温暖风',
    colors: {
      accent: '#E8633C',       // 温暖橙红 - 关键词/金句
      data: '#D97706',         // 琥珀 - 数据
      danger: '#DC2626',       // 红 - 警示
      growth: '#059669',       // 绿 - 增长
      text: '#3D3D3D',         // 正文（偏暖黑）
      title: '#1A1A1A',        // 标题
      bg: '#FFF5F0',           // 引用/摘要背景（浅暖）
      border: '#E8633C',       // 边框
      muted: '#A3A3A3',        // 辅助
      subtitle: '#6B6B6B',     // 子标题
    },
    headingBorder: '4px solid #E8633C',
    blockquoteBorder: '4px solid #E8633C',
    summaryBorder: '4px solid #E8633C',
  },

  // ═══════════════════════════════════════
  // 风格 C: 专业风
  // 适用：②干货教程主义、③观点评论主义、⑤深度长文主义
  // 特点：简洁专业，深色为主
  // ═══════════════════════════════════════
  professional: {
    name: '专业风',
    colors: {
      accent: '#1E40AF',       // 深蓝 - 关键词
      data: '#B45309',         // 棕橙 - 数据
      danger: '#B91C1C',       // 深红 - 警示
      growth: '#047857',       // 深绿 - 增长
      text: '#374151',         // 正文
      title: '#111827',        // 标题
      bg: '#F3F4F6',           // 引用/摘要背景
      border: '#1E40AF',       // 边框
      muted: '#9CA3AF',        // 辅助
      subtitle: '#4B5563',     // 子标题
    },
    headingBorder: '4px solid #1E40AF',
    blockquoteBorder: '4px solid #1E40AF',
    summaryBorder: '4px solid #1E40AF',
  },

  // ═══════════════════════════════════════
  // 风格 D: 活泼风
  // 适用：④轻松幽默主义
  // 特点：明亮轻快，年轻化
  // ═══════════════════════════════════════
  lively: {
    name: '活泼风',
    colors: {
      accent: '#7C3AED',       // 紫色 - 关键词
      data: '#F59E0B',         // 橙 - 数据
      danger: '#EF4444',       // 红 - 警示
      growth: '#10B981',       // 绿 - 增长
      text: '#4A4A4A',         // 正文
      title: '#2D2D2D',        // 标题
      bg: '#F5F3FF',           // 引用/摘要背景（浅紫）
      border: '#7C3AED',       // 边框
      muted: '#A1A1AA',        // 辅助
      subtitle: '#6B7280',     // 子标题
    },
    headingBorder: '4px solid #7C3AED',
    blockquoteBorder: '4px solid #7C3AED',
    summaryBorder: '4px solid #7C3AED',
  },
};

// 写作风格 → 视觉风格映射
const STYLE_MAP = {
  // ① 情感共鸣主义 → 温暖风
  1: 'warm',
  '情感共鸣': 'warm',
  // ② 干货教程主义 → 专业风
  2: 'professional',
  '干货教程': 'professional',
  // ③ 观点评论主义 → 专业风
  3: 'professional',
  '观点评论': 'professional',
  // ④ 轻松幽默主义 → 活泼风
  4: 'lively',
  '轻松幽默': 'lively',
  // ⑤ 深度长文主义 → 专业风
  5: 'professional',
  '深度长文': 'professional',
  // ⑥ 资讯日报主义 → 日报风
  6: 'daily',
  '资讯日报': 'daily',
  // ⑦ 情感叙事文风 → 温暖风
  7: 'warm',
  '情感叙事': 'warm',
  // ⑧ 自定义风格 → 日报风（默认）
  8: 'daily',
  '自定义': 'daily',
};

function getVisualStyle(writingStyleIndex) {
  const key = String(writingStyleIndex);
  const visualName = STYLE_MAP[key] || 'daily';
  return VISUAL_STYLES[visualName] || VISUAL_STYLES.daily;
}

function getStyleByName(name) {
  const mapped = STYLE_MAP[name] || name;
  return VISUAL_STYLES[mapped] || VISUAL_STYLES.daily;
}

module.exports = { VISUAL_STYLES, STYLE_MAP, getVisualStyle, getStyleByName };
