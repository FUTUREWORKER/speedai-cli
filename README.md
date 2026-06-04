# Speed AI CLI 使用说明

Speed AI CLI 用于让本地 Agent 通过命令行调用 Speed AI 系统的图片生成功能。

CLI 不直接调用上游图片模型供应商。它会使用用户授权后的系统 token 调用 Speed AI 后端，所以积分扣除、OSS 存储、任务队列、创作历史都和 H5 页面里的生图流程一致。

## 安装

Windows PowerShell：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File D:\speedai-cli\install-speedai-cli.ps1
```

macOS / Linux：

```bash
bash /path/to/speedai-cli/install-speedai-cli.sh
```

安装后重新打开终端，验证命令：

```bash
speedai --help
```

如果当前 Windows 终端暂时找不到 `speedai`，可以临时加入 PATH：

```powershell
$env:Path = "$env:USERPROFILE\.speed-ai\bin;$env:Path"
```

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

## 与 Skill 的关系

当前 Codex skill 名称：

```text
gpt-image-2-image-generation
```

这个 skill 的职责是告诉 Agent：需要生图时调用 `speedai` CLI，而不是直接调用上游 `gpt-image-2` 供应商接口。

Agent 调用链路：

```text
用户自然语言
  -> Agent 触发 gpt-image-2-image-generation skill
  -> Agent 执行 speedai image generate ...
  -> CLI 调用 Speed AI API
  -> 后端完成用户鉴权、扣积分、生图、OSS 存储、创作历史写入
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
