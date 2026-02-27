# HexStrike AI & Gemini CLI Auto Installer

Công cụ tự động hóa việc cài đặt toàn bộ hệ sinh thái HexStrike AI MCP và Gemini CLI trên Linux (Kali/Ubuntu).

## Tính năng
- Tự động cài đặt Node.js, npm.
- Cài đặt Gemini CLI (kiểm tra phiên bản để tránh cài lại không cần thiết).
- Cài đặt HexStrike AI (Git clone, Venv, Pip).
- Tự động cấu hình kết nối MCP giữa Gemini CLI và HexStrike AI.
- Tự động sao lưu file cấu hình `~/.gemini/settings.json` trước khi chỉnh sửa.

## Cách sử dụng

1.  **Tải script về từ repository của bạn:**
    ```bash
    wget https://raw.githubusercontent.com/cuongDinh105/Gemini-CLI-auto-installer/main/setup_hexstrike_gemini.py
    ```

2.  **Chạy script:**
    Để cài đặt hoặc cập nhật thông thường:
    ```bash
    python3 setup_hexstrike_gemini.py
    ```

    **Tùy chọn Nâng cao:**
    *   **Buộc cài đặt lại (`--force-reinstall`):** Bỏ qua kiểm tra phiên bản và buộc cài đặt lại tất cả các thành phần (Node.js, npm, Gemini CLI, HexStrike AI). Hữu ích khi gặp lỗi hoặc muốn cài đặt lại từ đầu.
        ```bash
        python3 setup_hexstrike_gemini.py --force-reinstall
        ```
    *   **Sử dụng cổng tùy chỉnh (`--port`):** Chỉ định một cổng khác thay cho cổng mặc định `8888` cho HexStrike AI server.
        ```bash
        python3 setup_hexstrike_gemini.py --port 9999
        ```
        *(Thay `9999` bằng cổng bạn muốn sử dụng)*

3.  **Đăng nhập Gemini:**
    Nếu bạn chưa đăng nhập, hãy chạy lệnh này:
    ```bash
    gemini login
    ```

4.  **Bật server HexStrike:**
    Mở một terminal khác, di chuyển vào thư mục `hexstrike-ai` và khởi động server. Đảm bảo sử dụng cùng cổng nếu bạn đã tùy chỉnh ở bước 2:
    ```bash
    cd hexstrike-ai
    python3 hexstrike_server.py --port <YOUR_CHOSEN_PORT_IF_ANY>
    ```
    *(Ví dụ nếu bạn dùng cổng 9999: `python3 hexstrike_server.py --port 9999`)*

## Repository chính thức
- Script Installer: https://github.com/cuongDinh105/Gemini-CLI-auto-installer/main/setup_hexstrike_gemini.py
- HexStrike AI (Gốc): https://github.com/0x4m4/hexstrike-ai.git