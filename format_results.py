import json
import os
from datetime import datetime

def format_soda_results(json_path):
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found.")
        return

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {e}")
        return

    # 提取基本資訊
    data_source = data.get('defaultDataSource', 'Unknown')
    scanned_at = data.get('dataTimestamp', 'Unknown')
    
    # 統計結果
    checks = data.get('checks', [])
    total = len(checks)
    passed = len([c for c in checks if c.get('outcome') == 'pass'])
    failed = len([c for c in checks if c.get('outcome') == 'fail'])
    warned = len([c for c in checks if c.get('outcome') == 'warn'])
    errors = len([c for c in checks if c.get('outcome') == 'error'])

    print("="*60)
    print(f"📊 Soda Scan Summary - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-"*60)
    print(f"Data Source : {data_source}")
    print(f"Scan Time   : {scanned_at}")
    print(f"Results     : ✅ {passed} Passed | ❌ {failed} Failed | ⚠️ {warned} Warned | 🛑 {errors} Errors")
    print("="*60)
    print(f"{'Status':<10} | {'Table':<20} | {'Check Name'}")
    print("-"*60)

    for check in checks:
        outcome = check.get('outcome', 'unknown').upper()
        status_icon = "✅" if outcome == "PASS" else "❌" if outcome == "FAIL" else "⚠️" if outcome == "WARN" else "🛑"
        table = check.get('table', 'N/A')
        name = check.get('name', 'N/A')
        # 如果有具體的數值，顯示出來
        value = check.get('checkValue')
        val_str = f" (Value: {value})" if value is not None else ""
        
        print(f"{status_icon} {outcome:<7} | {table:<20} | {name}{val_str}")

    print("="*60)

if __name__ == "__main__":
    format_soda_results('results.json')
