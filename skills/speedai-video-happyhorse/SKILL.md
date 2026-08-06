---
name: speedai-video-happyhorse
description: Generate HappyHorse videos through the Wooboo AI system using authorization, points billing, OSS direct upload, task queues, and creation history.
---

# Wooboo AI 快乐马视频创作

使用 `speedai` CLI 作为挖宝AI系统功能入口。不要直连模型供应商，不保存供应商 API Key，不绕过积分扣除和创作历史。

本 skill 面向 Codex、OpenClaw、Hermes 等通用 Agent。Agent 只需要会执行本机命令即可。

## 必须遵守

1. 确认本机已安装 `speedai`。
2. 如果未授权，运行 `speedai login web --open`，让用户在挖宝AI H5 页面完成授权。
3. 使用 `speedai video generate --series happyhorse` 提交任务。
4. 把返回的任务 id、状态、视频 URL、下载路径反馈给用户。
5. 如果失败，直接展示系统返回的错误，不要改用供应商直连接口。

## 常用命令

文生视频：

```bash
speedai video generate \
  --series happyhorse \
  --mode t2v \
  --prompt "一只可爱的品牌吉祥物在明亮展厅中向镜头挥手，动作夸张但流畅，镜头稳定" \
  --aspect-ratio 9:16 \
  --duration-seconds 5 \
  --output-dir ./generated-videos
```

图生视频：

```bash
speedai video generate \
  --series happyhorse \
  --mode i2v \
  --prompt "让图片中的角色做一个自然挥手动作，保持脸部和服装一致" \
  --first-frame /path/to/image.png \
  --aspect-ratio 9:16 \
  --duration-seconds 5 \
  --output-dir ./generated-videos
```

参考图生视频：

```bash
speedai video generate \
  --series happyhorse \
  --mode r2v \
  --prompt "参考图中的角色在简洁舞台上做展示动作，镜头固定，动作自然" \
  --reference-image /path/to/reference.png \
  --aspect-ratio 9:16 \
  --duration-seconds 5 \
  --output-dir ./generated-videos
```

Windows PowerShell：

```powershell
speedai video generate `
  --series happyhorse `
  --mode r2v `
  --prompt "参考图中的角色在简洁舞台上做展示动作，镜头固定，动作自然" `
  --reference-image C:\path\to\reference.png `
  --aspect-ratio 9:16 `
  --duration-seconds 5 `
  --output-dir .\generated-videos
```

## 参数约定

- `--series happyhorse`：固定使用快乐马系列。
- `--mode`：常用 `t2v`、`i2v`、`r2v`。
- `--reference-image`：快乐马参考生视频只使用图片参考，不使用视频或音频参考。
- `--aspect-ratio`：常用 `9:16`、`16:9`、`1:1`。
- `--duration-seconds`：常用 5 秒，按系统返回的模型限制为准。
- `--output-dir`：可选，本地下载目录；不传也会进入 H5 创作历史。

## 输出

生成完成后向用户报告：

- 任务 id
- 任务状态
- 视频 URL
- 本地下载路径（如果设置了 `--output-dir`）
