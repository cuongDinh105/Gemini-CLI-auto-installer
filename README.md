# Gemini-CLI-auto-installer (Pentest Edition)

Đây là công cụ tự động hóa toàn diện để biến Gemini CLI thành một **Nền tảng Pentest Tự động** (Autonomous Pentesting Platform) chuyên nghiệp.

---

## 1. Các thành phần chính

### Pentest Tools (Tự động cài đặt)
- **Công cụ Quét & Recon**: `nuclei` (vulnerability scanner), `subfinder` (subdomain enum), `httpx` (HTTP prober), `ffuf` (fuzzing), `dalfox` (XSS), `arjun` (parameter discovery).
- **Công cụ Khai thác & Phân tích**: `sqlmap` (SQLi), `ghidra` (reverse engineering), `radare2` (binary analysis).

### MCP Servers (Tự động đăng ký)
- `hexstrike-ai`: Điều khiển các công cụ pentest.
- `agentmemory`: Quản lý bộ nhớ ngữ cảnh và lịch sử dự án.
- `filesystem`, `sqlite`, `fetch`: Hỗ trợ quản lý báo cáo, truy vấn kết quả và tra cứu tài liệu.

### Anthropic Cybersecurity Skills
Dự án tự động tích hợp kho kỹ năng bảo mật từ [Anthropic-Cybersecurity-Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills.git). Đây là kho tài nguyên quý giá để Gemini AI học hỏi cách thực hiện các kỹ thuật bảo mật từ cơ bản đến nâng cao.

---

## 2. Cài đặt

1. **Clone dự án:**
   ```bash
   git clone https://github.com/cuongDinh105/Gemini-CLI-auto-installer.git
   cd Gemini-CLI-auto-installer
   ```

2. **Chạy script (tự động cài đặt tool, clone skills và cấu hình MCP):**
   ```bash
   python3 setup_hexstrike_gemini.py
   ```

---

## 3. Cách sử dụng

1. **Đăng nhập:** `gemini login`
2. **Khởi chạy HexStrike Server:**
   ```bash
   cd hexstrike-ai
   python3 hexstrike_server.py --port 8888
   ```
3. **Thực thi Pentest:**
   - Sử dụng workflow tự động: `python3 pentest_workflow.py <domain>`
   - Hoặc yêu cầu trực tiếp với AI để kết hợp các Skills đã được cài đặt.

---

## 4. Quản lý
- **MCP Config:** `~/.gemini/settings.json`
- **Kỹ năng bảo mật:** Thư mục `anthropic-cybersecurity-skills/`
- **Công cụ:** Đã được đưa vào PATH hệ thống (thường thông qua `$HOME/go/bin`).
