# Gemini-CLI-auto-installer

Đây là công cụ tự động hóa quá trình cài đặt và cấu hình **Gemini CLI** kết hợp với các **MCP (Model Context Protocol)** server mạnh mẽ, tạo ra môi trường làm việc chuyên nghiệp cho các tác vụ Pentest và tự động hóa AI.

---

## 1. Các thành phần được cài đặt

### A. Gemini CLI (@google/gemini-cli)
- **Chức năng:** Giao diện dòng lệnh chính để tương tác với các mô hình ngôn ngữ lớn (LLM) của Google.
- **Vai trò:** Điều phối các yêu cầu và kết nối với các công cụ hỗ trợ thông qua giao thức MCP.

### B. HexStrike AI (HexStrike-AI)
- **Chức năng:** Bộ công cụ Pentest nâng cao được tích hợp dưới dạng MCP Server.
- **Tính năng:**
    - Quét mạng, quét lỗ hổng (nmap, nuclei, trivy,...).
    - Khai thác lỗ hổng (sqlmap, metasploit).
    - Phân tích mã nhị phân, reverse engineering (ghidra, radare2).
    - OSINT và thu thập thông tin mục tiêu.

### C. AgentMemory MCP Server
- **Chức năng:** Cung cấp khả năng ghi nhớ cho các tác nhân AI.
- **Vai trò:** Lưu trữ, truy xuất ngữ cảnh và các thông tin quan trọng trong quá trình làm việc, giúp AI duy trì sự nhất quán qua nhiều phiên làm việc.

---

## 2. Yêu cầu hệ thống
- Hệ điều hành: Linux (khuyên dùng Kali Linux).
- Python 3.x
- Node.js & npm (để cài đặt Gemini CLI và AgentMemory).
- Git.

---

## 3. Cách cài đặt

1. **Clone dự án:**
   ```bash
   git clone https://github.com/cuongDinh105/Gemini-CLI-auto-installer.git
   cd Gemini-CLI-auto-installer
   ```

2. **Chạy script tự động cài đặt:**
   ```bash
   python3 setup_hexstrike_gemini.py
   ```
   *Script sẽ tự động:* 
   - Kiểm tra và cập nhật Gemini CLI.
   - Clone repository HexStrike AI.
   - Tạo môi trường ảo Python và cài đặt thư viện.
   - Cấu hình các MCP Server vào `~/.gemini/settings.json`.

---

## 4. Cách sử dụng

### BƯỚC 1: Đăng nhập
Đảm bảo bạn đã đăng nhập vào Gemini CLI:
```bash
gemini login
```

### BƯỚC 2: Khởi chạy HexStrike Server
Để các công cụ pentest có thể giao tiếp với AI, bạn cần chạy HexStrike server riêng biệt:
```bash
cd hexstrike-ai
python3 hexstrike_server.py --port 8888
```

### BƯỚC 3: Sử dụng cùng AI
Khi đã chạy server, bạn có thể gọi trực tiếp các công cụ pentest ngay trong phiên trò chuyện của Gemini CLI:
*Ví dụ: "Hãy quét cổng mục tiêu 192.168.1.1"* (AgentMemory sẽ ghi nhớ tiến trình, HexStrike thực hiện tác vụ).

---

## 5. Quản lý cấu hình
Các MCP Server được quản lý trong file: `~/.gemini/settings.json`. Nếu cần tùy chỉnh thêm, bạn có thể chỉnh sửa trực tiếp file này.
