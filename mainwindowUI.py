# -*- coding: utf-8 -*-

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow

from os import *
from similarity import *
from DataAnalysis import *
from score import *
from top import *
import time
from urllib.request import *
from pyecharts import Bar

class Ui_MainWindow(QMainWindow):

    def setupUi(self,MainWindow):
        self.setWindowIcon(QtGui.QIcon('starbucks_icon.jpg'))
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        self.setMenuBar(self.menubar)

        self.shiqu = QtWidgets.QAction(self)
        self.shiqu.setObjectName("shiqu")

        self.shiquerji = QtWidgets.QAction(self)
        self.shiquerji.setObjectName("shiquerji")

        self.zhuzhuang = QtWidgets.QAction(self)
        self.zhuzhuang.setObjectName("zhuzhuang")

        self.bingtu = QtWidgets.QAction(self)
        self.bingtu.setObjectName("bingtu")

        self.fenbu = QtWidgets.QAction(self)
        self.fenbu.setObjectName("fenbu")

        self.shiqufenbu = QtWidgets.QAction(self)
        self.shiqufenbu.setObjectName("shiqufenbu")

        self.guojiajianbian = QtWidgets.QAction(self)
        self.guojiajianbian.setObjectName("guojiajianbian")

        self.menu.addAction(self.shiqu)
        self.menu.addAction(self.shiquerji)
        self.menu_2.addAction(self.zhuzhuang)
        self.menu_2.addAction(self.bingtu)
        self.menu_3.addAction(self.fenbu)
        self.menu_3.addAction(self.shiqufenbu)
        self.menu_3.addAction(self.guojiajianbian)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())

        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setFixedSize(200, 500)
        self.listWidget.setObjectName("listView")
        self.listWidget.close()

        self.set_topk()
        self.set_topr()
        self.set_score()
        self.set_webwindow()

        vbox = QtWidgets.QGridLayout()
        self.two = QtWidgets.QWidget()
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.topk)
        hbox.addWidget(self.topr)
        hbox.addWidget(self.score)
        self.two.setLayout(hbox)

        self.three = QtWidgets.QWidget()
        hbox_three = QtWidgets.QHBoxLayout()
        hbox_three.addWidget(self.web)
        hbox_three.addWidget(self.listWidget)
        self.listWidget.close()
        self.three.setLayout(hbox_three)

        vbox.addWidget(self.two)
        vbox.addWidget(self.three)
        self.main = QtWidgets.QWidget()
        self.resize(1600, 700)
        self.main.setLayout(vbox)
        self.setCentralWidget(self.main)

        self.retranslateUi(MainWindow)
        self.search_k.clicked.connect(self.search_kfun)
        self.shiqu.triggered.connect(self.shiqufun)
        self.shiquerji.triggered.connect(self.shiquerjifun)
        self.zhuzhuang.triggered.connect(self.zhuzhuangfun)
        self.bingtu.triggered.connect(self.bingtufun)
        self.guojiajianbian.triggered.connect(self.guojiajianbianfun)
        self.fenbu.triggered.connect(self.fenbufun)
        self.shiqufenbu.triggered.connect(self.shiqufenbufun)
        self.time_analysis.clicked.connect(self.time_analysisfun)
        self.search_r.clicked.connect(self.search_rfun)
        self.in_score.clicked.connect(self.pingfen)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        MainWindow.show()
        self.listWidget.close()

    def set_topk(self):
        self.topk = QtWidgets.QGroupBox("关键词检索")
        self.topk.setObjectName("topk")
        hbox = QtWidgets.QHBoxLayout()

        self.key = QtWidgets.QComboBox(self.topk)
        self.key.setObjectName("key")


        self.key.addItem("")
        self.key.addItem("Brand")
        self.key.addItem("Store Number")
        self.key.addItem("Store Name")
        self.key.addItem("Ownership Type")
        self.key.addItem("Street Address")
        self.key.addItem("City")
        self.key.addItem("State/Province")
        self.key.addItem("Country")
        self.key.addItem("Postcode")
        self.key.addItem("Phone Number")
        self.key.addItem("Timezone")

        self.keyword_text = ""
        self.key.activated[str].connect(self.keyword_onActivated)

        self.keyword = QtWidgets.QLineEdit(self.topk)
        self.keyword.setObjectName("keyword")
        self.keyword.setFixedWidth(60)

        self.label_k = QtWidgets.QLabel(self.topk)
        self.label_k.setObjectName("label_k")

        self.input_k = QtWidgets.QLineEdit(self.topk)
        self.input_k.setObjectName("input_k")

        self.label_lonk = QtWidgets.QLabel(self.topk)
        self.label_lonk.setObjectName("label")
        self.label_latk = QtWidgets.QLabel(self.topk)
        self.label_latk.setObjectName("label_latk")

        self.search_k = QtWidgets.QPushButton(self.topk)
        self.search_k.setObjectName("search_k")
        self.search_k.setFixedWidth(60)

        self.input_lat = QtWidgets.QLineEdit(self.topk)
        self.input_lat.setObjectName("input_lat")
        self.input_lat.setFixedWidth(50)

        self.input_lon = QtWidgets.QLineEdit(self.topk)
        self.input_lon.setObjectName("input_lon")
        self.input_lon.setFixedWidth(50)

        self.time_analysis = QtWidgets.QPushButton(self.topk)
        self.time_analysis.setObjectName("time_analysis")
        self.time_analysis.setFixedWidth(100)

        hbox.addWidget(self.key)
        hbox.addWidget(self.keyword)
        hbox.addWidget(self.label_lonk)
        hbox.addWidget(self.input_lon)
        hbox.addWidget(self.label_latk)
        hbox.addWidget(self.input_lat)
        hbox.addWidget(self.label_k)
        hbox.addWidget(self.input_k)
        hbox.addWidget(self.search_k)
        hbox.addWidget(self.time_analysis)
        self.topk.setLayout(hbox)

    def set_topr(self):
        hbox_r = QtWidgets.QHBoxLayout()

        self.topr = QtWidgets.QGroupBox("距离范围检索")
        self.topr.setObjectName("topr")

        self.label_lonr = QtWidgets.QLabel(self.topr)
        self.label_lonr.setObjectName("lonr")
        self.label_latr = QtWidgets.QLabel(self.topr)
        self.label_latr.setObjectName("label_latr")

        self.search_r = QtWidgets.QPushButton(self.topr)
        self.search_r.setObjectName("search_r")

        self.input_lat_r = QtWidgets.QLineEdit(self.topr)
        self.input_lat_r.setObjectName("input_lat_r")
        self.input_lat_r.setFixedWidth(50)

        self.input_lon_r = QtWidgets.QLineEdit(self.topr)
        self.input_lon_r.setObjectName("input_lon_r")
        self.input_lon_r.setFixedWidth(50)

        self.input_r = QtWidgets.QLineEdit(self.topr)
        self.input_r.setObjectName("input_r")

        self.rsearch = QtWidgets.QLabel(self.topr)

        self.rsearch.setObjectName("rsearch")

        hbox_r.addWidget(self.label_lonr)
        hbox_r.addWidget(self.input_lon_r)
        hbox_r.addWidget(self.label_latr)
        hbox_r.addWidget(self.input_lat_r)
        hbox_r.addWidget(self.rsearch)
        hbox_r.addWidget(self.input_r)
        hbox_r.addWidget(self.search_r)

        self.topr.setLayout(hbox_r)

    def set_score(self):
        hbox_s = QtWidgets.QHBoxLayout()

        self.score = QtWidgets.QGroupBox("评分")
        self.score.setObjectName("score")

        self.label_score = QtWidgets.QLabel(self.score)
        self.label_score.setObjectName("label_score")

        self.countSpineBox = QtWidgets.QSpinBox()
        self.countSpineBox.setRange(0, 10)
        self.countSpineBox.setEnabled(False)

        self.in_score = QtWidgets.QPushButton(self.score)
        self.in_score.setObjectName("in_score")
        self.in_score.setEnabled(False)

        hbox_s.addWidget(self.label_score)
        hbox_s.addWidget(self.countSpineBox)
        hbox_s.addWidget(self.in_score)
        self.score.setLayout(hbox_s)

    def set_webwindow(self):
        self.web = QtWidgets.QGroupBox("显示结果")
        hbox_web = QtWidgets.QHBoxLayout()
        self.webwindow = QWebEngineView()
        self.webwindow.setAutoFillBackground(True)
        self.webwindow.setObjectName("webwindow")

        hbox_web.addWidget(self.webwindow)
        self.web.setLayout(hbox_web)

    def search_kfun(self):
        input_attr = self.keyword.text()
        input_lon = float(self.input_lon.text())
        input_lat = float(self.input_lat.text())
        input_k = int(self.input_k.text())

        ki = K()
        """run_time = ki.top_fun(input_lon, input_lat, input_k, "simtopk.html", self.keyword_text.decode(encoding="utf-8"),
                              input_attr)"""
        run_time = ki.top_fun(input_lon, input_lat, input_k, "simtopk.html", self.keyword_text,input_attr)
        self.statusBar().showMessage('查询时间为： '+str(run_time))

        k_analysis = ki.topk_k_analysis(ki.df, input_lon, input_lat)
        bar_time = Bar("该经纬度下topk计算时间随k变化")
        bar_pic(k_analysis, 'k时间顺序', 'k', 'time')
        bar_time.render(r'time_analysis.html')

        path = os.getcwd()
        url = pathname2url(path)
        url = 'file:' + url + '/simtopk.html'

        self.webwindow.load(QtCore.QUrl(url))
        self.webwindow.show()
        self.listWidget.clear()

        for i in range(ki.df_res.shape[0]):
             item = QtWidgets.QListWidgetItem(ki.df_res['Store Name'][i])
             self.listWidget.addItem(item)
        self.listWidget.show()

        self.listWidget.itemClicked['QListWidgetItem*'].connect(self.dia)

    def dia(self):
        self.countSpineBox.setEnabled(True)
        self.in_score.setEnabled(True)
        self.in_score.clicked.connect(self.pingfen)

    def pingfen(self):
        score_var = int(self.countSpineBox.text())

        starbucks_df = read_data()
        starbucks_df = input_score(starbucks_df, score_var, self.listWidget.currentItem().text())
        starbucks_df.to_csv('starbucks.csv', encoding="utf_8_sig", index=False)


    def keyword_onActivated(self, text):
        self.keyword_text = text.encode("utf-8")

    def search_rfun(self):
        lon_r_text = float(self.input_lon_r.text())
        lat_r_text = float(self.input_lat_r.text())
        r_text = int(self.input_r.text())

        ri = R()
        run_time = ri.top_fun(lon_r_text, lat_r_text, r_text, "range.html", '', '')
        self.statusBar().showMessage('查询时间为： ' + str(run_time))

        path = os.getcwd()
        url = pathname2url(path)
        url = 'file:' + url + '/range.html'

        self.webwindow.load(QtCore.QUrl(url))
        self.webwindow.show()
        self.listWidget.clear()

        for i in range(ri.df_res.shape[0]):
             item = QtWidgets.QListWidgetItem(ri.df_res['Store Name'][i])
             self.listWidget.addItem(item)
        self.listWidget.show()

        self.listWidget.itemClicked['QListWidgetItem*'].connect(self.dia)


    def time_analysisfun(self):
        path = os.getcwd()
        url = pathname2url(path)
        url = 'file:' + url + '/time_analysis.html'
        self.webwindow.load(QtCore.QUrl(url))
        self.webwindow.show()
        self.listWidget.close()


    def shiqufun(self):
        # 时区图
        path = os.getcwd()
        url = pathname2url(path)
        url = 'file:' + url + '/Amout_in_Each_Timezone_Pie.html'
        self.webwindow.load(QtCore.QUrl(url))
        self.webwindow.show()
        self.listWidget.close()

    def shiquerjifun(self):
        # 时区二级图
        path = os.getcwd()
        url = pathname2url(path)
        url = 'file:' + url + '/Amount_of_Country_in_Timezone_Pie.html'
        self.webwindow.load(QtCore.QUrl(url))
        # self.setCentralWidget(self.webwindow)
        self.webwindow.show()
        self.listWidget.close()

    def shiqujianbianfun(self):
        path = os.getcwd()
        url = pathname2url(path)
        url = 'file:'+url+'/map_time.html'
        self.webwindow.load(QtCore.QUrl(url))
        self.webwindow.show()
        self.listWidget.close()

    def zhuzhuangfun(self):
        # 柱状图
        path = os.getcwd()
        url = pathname2url(path)
        url = 'file:' + url + '/Amount_Each_Country_Bar.html'
        self.webwindow.load(QtCore.QUrl(url))
        self.webwindow.show()
        self.listWidget.close()

    def bingtufun(self):
        # 饼状图
        path = os.getcwd()
        url = pathname2url(path)
        url = 'file:' + url + '/Amount_Each_Country_Pie.html'
        self.webwindow.load(QtCore.QUrl(url))
        self.webwindow.show()
        self.listWidget.close()


    def fenbufun(self):
        # 店铺分布图
        path = os.getcwd()
        url = pathname2url(path)
        url = 'file:' + url + '/fenbutu.html'
        self.webwindow.load(QtCore.QUrl(url))
        self.webwindow.show()
        self.listWidget.close()


    def shiqufenbufun(self):
        # 店铺时区分布图
        path = os.getcwd()
        url = pathname2url(path)
        url = 'file:' + url + '/map_time.html'
        self.webwindow.load(QtCore.QUrl(url))
        self.webwindow.show()
        self.listWidget.close()

    def guojiajianbianfun(self):
        path = os.getcwd()
        url = pathname2url(path)
        url = 'file:' + url + '/distribution_map_country.html'
        self.webwindow.load(QtCore.QUrl(url))
        self.webwindow.show()
        self.listWidget.close()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_k.setText(_translate("MainWindow", "结果数:"))
        self.label_lonk.setText(_translate("MainWindow", "经度:"))
        self.label_latk.setText(_translate("MainWindow", "纬度:"))
        self.search_k.setText(_translate("MainWindow", "查询"))
        self.time_analysis.setText(_translate("MainWindow", "查询时间分析"))
        self.label_lonr.setText(_translate("MainWindow", "经度:"))
        self.label_latr.setText(_translate("MainWindow", "纬度:"))
        self.search_r.setText(_translate("MainWindow", "查询"))
        self.rsearch.setText(_translate("MainWindow", "距离范围(米):"))
        self.label_score.setText(_translate("MainWindow", "输入分数(1-10):"))
        self.in_score.setText(_translate("MainWindow", "评分"))
        self.menu.setTitle(_translate("MainWindow", "按时区数据统计"))
        self.menu_2.setTitle(_translate("MainWindow", "按国家数据统计"))
        self.menu_3.setTitle(_translate("MainWindow", "分布地图"))
        self.shiqu.setText(_translate("MainWindow", "各时区店铺数量统计饼图"))
        self.shiquerji.setText(_translate("MainWindow", "各时区店铺数量统计饼图（详细）"))
        self.zhuzhuang.setText(_translate("MainWindow", "柱状图"))
        self.bingtu.setText(_translate("MainWindow", "饼图"))
        self.guojiajianbian.setText(_translate("MainWindow", "各国家店铺数量渐变图"))
        self.fenbu.setText(_translate("MainWindow", "店铺分布图"))
        self.shiqufenbu.setText(_translate("MainWindow", "时区店铺分布图"))
