# CT999 - Năng lực số nâng cao - Đồ án cuối kỳ - Chatbot về Lớp Thú trong sách đỏ Việt Nam

Đây là dự án Chatbot sử dụng kỹ thuật RAG để tăng cường khả năng truy xuất thông tin của mô hình. Mô hình embedding là `bre-m3` của OLlama, mô hình LLM là `command-r-08-2024`.

Tác giả: Nguyễn Minh Nhật, Lê Trúc Nhi, Phạm Thành Tuấn Lộc.

## Chạy Chatbox

### 1. Tạo và kích hoạt môi trường

```bash
python -m venv venv
```

### 2. Cài thư viện

- python-docx
- PyPDF2
- beautifulsoup4
- faiss-cpu
- sentence-transformers
- langchain==0.3.0
- langchain-community
- langchain-cohere==0.3.1
- langchain-core==0.3.15
- langchain-experimental==0.3.2
- langchain-text-splitters==0.3.2
- flask
- requests
- cohere
- pdfminer.six
- pydantic

Cài đặt các thư viện bằng lệnh sau:

```bash
pip install -r requirements.txt
```

### 3. Tạo dataset

```bash
python .\scripts\process_vnredlist_data.py
```

File `processed_data.txt` sẽ được tạo trong thư mục `dataset`

### 4. Run web app

```bash
python .\app\main.py  
```

Truy cập web Chatbot tại: <http://127.0.0.1:5001/>
