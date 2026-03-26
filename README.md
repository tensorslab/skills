[English](README.md) | [中文](README_zh.md)

# TensorLab Skills

TensorLab Skills are AI task definitions for Claude Code, focusing on multimedia generation and processing using TensorsLab's AI models. It provides comprehensive capabilities including text-to-image and image-to-image generation, advanced image editing (avatar generation, watermark removal, object erasure, face replacement), as well as text-to-video and image-to-video generation.

## How do Skills work?

Skills are self-contained folders that package instructions, scripts, and resources together for Claude Code to use on specific use cases. Each folder includes a `SKILL.md` file with YAML frontmatter (name and description) followed by guidance for Claude Code to follow while the skill is active.

## Installation

TensorLab skills are compatible with Claude Code.

### Claude Code

1. Register the repository as a plugin marketplace:

```
/plugin marketplace add https://github.com/tensorslab/skills
```

2. To install a skill, run:

```
/plugin install <skill-name>@https://github.com/tensorslab/skills
```

For example:

```
/plugin install tl-image@https://github.com/tensorslab/skills
```

### opencode
use the following command to install skills:
```bash
npx skills add tensorslab/skills -g -y
```

## Available Skills

| Name | Description | Documentation |
|------|-------------|---------------|
| `tl-image` | Generate images using TensorsLab's AI image generation models. Supports text-to-image and image-to-image generation with automatic prompt enhancement, progress tracking, and local file saving. | [SKILL.md](skills/tl-image/SKILL.md) |
| `tl-video` | Generate videos using TensorsLab's AI video generation models. Supports text-to-video and image-to-video generation with automatic prompt enhancement, progress tracking, and local file saving. | [SKILL.md](skills/tl-video/SKILL.md) |

## Authorization

Before using TensorsLab skills, you need to authorize. The system will attempt to authorize automatically when you first run a skill.

### 1. Automatic Authorization (Recommended)
When you first use a skill, it will automatically trigger a browser-based authorization flow. Follow the prompts in your browser to complete the process. Once successful, your credentials will be stored locally in `~/.tensorslab/.env`.

### 2. Manual Configuration (For Cloud/Headless Environments)
If automatic authorization is not possible or fails (e.g., when the agent or openclaw is running in the cloud without a browser, the authorization URL callback will also fail), you must manually set your API key:

1. Get your API Key at [TensorsLab Console](https://tensorai.tensorslab.com/).
2. Set the environment variable in your cloud environment or local terminal:

```bash
# Windows (PowerShell)
$env:TENSORSLAB_API_KEY="your-api-key"

# Mac/Linux/Cloud
export TENSORSLAB_API_KEY="your-api-key"
```

## Using Skills

Once a skill is installed, mention it directly while giving Claude Code instructions:

- "Generate an image of an astronaut on the moon."
- "Animate this scenery picture into a 10s video."

Claude Code automatically loads the corresponding `SKILL.md` instructions and helper scripts while completing the task.


## References

Browse the latest instructions and scripts at [tensorslab/skills](https://github.com/tensorslab/skills).
