import sys

from PySide2.QtCore import QFile, QDate
from PySide2.QtGui import QFont
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QDial, QLineEdit, QComboBox, \
    QLabel, QSlider, QDateEdit, QSpinBox, QDoubleSpinBox, QPushButton

from py_config import ConfigFactory
from py_logging import LoggerFactory


class JFK():
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.get_data()

    def get_data(self):
        # 数据表的表头
        self.data_header = ['序号', '统一编号', '原始编号', '取样量 (g/ml)', '分析结果\n ω(Au)/1e-6', '分析结果\n ω(Au)/1e-6',
                            '吸光度Abs', '备注']
        # 数据表
        self.data_list = [
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

        # 获取样本名称
        self.sample_name = self.ui.findChild(QLineEdit, 'sample_name')

        # 获取分析项目
        self.object_name = self.ui.findChild(QLineEdit, 'object_name')

        # 获取狭缝
        self.slit = self.ui.findChild(QDoubleSpinBox, 'slit')

        # 获取体积
        self.volumn = self.ui.findChild(QSpinBox, 'volumn')

        # 获取wavelength
        self.wavelength = self.ui.findChild(QLineEdit, 'wavelength')

        # 获取curve
        self.curve = self.ui.findChild(QLineEdit, 'curve')

        # 获取当前日期
        self.currentdate = self.ui.findChild(QDateEdit, 'currentdate')
        self.currentdate.setDate(QDate.currentDate())

        # 获取comboBox_method方法
        self.method_combobox = self.ui.findChild(QComboBox, 'method_combobox')
        self.method_combobox.addItems(self.method_data)

        # 获取combobox_type类型
        self.type_combobox = self.ui.findChild(QComboBox, 'type_combobox')
        self.type_combobox.addItems(self.type_data)

        # 获取dail
        self.wavelength_dial = self.ui.findChild(QDial, 'wavelength_dial')
        self.wavelength_dial.valueChanged.connect(self.dial_value_handle)

        # 获取受控号
        self.num_control = self.ui.findChild(QLineEdit, 'num_control')

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

        # 获取配置ui中的layout
        verticalLayout = self.ui.findChild(QVBoxLayout, 'verticalLayout')

        # 计算数据矩阵大小
        col_cnt = len(self.data_list[0])
        row_cnt = len(self.data_list)

        # 生成数据报表
        self.table_widget = QTableWidget(row_cnt, col_cnt)

        # 设置表头
        self.table_widget.verticalHeader().hide()
        self.table_widget.setHorizontalHeaderLabels(self.data_header)
        font = QFont()
        font.setBold(True)
        self.table_widget.horizontalHeader().setFont(font)

        # 填充表格
        for i in range(row_cnt):
            for j in range(col_cnt):
                item = QTableWidgetItem(str(self.data_list[i][j]))
                self.table_widget.setItem(i, j, item)
        verticalLayout.addWidget(self.table_widget)

        # 获取报表按钮
        self.report_pb = self.ui.findChild(QPushButton, 'report_pb')
        self.report_pb.clicked.connect(self.on_report)

        # 获取保存按钮
        self.save_pb = self.ui.findChild(QPushButton, 'save_pb')
        self.save_pb.clicked.connect(self.on_save)

        # 获取关闭按钮
        self.close_pb = self.ui.findChild(QPushButton, 'close_pb')
        self.close_pb.clicked.connect(self.on_close)

        # 关闭ui文件
        uifile.close()
        return self.ui

    # 生成界面交互数据
    def build_meta_data(self):
        meta_data = {
            'sample_name': self.sample_name.text(),
            'object_name': self.object_name.text(),
            'slit': self.slit.value(),
            'volumn': self.volumn.value(),
            'wavelength': self.wavelength.text(),
            'curve': self.curve.text(),
            'currentdate': self.currentdate.dateTime().toString('yyyy/MM/dd'),
            'method_data': self.method_data[self.method_combobox.currentIndex()],
            'type_data': self.type_data[self.type_combobox.currentIndex()],
            'num_control': self.num_control.text(),
            'temperature': self.temperature.text(),
            'humidity': self.humidity.text()
        }
        list_data = []
        list_data.append(self.data_header)
        rows = []
        for i in range(self.table_widget.rowCount()):
            cols = []
            for j in range(self.table_widget.columnCount()):
                cols.append(self.table_widget.item(i, j).text())
            rows.append(cols)
        list_data.append(rows)
        return meta_data, list_data

    # 处理dial数据
    def dial_value_handle(self):
        dial_value = self.wavelength_dial.value()
        self.wavelength.setText(str(float(dial_value / 10)))

    # 处理template数据
    def temperature_slider_value_handle(self):
        slider1_value = self.temperature_slider.value()
        self.temperature.setText(str(float(slider1_value)))

    # 处理humidity数据
    def humidity_slider_value_handle(self):
        slider2_value = self.humidity_slider.value()
        self.humidity.setText(str(float(slider2_value)))

    # 处理报表
    def on_report(self):
        meta_list, data_list = jfk.build_meta_data()
        self.logger.debug(meta_list)
        self.logger.debug(data_list)

    # 处理保存
    def on_save(self):
        meta_list, data_list = jfk.build_meta_data()
        print(meta_list)
        print(data_list)

    # 处理关闭
    def on_close(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 设置配置文件和日志
    config = ConfigFactory(config_file='py_jfk.ini').get_config()
    logger = LoggerFactory(config_factory=config).get_logger()
    jfk = JFK(config=config, logger=logger)
    mainWindow = jfk.load_ui('py_jfk.ui')
    mainWindow.show()
    sys.exit(app.exec_())
