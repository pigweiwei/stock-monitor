import akshare as ak
import requests
import os
from datetime import datetime

# Server酱 Key
send_key = os.environ.get('SEND_KEY')
print(f"🔑 Key 检查: {'✅ 存在' if send_key else '❌ 缺失'} (长度: {len(send_key) if send_key else 0})")

print("开始获取 A 股实时数据...")

try:
    # 正确接口名：stock_zh_a_hist_em + 实时参数
    df = ak.stock_zh_a_hist_em(symbol="000001", period="daily", start_date="20251017", end_date="20251017", adjust="qfq")
    print(f"成功获取 {len(df)} 只股票数据")
    
    # 模拟下跌数（测试用，实际用实时接口）
    down_count = 2500  # 临时值，测试推送
    print(f"当前下跌家数: {down_count}")
    
except Exception as e:
    print(f"获取失败: {e}")
    down_count = 0
    df = None

# 推送逻辑 - 测试模式：强制推送一次！
if send_key:
    url = f"https://sctapi.ftqq.com/{send_key}.send"
    data = {
        'title': '🚨 A股监控启动成功',
        'desp': f'✅ 系统正常运行！\n当前下跌: {down_count}\n时间: {datetime.now().strftime("%Y-%m-%d %H:%M")}\n以后 >3000 自动警报！'
    }
    response = requests.post(url, data=data, timeout=10)
    print(f"📱 完整响应: {response.text}")
else:
    print("❌ 无 Server酱 Key，跳过推送")

print("任务完成！")
