# 在这里编写代码
import requests
from bs4 import BeautifulSoup
import csv

# 请求头，模拟浏览器访问
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 存储所有大学信息的列表
universities = []

def get_university_info(page):
    """获取单页的大学排名信息"""
    # 软科中国大学排名的翻页URL（2024年版，可根据实际情况调整）
    url = f"https://www.shanghairanking.cn/rankings/best-chinese-universities/{page}"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # 抛出HTTP请求错误
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 定位排名表格的行（排除表头）
        rows = soup.select("table tr")[1:]
        for row in rows:
            cols = row.select("td")
            if len(cols) >= 4:  # 确保数据列完整
                rank = cols[0].text.strip()  # 排名
                name = cols[1].text.strip()  # 学校名称
                location = cols[2].text.strip()  # 所在地区
                score = cols[3].text.strip()  # 总分
                universities.append({
                    "排名": rank,
                    "学校名称": name,
                    "所在地区": location,
                    "总分": score
                })
        print(f"第{page}页数据爬取完成，共获取{len(rows)}所高校信息")
    except Exception as e:
        print(f"第{page}页爬取失败：{str(e)}")

def main():
    """主函数：翻页爬取并保存数据"""
    # 软科排名总页数（2024年共30页，对应近600所高校）
    total_pages = 30
    for page in range(1, total_pages + 1):
        get_university_info(page)
    
    # 将数据保存为CSV文件，方便查看和分析
    with open("中国大学排名.csv", "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["排名", "学校名称", "所在地区", "总分"])
        writer.writeheader()
        writer.writerows(universities)
    print(f"爬取完成！共获取{len(universities)}所高校信息，已保存至【中国大学排名.csv】")

if __name__ == "__main__":
    main()
