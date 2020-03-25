import requests
import re
import sqlite3

def getImagesList(page):
    conn = sqlite3.connect('doutu.db')
    # 创建一个cursor：
    cursor = conn.cursor()
    #获取源代码
    html = requests.get('http://www.doutula.com/photo/list/?page={}'.format(page)).text
    #print(html)
    #正则表达式 。*？代表通配符， 括号代表想要的
    reg = r'data-original="(.*?)".*?alt="(.*?)"'
    #re.S代表多行匹配
    reg = re.compile(reg,re.S)
    ImagesList = re.findall(reg,html)
    #print(ImagesList) 这个时候ImageList是列表形式
    for i in ImagesList:
        image_url = i[0] #用下脚标去访问每个i中的内容
        image_title = i[1]
        # 插入一条记录：
        cursor.execute("insert into doutu (title, url) values('{}','{}')".format(image_title,image_url))
        print('正在保存 %s'%image_title)
        # 通过rowcount获得插入的行数：
    # 关闭Cursor:
    cursor.close()
    # 提交事务：
    conn.commit()
    # 关闭connection：
    conn.close()

'''
data-original="http://tva3.sinaimg.cn/bmiddle/9150e4e5gy1gd3nuakpp7j206o043dfr.jpg" 
alt="还有吗？白嫖怪" 
'''
if __name__ == "__main__":
    # 数据库文件是test.db，不存在，则自动创建

    for i in range(1,20):
        getImagesList(i)
