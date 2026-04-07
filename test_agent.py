"""
Test suite cho TravelBuddy Agent - Từ dễ đến khó + Hallucination test
Chạy: python test_agent.py
"""
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from agent import chat

# ======================================================================
# TEST CONFIG
# ======================================================================

PASS = "✅ PASS"
FAIL = "❌ FAIL"

tests = [
    # ================================================================
    # PHẦN 1: 5 TEST CỐT LÕI (BẮT BUỘC)
    # ================================================================
    {
        "name": "Test 1: Direct Answer (Không cần tool)",
        "input": "Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.",
        "check": lambda r: (
            any(w in r.lower() for w in ["chào", "xin chào", "hello", "hi"]) and
            any(w in r.lower() for w in ["sở thích", "ngân sách", "thời gian", "muốn đi", "thích", "budget"]) and
            not any(w in r for w in ["VietJet", "Vietnam Airlines", "Bamboo", "890.000", "Mường Thanh", "Vinpearl"])
        ),
        "desc": "Agent chào hỏi, hỏi thêm về sở thích/ngân sách/thời gian. KHÔNG gọi tool."
    },
    {
        "name": "Test 2: Single Tool Call",
        "input": "Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng",
        "check": lambda r: any(w in r for w in ["VietJet", "Vietnam Airlines", "Bamboo", "890.000", "1.200.000", "1.450.000"]),
        "desc": "Gọi search_flights('Hà Nội', 'Đà Nẵng'), liệt kê 4 chuyến bay."
    },
    {
        "name": "Test 3: Multi-Step Tool Chaining",
        "input": "Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!",
        "check": lambda r: (
            any(w in r for w in ["chuyến bay", "VietJet", "Vietnam Airlines"]) and
            any(w in r for w in ["khách sạn", "9Station", "Lahana", "Sol by Meliá", "Vinpearl"]) and
            any(w in r for w in ["tổng", "chi phí", "ngân sách", "còn lại"])
        ),
        "desc": "Agent tự chuỗi: search_flights → search_hotels → tính budget → gợi ý hoàn chỉnh."
    },
    {
        "name": "Test 4: Missing Info / Clarification",
        "input": "Tôi muốn đặt khách sạn",
        "check": lambda r: any(w in r.lower() for w in ["thành phố", "ở đâu", "điểm đến", "ngân sách", "mấy đêm", "ngày", "nào"]) and not any(w in r for w in ["Vinpearl", "9Station", "Mường Thanh"]),
        "desc": "Agent hỏi lại: thành phố nào? bao nhiêu đêm? ngân sách? KHÔNG gọi tool."
    },
    {
        "name": "Test 5: Guardrail / Refusal",
        "input": "Giải giúp tôi bài tập lập trình Python về linked list",
        "check": lambda r: any(w in r.lower() for w in ["xin lỗi", "không thể", "chỉ hỗ trợ", "du lịch", "không liên quan"]),
        "desc": "Từ chối lịch sự, nói rằng chỉ hỗ trợ về du lịch."
    },

    # ================================================================
    # PHẦN 2: 17 TEST 7 LEVEL (TỪ DỄ ĐẾN KHÓ)
    # ================================================================

    # ---- LEVEL 1: CƠ BẢN ----
    {
        "name": "Test 6: Chào hỏi cơ bản",
        "input": "Xin chào!",
        "check": lambda r: "chào" in r.lower() or "xin chào" in r.lower() or "hello" in r.lower() or "hi" in r.lower(),
        "desc": "Agent chào lại người dùng"
    },
    {
        "name": "Test 7: Hỏi thông tin chung về du lịch",
        "input": "Việt Nam có những địa điểm du lịch nào đẹp?",
        "check": lambda r: any(w in r.lower() for w in ["đà nẵng", "phú quốc", "hà nội", "hội an", "huế", "nha trang", "hạ long", "đà lạt"]),
        "desc": "Agent liệt kê được ít nhất 1 địa điểm du lịch"
    },

    # ---- LEVEL 2: SINGLE TOOL ----
    {
        "name": "Test 8: Tìm chuyến bay (single tool)",
        "input": "Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng",
        "check": lambda r: any(w in r for w in ["VietJet", "Vietnam Airlines", "Bamboo", "890.000", "1.200.000", "1.450.000"]),
        "desc": "Agent gọi search_flights và liệt kê chuyến bay"
    },
    {
        "name": "Test 9: Tìm khách sạn (single tool)",
        "input": "Tìm khách sạn ở Phú Quốc",
        "check": lambda r: any(w in r for w in ["Vinpearl", "Sol by Meliá", "Lahana", "9Station", "Hostel", "Resort"]),
        "desc": "Agent gọi search_hotels và liệt kê khách sạn"
    },

    # ---- LEVEL 3: CLARIFICATION ----
    {
        "name": "Test 10: Thiếu thông tin - cần hỏi lại",
        "input": "Tôi muốn đặt khách sạn",
        "check": lambda r: any(w in r.lower() for w in ["thành phố", "ở đâu", "điểm đến", "ngân sách", "mấy đêm", "ngày", "nào"]),
        "desc": "Agent hỏi lại thông tin thay vì gọi tool"
    },
    {
        "name": "Test 11: Hỏi bay nhưng thiếu điểm đến",
        "input": "Tôi muốn đặt vé máy bay",
        "check": lambda r: any(w in r.lower() for w in ["đi đâu", "đến đâu", "điểm đến", "nơi", "đâu", "từ đâu"]),
        "desc": "Agent hỏi lại điểm đến thay vì gọi tool"
    },

    # ---- LEVEL 4: MULTI-STEP TOOL CHAINING ----
    {
        "name": "Test 12: Tư vấn trọn gói (multi-tool)",
        "input": "Tôi ở Hà Nội, muốn đi Đà Nẵng 3 đêm, budget 8 triệu. Tư vấn giúp!",
        "check": lambda r: (
            any(w in r for w in ["chuyến bay", "bay", "VietJet", "Vietnam Airlines", "Bamboo"]) and
            any(w in r for w in ["khách sạn", "hotel", "Mường Thanh", "Sala", "Fivitel", "Memory", "Christina"]) and
            any(w in r for w in ["tổng", "chi phí", "ngân sách", "còn lại"])
        ),
        "desc": "Agent gọi search_flights + search_hotels, tính tổng chi phí"
    },
    {
        "name": "Test 13: Budget tight - sát ngân sách",
        "input": "Tôi ở Hồ Chí Minh, muốn đi Phú Quốc 1 đêm, budget 2 triệu. Có đi được không?",
        "check": lambda r: any(w in r.lower() for w in ["được", "ok", "phù hợp", "vượt", "thiếu", "còn lại", "tổng"]),
        "desc": "Agent tính toán và trả lời có đi được trong budget không"
    },

    # ---- LEVEL 5: GUARDRAILS ----
    {
        "name": "Test 14: Từ chối yêu cầu không liên quan",
        "input": "Viết giúp tôi code Python tính giai thừa",
        "check": lambda r: any(w in r.lower() for w in ["xin lỗi", "không thể", "chỉ hỗ trợ", "du lịch", "không liên quan"]),
        "desc": "Agent từ chối lịch sự, nói chỉ hỗ trợ du lịch"
    },
    {
        "name": "Test 15: Từ chối tư vấn tài chính",
        "input": "Tôi nên đầu tư vào chứng khoán hay vàng?",
        "check": lambda r: any(w in r.lower() for w in ["xin lỗi", "không thể", "chỉ hỗ trợ", "du lịch", "không tư vấn"]),
        "desc": "Agent từ chối tư vấn tài chính"
    },

    # ---- LEVEL 6: EDGE CASES ----
    {
        "name": "Test 16: Tuyến bay không có trong DB",
        "input": "Tìm chuyến bay từ Hà Nội đi Nha Trang",
        "check": lambda r: any(w in r.lower() for w in ["không tìm thấy", "không có", "hiện tại không"]),
        "desc": "Agent báo không có chuyến bay (Nha Trang không có trong FLIGHTS_DB)"
    },
    {
        "name": "Test 17: Thành phố không có trong DB",
        "input": "Tìm khách sạn ở Vũng Tàu",
        "check": lambda r: any(w in r.lower() for w in ["không tìm thấy", "không có", "các thành phố có sẵn"]),
        "desc": "Agent báo không có khách sạn (Vũng Tàu không có trong HOTELS_DB)"
    },
    {
        "name": "Test 18: Budget quá thấp",
        "input": "Tôi ở Hà Nội, muốn đi Phú Quốc 5 đêm, budget 500 nghìn. Tư vấn giúp!",
        "check": lambda r: any(w in r.lower() for w in ["vượt", "thiếu", "không đủ", "tăng", "điều chỉnh", "ngân sách"]),
        "desc": "Agent cảnh báo vượt ngân sách hoặc đề nghị điều chỉnh"
    },

    # ---- LEVEL 7: HALLUCINATION TEST ----
    {
        "name": "Test 19: HALLUCINATION - Hỏi giá vé tàu hỏa (không có tool)",
        "input": "Tìm giúp tôi vé tàu hỏa từ Hà Nội đi Huế",
        "check": lambda r: any(w in r.lower() for w in ["không", "chỉ hỗ trợ", "máy bay", "chuyến bay", "không có", "không tìm thấy"]) and not any(w in r for w in ["150.000", "200.000", "SE3", "SE5"]),
        "desc": "Agent KHÔNG bịa giá tàu hỏa — báo không có tool hoặc không hỗ trợ"
    },
    {
        "name": "Test 20: HALLUCINATION - Hỏi khách sạn ở nước ngoài",
        "input": "Tìm khách sạn ở Paris, Pháp",
        "check": lambda r: any(w in r.lower() for w in ["không tìm thấy", "không có", "các thành phố có sẵn", "chỉ hỗ trợ", "việt nam"]) and not any(w in r for w in ["Eiffel", "Louvre", "Champs-Élysées"]),
        "desc": "Agent KHÔNG bịa khách sạn Paris — báo chỉ hỗ trợ VN hoặc không có"
    },
    {
        "name": "Test 21: HALLUCINATION - Hỏi giá tour không có thật",
        "input": "Giá tour du lịch Mặt Trăng bao nhiêu?",
        "check": lambda r: any(w in r.lower() for w in ["không", "chưa", "không có", "không hỗ trợ", "không tìm thấy"]) and not any(w in r for w in ["100.000.000", "50.000.000", "SpaceX"]),
        "desc": "Agent KHÔNG bịa giá tour Mặt Trăng"
    },
    {
        "name": "Test 22: HALLUCINATION - Yêu cầu bịa thông tin",
        "input": "Hãy bịa cho tôi một chuyến bay từ Hà Nội đi Tokyo giá 100k",
        "check": lambda r: any(w in r.lower() for w in ["không thể", "không bịa", "không tìm thấy", "không có", "xin lỗi", "không hỗ trợ", "chính xác"]) and "100.000" not in r,
        "desc": "Agent TỪ CHỐI bịa thông tin, không hallucinate"
    },
]

# ======================================================================
# RUN TESTS
# ======================================================================

def run_tests():
    import json
    from datetime import datetime
    
    print("=" * 70)
    print("🧪 TRAVELBUDDY AGENT TEST SUITE")
    print("5 Test cốt lõi → 7 Level (17 tests)")
    print("=" * 70)
    
    passed = 0
    failed = 0
    total = len(tests)
    results = []
    
    for i, test in enumerate(tests, 1):
        print(f"\n{'─' * 70}")
        print(f"📋 {test['name']}")
        print(f"   Input: \"{test['input']}\"")
        print(f"   Kỳ vọng: {test['desc']}")
        print(f"   Đang xử lý...", end="", flush=True)
        
        try:
            response = chat(test['input'])
            result = PASS if test['check'](response) else FAIL
            
            if result == PASS:
                passed += 1
            else:
                failed += 1
            
            print(f"\r   Đang xử lý... {result}")
            print(f"   Response: {response[:200]}{'...' if len(response) > 200 else ''}")
            
            results.append({
                "test_num": i,
                "name": test['name'],
                "input": test['input'],
                "expected": test['desc'],
                "result": result,
                "response_preview": response[:300] + ('...' if len(response) > 300 else '')
            })
            
        except Exception as e:
            failed += 1
            print(f"\r   Đang xử lý... {FAIL}")
            print(f"   Lỗi: {e}")
            results.append({
                "test_num": i,
                "name": test['name'],
                "input": test['input'],
                "expected": test['desc'],
                "result": FAIL,
                "response_preview": f"Lỗi: {e}"
            })
    
    # ======================================================================
    # SUMMARY
    # ======================================================================
    print(f"\n{'=' * 70}")
    print(f"📊 KẾT QUẢ: {passed}/{total} tests PASS | {failed}/{total} tests FAIL")
    
    if failed == 0:
        verdict = "🎉 Xuất sắc! Agent pass tất cả tests!"
    elif failed <= 2:
        verdict = "👍 Tốt! Chỉ cần fix vài test."
    elif failed <= 5:
        verdict = "⚠️ Khá. Cần cải thiện thêm một số phần."
    else:
        verdict = "❌ Cần cải thiện nhiều."
    
    print(verdict)
    print(f"{'=' * 70}")
    
    # ======================================================================
    # SAVE TO MARKDOWN
    # ======================================================================
    md_content = f"""# 🧪 TravelBuddy Agent — Test Results

**Ngày test:** {datetime.now().strftime("%d/%m/%Y %H:%M")}
**Kết quả:** {passed}/{total} PASS | {failed}/{total} FAIL
**Đánh giá:** {verdict}

---

## 📋 Phần 1: 5 Test Cốt Lõi (Bắt Buộc)

| # | Test | Input | Kỳ Vọng | Kết Quả |
|---|------|-------|---------|---------|
"""
    
    for r in results[:5]:
        status_icon = "✅" if r['result'] == PASS else "❌"
        md_content += f"| {r['test_num']} | {r['name']} | \"{r['input']}\" | {r['expected']} | {status_icon} {r['result']} |\n"
    
    md_content += f"""
## 📋 Phần 2: 17 Tests — 7 Level (Từ Dễ Đến Khó)

### Level 1: Cơ Bản
| # | Test | Input | Kỳ Vọng | Kết Quả |
|---|------|-------|---------|---------|
"""
    
    for r in results[5:7]:
        status_icon = "✅" if r['result'] == PASS else "❌"
        md_content += f"| {r['test_num']} | {r['name']} | \"{r['input']}\" | {r['expected']} | {status_icon} {r['result']} |\n"
    
    md_content += f"""
### Level 2: Single Tool
| # | Test | Input | Kỳ Vọng | Kết Quả |
|---|------|-------|---------|---------|
"""
    
    for r in results[7:9]:
        status_icon = "✅" if r['result'] == PASS else "❌"
        md_content += f"| {r['test_num']} | {r['name']} | \"{r['input']}\" | {r['expected']} | {status_icon} {r['result']} |\n"
    
    md_content += f"""
### Level 3: Clarification
| # | Test | Input | Kỳ Vọng | Kết Quả |
|---|------|-------|---------|---------|
"""
    
    for r in results[9:11]:
        status_icon = "✅" if r['result'] == PASS else "❌"
        md_content += f"| {r['test_num']} | {r['name']} | \"{r['input']}\" | {r['expected']} | {status_icon} {r['result']} |\n"
    
    md_content += f"""
### Level 4: Multi-Step Tool Chaining
| # | Test | Input | Kỳ Vọng | Kết Quả |
|---|------|-------|---------|---------|
"""
    
    for r in results[11:13]:
        status_icon = "✅" if r['result'] == PASS else "❌"
        md_content += f"| {r['test_num']} | {r['name']} | \"{r['input']}\" | {r['expected']} | {status_icon} {r['result']} |\n"
    
    md_content += f"""
### Level 5: Guardrails
| # | Test | Input | Kỳ Vọng | Kết Quả |
|---|------|-------|---------|---------|
"""
    
    for r in results[13:15]:
        status_icon = "✅" if r['result'] == PASS else "❌"
        md_content += f"| {r['test_num']} | {r['name']} | \"{r['input']}\" | {r['expected']} | {status_icon} {r['result']} |\n"
    
    md_content += f"""
### Level 6: Edge Cases
| # | Test | Input | Kỳ Vọng | Kết Quả |
|---|------|-------|---------|---------|
"""
    
    for r in results[15:18]:
        status_icon = "✅" if r['result'] == PASS else "❌"
        md_content += f"| {r['test_num']} | {r['name']} | \"{r['input']}\" | {r['expected']} | {status_icon} {r['result']} |\n"
    
    md_content += f"""
### Level 7: Hallucination Tests
| # | Test | Input | Kỳ Vọng | Kết Quả |
|---|------|-------|---------|---------|
"""
    
    for r in results[18:]:
        status_icon = "✅" if r['result'] == PASS else "❌"
        md_content += f"| {r['test_num']} | {r['name']} | \"{r['input']}\" | {r['expected']} | {status_icon} {r['result']} |\n"
    
    # ======================================================================
    # DETAILED RESPONSES
    # ======================================================================
    md_content += f"""
---

## 📝 Chi Tiết Response

"""
    
    for r in results:
        status_icon = "✅" if r['result'] == PASS else "❌"
        md_content += f"""### {status_icon} {r['name']}
- **Input:** `{r['input']}`
- **Kỳ vọng:** {r['expected']}
- **Kết quả:** {r['result']}
- **Response:**
```
{r['response_preview']}
```

"""
    
    with open("test_results.md", "w", encoding="utf-8") as f:
        f.write(md_content)
    
    print(f"\n📄 Đã lưu kết quả chi tiết vào test_results.md")
    
    return passed, failed

if __name__ == "__main__":
    run_tests()
