#!/usr/bin/env python3
"""
从 worldcup26.ir 抓取最新比赛数据，更新 matches.json 文件
避免制裁问题：不直接调用伊朗 API，而是用 GitHub Actions 定时抓取
"""

import json
import urllib.request
import urllib.error
import sys
import time
from datetime import datetime

def fetch_latest_matches(max_retries=3):
    """从 worldcup26.ir 抓取最新比赛数据（带重试机制）"""
    url = "https://worldcup26.ir/get/games"
    
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url)
            # 添加 User-Agent，避免被识别为爬虫
            req.add_header('User-Agent', 'Mozilla/5.0 (compatible; WorldCupDataUpdater/1.0)')
            
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
                
        except urllib.error.HTTPError as e:
            print(f"⚠️  第 {attempt + 1} 次尝试失败: HTTP Error {e.code}: {e.reason}")
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # 指数退避：1秒、2秒、4秒
                print(f"   等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
            else:
                print(f"❌ 抓取数据失败（已重试 {max_retries} 次）: {e}")
                sys.exit(1)
        except urllib.error.URLError as e:
            print(f"⚠️  第 {attempt + 1} 次尝试失败: {e}")
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"   等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
            else:
                print(f"❌ 网络连接失败（已重试 {max_retries} 次）: {e}")
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
    
    # 3. 检查是否有更新（对比整个 JSON 字符串）
    old_str = json.dumps(old_data, sort_keys=True, ensure_ascii=False)
    new_str = json.dumps(latest_data, sort_keys=True, ensure_ascii=False)
    
    if old_str == new_str:
        print("✅ 数据无变化，无需更新")
        sys.exit(0)
    
    # 4. 保存新数据
    with open("matches.json", "w", encoding="utf-8") as f:
        json.dump(latest_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 数据已更新！比赛场数: {len(latest_data['games'])}")
    
    # 5. 显示变化（用于调试）
    if len(latest_data["games"]) > 0:
        first_match = latest_data["games"][0]
        print(f"   第一场比赛: {first_match.get('home_team_name_en')} vs {first_match.get('away_team_name_en')}")
        print(f"   状态: {first_match.get('finished')} ({first_match.get('time_elapsed')})")
        print(f"   比分: {first_match.get('home_score')} - {first_match.get('away_score')}")

if __name__ == "__main__":
    main()
