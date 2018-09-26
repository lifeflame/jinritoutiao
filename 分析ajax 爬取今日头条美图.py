"""
步骤：
分析ajax请求得到真正的url入口，并将response转为json模式
解析提取我们想要的title以及name
保存图片，文件名保存为md5值（为了避免重复）
采用多进程进行爬取，缩短时间
"""
import requests
import os
from hashlib import md5
from multiprocessing import Pool

def get_page(offset):
    params = {
        "offset": offset,
        "format": "json",
        "keyword": "刘亦菲",
        "autoload": "true",
        "count": "20"
    }
    base_url = "https://www.toutiao.com/search_content/?"
    try:
        response = requests.get(base_url,params=params)
        if response.status_code == 200:
            return response.json()
    except:
        return None
def get_images(json):
    if json.get("data"):
        for item in json.get("data"):
            title = item.get("title")
            if title is None:
                continue
            large_image = item.get("large_image_url")
            yield {
                "title": title,
                "image": large_image
            }

def save_image(item):
    if not os.path.exists(os.path.join("D:\crawl picture\\toutiao",item.get("title"))):
        os.mkdir(os.path.join("D:\crawl picture\\toutiao",item.get("title")))
    try:
        response = requests.get(item.get("image"))
        if response.status_code == 200:
            file_path = "{0}".format(md5(response.content).hexdigest())
            if not os.path.exists(file_path):
                os.chdir(os.path.join("D:\crawl picture\\toutiao",item.get("title")))
                with open(file_path+".jpg", "wb") as f:
                    f.write(response.content)
            else:
                print("Downloaded:",file_path)
    except:
        print("Failed to save picture")

def main(offset):
    json = get_page(offset)
    for item in get_images(json):
        print(item)
        save_image(item)

if __name__ == '__main__':
    pool = Pool()
    groups = [x*20 for x in range(5)]
    pool.map(main,groups)
    pool.close()
    pool.join()



