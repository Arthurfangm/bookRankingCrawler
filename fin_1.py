# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fin_1.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

class Book:
    '''
    构造函数
    '''

    def __init__(self, title, score, num_of_review, publish):
        self.title = title  # 书名
        self.score = score  # 评分
        self.num_of_review = num_of_review  # 评分人数
        self.publish = publish  # 出版信息

    def __lt__(self, other):
        return self.score > other.score

def table_exists(cur, table_name):
    import re
    sql = "show tables;"
    cur.execute(sql)
    tables = [cur.fetchall()]
    table_list = re.findall('(\'.*?\')',str(tables))
    table_list = [re.sub("'",'',each) for each in table_list]
    if table_name in table_list:
        return 1
    else:
        return 0


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1259, 607)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(50, 140, 121, 51))
        self.pushButton.setObjectName("pushButton")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(10, 10, 211, 101))
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(Form)
        self.textEdit_2.setGeometry(QtCore.QRect(230, 10, 1021, 581))
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit.setText("请在右边的输入框中输入要搜索的关键词，再按下方的按钮")

        self.retranslateUi(Form)
        self.pushButton.clicked.connect(Form.pushButton_click)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "搜索"))

    def pushButton_click(self):
        key = self.textEdit_2.toPlainText()
        # 获取关键词输入
        # key = "深度学习"
        table_name = "{}_infos".format(key)

        import pymysql
        import re
        conn = pymysql.connect(host='localhost', user='root', passwd='123456', port=3306, db='douban_books',
                               charset='utf8')

        cur = conn.cursor()
        if (table_exists(cur, table_name)):
            # 获取表的长度
            cur = conn.cursor()
            sql = "SELECT * FROM {}".format(table_name)
            result = cur.execute(sql)
            book_s=""

            self.textEdit.setText("共有{}条数据，为你展示{}条".format(result, min(result, 20)))
            for i in range(0, min(20, result)):
                book_s=book_s+str(i+1)+"  "+str(cur.fetchone())+"\n"
            self.textEdit_2.setText(book_s)
            conn.close()
        else:
            self.textEdit.setText("现在开始从网络获取数据，请稍等...")
            from selenium import webdriver  # 用于打开浏览器

            #         实现等待需要用到下面三个库
            #         1.用于指定 HTML 文件中 DOM 标签元素
            #         2.等待网页加载完成
            #         3.用于指定网页加载结束条件

            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC

            url = 'https://search.douban.com/book/subject_search?search_text={}&cat=1001&start=0'.format(str(key))
            # 实例化浏览器对象
            broswer = webdriver.Chrome()

            # 打开网页
            broswer.get(url)
            books = []  # 用于存放书籍数据
            book_count = -1  # 用于记录
            while True:  # 循环翻页
                # 等待元素加载出来
                WebDriverWait(broswer, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, 'title-text')))

                books_WebElement = broswer.find_elements_by_xpath('//div[@class="detail"]')#找到所有的书，用于得出该页面中书籍的数量
                num_of_book = len(books_WebElement) + 1
                for j in range(1, num_of_book):#j表示当前页面中的第j本书，一般来说，每个页面有15本书

                    title_path = '//*[@id="root"]/div/div[2]/div[1]/div[1]/div[{}]/div/div/div[1]/a'.format(
                        str(j))
                    score_path = '//*[@id="root"]/div/div[2]/div[1]/div[1]/div[{}]/div/div/div[2]/span[2]'.format(
                        str(j))
                    num_of_review_path = '//*[@id="root"]/div/div[2]/div[1]/div[1]/div[{}]/div/div/div[2]/span[3]'.format(
                        str(j))
                    publish_path = '//*[@id="root"]/div/div[2]/div[1]/div[1]/div[{}]/div/div/div[3]'.format(
                        str(j))

                    title = broswer.find_elements_by_xpath(title_path)
                    score = broswer.find_elements_by_xpath(score_path)
                    num_of_review = broswer.find_elements_by_xpath(num_of_review_path)
                    publish = broswer.find_elements_by_xpath(publish_path)
                    if title == [] or score == [] or num_of_review == [] or publish == []:
                        continue
                    else:
                        book_count += 1
                        book = Book(title[0].text, float(score[0].text), int(num_of_review[0].text[1:-4]),
                                    publish[0].text)
                        books.append(book)

                # 定位‘后页’的元素，并点击。这里可以用broswer.find_element_by_xpath(),即就找一个
                next = broswer.find_elements_by_xpath('//a[@class="next"]')
                if next == []:  # 如果到了最后一页————没有“下一页”这个按钮
                    break;
                else:
                    next[0].click()  # 定位“后叶”的元素，并点击

            '''
            特殊字符处理：
            1.所有的双引号转换成单引号——否则在写sql语句的时候可能会有问题
            2.去掉字符串里的'\r','\n'——虽然没有用，目前并未发现存在什么问题
            '''

            for book in books:
                book.title = book.title.replace('\r', '').replace('\n', '').replace('"', "'")
                book.publish = book.publish.replace('\r', '').replace('\n', '').replace('"', "'")

            import pymysql

            conn = pymysql.connect(host='localhost', user='root', passwd='123456', port=3306, db='douban_books',
                                   charset='utf8')

            '''
            新建数据表
            '''
            cur = conn.cursor()

            try:
                sql = "DROP TABLE IF EXISTS {}_infos".format(key)
                cur.execute(sql)
                conn.commit()
                sql = "CREATE TABLE {}_infos (书名 VARCHAR(200), 评分 NUMERIC(4,2), 评分人数 INT(10), 出版信息 VARCHAR(500));".format(
                    key)
                cur.execute(sql)
                conn.commit()
            except:
                print("创建表失败")
                conn.rollback()
            conn.close()

            '''
            将存在dooks列表里的数据存到数据库里
            '''
            '''
                排序
            '''
            books.sort()

            # import pymysql
            conn = pymysql.connect(host='localhost', user='root', passwd='123456', port=3306, db='douban_books',
                                   charset='utf8')

            for book in books:
                cur = conn.cursor()

                try:
                    sql = 'INSERT INTO {}_infos VALUES("{}",{},{},"{}");'.format(key, book.title, book.score,
                                                                                 book.num_of_review,
                                                                                 book.publish)
                    cur.execute(sql)
                    conn.commit()
                except:
                    print("插入表失败")
                    conn.rollback()

            # 爬取完成
            self.textEdit.setText("已完成书籍数据搜索，共{}条数据,为你展示了{}条".format(book_count + 1, min(20, book_count+1)))
            book_s=""
            for i in range(0, min(20, book_count+1)):
                book_s=book_s+str(i+1)
                book_s=book_s+"   "
                book_s=book_s+str(books[i].title)
                book_s = book_s + " "
                book_s=book_s+str(books[i].score)
                book_s = book_s + " "
                book_s=book_s+str(books[i].num_of_review)
                book_s = book_s + " "
                book_s=book_s+str(books[i].publish)
                book_s=book_s+"\n"

            self.textEdit_2.setText(book_s)
