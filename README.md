# Gemini-CLI-auto-installer (Pentest Edition)

Đây là công cụ tự động hóa toàn diện để biến Gemini CLI thành một **Nền tảng Pentest Tự động** (Autonomous Pentesting Platform).

---

## 1. Công cụ & Thành phần tích hợp

### Pentest Tools (Tự động cài đặt)
- **ProjectDiscovery Suite**: `nuclei` (quét lỗ hổng), `subfinder` (recon), `httpx` (prober), `ffuf` (fuzzing), `dalfox` (XSS), `arjun` (param discovery).
- **Hệ thống**: `sqlmap` (khai thác SQLi), `ghidra` (reverse engineering), `radare2` (phân tích binary).

### MCP Servers (Tự động đăng ký)
- `hexstrike-ai`: Server điều khiển các công cụ pentest.
- `agentmemory`: Lưu trữ ngữ cảnh dự án và bộ nhớ cho AI.
- `filesystem`: Truy cập đọc/ghi file báo cáo/log trực tiếp.
- `sqlite`: Truy vấn database kết quả pentest (`results.db`).
- `fetch`: Truy cập tài liệu bảo mật trực tuyến.

### Skills Nâng cao
- `automated-api-audit`: Tự động audit API bằng chuỗi công cụ `httpx` + `arjun` + `nuclei`.
- `recon-workflow`: Quy trình tự động từ subdomain đến báo cáo lỗ hổng.
- `binary-exploitation-triage`: Tự động phân tích binary.
- `cloud-threat-hunting`: Phân tích logs AWS/Azure để tìm dấu hiệu xâm nhập.

---

## 2. Cài đặt

1. **Clone dự án:**
   ```bash
   git clone https://github.com/cuongDinh105/Gemini-CLI-auto-installer.git
   cd Gemini-CLI-auto-installer
   ```

2. **Chạy script (tự động cài đặt tool và cấu hình MCP):**
   ```bash
   python3 setup_hexstrike_gemini.py
   ```

---

## 3. Cách sử dụng

1. **Đăng nhập:** `gemini login`
2. **Khởi chạy HexStrike Server:** `cd hexstrike-ai && python3 hexstrike_server.py --port 8888`
3. **Tác vụ Pentest:**
   - Hỏi AI: *"Quét lỗ hổng API tại mục tiêu [URL]"* -> AI sẽ tự động kích hoạt workflow API Audit.
   - Hỏi AI: *"Liệt kê danh sách endpoint đã tìm thấy"* -> AI truy vấn SQLite/Filesystem để đưa ra báo cáo.

---

## 4. Quản lý
Toàn bộ cấu hình MCP nằm tại `~/.gemini/settings.json`.
