# Gemini-CLI-auto-installer (Pentest Edition)

Đây là nền tảng **Pentest Tự động (Autonomous Pentesting Platform)**, tích hợp Gemini CLI cùng các công cụ bảo mật chuyên dụng và MCP Servers để tối ưu hóa quy trình kiểm thử.

---

## 1. Thành phần Tích hợp

### 🛠 Pentest Tools (Tự động cài đặt)
- **Recon**: `nuclei`, `subfinder`, `httpx`, `ffuf`, `dalfox`, `arjun`.
- **Exploit & Analysis**: `sqlmap`, `ghidra`, `radare2`.

### 🔌 MCP Servers (Giao diện điều khiển AI)
- `hexstrike-ai`: Server điều khiển trực tiếp các tool pentest qua lệnh AI.
- `agentmemory`: Ghi nhớ ngữ cảnh, kết quả quét và các phát hiện quan trọng.
- `filesystem`: Đọc/ghi các file báo cáo, log, script trực tiếp vào máy.
- `sqlite`: Truy vấn dữ liệu từ các file kết quả `.db`.
- `fetch`: Tra cứu nhanh tài liệu bảo mật, blog, hoặc kỹ thuật tấn công mới nhất.

---

## 2. Hướng dẫn sử dụng chi tiết

### A. Sử dụng MCP Servers
Bạn có thể ra lệnh cho AI gọi các server này:

| MCP Server | Mục đích | Ví dụ lệnh yêu cầu AI |
| :--- | :--- | :--- |
| `filesystem` | Đọc báo cáo | "Đọc file `vulnerabilities.txt` và tóm tắt lỗ hổng nghiêm trọng" |
| `sqlite` | Query dữ liệu | "Truy vấn các subdomain đã tìm thấy trong `results.db`" |
| `fetch` | Tra cứu kỹ thuật | "Tìm tài liệu về CVE-2023-xxxx từ Google" |
| `agentmemory`| Ghi nhớ | "Ghi nhớ rằng mục tiêu hiện tại là vanphongso.bvmat.vn" |

### B. Sử dụng các Skills nâng cao
Các skills này giúp tự động hóa quy trình:

1. **`recon-workflow`**: Tự động hóa recon từ A-Z.
   - *Yêu cầu AI:* "Chạy recon-workflow cho mục tiêu [domain]"
2. **`automated-api-audit`**: Quét lỗ hổng API chuyên sâu.
   - *Yêu cầu AI:* "Thực hiện automated-api-audit cho [URL]"
3. **`binary-exploitation-triage`**: Phân tích file binary.
   - *Yêu cầu AI:* "Phân tích binary [file_path] bằng skill binary-exploitation-triage"
4. **`cloud-threat-hunting`**: Hunting trên môi trường Cloud.
   - *Yêu cầu AI:* "Chạy cloud-threat-hunting trên cấu hình AWS hiện tại"

---

## 3. Cài đặt & Khởi chạy

1. **Clone dự án:**
   ```bash
   git clone https://github.com/cuongDinh105/Gemini-CLI-auto-installer.git
   cd Gemini-CLI-auto-installer
   ```

2. **Cài đặt:**
   ```bash
   python3 setup_hexstrike_gemini.py --force-reinstall
   ```
   *(Chọn công cụ CLI bạn muốn sử dụng: Gemini, Claude hoặc Codex).*

3. **Khởi chạy HexStrike Server:**
   ```bash
   cd hexstrike-ai
   python3 hexstrike_server.py --port 8888
   ```

---

## 4. Lưu ý
- Mọi cấu hình kết nối MCP nằm tại `~/.gemini/settings.json` (hoặc `.claude`, `.codex` tùy lựa chọn).
- Hãy đảm bảo bạn đã cấp quyền chạy file thực thi trong thư mục `hexstrike-ai`.
