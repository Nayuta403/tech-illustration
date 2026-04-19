# tech-illustration

[English](README.md) · [中文](README_zh.md)

> 多风格技术插图生成器。以 [Agent Skill](https://docs.claude.com/en/docs/claude-code/skills) 形式发布（支持 Claude Code、Cursor 以及任何能读 `SKILL.md` 的 agent），同时也可作为独立的 Python CLI 使用。

给一个概念，选一种风格，得到一张出版级别的图。当前使用 Google Gemini 3.1 Flash Image——选它是因为在技术图表场景下效果最好。

## 风格

| 风格 | 预览 |
|------|------|
| **blueprint** — 工程网格、藏青 + 橙色、手绘感。默认风格。 | ![blueprint](examples/blueprint.png) |
| **clean** — 极简矢量图、白底。 | ![clean](examples/clean.png) |
| **dynamic** — 等距视角、发光能量流、深色背景。 | ![dynamic](examples/dynamic.png) |
| **bold** — 前卫编辑风、超大字体。 | ![bold](examples/bold.png) |

## 安装

### 任意 agent 里——一句话搞定

大多数支持 skill 的 agent 都能从 URL 直接安装。以 Claude Code 为例：

```
帮我安装一下 https://github.com/Nayuta403/tech-illustration 这个 skill
```

Agent 会自己 clone 到对应的 skills 目录（Claude Code 是 `~/.claude/skills/tech-illustration`），通过 `SKILL.md` 自动识别。之后想用就直接说：

> 用 blueprint 风格画一张 OAuth 流程的技术插图。

### 手动安装 / 独立 CLI

如果想自己动手，或者脱离 agent 单独用这个脚本：

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

## 使用方式

### 通过 agent 使用（推荐）

用自然语言说清楚你要什么，agent 会自己去调脚本。几个例子：

```
画一张 blueprint 风格的技术插图，主题是 OAuth 2.0 授权码流程，
保存为 oauth.png。
```

```
用 dynamic 风格画一张 Kubernetes 部署图：包含 Ingress、Service、Pod
三层。中文标注，输出 k8s.png。
```

```
帮我做一张 bold 风格的文章封面，主题是 AI Agent 的进化三阶段：
聊天机器人 2022、助手 2024、自主智能体 2026，对角线构图，中文，
保存为 cover.png。
```

如果出图看起来空洞或通用，多半是你描述得太短——读一下下面的**如何写 topic**，然后让 agent 用更丰富的 prompt 重试。

### 直接用 CLI

```
uv run scripts/gen_illustration.py \
  --topic  TEXT   # 要画什么（见下方"如何写 topic"）
  --filename PATH # 输出 .png 路径
  [--style  blueprint | clean | dynamic | bold]   # 默认 blueprint
  [--lang   zh | en]                              # 默认 zh
  [--api-key KEY]                                 # 覆盖 GEMINI_API_KEY
```

### 如何写 topic

出图质量的天花板由你 topic 的信息密度决定。像 *"微服务架构"* 这样笼统的 prompt 只会得到一张空洞的通用图。

应该写清：

1. 每个元素具体画什么（图标、形状、标注）
2. 图上所有要出现的文字都要明写
3. 颜色的语义（例如"红色 = 当前状态"）
4. 一句话概括整体要传达什么

详见 `SKILL.md` 里的好坏对比范例。

## 模型

目前固定使用 `gemini-3.1-flash-image-preview`。在我们的测试里，这个模型在技术图表场景（排版干净、布局准确、图标正确）下效果最好，所以我们锁死它，不做多 provider 的抽象层。

模型名就是 `scripts/gen_illustration.py` 里的一个常量。想换别的图像模型（Imagen、其他 provider、或者更新的 Gemini），把字符串换掉并适配 SDK 调用即可——但跨模型兼容性我们不维护，换了以后这个分支就是你自己的了。

由于当前模型是 preview 版本，Google 可能随时改名或下线——到时更新这个字符串就行。

## 安全

脚本只从环境变量（或 `--api-key`）读取 `GEMINI_API_KEY`，不会写入磁盘或打印到日志。Fork 之前再扫一遍更放心。

## License

MIT — 见 [LICENSE](LICENSE)。
