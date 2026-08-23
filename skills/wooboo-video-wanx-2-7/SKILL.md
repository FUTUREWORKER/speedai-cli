---
name: wooboo-video-wanx-2-7
description: Generate Wanx 2.7 videos through the Wooboo AI system using authorization, points billing, OSS direct upload, task queues, and creation history.
---

# Wooboo AI 万相 2.7 视频创作

使用 `wooboo` CLI 作为挖宝AI系统功能入口。不要直连模型供应商，不保存供应商 API Key，不绕过积分扣除和创作历史。

本 skill 面向 Codex、OpenClaw、Hermes 等通用 Agent。Agent 只需要会执行本机命令即可。

## 必须遵守

1. 确认本机已安装 `wooboo`。
2. 如果未授权，运行 `wooboo login web --open`，让用户在挖宝AI H5 页面完成授权。
3. 使用 `wooboo video generate --series wanx` 提交任务。
4. 把返回的任务 id、状态、视频 URL、下载路径反馈给用户。
5. 如果失败，直接展示系统返回的错误，不要改用供应商直连接口。

## 常用命令

文生视频：

```bash
wooboo video generate \
  --series wanx \
  --mode t2v \
  --prompt "一段高级产品宣传短片，黑色无线音箱放在混凝土桌面上，镜头缓慢推进，电影感灯光" \
  --aspect-ratio 9:16 \
  --duration-seconds 5 \
  --output-dir ./generated-videos
```

图生视频：

```bash
wooboo video generate \
  --series wanx \
  --mode i2v \
  --prompt "让画面中的产品缓慢旋转，背景光线流动，保持主体细节稳定" \
  --first-frame /path/to/image.png \
  --aspect-ratio 9:16 \
  --duration-seconds 5 \
  --output-dir ./generated-videos
```

参考生视频：

```bash
wooboo video generate \
  --series wanx \
  --mode r2v \
  --prompt "参考素材中的角色走进未来感展厅，镜头跟拍，动作自然" \
  --reference-image /path/to/reference.png \
  --aspect-ratio 9:16 \
  --duration-seconds 5 \
  --output-dir ./generated-videos
```

Windows PowerShell 使用反引号换行：

```powershell
wooboo video generate `
  --series wanx `
  --mode t2v `
  --prompt "一段高级产品宣传短片，黑色无线音箱放在混凝土桌面上，镜头缓慢推进，电影感灯光" `
  --aspect-ratio 9:16 `
  --duration-seconds 5 `
  --output-dir .\generated-videos
```

## 参数约定

- `--series wanx`：固定使用万相 2.7 系列。
- `--mode`：常用 `t2v`、`i2v`、`r2v`。
- `--prompt`：必填，写清主体、动作、镜头、场景、风格。
- `--first-frame`：`i2v` 模式必填 1 张图片。
- `--reference-image` / `--reference-video`：`r2v` 模式至少提供 1 个参考素材；可重复传入。
- `--aspect-ratio`：常用 `9:16`、`16:9`、`1:1`。
- `--duration-seconds`：常用 5 秒；参考生视频包含视频素材时不要超过 10 秒。
- `--output-dir`：可选，本地下载目录；不传也会进入 H5 创作历史。

## 输出

生成完成后向用户报告：

- 任务 id
- 任务状态
- 视频 URL
- 本地下载路径（如果设置了 `--output-dir`）
