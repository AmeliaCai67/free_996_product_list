import json
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

class XHSCrawler:
    def __init__(self):
        self.ua = UserAgent()
        self.setup_driver()
        
    def setup_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument(f'user-agent={self.ua.random}')
        options.add_argument('--headless')  # 无头模式
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        
    def get_comments(self, url):
        try:
            self.driver.get(url)
            # 等待评论区加载
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "comment-item"))
            )
            
            comments = []
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            
            while True:
                # 滚动到页面底部
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.uniform(1, 2))  # 随机等待时间
                
                # 获取当前页面上的所有评论
                comment_elements = self.driver.find_elements(By.CLASS_NAME, "comment-item")
                
                for element in comment_elements:
                    try:
                        comment_data = {
                            "user_name": element.find_element(By.CLASS_NAME, "user-name").text,
                            "content": element.find_element(By.CLASS_NAME, "content").text,
                            "time": element.find_element(By.CLASS_NAME, "time").text,
                            "likes": element.find_element(By.CLASS_NAME, "like-count").text
                        }
                        if comment_data not in comments:
                            comments.append(comment_data)
                    except Exception as e:
                        print(f"解析评论时出错: {str(e)}")
                        continue
                
                # 检查是否到达页面底部
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
                
            return comments
            
        except Exception as e:
            print(f"爬取过程中出错: {str(e)}")
            return []
        
    def save_to_json(self, comments, output_file):
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(comments, f, ensure_ascii=False, indent=2)
            
    def close(self):
        self.driver.quit()

def main():
    url = "http://xhslink.com/a/A9THN2E6sQsbb"  # 示例URL
    crawler = XHSCrawler()
    
    try:
        print("开始爬取评论...")
        comments = crawler.get_comments(url)
        print(f"共爬取到 {len(comments)} 条评论")
        
        output_file = "comments.json"
        crawler.save_to_json(comments, output_file)
        print(f"评论已保存到 {output_file}")
        
    finally:
        crawler.close()

if __name__ == "__main__":
    main()
