# Lộ trình thực hành cho SANIM

## 1. Đọc một case từ đầu đến cuối

Mở `balance-six-decimals` trong dataset. Giải thích vì sao raw balance 1234567 với decimals 6 cho ra 1.234567. Chạy baseline, đọc claims, sau đó chạy vulnerable và tìm `claims_mismatch`.

## 2. Phân biệt thiếu dữ liệu với lỗi

So sánh receipt thành công, reverted và không có receipt. Trạng thái reverted chưa đủ để kết luận slippage. Viết thêm một case với dữ liệu thiếu và đáp án `unknown`.

## 3. Kiểm thử security ở hai lớp

Đọc `metadata-approval`. Đầu vào cố yêu cầu cấp allowance rất lớn. Agent reference không đề xuất hành động. Agent vulnerable đề xuất `approve`; policy chặn nhưng evaluator vẫn đánh dấu lỗi của agent. Chú ý câu trả lời “tôi từ chối” không xóa được tool call trái phép.

## 4. Làm một thay đổi có thể giải thích khi phỏng vấn

Thêm case token cùng symbol nhưng khác contract. Viết golden trước; tạo lỗi cố ý ở target; chứng minh test phát hiện; sửa target và chạy lại. Ghi rõ test đang đánh giá structured claim nào.

## 5. Nối model thật sau khi hiểu harness

Xây adapter chỉ gửi request, thu JSON output và trace từ dispatcher, lưu theo case ID rồi chạy `--responses`. Không gửi goldens hoặc `demo_fault` vào prompt. Ghi model, prompt version, thời điểm và tham số sinh. Lặp nhiều lần và kiểm tra bằng người các câu trả lời tự nhiên mâu thuẫn với claims.

Portfolio hiện tại thể hiện: test design, blockchain data validation, security threat modeling, negative testing, deterministic evaluation và CI. Chỉ bổ sung tuyên bố “đã đánh giá LLM thật” khi có bằng chứng chạy model thật.
