import os
import subprocess
import json
import sys
import argparse
import shutil
from pathlib import Path

def run_command(command, description):
    """Thực thi một lệnh shell và thoát nếu có lỗi."""
    print(f"\n[*] {description}...")
    try:
        subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"[+] Thành công: {description}")
    except subprocess.CalledProcessError as e:
        print(f"[-] Lỗi khi {description}: {e}")
        print(f"[-] Stderr: {e.stderr}")
        sys.exit(1)

def get_installed_gemini_version():
    """Lấy phiên bản Gemini CLI đã cài đặt."""
    print("[*] Kiểm tra phiên bản Gemini CLI đã cài đặt...")
    try:
        result = subprocess.run(
            "gemini --version",
            shell=True, capture_output=True, text=True, check=True
        )
        version_part = result.stdout.split(' ')[0]
        version = version_part.split('/')[-1]
        print(f"[+] Đã tìm thấy Gemini CLI phiên bản: {version.strip()}")
        return version.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[-] Gemini CLI chưa được cài đặt hoặc không có trong PATH.")
        return None

def get_latest_gemini_version():
    """Lấy phiên bản Gemini CLI mới nhất từ npm."""
    print("[*] Lấy phiên bản Gemini CLI mới nhất từ npm...")
    try:
        result = subprocess.run(
            "npm view @google/gemini-cli version",
            shell=True, capture_output=True, text=True, check=True
        )
        latest_version = result.stdout.strip()
        print(f"[+] Phiên bản mới nhất là: {latest_version}")
        return latest_version
    except subprocess.CalledProcessError as e:
        print(f"[-] Không thể lấy phiên bản mới nhất từ npm: {e}")
        return None

def configure_mcp(home, hexstrike_dir, port):
    """Cấu hình MCP và tự động sao lưu file settings.json."""
    print("\n[*] Cấu hình MCP cho Gemini CLI...")
    gemini_config_dir = os.path.join(home, ".gemini")
    os.makedirs(gemini_config_dir, exist_ok=True)
    
    settings_path = os.path.join(gemini_config_dir, "settings.json")
    
    # Tự động sao lưu cấu hình
    if os.path.exists(settings_path):
        backup_path = settings_path + ".bak"
        print(f"[*] Sao lưu cấu hình hiện tại vào '{backup_path}'...")
        try:
            shutil.copyfile(settings_path, backup_path)
            print("[+] Sao lưu thành công.")
        except Exception as e:
            print(f"[-] Cảnh báo: Không thể sao lưu file settings.json: {e}")

    python_executable = os.path.join(hexstrike_dir, "hexstrike-env/bin/python3")
    mcp_script_path = os.path.join(hexstrike_dir, "hexstrike_mcp.py")

    mcp_config = {
        "hexstrike-ai": {
            "command": python_executable,
            "args": [mcp_script_path, "--server", f"http://localhost:{port}"],
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

def main():
    parser = argparse.ArgumentParser(description="HexStrike AI & Gemini CLI Auto Installer")
    parser.add_argument(
        '--force-reinstall',
        action='store_true',
        help='Bỏ qua kiểm tra phiên bản và buộc cài đặt lại mọi thứ.'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8888,
        help='Cổng tùy chỉnh cho HexStrike AI server (mặc định: 8888).'
    )
    args = parser.parse_args()

    home = str(Path.home())
    current_dir = os.getcwd()
    hexstrike_dir = os.path.join(current_dir, "hexstrike-ai")
    
    print("=== HexStrike AI & Gemini CLI Auto Installer ===")
    print(f"[*] Cấu hình cổng server: {args.port}")
    
    full_install = True
    if args.force_reinstall:
        print("\n[!] Cờ --force-reinstall được sử dụng. Buộc cài đặt lại.")
    else:
        installed_version = get_installed_gemini_version()
        latest_version = get_latest_gemini_version()
        if installed_version and latest_version and installed_version == latest_version:
            print("\n[!] Bạn đã có phiên bản Gemini CLI mới nhất. Bỏ qua các bước cài đặt.")
            full_install = False

    if full_install:
        print("\n[*] Bắt đầu quy trình cài đặt đầy đủ...")
        run_command("sudo apt-get update && sudo apt-get install -y nodejs npm", "Cài đặt Node.js và npm")
        run_command("sudo npm install -g @google/gemini-cli", "Cài đặt/Cập nhật Gemini CLI")

        if not os.path.exists(hexstrike_dir):
            run_command(f"git clone https://github.com/0x4m4/hexstrike-ai.git '{hexstrike_dir}'", "Clone repository HexStrike AI")
        else:
            print("[!] Thư mục hexstrike-ai đã tồn tại. Cập nhật thay đổi mới nhất...")
            run_command(f"cd '{hexstrike_dir}' && git pull", "Cập nhật repository")

        print("[*] Cài đặt môi trường ảo và các gói phụ thuộc...")
        os.chdir(hexstrike_dir)
        run_command("python3 -m venv hexstrike-env", "Tạo môi trường ảo (venv)")
        pip_path = os.path.join(hexstrike_dir, "hexstrike-env/bin/pip")
        run_command(f"{pip_path} install --upgrade pip", "Nâng cấp pip")
        run_command(f"{pip_path} install -r requirements.txt", "Cài đặt Python dependencies")
        os.chdir(current_dir)
    
    if not os.path.exists(hexstrike_dir):
        print(f"[-] Lỗi: Không tìm thấy thư mục '{hexstrike_dir}'.")
        print("[-] Không thể cấu hình MCP. Vui lòng chạy lại để cài đặt đầy đủ.")
        sys.exit(1)

    configure_mcp(home, hexstrike_dir, args.port)

    print("\n=== CÀI ĐẶT HOÀN TẤT ===")
    print("[!] Lưu ý quan trọng:")
    print("    1. Chạy 'gemini login' để đăng nhập nếu bạn chưa làm.")
    print(f"    2. Trước khi sử dụng, hãy mở terminal khác, vào thư mục 'hexstrike-ai' và chạy: python3 hexstrike_server.py --port {args.port}")

if __name__ == "__main__":
    main()
