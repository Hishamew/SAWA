import json
import os
import re
import csv
import shutil
import time
import requests
from DrissionPage.common import ActionChains
from bs4 import BeautifulSoup
from DrissionPage import WebPage, ChromiumOptions, ChromiumPage
from lxml import etree

do = ChromiumOptions(read_file=False)


def slide2(browser):
    container_old = 0
    while True:
        container = browser.eles('.list-container')[0].eles('.comment-item')
        ac.scroll(delta_x=0, delta_y=50, on_ele=container[-1])
        time.sleep(1)
        # print(len(container))
        if (len(container) == container_old):
            break
        else:
            container_old = len(container)
    # print('滑动结束')


def save_csv(file_path, data, encoding='utf-8-sig'):
    # 根据文件是否存在选择文件打开模式（追加或写入）
    mode = 'a' if os.path.exists(file_path) else 'w'

    # 打开文件并写入数据
    with open(file_path, mode, encoding=encoding, newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        # 如果文件不存在，写入表头
        if mode == 'w':
            writer.writeheader()
        # 写入字典数据
        writer.writerow(data)


def selenium_init():
    browser = ChromiumPage()
    browser.get('https://www.xiaohongshu.com/explore')
    return browser


def get_picture(html, keyword):
    soup = etree.HTML(html)
    data = soup.xpath('//*[@id="noteContainer"]/div[2]/div/div/div[1]/div/div')
    for pictureUrls in data[1:]:
        pictureUrl = pictureUrls.xpath('//@style')
        pictureUrl = ''.join(pictureUrl)
        imgs = re.findall('url\("(.*?)"\);', pictureUrl)
        try:
            text = soup.xpath('//*[@id="detail-title"]/text()')[0].strip()
            # 创建文件夹
            folder_name = text  # 文件夹名称为标题文本
            if not os.path.exists(os.path.join(keyword, folder_name)):  # 如果文件夹不存在，则创建
                os.mkdir(os.path.join(keyword, folder_name))
            id = 1
            for img in imgs[1:-1]:
                response = requests.get(img)
                picture = response.content
                try:
                    name = re.findall('[\u4e00-\u9fa5]+', text)[0] + str(id)
                    file_path = os.path.join(keyword, folder_name, f'{name}.jpg')
                    with open(file_path, 'wb') as f:
                        f.write(picture)
                        id += 1
                except Exception as e:
                    # print(text)
                    pass
        except:
            pass


def scroll(browser, urls):
    # 获取第一页的笔记链接
    get_detail(browser, urls)
    end_url = urls[-1]
    # 滚动鼠标获取更多的笔记链接
    while True:
        slide(browser)
        get_detail(browser, urls)
        if end_url == urls[-1]:
            break
            # 已经滑动到页面底部，退出循环
        else:
            # 更新end_url值
            end_url = urls[-1]


def slide(browser):
    # 模拟鼠标操作，滚动到页面底部
    browser.run_js('_ => { window.scrollBy(0, 300); }')
    ac.wait(0.2)  # 等待 1 秒


def get_detail(browser, urls):
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')  # 获取页面HTML代码
    a_list = soup.select('div.feeds-container > section > div > a:first-of-type')
    for a in a_list:
        href = a.get('href')
        url = f'https://www.xiaohongshu.com{href}'
        urls.append(url)
    return urls


def quchong(list1):
    list2 = []
    for index in range(len(list1)):
        i = list1[index]
        flag = False
        for index2 in range(index + 1, len(list1)):
            j = list1[index2]
            if i == j:
                flag = True
        if flag == False:
            list2.append(i)
    return list2


def get_comment(browser):
    html = browser.html
    data = etree.HTML(html)
    comment_li = data.xpath('//div[@class="comments-container"]/div[2]/div')
    for comment_l in comment_li:
        comment_l = comment_l.xpath('./div/div[2]/div[2]/text()')
        comment_l = ''.join(comment_l)
        comment_list.append(comment_l)
    # print(comment_list)

    list_er_comment = data.xpath('//div[@class="comments-container"]/div[2]/div')
    for list in list_er_comment:
        er_comments = list.xpath('./div/div[2]/div[5]/div[1]/div')
        for er_comment in er_comments:
            er_comment = er_comment.xpath('./div/div[2]/div[2]/text()')
            er_comment = ''.join(er_comment)
            er_comment_list.append(er_comment)
    # print(er_comment_list)
    return comment_list, er_comment_list


browser = selenium_init()
ac = ActionChains(browser)
搜索 = browser.ele('xpath://*[@id="app"]/div[1]/div[1]/header/div[2]/input')
# keyword = input("输入关键词:")

import argparse
parser = argparse.ArgumentParser(description="一个简单的命令行参数示例")
parser.add_argument( "--title", help="输入关键字", required=True)
parser.add_argument("--topk", help="输入排行", required=True)
parser.add_argument("--output_dir", help="输出存放的位置", required=True)
args = parser.parse_args()
keyword=args.title
搜索.input(str(keyword) + '\n')
ac.wait(1)
点击图文 = browser.ele(
    'xpath://*[@id="app"]/div[1]/div[2]/div[2]/div/div[1]/div[1]/div/div[2] | //*[@id="search-type"]/div[1]/div/div[2]')
点击图文.click()
ac.wait(2)
keyword1 = keyword
file_path = args.output_dir + keyword1 + '图片'
# 如果文件夹已存在，则先删除文件夹及其内容
if os.path.exists(file_path):
    shutil.rmtree(file_path)
os.makedirs(file_path)

file_path1 = args.output_dir + keyword1
# 如果文件夹已存在，则先删除文件夹及其内容
if os.path.exists(file_path1):
    shutil.rmtree(file_path1)
os.makedirs(file_path1)

# 打印列表
item = {}


def selenium_init():
    # 以该配置创建页面对象
    browser = WebPage(driver_or_options=do, session_or_options=False)
    return browser


browser = selenium_init()


def get_note_url_list(browser):
    note_url_list = []
    scroll(browser, note_url_list)  # 模拟滚动页面获取笔记链接
    note_url_list = quchong(note_url_list)
    print(len(note_url_list))
    return note_url_list


note_url_list = get_note_url_list(browser)
for note_url in note_url_list[:10]:
    comment_list = []
    er_comment_list = []
    browser.get(note_url)
    time.sleep(1)
    html = browser.html
    data = etree.HTML(html)
    get_picture(html, file_path)
    try:
        slide2(browser)
    except:
        item['评论内容'] = ''
    comment_list, er_comment_list = get_comment(browser)
    try:
        Id = browser.url
        Id = os.path.basename(Id).split('?')[0]
        item['笔记ID'] = Id
        if item['笔记ID'] == 'explore':
            item['笔记ID'] = os.path.basename(note_url).split('?')[0]
        try:
            item['笔记标题'] = data.xpath('//*[@id="detail-title"]/text()')[0]
        except:
            item['笔记标题'] = '无标题'
        item['笔记内容'] = data.xpath('//*[@id="detail-desc"]/span[1]//text()')
        item['笔记内容'] = ''.join(item['笔记内容'])
        item['一级评论'] = comment_list
        item['二级评论'] = er_comment_list
        item['昵称'] = \
        data.xpath('/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[1]/div/div[1]/a[2]/span/text()')[
            0].strip()
        try:
            item['发布时间'] = data.xpath('//*[@id="noteContainer"]/div[3]/div[2]/div[1]/div[4]/text()')[0]
        except:
            item['发布时间'] = data.xpath(
                '//*[@id="noteContainer"]/div[3]/div[2]/div[1]/div[3]/span/text() | //*[@id="noteContainer"]/div[3]/div[2]/div[1]/div[4]/span/text()')[
                0]
        item['点赞数'] = data.xpath('//*[@id="noteContainer"]/div[3]/div[3]/div[1]/div[1]/span[1]/span[2]/text()')[
            0].strip()
        item['收藏数'] = data.xpath('//*[@id="noteContainer"]/div[3]/div[3]/div[1]/div[1]/span[2]/span/text()')[
            0].strip()
        item['评论数'] = data.xpath('//*[@id="noteContainer"]/div[3]/div[3]/div[1]/div[1]/span[3]/span/text()')[
            0].strip()
        # shijian=time.time()
        # dt_object = datetime.datetime.fromtimestamp(shijian)
        # item['爬取时间'] = dt_object.strftime("%Y-%m-%d")
        print(item, '--->', 'test')
        detailName = item['笔记标题']
        with open(f'{file_path1}/{detailName}.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(item, indent=4, ensure_ascii=False))
        time.sleep(1)
    except:
        print(item, '--->', 'err')
