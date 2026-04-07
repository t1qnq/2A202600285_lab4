"""
5 Test cốt lõi cho TravelBuddy Agent
Chạy: python test_5_core.py
"""
import sys
import io
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from agent import chat

PASS = "✅ PASS"
FAIL = "❌ FAIL"

tests = [
    {
        "name": "Test 1 — Direct Answer (Không cần tool)",
        "input": "Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.",
        "check": lambda r: (
            any(w in r.lower() for w in ["chào", "xin chào", "hello", "hi"]) and
            any(w in r.lower() for w in ["sở thích", "ngân sách", "thời gian", "muốn đi", "thích", "budget"]) and
            not any(w in r for w in ["VietJet", "Vietnam Airlines", "Bamboo", "890.000", "Mường Thanh", "Vinpearl"])
        ),
        "desc": "Agent chào hỏi, hỏi thêm về sở thích/ngân sách/thời gian. KHÔNG gọi tool."
    },
    {
        "name": "Test 2 — Single Tool Call",
        "input": "Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng",
        "check": lambda r: any(w in r for w in ["VietJet", "Vietnam Airlines", "Bamboo", "890.000", "1.200.000", "1.450.000"]),
        "desc": "Gọi search_flights('Hà Nội', 'Đà Nẵng'), liệt kê 4 chuyến bay."
    },
    {
        "name": "Test 3 — Multi-Step Tool Chaining",
        "input": "Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!",
        "check": lambda r: (
            any(w in r for w in ["chuyến bay", "VietJet", "Vietnam Airlines"]) and
            any(w in r for w in ["khách sạn", "9Station", "Lahana", "Sol by Meliá", "Vinpearl"]) and
            any(w in r for w in ["tổng", "chi phí", "ngân sách", "còn lại"])
        ),
        "desc": "Agent tự chuỗi: search_flights → search_hotels → tính budget → gợi ý hoàn chỉnh."
    },
    {
        "name": "Test 4 — Missing Info / Clarification",
        "input": "Tôi muốn đặt khách sạn",
        "check": lambda r: any(w in r.lower() for w in ["thành phố", "ở đâu", "điểm đến", "ngân sách", "mấy đêm", "ngày", "nào"]) and not any(w in r for w in ["Vinpearl", "9Station", "Mường Thanh"]),
        "desc": "Agent hỏi lại: thành phố nào? bao nhiêu đêm? ngân sách? KHÔNG gọi tool."
    },
    {
        "name": "Test 5 — Guardrail / Refusal",
        "input": "Giải giúp tôi bài tập lập trình Python về linked list",
        "check": lambda r: any(w in r.lower() for w in ["xin lỗi", "không thể", "chỉ hỗ trợ", "du lịch", "không liên quan"]),
        "desc": "Từ chối lịch sự, nói rằng chỉ hỗ trợ về du lịch."
    },
]

def run_tests():
    print("=" * 70)
    print("🧪 TRAVELBUDDY AGENT — 5 TEST CỐT LÕI")
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
                "response_preview": response[:500] + ('...' if len(response) > 500 else '')
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
    
    # SUMMARY
    print(f"\n{'=' * 70}")
    print(f"📊 KẾT QUẢ: {passed}/{total} tests PASS | {failed}/{total} tests FAIL")
    
    if failed == 0:
        verdict = "🎉 Xuất sắc! Agent pass tất cả tests!"
    elif failed <= 2:
        verdict = "👍 Tốt! Chỉ cần fix vài test."
    else:
        verdict = "❌ Cần cải thiện nhiều."
    
    print(verdict)
    print(f"{'=' * 70}")
    
    # SAVE TO MARKDOWN
    md_content = f"""# 🧪 TravelBuddy Agent — 5 Test Cốt Lõi

**Ngày test:** {datetime.now().strftime("%d/%m/%Y %H:%M")}
**Kết quả:** {passed}/{total} PASS | {failed}/{total} FAIL
**Đánh giá:** {verdict}

---

## 📋 Bảng kết quả

| # | Test | Input | Kỳ Vọng | Kết Quả |
|---|------|-------|---------|---------|
"""
    
    for r in results:
        status_icon = "✅" if r['result'] == PASS else "❌"
        md_content += f"| {r['test_num']} | {r['name']} | \"{r['input']}\" | {r['expected']} | {status_icon} {r['result']} |\n"
    
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
