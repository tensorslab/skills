---
name: image-edit
description: 对图像进行编辑操作。支持四种功能：变宽高比（aspect）、擦除对象（erase）、去除背景（rmbg）、通用编辑（edit）。基于 tl-image 的 quickedit 模型实现快速图像编辑。当用户需要修改图片宽高比、移除图片中的对象、去除背景或进行自定义编辑时使用此技能。
---

# Image Edit - 图像编辑工具

基于 tl-image 的 quickedit 模型实现快速图像编辑操作。

## 脚本路径

本技能使用 tl-image 技能的 `tensorslab_image.py` 脚本，配合 `--model quickedit` 参数。脚本位于 tl-image 技能的 `scripts/` 目录下，**必须使用绝对路径执行**。根据 tl-image 技能的安装位置确定绝对路径。

例如，如果 tl-image 的 SKILL.md 位于 `/path/to/skills/tl-image/SKILL.md`，则：
```bash
python "<tl-image绝对路径>/scripts/tensorslab_image.py" "<编辑指令>" --source <image_path> --model quickedit
```

## 授权

使用前需确保已通过 TensorsLab 授权。运行：
```bash
python "<tl-image绝对路径>/scripts/tensorslab_auth.py"
```

如果之前已授权过（`~/.tensorslab/.env` 中有 key），则无需重复授权。

## 提示词规则

**所有传给脚本的提示词（prompt）必须用引号包裹**，防止 shell 解析问题：
```bash
# 正确
python "scripts/tensorslab_image.py" "remove the watermark" --source photo.jpg --model quickedit
python "scripts/tensorslab_image.py" "把天空改成星空" --source photo.jpg --model quickedit

# 错误 - 没有引号
python "scripts/tensorslab_image.py" remove the watermark --source photo.jpg --model quickedit
```

## 功能说明

### 1. 变宽高比（aspect）

改变图片宽高比，保持内容不变。

```bash
python "<tl-image绝对路径>/scripts/tensorslab_image.py" "保持画面内容不变，调整构图适应新的宽高比" --source input.jpg --model quickedit --resolution 16:9
```

支持的宽高比：`1:1`、`4:3`、`3:4`、`16:9`、`9:16`、`3:2`、`2:3`、`21:9`、`9:21`

用户请求映射：
- "正方形"、"1:1" → `1:1`
- "横屏"、"16:9"、"宽屏" → `16:9`
- "竖屏"、"9:16"、"手机屏" → `9:16`
- "4:3"、"标准" → `4:3`

### 2. 擦除对象（erase）

从图片中移除指定对象。

```bash
python "<tl-image绝对路径>/scripts/tensorslab_image.py" "remove the watermark from the image" --source photo.jpg --model quickedit
python "<tl-image绝对路径>/scripts/tensorslab_image.py" "remove the person in the background" --source photo.jpg --model quickedit
python "<tl-image绝对路径>/scripts/tensorslab_image.py" "remove the logo" --source photo.jpg --model quickedit
```

擦除提示词应明确描述要移除的对象，并用英文效果最佳。

### 3. 去除背景（rmbg）

移除图片背景，只保留主体。

```bash
python "<tl-image绝对路径>/scripts/tensorslab_image.py" "remove the background, keep only the main subject" --source portrait.jpg --model quickedit
```

### 4. 通用编辑（edit）

使用自定义指令编辑图片。

```bash
python "<tl-image绝对路径>/scripts/tensorslab_image.py" "change the sky to a starry night" --source input.jpg --model quickedit
python "<tl-image绝对路径>/scripts/tensorslab_image.py" "add snow effect" --source input.jpg --model quickedit --resolution 16:9
```

**可选参数:**
- `--resolution` - 输出宽高比（如 `16:9`、`1:1`）
- `--output-dir` - 自定义输出目录

编辑指令使用英文效果最佳，保留用户的创意意图。

## 通用参数

所有命令支持以下可选参数：
- `--output-dir` 或 `-o` - 输出目录（默认: `./tensorslab_output/`）
- `--resolution` - 输出宽高比（如 `16:9`、`1:1`）

## 文件名生成

生成文件名使用格式: `yyyy-mm-dd-hh-mm-ss-name.jpg`

**格式:** `{timestamp}-{descriptive-name}.jpg`
- Timestamp: 当前日期时间，格式 `yyyy-mm-dd-hh-mm-ss`（24小时制）
- Name: 描述性小写文本，用连字符分隔
- 描述部分保持简洁（通常1-5个词）
- 使用用户提示或对话的上下文
- 如不明确，使用随机标识符（如 `x9k2`、`a7b3`）

示例：
- 擦除水印 → `2025-01-19-20-30-05-remove-watermark.jpg`
- 改为9:16比例 → `2025-01-19-20-31-12-aspect-9-16.jpg`
- 去除背景 → `2025-01-19-20-32-33-remove-bg.jpg`
- 添加雪花效果 → `2025-01-19-20-33-48-snow-effect.jpg`

## 输出

- 图片默认保存到 `./tensorslab_output/` 目录
- 脚本输出生成图片的完整路径和远程 URL
- **不要回读图片** - 只需告知用户保存路径

## 注意事项

1. 输入图片支持常见格式：JPG、PNG、WEBP 等
2. 编辑指令使用英文效果最佳
3. quickedit 模型专为快速指令式编辑优化，响应速度快
