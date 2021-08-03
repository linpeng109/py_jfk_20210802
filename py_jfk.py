import sys

import pandas as pd
from PySide2.QtCore import QFile, QDate
from PySide2.QtGui import QFont
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QDial, QLineEdit, QComboBox, \
    QLabel, QSlider, QDateEdit, QSpinBox, QDoubleSpinBox

from py_config import ConfigFactory
from py_logging import LoggerFactory


class JFK():
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.get_data()

    def get_data(self):
        # the solvent data ...
        self.header_data = ['序号', '统一编号', '原始编号', '取样量 (g/ml)', '分析结果\n ω(Au)/10-6', '分析结果\n ω(Au)/10-6',
                            '吸光度Abs',
                            '备注']
        # use numbers for numeric data to sort properly
        self.list_data = [
            ['1', '标样', 'SG102', '30', '', '', '', ''],
            ['2', '2020A-28055', 'SG101', '30', '', '', '', ''],
            ['3', '2020A-28056', 'SG102', '30', '', '', '', ''],
            ['4', '2020A-28057', 'SG103', '30', '', '', '', ''],
            ['5', '2020A-28058', 'SG104', '30', '', '', '', ''],
            ['6', '2020A-28059', 'SG105', '30', '', '', '', ''],
            ['7', '2020A-28060', 'SG106', '30', '', '', '', ''],
            ['8', '2020A-28060', 'SG107', '30', '', '', '', ''],
            ['9', '2020A-28060', 'SG108', '30', '', '', '', ''],
            ['10', '2020A-28061', 'SG109', '30', '', '', '', ''],
            ['11', '2020A-28062', 'SG110', '30', '', '', '', ''],
            ['12', '2020A-28063', 'SG111', '30', '', '', '', ''],
        ]


        self.method_data = ['GB/T20899.1-2020', 'GB/T20899.2-2020', 'GB/T20899.3-2020']
        self.type_data = ['TAS-990F', 'TAS-991F', 'TAS-992F', 'TAS-993F']

    def load_ui(self, uifilename):
        loader = QUiLoader()
        uifile = QFile(uifilename)
        uifile.open(QFile.ReadOnly)
        self.ui = loader.load((uifile))

        # 获取comboBox_method
        self.method_combobox = self.ui.findChild(QComboBox, 'method_combobox')
        self.method_combobox.addItems(self.method_data)

        # 获取combobox_type
        self.type_combobox = self.ui.findChild(QComboBox, 'type_combobox')
        self.type_combobox.addItems(self.type_data)

        # 获取dail
        self.wavelength_dial = self.ui.findChild(QDial, 'wavelength_dial')
        self.wavelength_dial.valueChanged.connect(self.dial_value_handle)

        # 获取wavelength
        self.wavelength = self.ui.findChild(QLineEdit, 'wavelength')

        # 获取temperature_slider
        self.temperature_slider = self.ui.findChild(QSlider, 'temperature_slider')
        self.temperature_slider.valueChanged.connect(self.temperature_slider_value_handle)

        # 获取temperature
        self.temperature = self.ui.findChild(QLabel, 'temperature')

        # 获取humidity_slider
        self.humidity_slider = self.ui.findChild(QSlider, 'humidity_slider')
        self.humidity_slider.valueChanged.connect(self.humidity_slider_value_handle)

        # 获取humidity
        self.humidity = self.ui.findChild(QLabel, 'humidity')

        # 获取当前日期
        self.currentdate = self.ui.findChild(QDateEdit, 'currentdate')
        self.currentdate.setDate(QDate.currentDate())

        # 获取体积
        self.volumn = self.ui.findChild(QSpinBox, 'volumn')

        # 获取狭缝
        self.slit = self.ui.findChild(QDoubleSpinBox, 'slit')

        # 获取样本名称
        self.sample_name = self.ui.findChild(QLineEdit, 'sample_name')

        # 获取分析项目
        self.object_name = self.ui.findChild(QLineEdit, 'object_name')

        # 获取受控号
        self.num_control = self.ui.findChild(QLineEdit, 'num_control')

        # 获取配置ui中的layout
        verticalLayout = self.ui.findChild(QVBoxLayout, 'verticalLayout')

        # 计算数据矩阵大小
        col_cnt = len(self.list_data[0])
        row_cnt = len(self.list_data)

        # 生成数据报表
        self.table_widget = QTableWidget(row_cnt, col_cnt)

        # 设置表头
        self.table_widget.verticalHeader().hide()
        self.table_widget.setHorizontalHeaderLabels(self.header_data)
        font = QFont()
        font.setBold(True)
        self.table_widget.horizontalHeader().setFont(font)

        # 填充表格
        for i in range(row_cnt):
            for j in range(col_cnt):
                item = QTableWidgetItem(str(self.list_data[i][j]))
                self.table_widget.setItem(i, j, item)
        verticalLayout.addWidget(self.table_widget)



        # 关闭ui文件
        uifile.close()
        return self.ui

    def build_dataframe(self):
        


        self.dataframe = pd.DataFrame(self.list_data, columns=self.header_data)

        print(self.dataframe)


    # 处理dial数据
    def dial_value_handle(self):
        dial_value = self.wavelength_dial.value()
        self.wavelength.setText(str(float(dial_value / 10)))

    def temperature_slider_value_handle(self):
        slider1_value = self.temperature_slider.value()
        self.temperature.setText(str(float(slider1_value)))

    def humidity_slider_value_handle(self):
        slider2_value = self.humidity_slider.value()
        self.humidity.setText(str(float(slider2_value)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 设置配置文件和日志
    config = ConfigFactory(config_file='py_jfk.ini').get_config()
    logger = LoggerFactory(config_factory=config).get_logger()
    jfk = JFK(config=config, logger=logger)
    jfk.build_dataframe()
    mainWindow = jfk.load_ui('py_jfk.ui')

    mainWindow.show()
    sys.exit(app.exec_())
