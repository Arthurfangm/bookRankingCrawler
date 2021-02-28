from selenium import webdriver  # 用于打开浏览器

#         实现等待需要用到下面三个库
#         1.用于指定 HTML 文件中 DOM 标签元素
#         2.等待网页加载完成
#         3.用于指定网页加载结束条件

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

d = {}
d['a']=1
d['b']=2
d['c']=3
dd = d.keys()



url = 'https://yjszs.ecnu.edu.cn/system/sslqmd_list.asp?yxid=135'
# 实例化浏览器对象
broswer = webdriver.Chrome(executable_path='F:/temp/upan/pythonprogramming/hdsf/chromedriver.exe')

# 打开网页
broswer.get(url)
records = []  # 用于存放成绩记录数据
count = 0  # 用于记录

# WebDriverWait(broswer, 10).until(
#     EC.presence_of_all_elements_located((By.CLASS_NAME, 'title-text')))

for j in range(4, 207):  # j表示当前页面中的第j本书，一般来说，每个页面有15本书

    is_all_day = '/html/body/form/table/tbody/tr/td/table/tbody/tr[{}]/td[2]/div/font'.format(
        str(j))
    major = '/html/body/form/table/tbody/tr/td/table/tbody/tr[{}]/td[3]/div/font'.format(
        str(j))
    cj_zz = '/html/body/form/table/tbody/tr/td/table/tbody/tr[{}]/td[6]/div/font'.format(
        str(j))
    cj_yy = '/html/body/form/table/tbody/tr/td/table/tbody/tr[{}]/td[7]/div/font'.format(
        str(j))
    cj_sx = '/html/body/form/table/tbody/tr/td/table/tbody/tr[{}]/td[8]/div/font'.format(
        str(j))
    cj_408 = '/html/body/form/table/tbody/tr/td/table/tbody/tr[{}]/td[9]/div/font'.format(
        str(j))
    cj_fs = '/html/body/form/table/tbody/tr/td/table/tbody/tr[{}]/td[14]/div/font'.format(
        str(j))

    record = {}

    record['is_all_day'] = broswer.find_elements_by_xpath(is_all_day).text
    record['major'] = broswer.find_elements_by_xpath(major).text
    record['cj_zz'] = broswer.find_elements_by_xpath(cj_zz).text
    record['cj_yy'] = broswer.find_elements_by_xpath(cj_yy).text
    record['cj_sx'] = broswer.find_elements_by_xpath(cj_sx).text
    record['cj_408'] = broswer.find_elements_by_xpath(cj_408).text
    record['cj_fs'] = broswer.find_elements_by_xpath(cj_fs).text

    count += 1
    records.append(record)

