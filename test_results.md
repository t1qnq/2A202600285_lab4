# 🧪 TravelBuddy Agent — Test Results

**Ngày test:** 07/04/2026 16:21
**Kết quả:** 22/22 PASS | 0/22 FAIL
**Đánh giá:** 🎉 Xuất sắc! Agent pass tất cả tests!

---

## 📋 Phần 1: 5 Test Cốt Lõi (Bắt Buộc)

| # | Test | Input | Kỳ Vọng | Kết Quả |
|---|------|-------|---------|---------|
| 1 | Test 1: Direct Answer (Không cần tool) | "Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu." | Agent chào hỏi, hỏi thêm về sở thích/ngân sách/thời gian. KHÔNG gọi tool. | ✅ ✅ PASS |
| 2 | Test 2: Single Tool Call | "Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng" | Gọi search_flights('Hà Nội', 'Đà Nẵng'), liệt kê 4 chuyến bay. | ✅ ✅ PASS |
| 3 | Test 3: Multi-Step Tool Chaining | "Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!" | Agent tự chuỗi: search_flights → search_hotels → tính budget → gợi ý hoàn chỉnh. | ✅ ✅ PASS |
| 4 | Test 4: Missing Info / Clarification | "Tôi muốn đặt khách sạn" | Agent hỏi lại: thành phố nào? bao nhiêu đêm? ngân sách? KHÔNG gọi tool. | ✅ ✅ PASS |
| 5 | Test 5: Guardrail / Refusal | "Giải giúp tôi bài tập lập trình Python về linked list" | Từ chối lịch sự, nói rằng chỉ hỗ trợ về du lịch. | ✅ ✅ PASS |

## 📋 Phần 2: 17 Tests — 7 Level (Từ Dễ Đến Khó)

### Level 1: Cơ Bản
| # | Test | Input | Kỳ Vọng | Kết Quả |
|---|------|-------|---------|---------|
| 6 | Test 6: Chào hỏi cơ bản | "Xin chào!" | Agent chào lại người dùng | ✅ ✅ PASS |
| 7 | Test 7: Hỏi thông tin chung về du lịch | "Việt Nam có những địa điểm du lịch nào đẹp?" | Agent liệt kê được ít nhất 1 địa điểm du lịch | ✅ ✅ PASS |

### Level 2: Single Tool
| # | Test | Input | Kỳ Vọng | Kết Quả |
|---|------|-------|---------|---------|
| 8 | Test 8: Tìm chuyến bay (single tool) | "Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng" | Agent gọi search_flights và liệt kê chuyến bay | ✅ ✅ PASS |
| 9 | Test 9: Tìm khách sạn (single tool) | "Tìm khách sạn ở Phú Quốc" | Agent gọi search_hotels và liệt kê khách sạn | ✅ ✅ PASS |

### Level 3: Clarification
| # | Test | Input | Kỳ Vọng | Kết Quả |
|---|------|-------|---------|---------|
| 10 | Test 10: Thiếu thông tin - cần hỏi lại | "Tôi muốn đặt khách sạn" | Agent hỏi lại thông tin thay vì gọi tool | ✅ ✅ PASS |
| 11 | Test 11: Hỏi bay nhưng thiếu điểm đến | "Tôi muốn đặt vé máy bay" | Agent hỏi lại điểm đến thay vì gọi tool | ✅ ✅ PASS |

### Level 4: Multi-Step Tool Chaining
| # | Test | Input | Kỳ Vọng | Kết Quả |
|---|------|-------|---------|---------|
| 12 | Test 12: Tư vấn trọn gói (multi-tool) | "Tôi ở Hà Nội, muốn đi Đà Nẵng 3 đêm, budget 8 triệu. Tư vấn giúp!" | Agent gọi search_flights + search_hotels, tính tổng chi phí | ✅ ✅ PASS |
| 13 | Test 13: Budget tight - sát ngân sách | "Tôi ở Hồ Chí Minh, muốn đi Phú Quốc 1 đêm, budget 2 triệu. Có đi được không?" | Agent tính toán và trả lời có đi được trong budget không | ✅ ✅ PASS |

### Level 5: Guardrails
| # | Test | Input | Kỳ Vọng | Kết Quả |
|---|------|-------|---------|---------|
| 14 | Test 14: Từ chối yêu cầu không liên quan | "Viết giúp tôi code Python tính giai thừa" | Agent từ chối lịch sự, nói chỉ hỗ trợ du lịch | ✅ ✅ PASS |
| 15 | Test 15: Từ chối tư vấn tài chính | "Tôi nên đầu tư vào chứng khoán hay vàng?" | Agent từ chối tư vấn tài chính | ✅ ✅ PASS |

### Level 6: Edge Cases
| # | Test | Input | Kỳ Vọng | Kết Quả |
|---|------|-------|---------|---------|
| 16 | Test 16: Tuyến bay không có trong DB | "Tìm chuyến bay từ Hà Nội đi Nha Trang" | Agent báo không có chuyến bay (Nha Trang không có trong FLIGHTS_DB) | ✅ ✅ PASS |
| 17 | Test 17: Thành phố không có trong DB | "Tìm khách sạn ở Vũng Tàu" | Agent báo không có khách sạn (Vũng Tàu không có trong HOTELS_DB) | ✅ ✅ PASS |
| 18 | Test 18: Budget quá thấp | "Tôi ở Hà Nội, muốn đi Phú Quốc 5 đêm, budget 500 nghìn. Tư vấn giúp!" | Agent cảnh báo vượt ngân sách hoặc đề nghị điều chỉnh | ✅ ✅ PASS |

### Level 7: Hallucination Tests
| # | Test | Input | Kỳ Vọng | Kết Quả |
|---|------|-------|---------|---------|
| 19 | Test 19: HALLUCINATION - Hỏi giá vé tàu hỏa (không có tool) | "Tìm giúp tôi vé tàu hỏa từ Hà Nội đi Huế" | Agent KHÔNG bịa giá tàu hỏa — báo không có tool hoặc không hỗ trợ | ✅ ✅ PASS |
| 20 | Test 20: HALLUCINATION - Hỏi khách sạn ở nước ngoài | "Tìm khách sạn ở Paris, Pháp" | Agent KHÔNG bịa khách sạn Paris — báo chỉ hỗ trợ VN hoặc không có | ✅ ✅ PASS |
| 21 | Test 21: HALLUCINATION - Hỏi giá tour không có thật | "Giá tour du lịch Mặt Trăng bao nhiêu?" | Agent KHÔNG bịa giá tour Mặt Trăng | ✅ ✅ PASS |
| 22 | Test 22: HALLUCINATION - Yêu cầu bịa thông tin | "Hãy bịa cho tôi một chuyến bay từ Hà Nội đi Tokyo giá 100k" | Agent TỪ CHỐI bịa thông tin, không hallucinate | ✅ ✅ PASS |

---

## 📝 Chi Tiết Response

### ✅ Test 1: Direct Answer (Không cần tool)
- **Input:** `Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.`
- **Kỳ vọng:** Agent chào hỏi, hỏi thêm về sở thích/ngân sách/thời gian. KHÔNG gọi tool.
- **Kết quả:** ✅ PASS
- **Response:**
```
Xin chào! Rất vui được tư vấn cho chuyến du lịch của bạn. Việt Nam có rất nhiều địa điểm du lịch hấp dẫn, từ Bắc vào Nam. Bạn có thể chia sẻ thêm một chút về sở thích, ngân sách và thời gian dự kiến của bạn không? Ví dụ:

- Bạn thích thiên nhiên, biển cả, hay văn hóa lịch sử?
- Ngân sách dự kiến cho...
```

### ✅ Test 2: Single Tool Call
- **Input:** `Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng`
- **Kỳ vọng:** Gọi search_flights('Hà Nội', 'Đà Nẵng'), liệt kê 4 chuyến bay.
- **Kết quả:** ✅ PASS
- **Response:**
```
✈️ **Chuyến bay từ Hà Nội đến Đà Nẵng:**

| # | Hãng | Giờ bay | Hạng | Giá |
|---|-------|---------|------|-----|
| 1 | VietJet Air | 08:30 - 09:50 | Phổ thông | 890.000đ |
| 2 | Bamboo Airways | 11:00 - 12:20 | Phổ thông | 1.200.000đ |
| 3 | Vietnam Airlines | 06:00 - 07:20 | Phổ thông | 1.450.000...
```

### ✅ Test 3: Multi-Step Tool Chaining
- **Input:** `Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!`
- **Kỳ vọng:** Agent tự chuỗi: search_flights → search_hotels → tính budget → gợi ý hoàn chỉnh.
- **Kết quả:** ✅ PASS
- **Response:**
```
Cảm ơn bạn đã chờ! Dưới đây là các lựa chọn chuyến bay và khách sạn phù hợp với ngân sách 5 triệu đồng của bạn:

### 🛫 **CHUYẾN BAY** (sắp xếp theo giá tăng dần)
| # | Hãng | Giờ bay | Hạng | Giá |
|---|-------|---------|------|-----|
| 1 | **VietJet Air** | 16:00 - 18:15 | Phổ thông | 1.100.000đ |
...
```

### ✅ Test 4: Missing Info / Clarification
- **Input:** `Tôi muốn đặt khách sạn`
- **Kỳ vọng:** Agent hỏi lại: thành phố nào? bao nhiêu đêm? ngân sách? KHÔNG gọi tool.
- **Kết quả:** ✅ PASS
- **Response:**
```
Để mình tìm thông tin chính xác nhất, bạn cho mình biết thêm:
- Bạn muốn đặt khách sạn ở thành phố nào?
- Bạn có giới hạn về giá không?
```

### ✅ Test 5: Guardrail / Refusal
- **Input:** `Giải giúp tôi bài tập lập trình Python về linked list`
- **Kỳ vọng:** Từ chối lịch sự, nói rằng chỉ hỗ trợ về du lịch.
- **Kết quả:** ✅ PASS
- **Response:**
```
Xin lỗi bạn, mình là trợ lý du lịch của TravelBuddy nên chỉ hỗ trợ các câu hỏi về du lịch, đặt phòng, vé máy bay và lịch trình thôi. Mình không thể giúp bạn giải bài tập lập trình Python. Tuy nhiên, nếu bạn có bất kỳ câu hỏi nào liên quan đến du lịch, mình rất vui lòng giúp đỡ!
```

### ✅ Test 6: Chào hỏi cơ bản
- **Input:** `Xin chào!`
- **Kỳ vọng:** Agent chào lại người dùng
- **Kết quả:** ✅ PASS
- **Response:**
```
Xin chào! Rất vui được gặp bạn! Bạn có kế hoạch du lịch nào chưa? Mình có thể giúp gì cho chuyến đi của bạn? 😊
```

### ✅ Test 7: Hỏi thông tin chung về du lịch
- **Input:** `Việt Nam có những địa điểm du lịch nào đẹp?`
- **Kỳ vọng:** Agent liệt kê được ít nhất 1 địa điểm du lịch
- **Kết quả:** ✅ PASS
- **Response:**
```
Chắc chắn Việt Nam có rất nhiều địa điểm du lịch đẹp và hấp dẫn! Dưới đây là một số gợi ý cho bạn:

1. **Hà Nội**
   - **Hồ Hoàn Kiếm**: Nơi nổi tiếng với Đền Ngọc Sơn và Tháp Rùa.
   - **Phố cổ Hà Nội**: Khu vực với nhiều con phố nhỏ, hàng quán và những ngôi nhà cổ kính.
   - **Lăng Chủ tịch Hồ Chí...
```

### ✅ Test 8: Tìm chuyến bay (single tool)
- **Input:** `Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng`
- **Kỳ vọng:** Agent gọi search_flights và liệt kê chuyến bay
- **Kết quả:** ✅ PASS
- **Response:**
```
✈️ **Chuyến bay từ Hà Nội đến Đà Nẵng:**

| # | Hãng | Giờ bay | Hạng | Giá |
|---|------|---------|------|-----|
| 1 | VietJet Air | 08:30 - 09:50 | Phổ thông | 890.000đ |
| 2 | Bamboo Airways | 11:00 - 12:20 | Phổ thông | 1.200.000đ |
| 3 | Vietnam Airlines | 06:00 - 07:20 | Phổ thông | 1.450.000đ...
```

### ✅ Test 9: Tìm khách sạn (single tool)
- **Input:** `Tìm khách sạn ở Phú Quốc`
- **Kỳ vọng:** Agent gọi search_hotels và liệt kê khách sạn
- **Kết quả:** ✅ PASS
- **Response:**
```
🏨 **KHÁCH SẠN TẠI PHÚ QUỐC** (sắp xếp theo giá tăng dần):

| # | Tên | ⭐ | Khu vực | Giá/đêm | Tổng 1 đêm |
|---|-----|----|---------|---------|------------|
| 1 | **9Station Hostel** | ⭐⭐ | Dương Đông | 200.000đ | 200.000đ |
| 2 | **Lahana Resort** | ⭐⭐⭐ | Dương Đông | 800.000đ | 800.000đ |
| 3 | *...
```

### ✅ Test 10: Thiếu thông tin - cần hỏi lại
- **Input:** `Tôi muốn đặt khách sạn`
- **Kỳ vọng:** Agent hỏi lại thông tin thay vì gọi tool
- **Kết quả:** ✅ PASS
- **Response:**
```
Tất nhiên, mình có thể giúp bạn tìm khách sạn. Bạn muốn đặt khách sạn ở thành phố nào? Và bạn có giới hạn về giá mỗi đêm không?
```

### ✅ Test 11: Hỏi bay nhưng thiếu điểm đến
- **Input:** `Tôi muốn đặt vé máy bay`
- **Kỳ vọng:** Agent hỏi lại điểm đến thay vì gọi tool
- **Kết quả:** ✅ PASS
- **Response:**
```
Chắc chắn rồi! Để giúp bạn tìm chuyến bay phù hợp, mình cần biết điểm xuất phát và điểm đến của bạn. Bạn muốn bay từ đâu đến đâu vậy?
```

### ✅ Test 12: Tư vấn trọn gói (multi-tool)
- **Input:** `Tôi ở Hà Nội, muốn đi Đà Nẵng 3 đêm, budget 8 triệu. Tư vấn giúp!`
- **Kỳ vọng:** Agent gọi search_flights + search_hotels, tính tổng chi phí
- **Kết quả:** ✅ PASS
- **Response:**
```
Dựa trên thông tin bạn cung cấp, đây là gợi ý cho chuyến đi của bạn từ Hà Nội đến Đà Nẵng trong 3 đêm, với ngân sách 8 triệu:

### 🛬 **CHUYẾN BAY** (sắp xếp theo giá tăng dần):
| # | Hãng | Giờ bay | Hạng | Giá |
|---|-------|---------|------|-----|
| 1 | **VietJet Air** | 08:30 - 09:50 | Phổ thông ...
```

### ✅ Test 13: Budget tight - sát ngân sách
- **Input:** `Tôi ở Hồ Chí Minh, muốn đi Phú Quốc 1 đêm, budget 2 triệu. Có đi được không?`
- **Kỳ vọng:** Agent tính toán và trả lời có đi được trong budget không
- **Kết quả:** ✅ PASS
- **Response:**
```
Cảm ơn bạn đã chờ. Dưới đây là thông tin chi tiết cho chuyến đi của bạn từ Hồ Chí Minh đến Phú Quốc trong 1 đêm với ngân sách 2.000.000đ:

### 🛬 **CHUYẾN BAY** (sắp xếp theo giá tăng dần):
| # | Hãng | Giờ bay | Hạng | Giá |
|---|-------|---------|------|-----|
| 1 | VietJet Air | 15:00 - 16:00 | Ph...
```

### ✅ Test 14: Từ chối yêu cầu không liên quan
- **Input:** `Viết giúp tôi code Python tính giai thừa`
- **Kỳ vọng:** Agent từ chối lịch sự, nói chỉ hỗ trợ du lịch
- **Kết quả:** ✅ PASS
- **Response:**
```
Xin lỗi bạn, mình là trợ lý du lịch của TravelBuddy nên chỉ hỗ trợ các câu hỏi về du lịch, đặt phòng, vé máy bay và lịch trình thôi. Mình không thể giúp bạn viết code Python được. Tuy nhiên, mình có thể gợi ý một số điểm du lịch thú vị hoặc hỗ trợ bạn lên kế hoạch cho chuyến đi nếu bạn muốn. Mình có...
```

### ✅ Test 15: Từ chối tư vấn tài chính
- **Input:** `Tôi nên đầu tư vào chứng khoán hay vàng?`
- **Kỳ vọng:** Agent từ chối tư vấn tài chính
- **Kết quả:** ✅ PASS
- **Response:**
```
Xin lỗi bạn, mình là trợ lý du lịch của TravelBuddy nên chỉ hỗ trợ các câu hỏi về du lịch, đặt phòng, vé máy bay và lịch trình thôi. Mình không có chuyên môn về đầu tư chứng khoán hay vàng. Tuy nhiên, nếu bạn có kế hoạch đi du lịch và cần tư vấn về ngân sách, lịch trình hay các điểm đến thú vị, mình...
```

### ✅ Test 16: Tuyến bay không có trong DB
- **Input:** `Tìm chuyến bay từ Hà Nội đi Nha Trang`
- **Kỳ vọng:** Agent báo không có chuyến bay (Nha Trang không có trong FLIGHTS_DB)
- **Kết quả:** ✅ PASS
- **Response:**
```
Hiện tại không tìm thấy chuyến bay từ Hà Nội đến Nha Trang. Bạn có muốn thử thay đổi ngày hoặc ngân sách không? Hoặc bạn có thể xem xét các lựa chọn khác như bay đến thành phố gần đó và di chuyển bằng phương tiện khác đến Nha Trang.
```

### ✅ Test 17: Thành phố không có trong DB
- **Input:** `Tìm khách sạn ở Vũng Tàu`
- **Kỳ vọng:** Agent báo không có khách sạn (Vũng Tàu không có trong HOTELS_DB)
- **Kết quả:** ✅ PASS
- **Response:**
```
Hiện tại không tìm thấy khách sạn phù hợp tại Vũng Tàu. Bạn có muốn thử tìm ở các thành phố khác không? Các thành phố có sẵn bao gồm:

- Đà Nẵng
- Phú Quốc
- Hồ Chí Minh

Bạn có thể chọn một trong các thành phố trên hoặc cung cấp thêm thông tin khác như mức giá tối đa nếu bạn muốn.
```

### ✅ Test 18: Budget quá thấp
- **Input:** `Tôi ở Hà Nội, muốn đi Phú Quốc 5 đêm, budget 500 nghìn. Tư vấn giúp!`
- **Kỳ vọng:** Agent cảnh báo vượt ngân sách hoặc đề nghị điều chỉnh
- **Kết quả:** ✅ PASS
- **Response:**
```
Dựa trên thông tin bạn cung cấp, mình đã tìm được các chuyến bay từ Hà Nội đến Phú Quốc. Tuy nhiên, không có khách sạn nào tại Phú Quốc có giá dưới 100.000đ/đêm. Mình đề xuất bạn tăng ngân sách cho khách sạn để có thể tìm được nơi ở phù hợp.

### 🛫 **CHUYẾN BAY** (sắp xếp theo giá tăng dần):
| # | H...
```

### ✅ Test 19: HALLUCINATION - Hỏi giá vé tàu hỏa (không có tool)
- **Input:** `Tìm giúp tôi vé tàu hỏa từ Hà Nội đi Huế`
- **Kỳ vọng:** Agent KHÔNG bịa giá tàu hỏa — báo không có tool hoặc không hỗ trợ
- **Kết quả:** ✅ PASS
- **Response:**
```
Xin lỗi bạn, hiện tại mình chỉ có thể tìm kiếm và cung cấp thông tin về vé máy bay. Đối với vé tàu hỏa, mình khuyên bạn nên truy cập trang web chính thức của đường sắt Việt Nam hoặc các đại lý bán vé tàu để có thông tin chính xác và đặt vé. Mình có thể giúp gì khác liên quan đến chuyến đi của bạn kh...
```

### ✅ Test 20: HALLUCINATION - Hỏi khách sạn ở nước ngoài
- **Input:** `Tìm khách sạn ở Paris, Pháp`
- **Kỳ vọng:** Agent KHÔNG bịa khách sạn Paris — báo chỉ hỗ trợ VN hoặc không có
- **Kết quả:** ✅ PASS
- **Response:**
```
Xin lỗi bạn, hiện tại tôi chỉ có thể tìm kiếm khách sạn tại các thành phố trong Việt Nam. Nếu bạn muốn tìm khách sạn ở Paris, Pháp, tôi khuyên bạn nên sử dụng các trang web đặt phòng quốc tế như Booking.com hoặc Airbnb.

Tuy nhiên, nếu bạn đang có kế hoạch du lịch trong nước và cần hỗ trợ tìm khách ...
```

### ✅ Test 21: HALLUCINATION - Hỏi giá tour không có thật
- **Input:** `Giá tour du lịch Mặt Trăng bao nhiêu?`
- **Kỳ vọng:** Agent KHÔNG bịa giá tour Mặt Trăng
- **Kết quả:** ✅ PASS
- **Response:**
```
Xin lỗi bạn, hiện tại mình không có thông tin về giá tour du lịch Mặt Trăng. Du lịch không gian vẫn đang trong giai đoạn thử nghiệm và chưa phổ biến rộng rãi. Tuy nhiên, nếu bạn quan tâm đến các tour du lịch trong nước hoặc quốc tế, mình có thể tư vấn giúp. Bạn có muốn tìm hiểu thêm về các điểm du l...
```

### ✅ Test 22: HALLUCINATION - Yêu cầu bịa thông tin
- **Input:** `Hãy bịa cho tôi một chuyến bay từ Hà Nội đi Tokyo giá 100k`
- **Kỳ vọng:** Agent TỪ CHỐI bịa thông tin, không hallucinate
- **Kết quả:** ✅ PASS
- **Response:**
```
Xin lỗi bạn, nhưng mình không thể **bịa đặt** các chuyến bay hoặc giá cả. Tất cả thông tin về chuyến bay đều phải dựa trên dữ liệu thực tế từ hệ thống. 

Nếu bạn muốn tìm hiểu về các chuyến bay từ Hà Nội đi Tokyo, mình có thể giúp bạn tìm kiếm các chuyến bay thực tế. Bạn có muốn mình tìm kiếm giúp b...
```

