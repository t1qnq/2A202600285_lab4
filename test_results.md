# 🧪 TravelBuddy Agent — 5 Test Cốt Lõi

**Ngày test:** 07/04/2026 16:59
**Kết quả:** 5/5 PASS | 0/5 FAIL
**Đánh giá:** 🎉 Xuất sắc! Agent pass tất cả tests!

---

## 📋 Bảng kết quả

| # | Test | Input | Kỳ Vọng | Kết Quả |
|---|------|-------|---------|---------|
| 1 | Test 1 — Direct Answer (Không cần tool) | "Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu." | Agent chào hỏi, hỏi thêm về sở thích/ngân sách/thời gian. KHÔNG gọi tool. | ✅ ✅ PASS |
| 2 | Test 2 — Single Tool Call | "Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng" | Gọi search_flights('Hà Nội', 'Đà Nẵng'), liệt kê 4 chuyến bay. | ✅ ✅ PASS |
| 3 | Test 3 — Multi-Step Tool Chaining | "Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!" | Agent tự chuỗi: search_flights → search_hotels → tính budget → gợi ý hoàn chỉnh. | ✅ ✅ PASS |
| 4 | Test 4 — Missing Info / Clarification | "Tôi muốn đặt khách sạn" | Agent hỏi lại: thành phố nào? bao nhiêu đêm? ngân sách? KHÔNG gọi tool. | ✅ ✅ PASS |
| 5 | Test 5 — Guardrail / Refusal | "Giải giúp tôi bài tập lập trình Python về linked list" | Từ chối lịch sự, nói rằng chỉ hỗ trợ về du lịch. | ✅ ✅ PASS |

---

## 📝 Chi Tiết Response

### ✅ Test 1 — Direct Answer (Không cần tool)
- **Input:** `Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.`
- **Kỳ vọng:** Agent chào hỏi, hỏi thêm về sở thích/ngân sách/thời gian. KHÔNG gọi tool.
- **Kết quả:** ✅ PASS
- **Response:**
```
Xin chào! Rất vui được tư vấn cho bạn. Bạn có thể cho tôi biết một số thông tin để tôi giúp bạn lựa chọn điểm đến phù hợp không?

1. **Ngân sách dự kiến**: Bạn dự định chi bao nhiêu cho chuyến đi này?
2. **Thời gian đi**: Bạn có kế hoạch đi vào thời điểm nào không?
3. **Sở thích**: Bạn thích khám phá thiên nhiên, văn hóa lịch sử, hay nghỉ dưỡng thư giãn?
4. **Thành phố khởi hành**: Bạn sẽ xuất phát từ đâu?

Với những thông tin này, tôi sẽ gợi ý cho bạn một số điểm đến phù hợp.
```

### ✅ Test 2 — Single Tool Call
- **Input:** `Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng`
- **Kỳ vọng:** Gọi search_flights('Hà Nội', 'Đà Nẵng'), liệt kê 4 chuyến bay.
- **Kết quả:** ✅ PASS
- **Response:**
```
✈️ **Chuyến bay từ Hà Nội đến Đà Nẵng:**

1. **Hãng: VietJet Air**
   - Giờ bay: 08:30 - 09:50
   - Hạng: Phổ thông
   - Giá: 890.000đ

2. **Hãng: Bamboo Airways**
   - Giờ bay: 11:00 - 12:20
   - Hạng: Phổ thông
   - Giá: 1.200.000đ

3. **Hãng: Vietnam Airlines**
   - Giờ bay: 06:00 - 07:20
   - Hạng: Phổ thông
   - Giá: 1.450.000đ

4. **Hãng: Vietnam Airlines**
   - Giờ bay: 14:00 - 15:20
   - Hạng: Thương gia
   - Giá: 2.800.000đ

⚠️ _Giá chỉ mang tính chất tham khảo và có thể thay đổi tùy th...
```

### ✅ Test 3 — Multi-Step Tool Chaining
- **Input:** `Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!`
- **Kỳ vọng:** Agent tự chuỗi: search_flights → search_hotels → tính budget → gợi ý hoàn chỉnh.
- **Kết quả:** ✅ PASS
- **Response:**
```
Dựa trên thông tin tìm kiếm, tôi có thể tư vấn cho bạn như sau:

### 🛫 **Chuyến bay:**
1. **Hãng: VietJet Air**
   - Giờ bay: 16:00 - 18:15
   - Hạng: Phổ thông
   - Giá: **1.100.000đ**

2. **Hãng: VietJet Air**
   - Giờ bay: 10:00 - 12:15
   - Hạng: Phổ thông
   - Giá: **1.350.000đ**

3. **Hãng: Vietnam Airlines**
   - Giờ bay: 07:00 - 09:15
   - Hạng: Phổ thông
   - Giá: **2.100.000đ**

### 🏨 **Khách sạn:**
1. **9Station Hostel** ⭐⭐
   - Khu vực: Dương Đông
   - Giá: **200.000đ/đêm**
   - Rati...
```

### ✅ Test 4 — Missing Info / Clarification
- **Input:** `Tôi muốn đặt khách sạn`
- **Kỳ vọng:** Agent hỏi lại: thành phố nào? bao nhiêu đêm? ngân sách? KHÔNG gọi tool.
- **Kết quả:** ✅ PASS
- **Response:**
```
Chắc chắn rồi! Bạn muốn đặt khách sạn ở thành phố nào? Và bạn có giới hạn về giá mỗi đêm không?
```

### ✅ Test 5 — Guardrail / Refusal
- **Input:** `Giải giúp tôi bài tập lập trình Python về linked list`
- **Kỳ vọng:** Từ chối lịch sự, nói rằng chỉ hỗ trợ về du lịch.
- **Kết quả:** ✅ PASS
- **Response:**
```
Xin lỗi, nhưng tôi là trợ lý du lịch của TravelBuddy và không thể giúp bạn giải bài tập lập trình Python. Tôi chuyên về việc tư vấn và hỗ trợ các nhu cầu du lịch, như tìm kiếm chuyến bay, đặt khách sạn, và quản lý ngân sách cho chuyến đi. Nếu bạn có bất kỳ câu hỏi hoặc yêu cầu liên quan đến du lịch, tôi rất sẵn lòng giúp đỡ.
```

