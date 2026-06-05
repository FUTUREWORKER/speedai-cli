#!/usr/bin/env python3
import argparse
import json
import mimetypes
import os
import sys
import time
import uuid
import webbrowser
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


DEFAULT_API_BASE = "https://speed.ycszai.com"
DEFAULT_H5_BASE = "https://speed.ycszai.com"
CONFIG_DIR = Path.home() / ".speed-ai"
CREDENTIALS_PATH = CONFIG_DIR / "credentials.json"
CONFIG_PATH = CONFIG_DIR / "config.json"


def parse_args():
    parser = argparse.ArgumentParser(description="Speed AI CLI for user-authorized system image generation.")
    parser.add_argument("--api-base", default="", help="API base URL. Overrides SPEEDAI_API_BASE and config.")
    parser.add_argument("--h5-base", default="", help="H5 web base URL. Overrides SPEEDAI_H5_BASE and config.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    login = subparsers.add_parser("login")
    login_sub = login.add_subparsers(dest="login_command", required=True)
    login_web = login_sub.add_parser("web")
    login_web.add_argument("--open", action="store_true", help="Open the authorization URL in the default browser.")
    login_web.add_argument("--client-name", default="Speed AI CLI")
    login_web.add_argument("--poll-interval", type=float, default=2.0)

    subparsers.add_parser("logout")
    subparsers.add_parser("account")

    config = subparsers.add_parser("config")
    config_sub = config.add_subparsers(dest="config_command", required=True)
    config_sub.add_parser("list")
    config_get = config_sub.add_parser("get")
    config_get.add_argument("key", choices=["api-base", "h5-base", "output-dir"])
    config_set = config_sub.add_parser("set")
    config_set.add_argument("key", choices=["api-base", "h5-base", "output-dir"])
    config_set.add_argument("value")
    config_unset = config_sub.add_parser("unset")
    config_unset.add_argument("key", choices=["api-base", "h5-base", "output-dir"])

    image = subparsers.add_parser("image")
    image_sub = image.add_subparsers(dest="image_command", required=True)
    generate = image_sub.add_parser("generate")
    generate.add_argument("--prompt", required=True)
    generate.add_argument("--scene", default="图片生成")
    generate.add_argument("--aspect-ratio", default="auto")
    generate.add_argument("--quality", default="1k")
    generate.add_argument("--variant-key", default="")
    generate.add_argument("--model-config-id", default="")
    generate.add_argument("--reference-image", action="append", default=[])
    generate.add_argument("--wait", action=argparse.BooleanOptionalAction, default=True)
    generate.add_argument("--poll-interval", type=float, default=3.0)
    generate.add_argument("--timeout", type=int, default=600)
    generate.add_argument("--output-dir", default="")

    voice = subparsers.add_parser("voice")
    voice_sub = voice.add_subparsers(dest="voice_command", required=True)
    voice_sub.add_parser("list")
    voice_clone = voice_sub.add_parser("clone")
    voice_clone.add_argument("--audio", required=True)
    voice_clone.add_argument("--prefix", default="我的音色")
    voice_clone.add_argument("--sex", type=int, default=0)
    voice_clone.add_argument("--language", default="")

    audio = subparsers.add_parser("audio")
    audio_sub = audio.add_subparsers(dest="audio_command", required=True)
    synthesize = audio_sub.add_parser("synthesize")
    synthesize.add_argument("--text", required=True)
    synthesize.add_argument("--voice-record-id", required=True)
    synthesize.add_argument("--language", default="")
    synthesize.add_argument("--speech-rate", type=float, default=0)
    synthesize.add_argument("--pitch-rate", type=float, default=0)
    synthesize.add_argument("--volume", type=float, default=50)
    synthesize.add_argument("--prompt", default="")
    synthesize.add_argument("--wait", action=argparse.BooleanOptionalAction, default=True)
    synthesize.add_argument("--poll-interval", type=float, default=3.0)
    synthesize.add_argument("--timeout", type=int, default=600)
    synthesize.add_argument("--output-dir", default="")

    human = subparsers.add_parser("digital-human")
    human_sub = human.add_subparsers(dest="human_command", required=True)
    human_generate = human_sub.add_parser("generate")
    human_generate.add_argument("--image", required=True)
    human_generate.add_argument("--text", required=True)
    human_generate.add_argument("--voice-record-id", required=True)
    human_generate.add_argument("--audio-url", required=True)
    human_generate.add_argument("--audio-duration", type=float, required=True)
    human_generate.add_argument("--language", default="")
    human_generate.add_argument("--speech-rate", type=float, default=0)
    human_generate.add_argument("--pitch-rate", type=float, default=0)
    human_generate.add_argument("--volume", type=float, default=50)
    human_generate.add_argument("--model", default="")
    human_generate.add_argument("--prompt", default="")
    human_generate.add_argument("--video-prompt", default="")
    human_generate.add_argument("--wait", action=argparse.BooleanOptionalAction, default=True)
    human_generate.add_argument("--poll-interval", type=float, default=5.0)
    human_generate.add_argument("--timeout", type=int, default=1200)
    human_generate.add_argument("--output-dir", default="")

    return parser.parse_args()


def normalize_base(url):
    return url.rstrip("/")


def resolve_api_base(args):
    return normalize_base(
        args.api_base
        or os.environ.get("SPEEDAI_API_BASE", "")
        or str(load_config().get("api_base", "") or "")
        or DEFAULT_API_BASE
    )


def resolve_h5_base(args):
    return normalize_base(
        args.h5_base
        or os.environ.get("SPEEDAI_H5_BASE", "")
        or str(load_config().get("h5_base", "") or "")
        or DEFAULT_H5_BASE
    )


def request_json(method, url, payload=None, token="", timeout=30):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {}
    if payload is not None:
        headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")
            return response.status, json.loads(body) if body else {}
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        try:
            payload = json.loads(body)
            message = payload.get("message") or payload.get("error", {}).get("message") or body
        except json.JSONDecodeError:
            message = body
        raise RuntimeError(f"HTTP {error.code}: {message}") from error


def encode_multipart(fields, files):
    boundary = f"----speedai-{uuid.uuid4().hex}"
    chunks = []
    for name, value in fields:
        chunks.append(f"--{boundary}\r\n".encode("utf-8"))
        chunks.append(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8"))
        chunks.append(str(value).encode("utf-8"))
        chunks.append(b"\r\n")
    for name, path in files:
        file_path = Path(path).expanduser().resolve()
        if not file_path.is_file():
            raise RuntimeError(f"Reference image does not exist: {file_path}")
        content_type = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
        chunks.append(f"--{boundary}\r\n".encode("utf-8"))
        chunks.append(
            (
                f'Content-Disposition: form-data; name="{name}"; filename="{file_path.name}"\r\n'
                f"Content-Type: {content_type}\r\n\r\n"
            ).encode("utf-8")
        )
        chunks.append(file_path.read_bytes())
        chunks.append(b"\r\n")
    chunks.append(f"--{boundary}--\r\n".encode("utf-8"))
    return b"".join(chunks), f"multipart/form-data; boundary={boundary}"


def request_multipart(url, fields, files, token, timeout=60):
    data, content_type = encode_multipart(fields, files)
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Authorization": f"Bearer {token}", "Content-Type": content_type},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        try:
            payload = json.loads(body)
            message = payload.get("message") or payload.get("error", {}).get("message") or body
        except json.JSONDecodeError:
            message = body
        raise RuntimeError(f"HTTP {error.code}: {message}") from error


def save_credentials(api_base, h5_base, token, user):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CREDENTIALS_PATH.write_text(
        json.dumps(
            {
                "api_base": api_base,
                "h5_base": h5_base,
                "token": token,
                "user": user,
                "saved_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def load_credentials():
    if not CREDENTIALS_PATH.is_file():
        raise RuntimeError("Not logged in. Run: speedai login web")
    return json.loads(CREDENTIALS_PATH.read_text(encoding="utf-8"))


def load_config():
    if not CONFIG_PATH.is_file():
        return {}
    data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def save_config(config):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")


def normalize_config_key(key):
    if key == "api-base":
        return "api_base"
    if key == "h5-base":
        return "h5_base"
    if key == "output-dir":
        return "output_dir"
    raise RuntimeError(f"Unsupported config key: {key}")


def login_web(args):
    api_base = resolve_api_base(args)
    h5_base = resolve_h5_base(args)
    _, grant = request_json("POST", f"{api_base}/api/cli/auth/grants", {"clientName": args.client_name})
    code = grant["code"]
    authorize_url = f"{h5_base}/cli/authorize?code={urllib.parse.quote(code)}"
    print(f"Open this URL to authorize:\n{authorize_url}", flush=True)
    if args.open:
        webbrowser.open(authorize_url)
    while True:
        status, payload = request_json("POST", f"{api_base}/api/cli/auth/grants/{code}/exchange")
        if status == 200:
            save_credentials(api_base, h5_base, payload["token"], payload["user"])
            print(json.dumps({"ok": True, "user": payload["user"], "credentials": str(CREDENTIALS_PATH)}, ensure_ascii=False))
            return
        time.sleep(max(0.5, args.poll_interval))


def logout(_args):
    if CREDENTIALS_PATH.exists():
        CREDENTIALS_PATH.unlink()
    print(json.dumps({"ok": True}, ensure_ascii=False))


def account(_args):
    credentials = load_credentials()
    api_base = normalize_base(credentials.get("api_base") or DEFAULT_API_BASE)
    token = credentials["token"]
    _, payload = request_json("GET", f"{api_base}/api/auth/user/me", token=token)
    credentials["user"] = payload["user"]
    save_credentials(api_base, credentials.get("h5_base") or DEFAULT_H5_BASE, token, payload["user"])
    print(json.dumps(payload, ensure_ascii=False))


def config_list(_args):
    print(json.dumps(load_config(), ensure_ascii=False, indent=2))


def config_get(args):
    key = normalize_config_key(args.key)
    config = load_config()
    print(json.dumps({key: config.get(key, "")}, ensure_ascii=False))


def config_set(args):
    key = normalize_config_key(args.key)
    value = args.value.strip()
    if not value:
        raise RuntimeError(f"{args.key} cannot be empty")
    if key in ("api_base", "h5_base"):
        value = normalize_base(value)
        parsed = urllib.parse.urlparse(value)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            raise RuntimeError(f"{args.key} must be an http(s) URL")
    elif key == "output_dir":
        if not value:
            raise RuntimeError("output-dir cannot be empty")
        value = str(Path(value).expanduser().resolve())
    config = load_config()
    config[key] = value
    save_config(config)
    print(json.dumps({"ok": True, key: value, "config": str(CONFIG_PATH)}, ensure_ascii=False))


def config_unset(args):
    key = normalize_config_key(args.key)
    config = load_config()
    removed = key in config
    config.pop(key, None)
    save_config(config)
    print(json.dumps({"ok": True, "removed": removed, "config": str(CONFIG_PATH)}, ensure_ascii=False))


def download_record(api_base, token, record_id, output_dir):
    output_path = Path(output_dir).expanduser().resolve()
    output_path.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(
        f"{api_base}/api/h5/image-generations/{urllib.parse.quote(record_id)}/download",
        headers={"Authorization": f"Bearer {token}"},
        method="GET",
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        content_type = response.headers.get("content-type", "image/png").split(";")[0]
        extension = mimetypes.guess_extension(content_type) or ".png"
        target = output_path / f"{record_id}{extension}"
        target.write_bytes(response.read())
        return str(target)


def download_url(url, output_dir, filename):
    output_path = Path(output_dir).expanduser().resolve()
    output_path.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(request, timeout=300) as response:
        content_type = response.headers.get("content-type", "").split(";")[0]
        extension = mimetypes.guess_extension(content_type) or Path(urllib.parse.urlparse(url).path).suffix or ""
        target = output_path / f"{filename}{extension}"
        target.write_bytes(response.read())
        return str(target)


def get_cli_credentials():
    credentials = load_credentials()
    return normalize_base(credentials.get("api_base") or DEFAULT_API_BASE), credentials["token"]


def image_generate(args):
    credentials = load_credentials()
    config = load_config()
    api_base = normalize_base(credentials.get("api_base") or resolve_api_base(args))
    token = credentials["token"]
    output_dir = args.output_dir or os.environ.get("SPEEDAI_OUTPUT_DIR", "") or str(config.get("output_dir", "") or "")
    fields = [
        ("prompt", args.prompt),
        ("scene", args.scene),
        ("aspectRatio", args.aspect_ratio),
        ("quality", args.quality),
    ]
    if args.variant_key:
        fields.append(("variantKey", args.variant_key))
    if args.model_config_id:
        fields.append(("modelConfigId", args.model_config_id))
    files = [("referenceImages", item) for item in args.reference_image]
    _, payload = request_multipart(f"{api_base}/api/h5/image-generations", fields, files, token)
    record = payload.get("record", {})
    record_id = record.get("id", "")
    if not args.wait or not record_id:
        print(json.dumps(payload, ensure_ascii=False))
        return

    deadline = time.time() + args.timeout
    while time.time() < deadline:
        _, detail = request_json("GET", f"{api_base}/api/h5/image-generations/{urllib.parse.quote(record_id)}", token=token)
        item = detail.get("item", {})
        if item.get("status") in ("成功", "失败"):
            result = {"record": item}
            if item.get("status") == "成功" and output_dir:
                result["downloadedPath"] = download_record(api_base, token, record_id, output_dir)
            print(json.dumps(result, ensure_ascii=False))
            return
        time.sleep(max(1.0, args.poll_interval))
    raise RuntimeError(f"Timed out waiting for image generation record: {record_id}")


def voice_list(_args):
    api_base, token = get_cli_credentials()
    _, payload = request_json("GET", f"{api_base}/api/h5/digital-human/bootstrap", token=token)
    print(json.dumps(payload, ensure_ascii=False))


def voice_clone(args):
    api_base, token = get_cli_credentials()
    fields = [
        ("prefix", args.prefix),
        ("sex", args.sex),
    ]
    if args.language:
        fields.append(("language", args.language))
    _, payload = request_multipart(
        f"{api_base}/api/h5/digital-human/voices/clone",
        fields,
        [("audio", args.audio)],
        token,
    )
    print(json.dumps(payload, ensure_ascii=False))


def audio_synthesize(args):
    api_base, token = get_cli_credentials()
    config = load_config()
    output_dir = args.output_dir or os.environ.get("SPEEDAI_OUTPUT_DIR", "") or str(config.get("output_dir", "") or "")
    fields = [
        ("text", args.text),
        ("voiceRecordId", args.voice_record_id),
        ("volume", args.volume),
        ("prompt", args.prompt),
    ]
    if args.language:
        fields.append(("language", args.language))
    if args.speech_rate:
        fields.append(("speechRate", args.speech_rate))
    if args.pitch_rate:
        fields.append(("pitchRate", args.pitch_rate))
    _, payload = request_multipart(f"{api_base}/api/h5/digital-human/audio", fields, [], token)
    item = payload.get("item", {})
    task_id = item.get("id", "")
    if not args.wait or not task_id:
        print(json.dumps(payload, ensure_ascii=False))
        return
    deadline = time.time() + args.timeout
    while time.time() < deadline:
        _, detail = request_json("GET", f"{api_base}/api/h5/digital-human/audio/{urllib.parse.quote(task_id)}", token=token)
        item = detail.get("item", {})
        if item.get("status") in ("succeeded", "failed"):
            result = {"item": item}
            if item.get("status") == "succeeded" and output_dir and item.get("audioUrl"):
                result["downloadedPath"] = download_url(item["audioUrl"], output_dir, task_id)
            print(json.dumps(result, ensure_ascii=False))
            return
        time.sleep(max(1.0, args.poll_interval))
    raise RuntimeError(f"Timed out waiting for audio task: {task_id}")


def digital_human_generate(args):
    api_base, token = get_cli_credentials()
    config = load_config()
    output_dir = args.output_dir or os.environ.get("SPEEDAI_OUTPUT_DIR", "") or str(config.get("output_dir", "") or "")
    fields = [
        ("text", args.text),
        ("voiceRecordId", args.voice_record_id),
        ("audioUrl", args.audio_url),
        ("audioDuration", args.audio_duration),
        ("volume", args.volume),
        ("prompt", args.prompt),
        ("videoPrompt", args.video_prompt),
    ]
    if args.language:
        fields.append(("language", args.language))
    if args.speech_rate:
        fields.append(("speechRate", args.speech_rate))
    if args.pitch_rate:
        fields.append(("pitchRate", args.pitch_rate))
    if args.model:
        fields.append(("model", args.model))
    _, payload = request_multipart(
        f"{api_base}/api/h5/digital-human/tasks",
        fields,
        [("image", args.image)],
        token,
    )
    item = payload.get("item", {})
    task_id = item.get("id", "")
    if not args.wait or not task_id:
        print(json.dumps(payload, ensure_ascii=False))
        return
    deadline = time.time() + args.timeout
    while time.time() < deadline:
        _, detail = request_json("GET", f"{api_base}/api/h5/digital-human/tasks/{urllib.parse.quote(task_id)}", token=token)
        item = detail.get("item", {})
        if item.get("status") in ("succeeded", "failed"):
            result = {"item": item}
            if item.get("status") == "succeeded" and output_dir and item.get("videoUrl"):
                result["downloadedPath"] = download_url(item["videoUrl"], output_dir, task_id)
            print(json.dumps(result, ensure_ascii=False))
            return
        time.sleep(max(1.0, args.poll_interval))
    raise RuntimeError(f"Timed out waiting for digital human task: {task_id}")


def main():
    args = parse_args()
    if args.command == "login" and args.login_command == "web":
        login_web(args)
    elif args.command == "logout":
        logout(args)
    elif args.command == "account":
        account(args)
    elif args.command == "config" and args.config_command == "list":
        config_list(args)
    elif args.command == "config" and args.config_command == "get":
        config_get(args)
    elif args.command == "config" and args.config_command == "set":
        config_set(args)
    elif args.command == "config" and args.config_command == "unset":
        config_unset(args)
    elif args.command == "image" and args.image_command == "generate":
        image_generate(args)
    elif args.command == "voice" and args.voice_command == "list":
        voice_list(args)
    elif args.command == "voice" and args.voice_command == "clone":
        voice_clone(args)
    elif args.command == "audio" and args.audio_command == "synthesize":
        audio_synthesize(args)
    elif args.command == "digital-human" and args.human_command == "generate":
        digital_human_generate(args)
    else:
        raise RuntimeError("Unsupported command")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
