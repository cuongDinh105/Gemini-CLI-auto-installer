# Gemini-CLI-auto-installer

Đây là công cụ tự động hóa quá trình cài đặt và cấu hình **Gemini CLI** cùng các dịch vụ **MCP (Model Context Protocol)** hỗ trợ cho **HexStrike AI**.

## Tính năng chính
- Tự động kiểm tra và cài đặt phiên bản Gemini CLI mới nhất.
- Clone và cập nhật tự động repository HexStrike AI.
- Thiết lập môi trường ảo Python (venv) và cài đặt các thư viện cần thiết.
- Tự động cấu hình MCP Server cho Gemini CLI:
  - **HexStrike AI**: Server phục vụ các công cụ pentest.
  - **AgentMemory**: Server quản lý bộ nhớ cho tác nhân AI.

## Cài đặt

1. Clone dự án về máy:
   ```bash
   git clone https://github.com/cuongDinh105/Gemini-CLI-auto-installer.git
   cd Gemini-CLI-auto-installer
   ```

2. Chạy script cài đặt:
   ```bash
   python3 setup_hexstrike_gemini.py
   ```

3. (Tùy chọn) Chạy lại với cờ force-reinstall nếu bạn muốn cài đặt lại từ đầu:
   ```bash
   python3 setup_hexstrike_gemini.py --force-reinstall
   ```

## Sử dụng
Sau khi cài đặt xong, hãy làm theo hướng dẫn in trên terminal:
1. Đăng nhập vào Gemini CLI:
   ```bash
   gemini login
   ```
2. Mở một terminal mới và chạy HexStrike server:
   ```bash
   cd hexstrike-ai
   python3 hexstrike_server.py --port 8888
   ```

## Cấu hình MCP
Script sẽ tự động cập nhật file `~/.gemini/settings.json` của bạn. Bạn có thể kiểm tra danh sách các server đã đăng ký bằng cách xem file này.
