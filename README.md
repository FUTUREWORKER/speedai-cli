# Wooboo AI CLI

`wooboo` 是挖宝AI（Wooboo AI）的本地命令行入口。它使用用户网页登录授权后的系统 token 调用平台 API，不直连模型供应商；积分扣除、任务队列、OSS 存储和创作历史均由平台统一处理。

项目、仓库和发行包名称统一为 `wooboo-ai-cli`，命令名为 `wooboo`，本机配置目录为 `~/.wooboo-ai`。CLI 只有一个版本，通过配置切换生产或本地开发环境。

## 安装 CLI

npm：

```bash
npm install -g github:FUTUREWORKER/wooboo-ai-cli
```

pipx：

```bash
pipx install git+https://github.com/FUTUREWORKER/wooboo-ai-cli.git
```

pip：

```bash
pip install git+https://github.com/FUTUREWORKER/wooboo-ai-cli.git
```

Windows PowerShell raw 安装：

```powershell
irm https://raw.githubusercontent.com/FUTUREWORKER/wooboo-ai-cli/main/install-wooboo-ai-cli.ps1 | iex
```

macOS / Linux raw 安装：

```bash
curl -fsSL https://raw.githubusercontent.com/FUTUREWORKER/wooboo-ai-cli/main/install-wooboo-ai-cli.sh | bash
```

验证：

```bash
wooboo --version
wooboo --help
```

如果 Windows 当前终端暂时找不到命令，可以临时加入 PATH：

```powershell
$env:Path = "$env:USERPROFILE\.wooboo-ai\bin;$env:Path"
```

Homebrew formula 尚未发布。

## 安装 Agent Skills

CLI 负责执行命令，Agent Skill 负责告诉 Codex、OpenClaw、Hermes 等 Agent 何时以及如何调用 `wooboo`。

推荐按需安装：

```bash
npx -y skills add FUTUREWORKER/wooboo-ai-cli --skill wooboo-image-generation
npx -y skills add FUTUREWORKER/wooboo-ai-cli --skill gpt-image-2-image-generation
npx -y skills add FUTUREWORKER/wooboo-ai-cli --skill wooboo-video-wanx-2-7
npx -y skills add FUTUREWORKER/wooboo-ai-cli --skill wooboo-video-seedance-2-0
npx -y skills add FUTUREWORKER/wooboo-ai-cli --skill wooboo-video-happyhorse
npx -y skills add FUTUREWORKER/wooboo-ai-cli --skill wooboo-video-kling-3-0
npx -y skills add FUTUREWORKER/wooboo-ai-cli --skill wooboo-long-video-creation
npx -y skills add FUTUREWORKER/wooboo-ai-cli --skill wooboo-digital-human-avatar
npx -y skills add FUTUREWORKER/wooboo-ai-cli --skill wooboo-voice-clone
npx -y skills add FUTUREWORKER/wooboo-ai-cli --skill wooboo-voice-list
npx -y skills add FUTUREWORKER/wooboo-ai-cli --skill wooboo-digital-human-video
```

不支持 `skills` CLI 时，可把对应的 `skills/<skill-name>` 目录复制到 Agent 的 skill/instruction 目录。所有 Skill 都是 Agent 通用说明，不依赖 Codex 专属能力。

Codex、OpenClaw、Hermes 或其他能够读取本地 instruction/skill 文件并执行命令的 Agent，都可以使用同一份目录。

## 登录授权

```bash
wooboo login web --open
```

默认连接生产环境 `https://wooboo.ycszai.com`。用户需要在打开的 H5 页面中登录并确认授权。

凭据只保存在本机：

```text
~/.wooboo-ai/credentials.json
```

查看账号和积分：

```bash
wooboo account
```

退出：

```bash
wooboo logout
```

## 图片生成

先查看系统当前启用的模型、档位、比例和积分：

```bash
wooboo image models
```

使用系统默认模型和档位：

```bash
wooboo image generate --prompt "高级棚拍产品图，黑色无线音箱放在混凝土桌面上"
```

指定模型和规格：

```bash
wooboo image generate \
  --model gpt-image-2 \
  --prompt "把参考图改成高级棚拍产品图" \
  --reference-image /path/to/reference.png \
  --aspect-ratio 1:1 \
  --quality 2k \
  --output-dir ./generated-images
```

`--model` 可以使用 bootstrap 返回的模型展示名或底层模型名；也可以用 `--model-config-id` 精确指定后台配置。省略比例、质量和档位时，CLI 会使用该模型当前启用的默认配置，不再硬编码 `1k`。

## 视频生成

查看当前视频系列、模型能力和档位：

```bash
wooboo video models
```

CLI 支持系统当前的 `wanx`、`seedance`、`happyhorse` 和 `kling` 系列，并会按 `mode` 自动选择真正支持该模式的模型配置。

万相文生视频：

```bash
wooboo video generate \
  --series wanx \
  --mode t2v \
  --prompt "高级产品宣传短片，镜头缓慢推进，电影感灯光" \
  --duration-seconds 5 \
  --output-dir ./generated-videos
```

Seedance 图生视频：

```bash
wooboo video generate \
  --series seedance \
  --mode i2v \
  --prompt "让人物轻微转头微笑，保持脸部一致" \
  --first-frame /path/to/image.png \
  --duration-seconds 5
```

快乐马参考生视频：

```bash
wooboo video generate \
  --series happyhorse \
  --mode r2v \
  --prompt "参考角色在简洁舞台上做自然展示动作" \
  --reference-image /path/to/reference.png
```

可灵 3.0 混合参考素材：

```bash
wooboo video generate \
  --series kling \
  --mode r2v \
  --prompt "保持人物和产品一致，生成电影感品牌短片" \
  --reference-image /path/to/person.png \
  --reference-image /path/to/product.png \
  --reference-video /path/to/motion.mp4
```

本地视频素材会先通过平台签发的短期 URL 流式直传 OSS，再把上传记录 ID 交给生成任务。CLI 不保存 OSS 凭据，也不会把大视频整体读入内存。

## 长视频创作

长视频命令会自动创建项目、生成分镜、生成全部分镜并导出：

```bash
wooboo long-video generate \
  --prompt "制作一条约 30 秒的产品发布视频，科技感，镜头连贯" \
  --reference /path/to/reference.png \
  --aspect-ratio 9:16 \
  --output-dir ./generated-videos
```

带音色参考：

```bash
wooboo long-video generate \
  --prompt "制作一条商务口播品牌介绍视频" \
  --reference /path/to/reference.mp4 \
  --voice /path/to/voice.wav
```

## 数字人形象

新版数字人需要先用训练视频创建可复用形象，不再支持旧版单张图片一次性合成。

创建形象并等待训练完成：

```bash
wooboo avatar create --video /path/to/avatar-training.mp4 --title "品牌主理人"
```

查询形象：

```bash
wooboo avatar list
```

删除形象：

```bash
wooboo avatar delete <avatar-record-id>
```

非 H.264 训练视频由平台后台按系统规则转码。CLI 会轮询到 `ready` 或 `failed`。

## 音色克隆

```bash
wooboo voice clone \
  --audio /path/to/sample.wav \
  --name "我的音色" \
  --language zh
```

`--prefix` 仍作为 `--name` 的兼容别名。音色克隆是异步任务，CLI 默认等待到 `ready`、`failed` 或 `migration_pending`。

查询和删除音色：

```bash
wooboo voice list
wooboo voice delete <voice-record-id>
```

## 数字人视频

文本驱动：

```bash
wooboo digital-human generate \
  --drive-mode text \
  --avatar-record-id <avatar-record-id> \
  --voice-record-id <voice-record-id> \
  --text "大家好，欢迎来到挖宝AI。" \
  --subtitle \
  --output-dir ./generated-videos
```

声音驱动：

```bash
wooboo digital-human generate \
  --drive-mode audio \
  --avatar-record-id <avatar-record-id> \
  --audio /path/to/drive-audio.mp3 \
  --title "声音驱动演示" \
  --output-dir ./generated-videos
```

任务可能进入 `payment_pending`。CLI 会继续轮询，用户补足积分后平台会继续结算。

旧 `wooboo audio synthesize` 独立音频接口已经下线。CLI 暂时保留该命令用于返回明确迁移提示，不再向已删除的接口提交请求。

## 下载目录

单次通过 `--output-dir` 指定，或设置默认值：

```bash
wooboo config set output-dir /path/to/generated-media
wooboo config get output-dir
wooboo config unset output-dir
```

优先级：

1. `--output-dir`
2. `WOOBOO_OUTPUT_DIR`
3. `wooboo config set output-dir ...`

## 环境配置

默认生产地址：

```text
API: https://wooboo.ycszai.com
H5:  https://wooboo.ycszai.com
```

持久配置：

```bash
wooboo config set api-base https://wooboo.ycszai.com
wooboo config set h5-base https://wooboo.ycszai.com
wooboo config list
```

本地开发单次覆盖：

```bash
wooboo --api-base http://127.0.0.1:3000 --h5-base http://127.0.0.1:5174 login web --open
```

也可以使用：

```text
WOOBOO_API_BASE
WOOBOO_H5_BASE
WOOBOO_OUTPUT_DIR
```

授权 token 与授权时的 API 地址绑定，切换环境后需要重新登录。

## Agent 调用链

```text
用户自然语言
  -> Agent 触发对应通用 Skill
  -> Agent 执行 wooboo image/video/avatar/voice/digital-human ...
  -> CLI 调用 Wooboo AI 系统 API
  -> 后端完成用户鉴权、积分、任务队列、OSS 和创作历史
```

## 重要约束

- CLI 是系统功能入口，不是模型供应商直连工具。
- CLI 不绕过积分扣除和创作历史。
- CLI 不保存模型供应商 API Key 或 OSS Key。
- 授权 token 只保存在本机 `~/.wooboo-ai/credentials.json`。
- 不要把凭据文件、生成媒体或本地测试输出提交到仓库。
