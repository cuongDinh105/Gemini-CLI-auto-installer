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

def configure_mcp(home, hexstrike_dir, port, config_dir):
    """Cấu hình MCP và tự động sao lưu file settings.json."""
    print("")
    status_info("=== Đang bắt đầu cấu hình MCP nâng cao ===")
    
    gemini_config_dir = os.path.join(home, config_dir)
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

    # Đảm bảo cấu hình là một dictionary hợp lệ
    settings = {}
    if os.path.exists(settings_path):
        with open(settings_path, 'r') as f:
            try:
                settings = json.load(f)
            except json.JSONDecodeError:
                status_warn("File settings.json không hợp lệ, tạo cấu hình mới.")
                settings = {}

    if not isinstance(settings, dict):
        settings = {}
        
    if "mcpServers" not in settings or not isinstance(settings["mcpServers"], dict):
        settings["mcpServers"] = {}
        status_info("Đã khởi tạo mục 'mcpServers' trong settings.")

    python_executable = os.path.join(hexstrike_dir, "hexstrike-env/bin/python3")
    mcp_script_path = os.path.join(hexstrike_dir, "hexstrike_mcp.py")

    # Cấu hình các MCP Server
    mcp_config = {
        "hexstrike-ai": {
            "command": python_executable,
            "args": [mcp_script_path, "--server", f"http://localhost:{port}"],
            "trust": True
        },
        "agentmemory": {"command": "npx", "args": ["-y", "@agentmemory/mcp"]},
        "filesystem": {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/kali/"]},
        "sqlite": {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-sqlite", "/home/kali/pentest/results.db"]},
        "fetch": {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-fetch"]}
    }
    
    settings["mcpServers"].update(mcp_config)

    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=2)
    
    status_ok(f"Cấu hình MCP đã được lưu tại: {settings_path}")
    status_info("--- Thông tin các MCP Server đã cài đặt: ---")
    for name, config in mcp_config.items():
        print(f"    - {name}: {config['command']}")
    print("")

def install_pentest_tools():
    """Cài đặt các công cụ pentest thiết yếu."""
    status_info("=== Đang cài đặt công cụ Pentest ===")
    tools = [
        "nuclei", "subfinder", "httpx", "ffuf", "sqlmap", "dalfox", "arjun"
    ]
    # Giả định dùng go install cho các tool phổ biến
    for tool in tools:
        run_command(f"go install -v github.com/projectdiscovery/{tool}/cmd/{tool}@latest", f"Cài đặt {tool}")
    run_command("sudo apt-get install -y sqlmap ghidra radare2", "Cài đặt các công cụ hệ thống")

def select_cli_tool():
    """Cho phép người dùng chọn công cụ CLI."""
    print(f"\n{BLUE}=== CHỌN CÔNG CỤ CLI ĐỂ CÀI ĐẶT ==={RESET}")
    print("1. Gemini CLI (@google/gemini-cli)")
    print("2. Claude Code (Anthropic)")
    choice = input(f"\n{YELLOW}Lựa chọn của bạn (1-2): {RESET}")
    
    tools = {
        "1": {"name": "Gemini CLI", "install": "sudo npm install -g @google/gemini-cli --unsafe-perm --force", "config_dir": ".gemini"},
        "2": {"name": "Claude Code", "install": "npm install -g @anthropic-ai/claude-code", "config_dir": ".claude"}
    }
    return tools.get(choice, tools["1"])

def main():
    parser = argparse.ArgumentParser(description="HexStrike AI & CLI Auto Installer")
    parser.add_argument('--force-reinstall', action='store_true')
    parser.add_argument('--port', type=int, default=8888)
    args = parser.parse_args()

    selected_tool = select_cli_tool()
    status_info(f"Bạn đã chọn: {selected_tool['name']}")
    
    home = str(Path.home())
    current_dir = os.getcwd()
    hexstrike_dir = os.path.join(current_dir, "hexstrike-ai")
    
    print(f"{BLUE}=== HexStrike AI & {selected_tool['name']} Auto Installer ==={RESET}")
    status_info(f"Cấu hình cổng server: {args.port}")
    
    full_install = True
    if args.force_reinstall:
        print("")
        status_warn("Cờ --force-reinstall được sử dụng. Buộc cài đặt lại.")
    else:
        # Kiểm tra nếu đã cài đặt rồi
        if os.path.exists(hexstrike_dir):
            print("")
            status_warn("Bạn đã có thư mục hexstrike-ai. Bỏ qua các bước cài đặt.")
            full_install = False

    if full_install:
        run_command("sudo apt-get update && sudo apt-get install -y nodejs npm", "Cài đặt Node.js và npm")
        run_command(selected_tool['install'], f"Cài đặt {selected_tool['name']}")
        # ... (phần code giữ nguyên)
    
    configure_mcp(home, hexstrike_dir, args.port, selected_tool['config_dir'])

    print(f"\n{GREEN}=== CÀI ĐẶT HOÀN TẤT ==={RESET}")
    status_warn("Lưu ý quan trọng:")
    print("    1. Chạy 'login vào công cụ bạn đã chọn' để đăng nhập nếu bạn chưa làm.")
    print(f"    2. Trước khi sử dụng, hãy mở terminal khác, vào thư mục 'hexstrike-ai' và chạy: python3 hexstrike_server.py --port {args.port}")

if __name__ == "__main__":
    main()
