import http.server
import os
import socketserver
import cgi
import json
import label_processor.image_processor as image_processor

PORT = 8000

class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        # Xử lý yêu cầu POST (upload ảnh)
        content_type = self.headers['Content-Type']
        if 'multipart/form-data' in content_type:
            # Lấy boundary từ Content-Type để phân tách dữ liệu
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )

            # Tìm trường file (ví dụ: 'file' là tên trường trong form)
            file_item = form['file']
            if file_item.filename:
                # Lưu file ảnh được upload vào ổ đĩa
                file_data = file_item.file.read()
                file_name = file_item.filename
                file_path = f"./uploaded_images/{file_name}"
                with open(file_path, "wb") as output_file:
                    output_file.write(file_data)

                result = image_processor.image_to_product_label_model(file_path)
                # response = {
                #     'status': 'success',
                #     'message': 'File uploaded successfully!',
                #     'file_name': file_name
                # }
                os.remove(file_path)
                if result != None:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(result.to_json().encode('utf-8'))
                else:
                    response = {'status': 'error', 'message': 'No file uploaded!'}
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode('utf-8'))
            else:
                # Xử lý nếu không có file trong yêu cầu POST
                response = {'status': 'error', 'message': 'No file uploaded!'}
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            # Trường hợp Content-Type không phải multipart/form-data
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'error', 'message': 'Invalid content type!'}).encode('utf-8'))

# Khởi tạo server
with socketserver.TCPServer(("", PORT), SimpleHTTPRequestHandler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()
