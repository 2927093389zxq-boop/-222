import time
import random
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import os

# 我们不再需要 stealth.min.js 文件，代码已简化
URL = "https://www.amazon.com/bestsellers"

def scrape_amazon_bestsellers() -> List[Dict[str, Any]]:
    """
    人机协作版爬虫。
    这将启动一个真实的、可见的浏览器窗口。
    如果出现验证码，需要您手动完成验证。
    """
    
    with sync_playwright() as p:
        print("--- 启动人机协作模式 ---")
        print("一个浏览器窗口即将弹出，请不要关闭它。")
        
        # --- 核心改动：headless=False ---
        # 这将启动一个可见的浏览器窗口，而不是在后台运行。
        browser = p.chromium.launch(headless=False, slow_mo=50) # slow_mo减慢操作，让您看清过程
        
        context = browser.new_context()
        page = context.new_page()
        
        try:
            print("正在导航到亚马逊畅销榜页面...")
            page.goto(URL, timeout=120000) # 延长超时时间到2分钟，给您充足的时间操作

            # --- 等待您的操作 ---
            print("\n" + "="*50)
            print("请注意：浏览器已打开。")
            print("如果页面上出现了【验证码】（例如拖动滑块、点击图片），请立即手动完成它。")
            print("完成验证后，程序会自动接管。您无需进行其他任何操作。")
            print("正在等待页面加载或您的验证...")
            print("="*50 + "\n")
            
            # 等待直到商品列表出现，或者直到超时
            # 这是程序在等您完成验证的关键
            page.wait_for_selector('div.zg-grid-general-faceout, div.p13n-sc-uncoverable-faceout', timeout=120000)

            print("检测到商品列表！您已成功通过验证，程序现在接管。")
            print("正在抓取数据...")

            # 抓取前最后向下滚动一次，确保内容完整
            page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
            time.sleep(2)

            html_content = page.content()
            
        finally:
            print("操作完成，正在关闭浏览器...")
            browser.close()

        soup = BeautifulSoup(html_content, 'lxml')
        products = soup.select('div.zg-grid-general-faceout, div.p13n-sc-uncoverable-faceout')

        if not products:
            raise Exception("未找到商品列表。可能是验证码未能正确通过，或页面结构已更新。")

        scraped_data = []
        for product in products:
            try:
                rank_element = product.select_one('span.zg-bdg-text')
                rank = rank_element.text.strip('#') if rank_element else 'N/A'

                name_element = product.select_one('div._cDEzb_p13n-sc-css-line-clamp-3_g3dy1, a.a-link-normal > span')
                name = name_element.text.strip() if name_element else 'N/A'
                
                reviews_element = product.select_one('a.a-link-normal.a-size-small > span')
                reviews_count = reviews_element.text.strip() if reviews_element else 'N/A'

                price_element = product.select_one('span._cDEzb_p13n-sc-price_3mJ9Z, span.a-price > span.a-offscreen')
                price = price_element.text.strip() if price_element else 'N/A'

                scraped_data.append({
                    "Rank": rank, "Name": name, "Reviews Count": reviews_count,
                    "Price": price, "Source": "Amazon (Human Assisted)"
                })
            except Exception:
                continue
        
        print(f"成功解析到 {len(scraped_data)} 条商品数据！")
        return scraped_data