'''

class Book:
    #构造函数

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
    print(tables)
    print("========================")
    table_list = re.findall('(\'.*?\')',str(tables))
    print(table_list)
    print("========================")
    table_list = [re.sub("'",'',each) for each in table_list]
    print(table_list)
    print("========================")
    if table_name in table_list:
        return 1
    else:
        return 0

'''

import sys
from PyQt5 import QtWidgets
from fin_1 import Ui_Form

class MyPyQT_Form(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(MyPyQT_Form, self).__init__()
        self.setupUi(self)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    my_pyqt_form = MyPyQT_Form()
    my_pyqt_form.show()
    sys.exit(app.exec_())