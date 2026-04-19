# tech-illustration

[English](README.md) · [中文](README_zh.md)

> 一个 Claude [Agent Skill](https://docs.claude.com/en/docs/claude-code/skills)，基于 Google Gemini 3.1 Flash Image 模型，为文章、幻灯片、技术文档生成多风格的技术插图。

给一个概念，选一种风格，得到一张出版级别的图。

## 风格

| 风格 | 预览 |
|------|------|
| **blueprint** — 工程网格、藏青 + 橙色、手绘感。默认风格。 | ![blueprint](examples/blueprint.png) |
| **clean** — 极简矢量图、白底。 | ![clean](examples/clean.png) |
| **dynamic** — 等距视角、发光能量流、深色背景。 | ![dynamic](examples/dynamic.png) |
| **bold** — 前卫编辑风、超大字体。 | ![bold](examples/bold.png) |

## 安装

### Claude Code 里——一句话搞定

直接跟 Claude 说：

```
帮我安装一下 https://github.com/Nayuta403/tech-illustration 这个 skill
```

Claude Code 会自己 clone 到 `~/.claude/skills/tech-illustration`，通过 `SKILL.md` 自动识别。之后想用就直接说：

> 用 blueprint 风格画一张 OAuth 流程的技术插图。

### 手动安装 / 独立 CLI

如果想自己动手，或者脱离 Claude 单独用这个脚本：

```bash
git clone https://github.com/Nayuta403/tech-illustration.git
cd tech-illustration
export GEMINI_API_KEY="你的-key"

uv run scripts/gen_illustration.py \
  --topic "详细的主题描述" \
  --filename out.png \
  --style blueprint \
  --lang zh
```

## 环境要求

- Python 3.10+
- [`uv`](https://docs.astral.sh/uv/)（推荐，脚本内联依赖，无需 `pip install`）
- Google Gemini API Key：<https://aistudio.google.com/app/apikey>

脚本顶部用 inline 方式声明了依赖（`google-genai`、`pillow`），`uv run` 会自动处理环境。

## 命令行参数

```
uv run scripts/gen_illustration.py \
  --topic  TEXT   # 要画什么（见下方"如何写 topic"）
  --filename PATH # 输出 .png 路径
  [--style  blueprint | clean | dynamic | bold]   # 默认 blueprint
  [--lang   zh | en]                              # 默认 zh
  [--api-key KEY]                                 # 覆盖 GEMINI_API_KEY
```

## 如何写 topic

出图质量的天花板由你 topic 的信息密度决定。像 *"微服务架构"* 这样笼统的 prompt 只会得到一张空洞的通用图。

应该写清：

1. 每个元素具体画什么（图标、形状、标注）
2. 图上所有要出现的文字都要明写
3. 颜色的语义（例如"红色 = 当前状态"）
4. 一句话概括整体要传达什么

详见 `SKILL.md` 里的好坏对比范例。

## 模型

使用 `gemini-3.1-flash-image-preview`。由于这是预览模型，Google 可能随时改名或下线——需要时在 `scripts/gen_illustration.py` 中修改模型名字符串即可。

## 安全

脚本只从环境变量（或 `--api-key`）读取 `GEMINI_API_KEY`，不会写入磁盘或打印到日志。Fork 之前再扫一遍更放心。

## License

MIT — 见 [LICENSE](LICENSE)。
