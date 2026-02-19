import os
import subprocess
import json
import sys
from pathlib import Path

def run_command(command, description):
    print(f"
[*] {description}...")
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"[+] Thành công: {description}")
    except subprocess.CalledProcessError as e:
        print(f"[-] Lỗi khi {description}: {e}")
        sys.exit(1)

def main():
    home = str(Path.home())
    current_dir = os.getcwd()
    hexstrike_dir = os.path.join(current_dir, "hexstrike-ai")
    
    print("=== HexStrike AI & Gemini CLI Auto Installer ===")

    # 1. Cài đặt Node.js và npm
    run_command("sudo apt-get update && sudo apt-get install -y nodejs npm", "Cài đặt Node.js và npm")

    # 2. Cài đặt Gemini CLI
    run_command("sudo npm install -g @google/gemini-cli", "Cài đặt Gemini CLI")

    # 3. Clone HexStrike AI
    if not os.path.exists(hexstrike_dir):
        run_command("git clone https://github.com/0x4m4/hexstrike-ai.git", "Clone repository HexStrike AI")
    else:
        print("[!] Thư mục hexstrike-ai đã tồn tại, bỏ qua bước clone.")

    # 4. Thiết lập môi trường ảo và cài đặt dependencies
    os.chdir(hexstrike_dir)
    run_command("python3 -m venv hexstrike-env", "Tạo môi trường ảo (venv)")
    
    pip_path = os.path.join(hexstrike_dir, "hexstrike-env/bin/pip3")
    run_command(f"{pip_path} install --upgrade pip", "Nâng cấp pip")
    run_command(f"{pip_path} install -r requirements.txt", "Cài đặt Python dependencies")

    # 5. Cấu hình MCP cho Gemini CLI
    print("
[*] Cấu hình MCP cho Gemini CLI...")
    gemini_config_dir = os.path.join(home, ".gemini")
    os.makedirs(gemini_config_dir, exist_ok=True)
    
    settings_path = os.path.join(gemini_config_dir, "settings.json")
    
    python_executable = os.path.join(hexstrike_dir, "hexstrike-env/bin/python3")
    mcp_script_path = os.path.join(hexstrike_dir, "hexstrike_mcp.py")

    mcp_config = {
        "hexstrike-ai": {
            "command": python_executable,
            "args": [mcp_script_path, "--server", "http://localhost:8888"],
            "trust": True
        }
    }

    settings = {}
    if os.path.exists(settings_path):
        with open(settings_path, 'r') as f:
            try:
                settings = json.load(f)
            except json.JSONDecodeError:
                settings = {}

    if "mcpServers" not in settings:
        settings["mcpServers"] = {}
    
    settings["mcpServers"].update(mcp_config)

    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=2)
    
    print(f"[+] Đã cập nhật cấu hình MCP tại: {settings_path}")
    print("
=== CÀI ĐẶT HOÀN TẤT ===")
    print("[!] Lưu ý: Chạy 'gemini login' để đăng nhập trước khi sử dụng.")
    print("[!] Chạy 'python3 hexstrike_server.py' trong thư mục hexstrike-ai để bật server trước.")

if __name__ == "__main__":
    main()
