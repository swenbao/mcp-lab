"""建立專案內的 Python 環境；也支援系統缺少 pip / ensurepip 的情況。"""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import urllib.request
import venv


ROOT = Path(__file__).resolve().parent.parent
PIP_VERSION = "26.2.1"


def main() -> None:
    if sys.version_info < (3, 10):
        raise SystemExit("需要 Python 3.10 以上。")

    environment = ROOT / ".venv"
    if not (environment / "pyvenv.cfg").exists():
        venv.EnvBuilder(with_pip=False).create(environment)
    python = environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    pip_available = subprocess.run(
        [str(python), "-m", "pip", "--version"], capture_output=True
    ).returncode == 0

    if not pip_available:
        print("從 PyPI 取得 pip，安裝到專案的 .venv。", flush=True)
        with urllib.request.urlopen(
            f"https://pypi.org/pypi/pip/{PIP_VERSION}/json", timeout=30
        ) as response:
            metadata = json.load(response)
        wheel = next(item for item in metadata["urls"] if item["filename"].endswith(".whl"))
        with urllib.request.urlopen(wheel["url"], timeout=30) as response:
            payload = response.read()
        if hashlib.sha256(payload).hexdigest() != wheel["digests"]["sha256"]:
            raise RuntimeError("pip 下載檔案的 SHA-256 不符，停止安裝。")
        with tempfile.TemporaryDirectory(prefix="mcp-lab-pip-") as directory:
            wheel_path = Path(directory) / wheel["filename"]
            wheel_path.write_bytes(payload)
            subprocess.run(
                [str(python), "-m", "pip", "install", "--no-index", str(wheel_path)],
                env=dict(os.environ, PYTHONPATH=str(wheel_path)),
                check=True,
            )

    subprocess.run(
        [
            str(python), "-m", "pip", "--disable-pip-version-check", "--no-cache-dir",
            "install", "--index-url", "https://pypi.org/simple",
            "-r", str(ROOT / "requirements.lock"),
        ],
        check=True,
    )
    print("環境準備完成。套件都在專案的 .venv 裡。")


if __name__ == "__main__":
    main()
