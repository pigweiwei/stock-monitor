import akshare as ak
import requests
import os

# 从 GitHub Secrets 获取 SendKey（安全存储）
send_key = os.environ.get('SEND_KEY')  # 如果没有设置，会为空

# 获取 A 股实时行情数据
df = ak.stock_zh_a_spot_em()  # 返回所有 A 股实时数据 DataFrame

# 计算下跌股票数（change < 0）
down_count = (df['change'] < 0).sum()

# 打印日志（可选，用于调试）
print(f"当前下跌家数: {down_count}")

# 如果下跌超过 3000 家，发送微信推送
if down_count > 3000 and send_key:
    url = f"https://sctapi.ftqq.com/{send_key}.send"
    data = {
        'title': 'A股下跌警报',
        'desp': f'当前下跌家数: {down_count}\n时间: {df["trade_time"].iloc[0]}'  # 添加时间等额外信息
    }
    response = requests.post(url, data=data)
    print(f"推送响应: {response.text}")
else:
    print("未超过阈值或无 SendKey，未推送")
