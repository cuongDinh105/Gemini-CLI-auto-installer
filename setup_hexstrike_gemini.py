import os
import subprocess
import json
import sys
import argparse
import shutil
from pathlib import Path

# ANSI Color Codes
GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def status_ok(msg):
    print(f"{GREEN}[+]{RESET} {msg}")

def status_err(msg):
    print(f"{RED}[-]{RESET} {msg}")

def status_info(msg):
    print(f"{BLUE}[*]{RESET} {msg}")

def status_warn(msg):
    print(f"{YELLOW}[!] {msg}{RESET}")

def run_command(command, description):
    """Thực thi một lệnh shell và thoát nếu có lỗi."""
    print("")
    status_info(f"{description}...")
    try:
        subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        status_ok(f"Thành công: {description}")
    except subprocess.CalledProcessError as e:
        status_err(f"Lỗi khi {description}: {e}")
        status_err(f"Stderr: {e.stderr}")
        sys.exit(1)

def get_installed_gemini_version():
    """Lấy phiên bản Gemini CLI đã cài đặt."""
    status_info("Kiểm tra phiên bản Gemini CLI đã cài đặt...")
    try:
        result = subprocess.run(
            "gemini --version",
            shell=True, capture_output=True, text=True, check=True
        )
        version_part = result.stdout.split(' ')[0]
        version = version_part.split('/')[-1]
        status_ok(f"Đã tìm thấy Gemini CLI phiên bản: {version.strip()}")
        return version.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        status_err("Gemini CLI chưa được cài đặt hoặc không có trong PATH.")
        return None

def get_latest_gemini_version():
    """Lấy phiên bản Gemini CLI mới nhất từ npm."""
    status_info("Lấy phiên bản Gemini CLI mới nhất từ npm...")
    try:
        result = subprocess.run(
            "npm view @google/gemini-cli version",
            shell=True, capture_output=True, text=True, check=True
        )
        latest_version = result.stdout.strip()
        status_ok(f"Phiên bản mới nhất là: {latest_version}")
        return latest_version
    except subprocess.CalledProcessError as e:
        status_err(f"Không thể lấy phiên bản mới nhất từ npm: {e}")
        return None

def configure_mcp(home, hexstrike_dir, port):
    """Cấu hình MCP và tự động sao lưu file settings.json."""
    print("")
    status_info("=== Đang bắt đầu cấu hình MCP ===")
    status_info("Hệ thống sẽ đăng ký các MCP Server vào Gemini CLI settings.")
    
    gemini_config_dir = os.path.join(home, ".gemini")
    os.makedirs(gemini_config_dir, exist_ok=True)
    
    settings_path = os.path.join(gemini_config_dir, "settings.json")
    
    # Tự động sao lưu cấu hình
    if os.path.exists(settings_path):
        backup_path = settings_path + ".bak"
        status_info(f"Sao lưu cấu hình hiện tại vào '{backup_path}'...")
        try:
            shutil.copyfile(settings_path, backup_path)
            status_ok("Sao lưu thành công.")
        except Exception as e:
            status_err(f"Cảnh báo: Không thể sao lưu file settings.json: {e}")

    python_executable = os.path.join(hexstrike_dir, "hexstrike-env/bin/python3")
    mcp_script_path = os.path.join(hexstrike_dir, "hexstrike_mcp.py")

    status_info("Đang định nghĩa cấu hình cho các MCP Server...")
    mcp_config = {
        "hexstrike-ai": {
            "command": python_executable,
            "args": [mcp_script_path, "--server", f"http://localhost:{port}"],
            "trust": True
        },
        "agentmemory": {
            "command": "npx",
            "args": [
                "-y",
                "@agentmemory/mcp"
            ]
        }
    }
    status_ok("Đã định nghĩa: hexstrike-ai và agentmemory.")

    settings = {}
    if os.path.exists(settings_path):
        with open(settings_path, 'r') as f:
            try:
                settings = json.load(f)
                status_info("Đã tải cấu hình hiện có từ settings.json.")
            except json.JSONDecodeError:
                status_warn("File settings.json không hợp lệ, tạo cấu hình mới.")
                settings = {}

    if "mcpServers" not in settings:
        settings["mcpServers"] = {}
        status_info("Đã tạo mục 'mcpServers' mới.")
    
    settings["mcpServers"].update(mcp_config)

    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=2)
    
    status_ok(f"Cấu hình MCP đã được lưu tại: {settings_path}")
    status_info("--- Thông tin các MCP Server đã cài đặt: ---")
    for name, config in mcp_config.items():
        print(f"    - {name}: {config['command']}")
    print("")

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
    
    print(f"{BLUE}=== HexStrike AI & Gemini CLI Auto Installer ==={RESET}")
    status_info(f"Cấu hình cổng server: {args.port}")
    
    full_install = True
    if args.force_reinstall:
        print("")
        status_warn("Cờ --force-reinstall được sử dụng. Buộc cài đặt lại.")
    else:
        installed_version = get_installed_gemini_version()
        latest_version = get_latest_gemini_version()
        if installed_version and latest_version and installed_version == latest_version:
            print("")
            status_warn("Bạn đã có phiên bản Gemini CLI mới nhất. Bỏ qua các bước cài đặt.")
            full_install = False

    if full_install:
        print("")
        status_info("Bắt đầu quy trình cài đặt đầy đủ...")
        
        # Xử lý ENOTEMPTY và Xung đột NPM bằng cách dọn dẹp và dùng flag an toàn
        run_command("sudo apt-get update && sudo apt-get install -y nodejs npm", "Cài đặt Node.js và npm")
        
        # Thêm flag --unsafe-perm và --force để tránh lỗi ghi đè thư mục (ENOTEMPTY)
        run_command("sudo npm install -g @google/gemini-cli --unsafe-perm --force", "Cài đặt/Cập nhật Gemini CLI")

        if not os.path.exists(hexstrike_dir):
            run_command(f"git clone https://github.com/0x4m4/hexstrike-ai.git '{hexstrike_dir}'", "Clone repository HexStrike AI")
        else:
            print("")
            status_warn("Thư mục hexstrike-ai đã tồn tại. Cập nhật thay đổi mới nhất...")
            run_command(f"cd '{hexstrike_dir}' && git pull", "Cập nhật repository")

        print("")
        status_info("Cài đặt môi trường ảo và các gói phụ thuộc...")
        os.chdir(hexstrike_dir)
        run_command("python3 -m venv hexstrike-env", "Tạo môi trường ảo (venv)")
        pip_path = os.path.join(hexstrike_dir, "hexstrike-env/bin/pip")
        run_command(f"{pip_path} install --upgrade pip", "Nâng cấp pip")
        run_command(f"{pip_path} install -r requirements.txt", "Cài đặt Python dependencies")
        os.chdir(current_dir)
    
    if not os.path.exists(hexstrike_dir):
        status_err(f"Lỗi: Không tìm thấy thư mục '{hexstrike_dir}'.")
        status_err("Không thể cấu hình MCP. Vui lòng chạy lại để cài đặt đầy đủ.")
        sys.exit(1)

    configure_mcp(home, hexstrike_dir, args.port)

    print(f"\n{GREEN}=== CÀI ĐẶT HOÀN TẤT ==={RESET}")
    status_warn("Lưu ý quan trọng:")
    print("    1. Chạy 'gemini login' để đăng nhập nếu bạn chưa làm.")
    print(f"    2. Trước khi sử dụng, hãy mở terminal khác, vào thư mục 'hexstrike-ai' và chạy: python3 hexstrike_server.py --port {args.port}")

if __name__ == "__main__":
    main()
