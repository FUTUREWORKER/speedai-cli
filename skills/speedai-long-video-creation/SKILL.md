---
name: speedai-long-video-creation
description: Generate long videos through the Speed AI system using the logged-in user's authorization, storyboard generation, scene generation, export, points billing, OSS storage, and H5 creation history.
---

# Speed AI 长视频创作

使用 Speed AI CLI 作为系统功能入口。不要直连模型供应商，不保存供应商 API Key，不绕过积分扣除和创作历史。

本 skill 面向 Codex、OpenClaw、Hermes 等通用 Agent。Agent 只需要会执行本机命令即可。

## 必须遵守

1. 确认本机已安装 `speedai`。
2. 如果未授权，运行 `speedai login web --open`，让用户在 Speed AI H5 页面完成授权。
3. 长视频创作必须提供一个参考图或参考视频文件。
4. 使用 `speedai long-video generate` 提交任务。
5. 把返回的项目 id、状态、分镜数量、最终视频 URL、下载路径反馈给用户。
6. 如果失败，直接展示系统返回的错误，不要改用供应商直连接口。

## 命令

```bash
speedai long-video generate \
  --prompt "制作一条 30 秒左右的产品发布长视频，参考图中的智能音箱作为主角，整体风格高级、科技感、镜头节奏流畅" \
  --reference /path/to/reference.png \
  --aspect-ratio 9:16 \
  --output-dir ./generated-videos
```

带音色参考：

```bash
speedai long-video generate \
  --prompt "制作一条口播风格的品牌介绍长视频，语气自信、节奏清晰，画面保持商务科技感" \
  --reference /path/to/reference.mp4 \
  --voice /path/to/voice.wav \
  --aspect-ratio 16:9 \
  --output-dir ./generated-videos
```

Windows PowerShell：

```powershell
speedai long-video generate `
  --prompt "制作一条 30 秒左右的产品发布长视频，参考图中的智能音箱作为主角，整体风格高级、科技感、镜头节奏流畅" `
  --reference C:\path\to\reference.png `
  --aspect-ratio 9:16 `
  --output-dir .\generated-videos
```

## 参数约定

- `--prompt`：必填，描述整条长视频的主题、角色、风格、节奏和目标。
- `--reference`：必填，参考图或参考视频文件。
- `--voice`：可选，音色/声音参考文件。
- `--aspect-ratio`：`9:16` 或 `16:9`。
- `--variant-key`：可选，指定系统模型档位；不传则使用系统默认档位。
- `--output-dir`：可选，本地下载目录；不传也会进入 H5 创作历史。

## 执行流程

CLI 会按系统流程依次执行：

1. 创建长视频项目。
2. 生成分镜。
3. 生成全部分镜视频。
4. 导出最终长视频。
5. 可选下载最终 MP4。

## 输出

生成完成后向用户报告：

- 项目 id
- 项目状态
- 分镜数量
- 最终视频 URL
- 本地下载路径（如果设置了 `--output-dir`）

