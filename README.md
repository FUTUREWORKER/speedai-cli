# Speed AI CLI 使用说明

Speed AI CLI 用于让本地 Agent 通过命令行调用 Speed AI 系统的图片生成功能。

CLI 不直接调用上游图片模型供应商。它会使用用户授权后的系统 token 调用 Speed AI 后端，所以积分扣除、OSS 存储、任务队列、创作历史都和 H5 页面里的生图流程一致。

## 安装 CLI

推荐使用包管理器安装。当前 GitHub 仓库已经具备 npm 和 pip 安装形态，后续可继续发布到 npm registry、PyPI 和 Homebrew。

npm：

```bash
npm install -g github:FUTUREWORKER/speedai-cli
```

pipx：

```bash
pipx install git+https://github.com/FUTUREWORKER/speedai-cli.git
```

pip：

```bash
pip install git+https://github.com/FUTUREWORKER/speedai-cli.git
```

如果不想使用包管理器，也可以使用安装脚本。

Windows PowerShell：

```powershell
irm https://raw.githubusercontent.com/FUTUREWORKER/speedai-cli/main/install-speedai-cli.ps1 | iex
```

macOS / Linux：

```bash
curl -fsSL https://raw.githubusercontent.com/FUTUREWORKER/speedai-cli/main/install-speedai-cli.sh | bash
```

安装后重新打开终端，验证命令：

```bash
speedai --help
```

如果当前 Windows 终端暂时找不到 `speedai`，可以临时加入 PATH：

```powershell
$env:Path = "$env:USERPROFILE\.speed-ai\bin;$env:Path"
```

Homebrew 目前还没有发布 formula。后续可以新增 Homebrew tap 或提交 formula 后支持：

```bash
brew install speedai-cli
```

## 安装 Agent Skill

CLI 负责执行命令；Agent Skill 负责告诉 Codex、OpenClaw、Hermes 等 Agent 什么时候、如何调用 `speedai`。

本仓库内置 Skill：

```text
skills/gpt-image-2-image-generation
skills/speedai-voice-clone
skills/speedai-voice-list
skills/speedai-audio-synthesis
skills/speedai-digital-human-video
skills/speedai-video-wanx-2-7
skills/speedai-video-seedance-2-0
skills/speedai-video-happyhorse
skills/speedai-long-video-creation
```

如果你的 Agent 支持 `skills` CLI，可以使用类似 libtv 的安装方式：

```bash
npx -y skills add FUTUREWORKER/speedai-cli --skill gpt-image-2-image-generation
npx -y skills add FUTUREWORKER/speedai-cli --skill speedai-voice-clone
npx -y skills add FUTUREWORKER/speedai-cli --skill speedai-voice-list
npx -y skills add FUTUREWORKER/speedai-cli --skill speedai-audio-synthesis
npx -y skills add FUTUREWORKER/speedai-cli --skill speedai-digital-human-video
npx -y skills add FUTUREWORKER/speedai-cli --skill speedai-video-wanx-2-7
npx -y skills add FUTUREWORKER/speedai-cli --skill speedai-video-seedance-2-0
npx -y skills add FUTUREWORKER/speedai-cli --skill speedai-video-happyhorse
npx -y skills add FUTUREWORKER/speedai-cli --skill speedai-long-video-creation
```

不同 Agent 的 skill 目录约定可能不同。如果不支持 `skills` CLI，把上面的目录复制到对应 Agent 的本地 skills/instruction 目录即可。

Codex 示例，Windows PowerShell：

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse -Force ".\skills\gpt-image-2-image-generation" "$env:USERPROFILE\.codex\skills\"
```

Codex 示例，macOS / Linux：

```bash
mkdir -p ~/.codex/skills
cp -R ./skills/gpt-image-2-image-generation ~/.codex/skills/
```

OpenClaw、Hermes 或其他 Agent 使用时，请复制 `skills/` 下需要的 skill 目录到对应 Agent 的 skill/instruction 目录，并保持目录内 `SKILL.md` 文件不变。

安装后，Agent 看到图片生成需求时应优先调用 `speedai` CLI，而不是直连模型供应商。

## 授权登录

发起网页登录授权：

```bash
speedai login web --open
```

默认会连接生产环境 `https://speed.ycszai.com`。执行后会打开 H5 授权页。如果未登录，需要先登录 H5 账号，然后点击确认授权。

授权凭据保存在本机：

```text
~/.speed-ai/credentials.json
```

不要把这个文件或其中的 token 发给别人，也不要粘贴到聊天里。

查看当前授权账号：

```bash
speedai account
```

退出登录：

```bash
speedai logout
```

## 生成图片

基础用法：

```bash
speedai image generate --prompt "一张高级棚拍产品图，黑色无线音箱放在混凝土桌面上"
```

带参数：

```bash
speedai image generate \
  --prompt "一张高级棚拍产品图，黑色无线音箱放在混凝土桌面上" \
  --aspect-ratio auto \
  --quality 1k
```

带参考图：

```bash
speedai image generate \
  --prompt "把参考图改成高级棚拍产品图" \
  --reference-image /path/to/reference.png \
  --aspect-ratio 1:1 \
  --quality 1k
```

Windows PowerShell 多行命令使用反引号：

```powershell
speedai image generate `
  --prompt "一张高级棚拍产品图，黑色无线音箱放在混凝土桌面上" `
  --aspect-ratio auto `
  --quality 1k
```

生成成功后，记录会出现在用户 H5 创作历史中。

## 视频创作

视频创作同样通过系统接口提交任务，积分扣除、任务队列、OSS 存储和 H5 创作历史都由 Speed AI 后端处理。

万相 2.7：
```bash
speedai video generate \
  --series wanx \
  --mode t2v \
  --prompt "一段高级产品宣传短片，黑色无线音箱放在混凝土桌面上，镜头缓慢推进，电影感灯光" \
  --aspect-ratio 9:16 \
  --duration-seconds 5 \
  --output-dir ./generated-videos
```

Seedance 2.0：
```bash
speedai video generate \
  --series seedance \
  --mode i2v \
  --prompt "让人物轻微转头微笑，背景产生浅景深运动，保持脸部一致" \
  --first-frame /path/to/image.png \
  --aspect-ratio adaptive \
  --duration-seconds 5 \
  --output-dir ./generated-videos
```

快乐马：
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

常用参数：
- `--series`：模型系列，支持 `wanx`、`seedance`、`happyhorse`
- `--mode`：创作模式，常用 `t2v`、`i2v`、`r2v`
- `--first-frame`：图生视频首帧图片
- `--reference-image`：参考图，可重复传入
- `--reference-video`：参考视频，可重复传入；快乐马不使用视频参考
- `--output-dir`：可选，本地下载目录

## 长视频创作

长视频创作会按系统流程创建项目、生成分镜、生成全部分镜视频并导出最终视频。生成结果会进入用户 H5 创作历史。

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

常用参数：
- `--prompt`：整条长视频的主题、角色、风格、节奏和目标
- `--reference`：参考图或参考视频文件，必填
- `--voice`：可选，音色/声音参考文件
- `--aspect-ratio`：`9:16` 或 `16:9`
- `--output-dir`：可选，本地下载目录

## 声音克隆

```bash
speedai voice clone --audio /path/to/sample.wav --prefix "我的音色" --language zh
```

返回的 `item.id` 是系统内的音色记录 ID，后续声音合成和数字人视频合成都使用它作为 `--voice-record-id`。

## 音色查询

```bash
speedai voice list
```

常用字段：

- `voices[].id`：系统音色记录 ID
- `voices[].voiceName`：音色名称
- `voices[].voiceId`：供应商音色 ID
- `voices[].cloneStatus`：克隆状态

## 声音合成

```bash
speedai audio synthesize \
  --text "大家好，欢迎来到极速 AI。" \
  --voice-record-id <voice-record-id> \
  --language zh \
  --speech-rate 1 \
  --pitch-rate 1 \
  --volume 50 \
  --output-dir ./generated-audio
```

生成数字人视频前，通常需要先用这个命令生成音频，并记录返回的 `audioUrl` 和 `audioDuration`。

## 数字人视频合成

```bash
speedai digital-human generate \
  --image /path/to/portrait.png \
  --text "大家好，欢迎来到极速 AI。" \
  --voice-record-id <voice-record-id> \
  --audio-url <audio-url> \
  --audio-duration 12.3 \
  --language zh \
  --model XPro1.0 \
  --output-dir ./generated-videos
```

`--audio-url` 和 `--audio-duration` 通常来自 `speedai audio synthesize` 的返回结果。生成成功后，视频会进入用户 H5 创作历史。

## 下载目录

单次指定下载目录：

```bash
speedai image generate --prompt "..." --output-dir /path/to/images
```

设置默认下载目录：

```bash
speedai config set output-dir /path/to/images
```

Windows 示例：

```powershell
speedai config set output-dir D:\speed-ai\generated-images
```

查看配置：

```bash
speedai config list
speedai config get output-dir
```

清除默认下载目录：

```bash
speedai config unset output-dir
```

配置文件位置：

```text
~/.speed-ai/config.json
```

下载目录优先级：

1. 命令行参数 `--output-dir`
2. 环境变量 `SPEEDAI_OUTPUT_DIR`
3. 持久配置 `speedai config set output-dir ...`

## 环境地址配置

默认地址：

```text
API: https://speed.ycszai.com
H5:  https://speed.ycszai.com
```

正式使用不需要额外配置地址。需要固定使用某个环境时，可以写入持久配置：

```bash
speedai config set api-base https://speed.ycszai.com
speedai config set h5-base https://speed.ycszai.com
```

查看地址配置：

```bash
speedai config get api-base
speedai config get h5-base
speedai config list
```

清除地址配置后会回到默认生产地址：

```bash
speedai config unset api-base
speedai config unset h5-base
```

本地开发单次指定：

```bash
speedai --api-base http://127.0.0.1:3000 --h5-base http://127.0.0.1:5174 login web --open
```

也可以用环境变量：

```bash
SPEEDAI_API_BASE=http://127.0.0.1:3000
SPEEDAI_H5_BASE=http://127.0.0.1:5174
SPEEDAI_OUTPUT_DIR=/path/to/images
```

Windows PowerShell：

```powershell
$env:SPEEDAI_API_BASE="http://127.0.0.1:3000"
$env:SPEEDAI_H5_BASE="http://127.0.0.1:5174"
$env:SPEEDAI_OUTPUT_DIR="D:\speed-ai\generated-images"
```

地址优先级：

1. 命令行参数 `--api-base` / `--h5-base`
2. 环境变量 `SPEEDAI_API_BASE` / `SPEEDAI_H5_BASE`
3. 持久配置 `speedai config set api-base ...` / `speedai config set h5-base ...`
4. 默认生产地址 `https://speed.ycszai.com`

注意：授权 token 和授权时的 API 地址绑定。切换环境后需要重新执行 `speedai login web --open`。

## 与 Agent Skill 的关系

当前通用 Agent Skill 名称：

```text
gpt-image-2-image-generation
speedai-voice-clone
speedai-voice-list
speedai-audio-synthesis
speedai-digital-human-video
speedai-video-wanx-2-7
speedai-video-seedance-2-0
speedai-video-happyhorse
speedai-long-video-creation
```

这些 skill 的职责是告诉 Agent：需要媒体创作时调用 `speedai` CLI，而不是直接调用上游模型供应商接口。

Agent 调用链路：

```text
用户自然语言
  -> Agent 触发对应 Speed AI skill
  -> Agent 执行 speedai image/video/audio/digital-human ...
  -> CLI 调用 Speed AI API
  -> 后端完成用户鉴权、扣积分、任务队列、OSS 存储、创作历史写入
```

Agent 常用命令：

```bash
speedai image generate --prompt "..." --aspect-ratio auto --quality 1k
```

如果用户还没有授权 CLI，先执行：

```bash
speedai login web --open
```

## 重要约束

- CLI 是系统功能入口，不是模型供应商直连工具。
- CLI 不绕过积分扣除。
- CLI 不绕过创作历史。
- CLI 不保存模型供应商 API Key。
- CLI 生成的图片会进入用户 H5 创作历史。
- 授权 token 只保存在本机 `~/.speed-ai/credentials.json`。
