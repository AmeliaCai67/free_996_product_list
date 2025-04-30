import json
import time
import random
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
import os

class XHSCrawler:
    def __init__(self):
        self.ua = UserAgent()
        self.setup_driver()
        
    def setup_driver(self):
        try:
            print("正在测试网络连接...")
            response = requests.get("https://www.baidu.com", timeout=5)
            print(f"网络连接正常，状态码：{response.status_code}")
        except Exception as e:
            print(f"网络连接测试失败：{str(e)}")
            print("请检查网络设置或代理配置")
            raise

        options = webdriver.ChromeOptions()
        options.add_argument(f'user-agent={self.ua.random}')
        # 注释掉无头模式
        # options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        
        driver_path = "/Users/kekoukelewenxue/Desktop/不加班！/free_996_product_list/chromedriver"
        print(f"使用 ChromeDriver 路径: {driver_path}")
        
        if not os.path.exists(driver_path):
            print(f"错误：ChromeDriver 文件不存在于路径 {driver_path}")
            raise FileNotFoundError(f"ChromeDriver not found at {driver_path}")
        
        if not os.access(driver_path, os.X_OK):
            print(f"正在设置 ChromeDriver 执行权限...")
            os.chmod(driver_path, 0o755)
        
        service = Service(driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        
    def wait_for_login(self):
        try:
            print("请点击左侧'登录'按钮，并使用手机扫描二维码登录...")
            print("等待扫码登录中，您有60秒的时间完成登录...")
            
            # 直接等待60秒
            time.sleep(60)
            print("继续执行爬取...")
            return True
        
        except Exception as e:
            print(f"等待过程中出错: {str(e)}")
            return False
    
    def get_comments(self, url):
        try:
            print("正在访问目标页面...")
            self.driver.get(url)
            time.sleep(3)  # 等待页面加载
            
            comments = set()  # 使用set自动去重
            start_time = time.time()
            comment_count = 0
            
            while True:
                # 检查是否超过5分钟
                if time.time() - start_time > 300:  # 300秒 = 5分钟
                    print("已达到5分钟时限，停止爬取")
                    break
                
                # 使用 XPath 获取所有评论内容
                comment_elements = self.driver.find_elements(By.XPATH, "//div[contains(@id, 'comment-')]/div/div[2]/div[2]")
                
                for element in comment_elements:
                    try:
                        comment_text = element.text
                        if comment_text:
                            comments.add(comment_text)
                    except Exception as e:
                        print(f"解析评论时出错: {str(e)}")
                        continue
                
                # 每爬取10条评论后滚动
                new_count = len(comments)
                if new_count >= comment_count + 10:
                    print(f"已爬取{new_count}条评论，正在翻页...")
                    self.driver.execute_script("window.scrollBy(0, 1000);")  # 向下滚动1000像素
                    time.sleep(5)  # 等待5秒加载新内容
                    comment_count = new_count
                
                # 小范围滚动以触发加载
                self.driver.execute_script("window.scrollBy(0, 100);")
                time.sleep(0.5)
                
            print(f"爬取完成，共获取{len(comments)}条不重复评论")
            return list(comments)  # 转换回列表返回
            
        except Exception as e:
            print(f"爬取过程中出错: {str(e)}")
            return []
        
    def save_to_json(self, comments, output_file):
        # 修改保存格式，直接保存评论内容列表
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(comments, f, ensure_ascii=False, indent=2)
            
    def close(self):
        self.driver.quit()

def main():
    parser = argparse.ArgumentParser(description='小红书评论爬虫')
    parser.add_argument('--url', type=str, required=True, help='要爬取的页面URL')
    args = parser.parse_args()
    
    crawler = XHSCrawler()
    
    try:
        print("正在打开目标页面...")
        crawler.driver.get(args.url)  # 直接打开目标URL
        time.sleep(2)
        
        if not crawler.wait_for_login():
            print("登录失败，程序退出")
            return
        
        print("开始爬取评论...")
        comments = crawler.get_comments(args.url)
        print(f"共爬取到 {len(comments)} 条评论")
        
        output_file = "comments.json"
        crawler.save_to_json(comments, output_file)
        print(f"评论已保存到 {output_file}")
        
    finally:
        crawler.close()

if __name__ == "__main__":
    main()
