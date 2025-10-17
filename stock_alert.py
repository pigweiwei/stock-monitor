import requests
from datetime import datetime
import os

# ===== 配置 =====
THRESHOLD = 3000
SEND_KEY = os.getenv("SERVER_SENDKEY")  # 从 GitHub Secrets 读取

# ===== 获取下跌家数 =====
def get_down_count():
    url = "https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&fields=f3&fs=m:0+t:6,m:0+t:80"
    r = requests.get(url, timeout=10)
    data = r.json()
    items = data.get("data", {}).get("diff", [])
    down_count = sum(1 for i in items if i.get("f3", 0) < 0)
    return down_count

# ===== 微信推送 =====
def send_wechat(title, content):
    url = f"https://sctapi.ftqq.com/{SEND_KEY}.send"
    data = {"title": title, "desp": content}
    r = requests.post(url, data=data)
    print("✅ 微信推送成功" if r.status_code == 200 else f"❌ 微信推送失败：{r.text}")

# ===== 主程序 =====
if __name__ == "__main__":
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        count = get_down_count()
        print(f"[{now}] 当前下跌家数：{count}")
        if count > THRESHOLD:
            title = f"⚠️ A股预警：{count}"
            content = f"当前下跌家数：{count}（超过 {THRESHOLD}）\n时间：{now}"
            send_wechat(title, content)
        else:
            print(f"✅ 低于阈值 {THRESHOLD}，无需提醒。")
    except Exception as e:
        print("❌ 获取数据失败：", e)
