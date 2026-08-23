#!/usr/bin/env python3
import argparse
import http.client
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


VERSION = "0.6.0"
DEFAULT_API_BASE = "https://wooboo.ycszai.com"
DEFAULT_H5_BASE = "https://wooboo.ycszai.com"
CONFIG_DIR = Path.home() / ".wooboo-ai"
CREDENTIALS_PATH = CONFIG_DIR / "credentials.json"
CONFIG_PATH = CONFIG_DIR / "config.json"


def parse_args():
    parser = argparse.ArgumentParser(description="Wooboo AI system media generation CLI.")
    parser.add_argument("--version", action="version", version=f"wooboo {VERSION}")
    parser.add_argument("--api-base", default="", help="API base URL. Overrides WOOBOO_API_BASE and config.")
    parser.add_argument("--h5-base", default="", help="H5 web base URL. Overrides WOOBOO_H5_BASE and config.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    login = subparsers.add_parser("login")
    login_sub = login.add_subparsers(dest="login_command", required=True)
    login_web = login_sub.add_parser("web")
    login_web.add_argument("--open", action="store_true", help="Open the authorization URL in the default browser.")
    login_web.add_argument("--client-name", default="Wooboo AI CLI")
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
    image_models = image_sub.add_parser("models")
    image_models.add_argument("--scene", default="图片生成")
    generate = image_sub.add_parser("generate")
    generate.add_argument("--prompt", required=True)
    generate.add_argument("--scene", default="图片生成")
    generate.add_argument("--aspect-ratio", default="")
    generate.add_argument("--quality", default="")
    generate.add_argument("--variant-key", default="")
    generate.add_argument("--model-config-id", default="")
    generate.add_argument("--model", default="", help="Model display name or provider model name.")
    generate.add_argument("--reference-image", action="append", default=[])
    generate.add_argument("--wait", action=argparse.BooleanOptionalAction, default=True)
    generate.add_argument("--poll-interval", type=float, default=3.0)
    generate.add_argument("--timeout", type=int, default=600)
    generate.add_argument("--output-dir", default="")

    video = subparsers.add_parser("video")
    video_sub = video.add_subparsers(dest="video_command", required=True)
    video_sub.add_parser("models")
    video_generate_parser = video_sub.add_parser("generate")
    video_generate_parser.add_argument("--series", default="", help="Video series such as wanx, seedance, happyhorse, or kling.")
    video_generate_parser.add_argument("--model", default="", help="Model display name or provider model name.")
    video_generate_parser.add_argument("--prompt", required=True)
    video_generate_parser.add_argument("--mode", default="t2v", choices=["t2v", "i2v", "first_last_frame", "r2v", "video_extend", "video_edit"])
    video_generate_parser.add_argument("--aspect-ratio", default="")
    video_generate_parser.add_argument("--duration-seconds", type=int, default=5)
    video_generate_parser.add_argument("--resolution", default="")
    video_generate_parser.add_argument("--variant-key", default="")
    video_generate_parser.add_argument("--model-config-id", default="")
    video_generate_parser.add_argument("--first-frame", default="")
    video_generate_parser.add_argument("--last-frame", default="")
    video_generate_parser.add_argument("--extend-video", default="")
    video_generate_parser.add_argument("--edit-video", default="")
    video_generate_parser.add_argument("--reference-image", action="append", default=[])
    video_generate_parser.add_argument("--reference-video", action="append", default=[])
    video_generate_parser.add_argument("--negative-prompt", default="")
    video_generate_parser.add_argument("--camera-fixed", action=argparse.BooleanOptionalAction, default=False)
    video_generate_parser.add_argument("--trim-long-media", action=argparse.BooleanOptionalAction, default=False)
    video_generate_parser.add_argument("--wait", action=argparse.BooleanOptionalAction, default=True)
    video_generate_parser.add_argument("--poll-interval", type=float, default=5.0)
    video_generate_parser.add_argument("--timeout", type=int, default=1800)
    video_generate_parser.add_argument("--output-dir", default="")

    long_video = subparsers.add_parser("long-video")
    long_video_sub = long_video.add_subparsers(dest="long_video_command", required=True)
    long_video_generate_parser = long_video_sub.add_parser("generate")
    long_video_generate_parser.add_argument("--prompt", required=True)
    long_video_generate_parser.add_argument("--reference", required=True)
    long_video_generate_parser.add_argument("--voice", default="")
    long_video_generate_parser.add_argument("--aspect-ratio", default="9:16", choices=["9:16", "16:9"])
    long_video_generate_parser.add_argument("--variant-key", default="")
    long_video_generate_parser.add_argument("--wait", action=argparse.BooleanOptionalAction, default=True)
    long_video_generate_parser.add_argument("--poll-interval", type=float, default=8.0)
    long_video_generate_parser.add_argument("--storyboard-timeout", type=int, default=600)
    long_video_generate_parser.add_argument("--generation-timeout", type=int, default=3600)
    long_video_generate_parser.add_argument("--export-timeout", type=int, default=900)
    long_video_generate_parser.add_argument("--output-dir", default="")

    voice = subparsers.add_parser("voice")
    voice_sub = voice.add_subparsers(dest="voice_command", required=True)
    voice_sub.add_parser("list")
    voice_clone = voice_sub.add_parser("clone")
    voice_clone.add_argument("--audio", required=True)
    voice_clone.add_argument("--name", "--prefix", dest="name", default="我的音色")
    voice_clone.add_argument("--sex", type=int, default=0, help=argparse.SUPPRESS)
    voice_clone.add_argument("--language", default="")
    voice_clone.add_argument("--wait", action=argparse.BooleanOptionalAction, default=True)
    voice_clone.add_argument("--poll-interval", type=float, default=5.0)
    voice_clone.add_argument("--timeout", type=int, default=1800)
    voice_delete = voice_sub.add_parser("delete")
    voice_delete.add_argument("id")

    avatar = subparsers.add_parser("avatar")
    avatar_sub = avatar.add_subparsers(dest="avatar_command", required=True)
    avatar_sub.add_parser("list")
    avatar_create = avatar_sub.add_parser("create")
    avatar_create.add_argument("--video", required=True)
    avatar_create.add_argument("--title", default="我的形象")
    avatar_create.add_argument("--wait", action=argparse.BooleanOptionalAction, default=True)
    avatar_create.add_argument("--poll-interval", type=float, default=8.0)
    avatar_create.add_argument("--timeout", type=int, default=7200)
    avatar_delete = avatar_sub.add_parser("delete")
    avatar_delete.add_argument("id")

    audio = subparsers.add_parser("audio")
    audio_sub = audio.add_subparsers(dest="audio_command", required=True)
    synthesize = audio_sub.add_parser("synthesize")
    synthesize.add_argument("--text", default="")
    synthesize.add_argument("--voice-record-id", default="")
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
    human_generate.add_argument("--avatar-record-id", required=True)
    human_generate.add_argument("--drive-mode", choices=["text", "audio"], default="text")
    human_generate.add_argument("--text", default="")
    human_generate.add_argument("--voice-record-id", default="")
    human_generate.add_argument("--audio", default="")
    human_generate.add_argument("--title", default="")
    human_generate.add_argument("--subtitle", action=argparse.BooleanOptionalAction, default=None)
    human_generate.add_argument("--wait", action=argparse.BooleanOptionalAction, default=True)
    human_generate.add_argument("--poll-interval", type=float, default=5.0)
    human_generate.add_argument("--timeout", type=int, default=7200)
    human_generate.add_argument("--output-dir", default="")

    return parser.parse_args()


def normalize_base(url):
    return url.rstrip("/")


def resolve_api_base(args):
    return normalize_base(
        args.api_base
        or os.environ.get("WOOBOO_API_BASE", "")
        or str(load_config().get("api_base", "") or "")
        or DEFAULT_API_BASE
    )


def resolve_h5_base(args):
    return normalize_base(
        args.h5_base
        or os.environ.get("WOOBOO_H5_BASE", "")
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


def resolve_local_file(path, label="File"):
    file_path = Path(path).expanduser().resolve()
    if not file_path.is_file():
        raise RuntimeError(f"{label} does not exist: {file_path}")
    return file_path


def guess_content_type(file_path, fallback="application/octet-stream"):
    return mimetypes.guess_type(str(file_path))[0] or fallback


def put_file_to_signed_url(url, file_path, headers=None, timeout=1800):
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise RuntimeError("Invalid signed upload URL")
    connection_class = http.client.HTTPSConnection if parsed.scheme == "https" else http.client.HTTPConnection
    connection = connection_class(parsed.hostname, parsed.port, timeout=timeout)
    target = parsed.path or "/"
    if parsed.query:
        target += f"?{parsed.query}"
    request_headers = {str(name): str(value) for name, value in (headers or {}).items()}
    request_headers["Content-Length"] = str(file_path.stat().st_size)
    try:
        connection.putrequest("PUT", target)
        for name, value in request_headers.items():
            connection.putheader(name, value)
        connection.endheaders()
        with file_path.open("rb") as file_handle:
            while True:
                chunk = file_handle.read(1024 * 1024)
                if not chunk:
                    break
                connection.send(chunk)
        response = connection.getresponse()
        body = response.read().decode("utf-8", errors="replace")
        if not 200 <= response.status < 300:
            raise RuntimeError(f"Signed upload failed: HTTP {response.status}: {body}")
    finally:
        connection.close()


def delete_media_upload(api_base, token, upload_id):
    try:
        request_json(
            "DELETE",
            f"{api_base}/api/h5/media-uploads/{urllib.parse.quote(upload_id)}",
            token=token,
        )
    except Exception:
        pass


def direct_upload_file(api_base, token, path, purpose, field_name, fallback_content_type="application/octet-stream"):
    file_path = resolve_local_file(path)
    content_type = guess_content_type(file_path, fallback_content_type)
    _, initialized = request_json(
        "POST",
        f"{api_base}/api/h5/media-uploads/init",
        {
            "purpose": purpose,
            "fieldName": field_name,
            "fileName": file_path.name,
            "mimeType": content_type,
            "sizeBytes": file_path.stat().st_size,
        },
        token=token,
    )
    intent = initialized.get("upload") or {}
    upload_id = str(intent.get("uploadId") or "")
    upload_url = str(intent.get("uploadUrl") or "")
    if not upload_id or not upload_url:
        raise RuntimeError("Media upload initialization returned an invalid response")
    try:
        put_file_to_signed_url(upload_url, file_path, intent.get("headers") or {})
        request_json(
            "POST",
            f"{api_base}/api/h5/media-uploads/{urllib.parse.quote(upload_id)}/complete",
            {},
            token=token,
        )
        return {"uploadId": upload_id, "fieldName": field_name, "path": str(file_path), "mimeType": content_type}
    except Exception:
        delete_media_upload(api_base, token, upload_id)
        raise


def encode_multipart(fields, files):
    boundary = f"----wooboo-{uuid.uuid4().hex}"
    chunks = []
    for name, value in fields:
        chunks.append(f"--{boundary}\r\n".encode("utf-8"))
        chunks.append(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8"))
        chunks.append(str(value).encode("utf-8"))
        chunks.append(b"\r\n")
    for name, path in files:
        file_path = resolve_local_file(path)
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
    if os.name != "nt":
        CREDENTIALS_PATH.chmod(0o600)


def load_credentials():
    if not CREDENTIALS_PATH.is_file():
        raise RuntimeError("Not logged in. Run: wooboo login web")
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


def download_video_record(api_base, token, task_id, output_dir):
    output_path = Path(output_dir).expanduser().resolve()
    output_path.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(
        f"{api_base}/api/h5/video-generations/{urllib.parse.quote(task_id)}/download",
        headers={"Authorization": f"Bearer {token}"},
        method="GET",
    )
    with urllib.request.urlopen(request, timeout=600) as response:
        content_type = response.headers.get("content-type", "video/mp4").split(";")[0]
        extension = mimetypes.guess_extension(content_type) or ".mp4"
        target = output_path / f"{task_id}{extension}"
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


def selector_matches(model, selector):
    normalized = str(selector or "").strip().casefold()
    if not normalized:
        return False
    return normalized in {
        str(model.get("id") or "").strip().casefold(),
        str(model.get("name") or "").strip().casefold(),
        str(model.get("modelName") or "").strip().casefold(),
    }


def fetch_image_bootstrap(api_base, token, scene):
    query = urllib.parse.urlencode({"scene": scene})
    _, payload = request_json("GET", f"{api_base}/api/h5/image-generation/bootstrap?{query}", token=token)
    return payload


def image_models(args):
    api_base, token = get_cli_credentials()
    print(json.dumps(fetch_image_bootstrap(api_base, token, args.scene), ensure_ascii=False))


def select_image_model(bootstrap, model_config_id="", model_selector=""):
    models = bootstrap.get("models") or []
    if model_config_id:
        selected = next((item for item in models if str(item.get("id") or "") == model_config_id), None)
        if not selected:
            raise RuntimeError(f"Image model config not found: {model_config_id}")
        return selected
    if model_selector:
        selected = next((item for item in models if selector_matches(item, model_selector)), None)
        if not selected:
            raise RuntimeError(f"Image model not found: {model_selector}")
        return selected
    if not models:
        raise RuntimeError("No enabled image model found")
    return models[0]


def select_image_variant(model, variant_key="", quality=""):
    variants = [item for item in (model.get("variants") or []) if item.get("status") == "启用"]
    if variant_key:
        selected = next((item for item in variants if str(item.get("variantKey") or "") == variant_key), None)
        if not selected:
            raise RuntimeError(f"Image model variant not found or disabled: {variant_key}")
        variant_quality = str(selected.get("quality") or "")
        if quality and variant_quality and variant_quality.casefold() != quality.casefold():
            raise RuntimeError(f"Image variant {variant_key} uses quality {variant_quality}, not {quality}")
        return selected
    if quality:
        selected = next((item for item in variants if str(item.get("quality") or "").casefold() == quality.casefold()), None)
        if not selected:
            raise RuntimeError(f"Image quality is not available for the selected model: {quality}")
        return selected
    default_variant = model.get("defaultVariant") or {}
    if default_variant and default_variant.get("status") == "启用":
        return default_variant
    if variants:
        return variants[0]
    raise RuntimeError("The selected image model has no enabled variant")


def image_generate(args):
    credentials = load_credentials()
    config = load_config()
    api_base = normalize_base(credentials.get("api_base") or resolve_api_base(args))
    token = credentials["token"]
    output_dir = args.output_dir or os.environ.get("WOOBOO_OUTPUT_DIR", "") or str(config.get("output_dir", "") or "")
    bootstrap = fetch_image_bootstrap(api_base, token, args.scene)
    model = select_image_model(bootstrap, args.model_config_id, args.model)
    variant = select_image_variant(model, args.variant_key, args.quality)
    quality = args.quality or str(variant.get("quality") or model.get("defaultQuality") or "1k")
    supported_aspect_ratios = model.get("aspectRatios") or bootstrap.get("aspectRatios") or []
    if args.aspect_ratio:
        aspect_ratio = args.aspect_ratio
    elif str(model.get("modelName") or "").strip().casefold() == "gpt-image-2" and "auto" in supported_aspect_ratios:
        aspect_ratio = "auto"
    else:
        aspect_ratio = str((supported_aspect_ratios or ["1:1"])[0])
    if supported_aspect_ratios and aspect_ratio not in supported_aspect_ratios:
        raise RuntimeError(f"Image aspect ratio is not available for the selected model: {aspect_ratio}")
    max_references = max(0, int(model.get("maxReferenceImages") or 0))
    if len(args.reference_image) > max_references:
        raise RuntimeError(f"The selected image model accepts at most {max_references} reference images")
    fields = [
        ("prompt", args.prompt),
        ("scene", args.scene),
        ("aspectRatio", aspect_ratio),
        ("quality", quality),
        ("variantKey", variant.get("variantKey") or ""),
        ("modelConfigId", model.get("id") or ""),
    ]
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


def fetch_video_bootstrap(api_base, token):
    _, payload = request_json("GET", f"{api_base}/api/h5/video-generation/bootstrap", token=token)
    return payload


def video_models(_args):
    api_base, token = get_cli_credentials()
    print(json.dumps(fetch_video_bootstrap(api_base, token), ensure_ascii=False))


def select_video_model(bootstrap, series="", model_config_id="", model_selector="", mode=""):
    models = bootstrap.get("models") or []
    selected = None
    if model_config_id:
        selected = next((item for item in models if str(item.get("id") or "") == model_config_id), None)
        if not selected:
            raise RuntimeError(f"Video model config not found: {model_config_id}")
    elif model_selector:
        selected = next((item for item in models if selector_matches(item, model_selector)), None)
        if not selected:
            raise RuntimeError(f"Video model not found: {model_selector}")
    else:
        candidates = [
            item for item in models
            if (not series or str((item.get("capability") or {}).get("series") or "") == series)
            and (not mode or mode in ((item.get("capability") or {}).get("modes") or []))
        ]
        selected = candidates[0] if candidates else None
    if not selected:
        label = f" for series {series}" if series else ""
        raise RuntimeError(f"No enabled video model found{label} supporting mode {mode}")
    capability = selected.get("capability") or {}
    if series and str(capability.get("series") or "") != series:
        raise RuntimeError(f"Selected video model does not belong to series: {series}")
    if mode and mode not in (capability.get("modes") or []):
        raise RuntimeError(f"Selected video model does not support mode: {mode}")
    return selected


def select_video_variant(model, variant_key="", resolution=""):
    variants = [item for item in (model.get("variants") or []) if item.get("status") == "启用"]
    if variant_key:
        selected = next((item for item in variants if str(item.get("variantKey") or "") == variant_key), None)
        if not selected:
            raise RuntimeError(f"Video model variant not found or disabled: {variant_key}")
        variant_resolution = str(selected.get("resolution") or "")
        if resolution and variant_resolution and variant_resolution.casefold() != resolution.casefold():
            raise RuntimeError(f"Video variant {variant_key} uses resolution {variant_resolution}, not {resolution}")
        return selected
    if resolution:
        selected = next(
            (item for item in variants if str(item.get("resolution") or "").casefold() == resolution.casefold()),
            None,
        )
        if not selected:
            raise RuntimeError(f"Video resolution is not available for the selected model: {resolution}")
        return selected
    default_variant = model.get("defaultVariant") or {}
    if default_variant and default_variant.get("status") == "启用":
        return default_variant
    if variants:
        return variants[0]
    raise RuntimeError("The selected video model has no enabled variant")


def build_video_upload_entries(args, series):
    entries = []
    for field_name, path in (
        ("firstFrameFile", args.first_frame),
        ("lastFrameFile", args.last_frame),
        ("extendVideoFile", args.extend_video),
        ("editVideoFile", args.edit_video),
    ):
        if path:
            entries.append((field_name, path))

    materials = []
    if args.mode == "r2v" and series in ("wanx", "kling", "seedance"):
        for path in args.reference_image:
            materials.append({"source": "local", "mediaFileIndex": len(materials), "mediaKind": "reference_image"})
            entries.append(("wanxR2vMediaFiles", path))
        for path in args.reference_video:
            materials.append({"source": "local", "mediaFileIndex": len(materials), "mediaKind": "reference_video"})
            entries.append(("wanxR2vMediaFiles", path))
        return entries, materials

    entries.extend(("referenceImageFiles", path) for path in args.reference_image)
    entries.extend(("referenceVideoFiles", path) for path in args.reference_video)
    return entries, materials


def validate_video_inputs(args, capability):
    series = str(capability.get("series") or "")
    image_count = len(args.reference_image)
    video_count = len(args.reference_video)
    mode_inputs = {
        "first_frame": bool(args.first_frame),
        "last_frame": bool(args.last_frame),
        "extend_video": bool(args.extend_video),
        "edit_video": bool(args.edit_video),
        "reference_image": bool(args.reference_image),
        "reference_video": bool(args.reference_video),
    }
    allowed_inputs = {
        "t2v": set(),
        "i2v": {"first_frame"},
        "first_last_frame": {"first_frame", "last_frame"},
        "r2v": {"reference_image", "reference_video"},
        "video_extend": {"extend_video"},
        "video_edit": {"edit_video", "reference_image"},
    }[args.mode]
    unexpected = [name for name, present in mode_inputs.items() if present and name not in allowed_inputs]
    if unexpected:
        raise RuntimeError(f"Video mode {args.mode} does not accept: {', '.join(unexpected)}")
    if args.mode in ("i2v", "first_last_frame") and not args.first_frame:
        raise RuntimeError(f"Video mode {args.mode} requires --first-frame")
    if args.mode == "video_extend" and not args.extend_video:
        raise RuntimeError("Video extend mode requires --extend-video")
    if args.mode == "video_edit" and not args.edit_video:
        raise RuntimeError("Video edit mode requires --edit-video")
    if image_count > int(capability.get("maxReferenceImages") or 0):
        raise RuntimeError("Reference image count exceeds the selected model limit")
    if video_count > int(capability.get("maxReferenceVideos") or 0):
        raise RuntimeError("Reference video count exceeds the selected model limit")
    if args.mode == "r2v" and not image_count and not video_count:
        raise RuntimeError("Reference-to-video mode requires at least one reference image or video")
    if series == "happyhorse" and video_count:
        raise RuntimeError("HappyHorse reference-to-video supports images only")
    if series == "kling" and video_count and image_count > 4:
        raise RuntimeError("Kling accepts at most four reference images when a video reference is present")
    if series == "seedance" and video_count > 1:
        raise RuntimeError("Seedance accepts at most one video reference")
    constraint = (capability.get("durationConstraints") or {}).get(args.mode) or {}
    minimum = int(constraint.get("min") or 0)
    maximum = int(
        constraint.get("maxWithVideoReference")
        if video_count and constraint.get("maxWithVideoReference") is not None
        else constraint.get("max") or 0
    )
    if minimum and args.duration_seconds < minimum:
        raise RuntimeError(f"Video duration must be at least {minimum} seconds for the selected model and mode")
    if maximum and args.duration_seconds > maximum:
        raise RuntimeError(f"Video duration must be at most {maximum} seconds for the selected model and mode")


def video_generate(args):
    api_base, token = get_cli_credentials()
    config = load_config()
    output_dir = args.output_dir or os.environ.get("WOOBOO_OUTPUT_DIR", "") or str(config.get("output_dir", "") or "")
    bootstrap = fetch_video_bootstrap(api_base, token)
    model = select_video_model(bootstrap, args.series, args.model_config_id, args.model, args.mode)
    capability = model.get("capability") or {}
    series = str(capability.get("series") or "")
    validate_video_inputs(args, capability)
    variant = select_video_variant(model, args.variant_key, args.resolution)
    variant_key = str(variant.get("variantKey") or "")
    resolution = str(variant.get("resolution") or args.resolution or "720P")
    aspect_ratio = args.aspect_ratio or ("adaptive" if series == "seedance" else "9:16")
    model_config_id = str(model.get("id") or "")

    fields = [
        ("clientSubmissionId", str(uuid.uuid4())),
        ("modelConfigId", model_config_id),
        ("mode", args.mode),
        ("prompt", args.prompt),
        ("resolution", resolution),
        ("durationSeconds", args.duration_seconds),
        ("aspectRatio", aspect_ratio),
        ("trimLongMedia", "true" if args.trim_long_media else "false"),
    ]
    if variant_key:
        fields.append(("variantKey", variant_key))
    if args.negative_prompt:
        fields.append(("negativePrompt", args.negative_prompt))
    if args.camera_fixed:
        fields.append(("cameraFixed", "true"))

    upload_entries, materials = build_video_upload_entries(args, series)
    if materials:
        fields.append(("wanxR2vMaterials", json.dumps(materials, ensure_ascii=False)))
    completed_uploads = []
    try:
        for field_name, path in upload_entries:
            completed_uploads.append(
                direct_upload_file(api_base, token, path, "video_generation", field_name)
            )
        if completed_uploads:
            fields.append(("mediaUploads", json.dumps([
                {"fieldName": item["fieldName"], "uploadId": item["uploadId"]}
                for item in completed_uploads
            ], ensure_ascii=False)))
        _, payload = request_multipart(f"{api_base}/api/h5/video-generations", fields, [], token, timeout=300)
    except Exception:
        for item in completed_uploads:
            delete_media_upload(api_base, token, item["uploadId"])
        raise
    task = payload.get("task", {})
    task_id = task.get("taskId", "")
    if not args.wait or not task_id:
        print(json.dumps(payload, ensure_ascii=False))
        return

    deadline = time.time() + args.timeout
    while time.time() < deadline:
        _, detail = request_json("GET", f"{api_base}/api/h5/video-generations/{urllib.parse.quote(task_id)}", token=token)
        task = detail.get("task", {})
        record = detail.get("record", {})
        status = str(task.get("taskStatus") or record.get("status") or "")
        if status in ("成功", "失败", "succeeded", "failed"):
            result = {"task": task, "record": record}
            video_url = task.get("videoUrl") or record.get("resultVideoUrl") or record.get("videoUrl")
            if status in ("成功", "succeeded") and output_dir and video_url:
                result["downloadedPath"] = download_video_record(api_base, token, task_id, output_dir)
            print(json.dumps(result, ensure_ascii=False))
            return
        time.sleep(max(1.0, args.poll_interval))
    raise RuntimeError(f"Timed out waiting for video generation task: {task_id}")


def long_video_project_failed(project):
    return str(project.get("status", "")) == "failed" or any(
        str(scene.get("status", "")) == "failed" for scene in project.get("scenes", [])
    )


def long_video_generate(args):
    api_base, token = get_cli_credentials()
    config = load_config()
    output_dir = args.output_dir or os.environ.get("WOOBOO_OUTPUT_DIR", "") or str(config.get("output_dir", "") or "")
    _, bootstrap = request_json("GET", f"{api_base}/api/h5/long-video/bootstrap", token=token)
    default_variant = (bootstrap.get("model", {}).get("defaultVariant") or {})
    variant_key = args.variant_key or str(default_variant.get("variantKey", "") or "")

    fields = [
        ("prompt", args.prompt),
        ("aspectRatio", args.aspect_ratio),
    ]
    if variant_key:
        fields.append(("variantKey", variant_key))
    files = [("referenceFile", args.reference)]
    if args.voice:
        files.append(("voiceFile", args.voice))

    _, created = request_multipart(f"{api_base}/api/h5/long-videos", fields, files, token, timeout=300)
    project = created.get("item", {})
    project_id = str(project.get("id", "") or "")
    if not project_id:
        print(json.dumps(created, ensure_ascii=False))
        return

    _, storyboard_payload = request_json("POST", f"{api_base}/api/h5/long-videos/{urllib.parse.quote(project_id)}/storyboards", token=token)
    if not args.wait:
        print(json.dumps({"item": storyboard_payload.get("item", project)}, ensure_ascii=False))
        return

    deadline = time.time() + args.storyboard_timeout
    while time.time() < deadline:
        _, detail = request_json("GET", f"{api_base}/api/h5/long-videos/{urllib.parse.quote(project_id)}", token=token)
        project = detail.get("item", {})
        if long_video_project_failed(project):
            print(json.dumps({"item": project}, ensure_ascii=False))
            return
        if str(project.get("status", "")) == "storyboard_ready" and project.get("scenes"):
            break
        time.sleep(max(1.0, args.poll_interval))
    else:
        raise RuntimeError(f"Timed out waiting for long-video storyboard: {project_id}")

    _, generate_payload = request_json("POST", f"{api_base}/api/h5/long-videos/{urllib.parse.quote(project_id)}/generate-all", token=token)
    project = generate_payload.get("item", project)
    deadline = time.time() + args.generation_timeout
    while time.time() < deadline:
        _, detail = request_json("GET", f"{api_base}/api/h5/long-videos/{urllib.parse.quote(project_id)}", token=token)
        project = detail.get("item", {})
        if long_video_project_failed(project):
            print(json.dumps({"item": project}, ensure_ascii=False))
            return
        scenes = project.get("scenes", [])
        if scenes and all(str(scene.get("status", "")) == "succeeded" for scene in scenes):
            break
        time.sleep(max(1.0, args.poll_interval))
    else:
        raise RuntimeError(f"Timed out waiting for long-video scene generation: {project_id}")

    _, exported = request_json("POST", f"{api_base}/api/h5/long-videos/{urllib.parse.quote(project_id)}/export", token=token, timeout=args.export_timeout)
    project = exported.get("item", project)
    result = {"item": project, "export": exported.get("export", {})}
    final_url = str(project.get("finalVideoUrl") or exported.get("export", {}).get("url") or "")
    if final_url and output_dir:
        result["downloadedPath"] = download_url(final_url, output_dir, project_id)
    print(json.dumps(result, ensure_ascii=False))


def voice_list(_args):
    api_base, token = get_cli_credentials()
    _, payload = request_json("GET", f"{api_base}/api/h5/digital-human/bootstrap", token=token)
    print(json.dumps(payload, ensure_ascii=False))


def voice_delete(args):
    api_base, token = get_cli_credentials()
    _, payload = request_json(
        "DELETE",
        f"{api_base}/api/h5/digital-human/voices/{urllib.parse.quote(args.id)}",
        token=token,
    )
    print(json.dumps(payload or {"ok": True}, ensure_ascii=False))


def voice_clone(args):
    api_base, token = get_cli_credentials()
    uploaded = direct_upload_file(
        api_base,
        token,
        args.audio,
        "digital_human_voice",
        "voiceAudio",
        "audio/mpeg",
    )
    try:
        _, payload = request_json(
            "POST",
            f"{api_base}/api/h5/digital-human/voices/clone",
            {
                "uploadId": uploaded["uploadId"],
                "voiceName": args.name,
                "language": args.language or "zh",
            },
            token=token,
        )
    except Exception:
        delete_media_upload(api_base, token, uploaded["uploadId"])
        raise
    item = payload.get("item") or {}
    voice_id = str(item.get("id") or "")
    if not args.wait or not voice_id:
        print(json.dumps(payload, ensure_ascii=False))
        return
    deadline = time.time() + args.timeout
    while time.time() < deadline:
        _, detail = request_json(
            "GET",
            f"{api_base}/api/h5/digital-human/voices/{urllib.parse.quote(voice_id)}",
            token=token,
        )
        item = detail.get("item") or {}
        if item.get("cloneStatus") in ("ready", "failed", "migration_pending"):
            print(json.dumps({"item": item}, ensure_ascii=False))
            return
        time.sleep(max(1.0, args.poll_interval))
    raise RuntimeError(f"Timed out waiting for voice clone: {voice_id}")


def avatar_list(_args):
    api_base, token = get_cli_credentials()
    _, payload = request_json("GET", f"{api_base}/api/h5/digital-human/bootstrap", token=token)
    print(json.dumps({"config": payload.get("config") or {}, "avatars": payload.get("avatars") or []}, ensure_ascii=False))


def avatar_create(args):
    api_base, token = get_cli_credentials()
    uploaded = direct_upload_file(
        api_base,
        token,
        args.video,
        "digital_human_avatar",
        "avatarVideo",
        "video/mp4",
    )
    try:
        _, payload = request_json(
            "POST",
            f"{api_base}/api/h5/digital-human/avatars",
            {"uploadId": uploaded["uploadId"], "title": args.title},
            token=token,
        )
    except Exception:
        delete_media_upload(api_base, token, uploaded["uploadId"])
        raise
    item = payload.get("item") or {}
    avatar_id = str(item.get("id") or "")
    if not args.wait or not avatar_id:
        print(json.dumps(payload, ensure_ascii=False))
        return
    deadline = time.time() + args.timeout
    while time.time() < deadline:
        _, detail = request_json(
            "GET",
            f"{api_base}/api/h5/digital-human/avatars/{urllib.parse.quote(avatar_id)}",
            token=token,
        )
        item = detail.get("item") or {}
        if item.get("status") in ("ready", "failed", "deleted"):
            print(json.dumps({"item": item}, ensure_ascii=False))
            return
        time.sleep(max(1.0, args.poll_interval))
    raise RuntimeError(f"Timed out waiting for digital-human avatar creation: {avatar_id}")


def avatar_delete(args):
    api_base, token = get_cli_credentials()
    _, payload = request_json(
        "DELETE",
        f"{api_base}/api/h5/digital-human/avatars/{urllib.parse.quote(args.id)}",
        token=token,
    )
    print(json.dumps(payload or {"ok": True}, ensure_ascii=False))


def audio_synthesize(args):
    raise RuntimeError(
        "The standalone audio synthesis API has been retired. "
        "Use `wooboo digital-human generate --drive-mode text --avatar-record-id ... "
        "--voice-record-id ... --text ...` instead."
    )


def digital_human_generate(args):
    api_base, token = get_cli_credentials()
    config = load_config()
    output_dir = args.output_dir or os.environ.get("WOOBOO_OUTPUT_DIR", "") or str(config.get("output_dir", "") or "")
    if args.drive_mode == "text":
        if not args.text.strip():
            raise RuntimeError("Text drive mode requires --text")
        if not args.voice_record_id.strip():
            raise RuntimeError("Text drive mode requires --voice-record-id")
        if args.audio:
            raise RuntimeError("Text drive mode does not accept --audio")
    elif not args.audio:
        raise RuntimeError("Audio drive mode requires --audio")

    uploaded = None
    if args.drive_mode == "audio":
        uploaded = direct_upload_file(
            api_base,
            token,
            args.audio,
            "digital_human_audio_drive",
            "driveAudio",
            "audio/mpeg",
        )
    title = args.title.strip()
    if not title:
        title = args.text.strip()[:20] if args.drive_mode == "text" else resolve_local_file(args.audio).stem[:20]
    payload_body = {
        "driveMode": args.drive_mode,
        "avatarRecordId": args.avatar_record_id,
        "voiceRecordId": args.voice_record_id if args.drive_mode == "text" else "",
        "audioUploadId": uploaded["uploadId"] if uploaded else "",
        "title": title or "数字人视频",
        "text": args.text.strip() if args.drive_mode == "text" else "",
    }
    if args.subtitle is not None:
        payload_body["subtitleSettings"] = {"enabled": bool(args.subtitle) and args.drive_mode == "text"}
    try:
        _, payload = request_json(
            "POST",
            f"{api_base}/api/h5/digital-human/tasks",
            payload_body,
            token=token,
        )
    except Exception:
        if uploaded:
            delete_media_upload(api_base, token, uploaded["uploadId"])
        raise
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
    elif args.command == "image" and args.image_command == "models":
        image_models(args)
    elif args.command == "image" and args.image_command == "generate":
        image_generate(args)
    elif args.command == "video" and args.video_command == "models":
        video_models(args)
    elif args.command == "video" and args.video_command == "generate":
        video_generate(args)
    elif args.command == "long-video" and args.long_video_command == "generate":
        long_video_generate(args)
    elif args.command == "voice" and args.voice_command == "list":
        voice_list(args)
    elif args.command == "voice" and args.voice_command == "clone":
        voice_clone(args)
    elif args.command == "voice" and args.voice_command == "delete":
        voice_delete(args)
    elif args.command == "avatar" and args.avatar_command == "list":
        avatar_list(args)
    elif args.command == "avatar" and args.avatar_command == "create":
        avatar_create(args)
    elif args.command == "avatar" and args.avatar_command == "delete":
        avatar_delete(args)
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
