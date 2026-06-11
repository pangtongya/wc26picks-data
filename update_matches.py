#!/usr/bin/env python3
"""
从 worldcup26.ir 抓取最新比赛数据，更新 matches.json 文件
避免制裁问题：不直接调用伊朗 API，而是用 GitHub Actions 定时抓取
"""

import json
import urllib.request
import urllib.error
import sys
from datetime import datetime

def fetch_latest_matches():
    """从 worldcup26.ir 抓取最新比赛数据"""
    url = "https://worldcup26.ir/get/games"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        # API 返回的是数组，需要包装成 {"games": [...]}
        if isinstance(data, list):
            return {"games": data}
        elif isinstance(data, dict) and "games" in data:
            return data
        else:
            print(f"❌ API 返回格式错误: {type(data)}")
            sys.exit(1)
    except urllib.error.URLError as e:
        print(f"❌ 抓取数据失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        sys.exit(1)

def main():
    print(f"🚀 开始更新比赛数据... {datetime.now()}")
    
    # 1. 抓取最新数据
    latest_data = fetch_latest_matches()
    
    # 2. 读取现有数据（用于对比）
    try:
        with open("matches.json", "r", encoding="utf-8") as f:
            old_data = json.load(f)
    except FileNotFoundError:
        old_data = {"games": []}
    
    # 3. 检查是否有更新
    old_games = old_data.get("games", [])
    new_games = latest_data.get("games", [])
    
    if len(old_games) == len(new_games):
        # 简单检查：对比第一场比赛的 finished 状态
        if len(old_games) > 0 and len(new_games) > 0:
            if old_games[0].get("finished") == new_games[0].get("finished"):
                print("✅ 数据无变化，无需更新")
                sys.exit(0)
    
    # 4. 保存新数据
    with open("matches.json", "w", encoding="utf-8") as f:
        json.dump(latest_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 数据已更新！比赛场数: {len(new_games)}")
    
    # 5. 显示变化（用于调试）
    if len(new_games) > 0:
        first_match = new_games[0]
        print(f"   第一场比赛: {first_match.get('home_team_name_en')} vs {first_match.get('away_team_name_en')}")
        print(f"   状态: {first_match.get('finished')} ({first_match.get('time_elapsed')})")
        print(f"   比分: {first_match.get('home_score')} - {first_match.get('away_score')}")

if __name__ == "__main__":
    main()
