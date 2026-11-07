# Third-Party Notices

## 1. wechat-topic-selector

- Upstream: https://github.com/lucianaib0318/wechat-auto-publish
- License: MIT
- Vendored at: `skills/social-media/ludus-wechat/references/_vendor/wechat/skills/wechat-topic-selector/`
- Original license: `references/_vendor/wechat/skills/wechat-topic-selector/LICENSE`.
- Modification: path references adapted by the entry skill; upstream body unchanged.

## 2. wechat-publisher (original magicx-wechat-publisher)

- Source: ClawHub, slug `magicx-wechat-publisher`, version 1.0.1
- Author: magicx
- License: ISC
- Vendored at: `skills/social-media/ludus-wechat/references/_vendor/wechat/skills/wechat-publisher/`
- Original license: `references/_vendor/wechat/skills/wechat-publisher/LICENSE`.
- Modification: path references and config defaults adapted by `scripts/run_wechat.py`; upstream body unchanged.

## 3. wechat-article-writer (self-authored replacement)

- Upstream ClawHub version had **no LICENSE file** and is **not included** in this package.
- The `wechat-article-writer/` directory is a new, self-authored MIT implementation of the six-stage writing workflow, title patterns, frameworks, style guide and image-prompt guide.
- License: MIT, same as this package's new content.
- Files: `SKILL.md`, `writing_style.md`, `references/`, `scripts/generate_images.py`, `scripts/image.env.example`.
- No upstream text, examples or scripts from the no-license version are retained.

## 4. wechat-article-pipeline

- Repository: https://github.com/davinci-seven/wechat-article-pipeline
- Commit: `ab90abb602712099dd364c43b16f4d65cfe34d68`
- License: MIT
- Vendored at: `skills/social-media/ludus-wechat/references/_vendor/wechat-enhancements/wechat-article-pipeline/`
- Included: `tools/*.py`, `tools/*.bat`, `tools/*.ps1`, `templates/article-template.md`, `docs/*.md`, `requirements.txt`, `LICENSE`, `README.md`, `SKILL.md`.
- Excluded: `examples/`, docs images, `.github/`.
- Original license: `references/_vendor/wechat-enhancements/wechat-article-pipeline/LICENSE`.

## 5. 本包新增内容

`SKILL.md`、`references/INDEX.md`、`references/PATHS.md`、`scripts/run_wechat.py`、`templates/wechat-config.example.json`、`install.py`、`tests/` 和包根文档由本包新增，采用 MIT；见 `LICENSE`。
