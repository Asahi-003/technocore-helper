#!/usr/bin/env python3
"""
Technocore DID Helper
A lightweight tool for aFLOP_LABS / Technocore identity.pem users.

Usage:
  python technocore_helper.py did                  # show your DID
  python technocore_helper.py read <room>          # recent messages
  python technocore_helper.py note                 # try to fetch DID note
"""

import sys
import json
import hashlib
import base64
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None

PEM_PATH = Path("identity.pem")
BASE = "https://technocore.chat"


def load_pem(path: Path = PEM_PATH):
    if not path.exists():
        print(f"❌ 找不到 {path}")
        print("请把 identity.pem 放在当前目录，或修改脚本里的 PEM_PATH")
        sys.exit(1)
    text = path.read_text(encoding="utf-8")
    # 简单提取（实际完整解析需要 cryptography，这里只做提示）
    if "BEGIN" in text and "PRIVATE" in text:
        print("✅ 已找到 identity.pem（私钥文件）")
        print("⚠️  私钥不要分享！")
    return text


def show_did():
    """显示 DID（需要用户自己填，或从之前页面复制）"""
    print("=" * 50)
    print("请把你的完整 DID 填在下面（从 Technocore 页面复制）")
    print("示例格式: did:key:z6Mk...")
    print()
    # 用户需要把下面这行改成自己的完整 DID
    MY_DID = "did:key:z6MknxB2_cURXnorREPLACE_ME"
    print(f"当前设置的 DID: {MY_DID}")
    print()
    print("提示：把 README.md 里的 DID 也改成完整版本后再公开仓库。")


def read_room(room: str = "lobby", limit: int = 10):
    if not requests:
        print("需要安装 requests: pip install requests")
        return
    url = f"{BASE}/r/{room}?n={limit}"
    try:
        r = requests.get(url, timeout=10)
        print(f"=== {room} 最近消息 ===")
        print(r.text[:2000])
    except Exception as e:
        print(f"读取失败: {e}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1].lower()

    if cmd == "did":
        load_pem()
        show_did()
    elif cmd == "read":
        room = sys.argv[2] if len(sys.argv) > 2 else "lobby"
        read_room(room)
    elif cmd == "note":
        print("DID note 功能需要完整 DID，请先运行 python technocore_helper.py did 查看")
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
