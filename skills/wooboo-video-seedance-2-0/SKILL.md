---
name: wooboo-video-seedance-2-0
description: Generate Seedance 2.0 videos through the Wooboo AI system using authorization, points billing, OSS direct upload, task queues, and creation history.
---

# Wooboo AI Seedance 2.0 视频创作

使用 `wooboo` CLI 作为挖宝AI系统功能入口。不要直连模型供应商，不保存供应商 API Key，不绕过积分扣除和创作历史。

本 skill 面向 Codex、OpenClaw、Hermes 等通用 Agent。Agent 只需要会执行本机命令即可。

## 必须遵守

1. 确认本机已安装 `wooboo`。
2. 如果未授权，运行 `wooboo login web --open`，让用户在挖宝AI H5 页面完成授权。
3. 使用 `wooboo video generate --series seedance` 提交任务。
4. 把返回的任务 id、状态、视频 URL、下载路径反馈给用户。
5. 如果失败，直接展示系统返回的错误，不要改用供应商直连接口。

## 常用命令

文生视频：

```bash
wooboo video generate \
  --series seedance \
  --mode t2v \
  --prompt "城市夜景中的年轻创业者走过玻璃幕墙，霓虹反射，手持咖啡，镜头稳定跟拍" \
  --aspect-ratio 9:16 \
  --duration-seconds 5 \
  --output-dir ./generated-videos
```

图生视频：

```bash
wooboo video generate \
  --series seedance \
  --mode i2v \
  --prompt "让人物轻微转头微笑，背景产生浅景深运动，保持脸部一致" \
  --first-frame /path/to/image.png \
  --aspect-ratio adaptive \
  --duration-seconds 5 \
  --output-dir ./generated-videos
```

参考生视频：

```bash
wooboo video generate \
  --series seedance \
  --mode r2v \
  --prompt "参考人物在简洁工作室中展示产品，镜头缓慢横移，动作自然" \
  --reference-image /path/to/reference.png \
  --aspect-ratio 9:16 \
  --duration-seconds 5 \
  --output-dir ./generated-videos
```

固定镜头：

```bash
wooboo video generate \
  --series seedance \
  --mode t2v \
  --prompt "桌面上的香水瓶被柔和光线扫过，背景保持干净，质感高级" \
  --camera-fixed \
  --aspect-ratio 16:9 \
  --duration-seconds 5
```

## 参数约定

- `--series seedance`：固定使用 Seedance 2.0 系列。
- `--mode`：常用 `t2v`、`i2v`、`r2v`。
- `--aspect-ratio`：支持 `adaptive`、`9:16`、`16:9`、`1:1`、`3:4`、`4:3`。
- `--camera-fixed`：需要固定镜头时使用。
- `--reference-image` / `--reference-video`：`r2v` 模式至少提供 1 个参考素材；Seedance 当前不使用音频或音色参考。
- `--duration-seconds`：常用 5 秒，按系统返回的模型限制为准。
- `--output-dir`：可选，本地下载目录；不传也会进入 H5 创作历史。

## 输出

生成完成后向用户报告：

- 任务 id
- 任务状态
- 视频 URL
- 本地下载路径（如果设置了 `--output-dir`）
