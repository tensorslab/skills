[English](README.md) | [中文](README_zh.md)

# TensorLab Skills

TensorLab Skills 是为 Claude Code 提供的 AI 任务定义，专注于使用 TensorsLab 的 AI 模型进行多媒体生成和处理。它提供全面的功能，包括文生图、图生图、高级图像编辑（生成数字分身、去水印、消除物体、换脸），以及文生视频和图生视频。

## Skills 是如何工作的？

Skills 是独立的文件夹，将指令、脚本和资源打包在一起，供 Claude Code 在特定用例中使用。每个文件夹包含一个带有 YAML frontmatter（包含名称和描述）的 `SKILL.md` 文件，随后是 Claude Code 在 skill 激活时需要遵循的指导。

## 安装

TensorLab skills 兼容 Claude Code。

### Claude Code

1. 将仓库注册为插件市场：

```
/plugin marketplace add https://github.com/tensorslab/skills
```

2. 安装一个 skill，运行：

```
/plugin install <skill-name>@https://github.com/tensorslab/skills
```

例如：

```
/plugin install tl-image@https://github.com/tensorslab/skills
```

### opencode
使用以下命令安装 skills：
```bash
npx skills add tensorslab/skills -g -y
```

## 可用的 Skills

| 名称 | 描述 | 文档 |
|------|-------------|---------------|
| `tl-image` | 使用 TensorsLab 的 AI 图像生成模型生成图像。支持文生图和图生图生成，具有自动提示词增强、进度跟踪和本地文件保存功能。 | [SKILL.md](skills/tl-image/SKILL.md) |
| `tl-video` | 使用 TensorsLab 的 AI 视频生成模型生成视频。支持文生视频和图生视频生成，具有自动提示词增强、进度跟踪和本地文件保存功能。 | [SKILL.md](skills/tl-video/SKILL.md) |

## 授权

在使用 TensorsLab skills 之前，您需要进行授权。系统在您首次运行 skill 时将尝试自动授权。

### 1. 自动授权 (推荐)
当您首次使用 skill 时，它将自动触发基于浏览器的授权流程。按照浏览器中的提示完成此过程。成功后，您的凭据将本地存储在 `~/.tensorslab/.env` 中。

### 2. 手动配置 (可选)
如果无法进行自动授权或授权失败，您可以手动设置 API 密钥：

1. 在 [TensorsLab 控制台](https://tensorai.tensorslab.com/) 获取您的 API 密钥。
2. 设置环境变量：

```bash
# Windows (PowerShell)
$env:TENSORSLAB_API_KEY="您的-api-key"

# Mac/Linux
export TENSORSLAB_API_KEY="您的-api-key"
```

## 使用 Skills

安装 skill 后，在向 Claude Code 下达指令时直接提及它：

- "Generate an image of an astronaut on the moon." (生成一张宇航员在月球上的图片。)
- "Animate this scenery picture into a 10s video." (将这张风景图片动画化为 10 秒的视频。)

Claude Code 在完成任务时会自动加载相应的 `SKILL.md` 指令和辅助脚本。

## 参考资料

浏览最新的指令和脚本：[tensorslab/skills](https://github.com/tensorslab/skills)。
