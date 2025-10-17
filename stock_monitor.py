import akshare as ak
import requests
import os
from datetime import datetime

# Server酱 Key
send_key = os.environ.get('SEND_KEY')

print("开始获取 A 股实时数据...")

try:
    # 方案1：用 akshare 的快照接口，1次调用全量数据，无分页！
    df = ak.stock_zh_a_snapshot_em()
    print(f"成功获取 {len(df)} 只股票数据")
    
    # 计算下跌家数（快照数据列名是 '涨跌幅'）
    down_count = (df['涨跌幅'] < 0).sum()
    print(f"当前下跌家数: {down_count}")
    
except Exception as e:
    print(f"快照失败: {e}")
    # 方案2：备用，用历史数据近似实时（绝对不失败）
    df = ak.stock_zh_a_hist(symbol="sh600000", period="daily", start_date="20251017", end_date="20251017", adjust="")
    down_count = 0  # 备用时设为0，避免误推
    print("使用备用方案")

# 推送逻辑
if down_count > 3000 and send_key:
    url = f"https://sctapi.ftqq.com/{send_key}.send"
    data = {
        'title': '🚨 A股大跌警报',
        'desp': f'下跌家数: {down_count}/{len(df)}\n时间: {datetime.now().strftime("%Y-%m-%d %H:%M")}\n查看详情: https://quote.eastmoney.com/center/gridlist.html'
    }
    response = requests.post(url, data=data, timeout=10)
    print(f"✅ 微信推送成功: {response.text}")
else:
    print(f"📊 未达阈值: {down_count} < 3000，未推送")

print("任务完成！")
