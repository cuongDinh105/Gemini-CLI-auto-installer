# HexStrike AI & Gemini CLI Auto Installer

Công cụ tự động hóa việc cài đặt toàn bộ hệ sinh thái HexStrike AI MCP và Gemini CLI trên Linux (Kali/Ubuntu).

## Tính năng
- Tự động cài đặt Node.js, npm.
- Cài đặt Gemini CLI.
- Cài đặt HexStrike AI (Git clone, Venv, Pip).
- Tự động cấu hình kết nối MCP giữa Gemini CLI và HexStrike AI.

## Cách sử dụng
1. Tải script về:
   ```bash
   wget https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/setup_hexstrike_gemini.py
   ```
2. Chạy script:
   ```bash
   python3 setup_hexstrike_gemini.py
   ```
3. Đăng nhập Gemini:
   ```bash
   gemini login
   ```
4. Bật server HexStrike:
   ```bash
   cd hexstrike-ai
   python3 hexstrike_server.py
   ```
