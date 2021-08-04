import sys
from PySide2.QtCore import QFile
from PySide2.QtGui import QFont
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QDial, QLineEdit, QComboBox, \
    QLabel, QSlider

from py_config import ConfigFactory
from py_logging import LoggerFactory


class JFK():
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.get_data()

    def get_data(self):
        # the solvent data ...
        self.data_header = ['序号', '统一编号', '原始编号', '取样量 (g/ml)', '分析结果\n ω(Au)/10-6', '分析结果\n ω(Au)/10-6',
                            '吸光度Abs',
                            '备注']
        # use numbers for numeric data to sort properly
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
        self.data_combobox_method = ['GB/T20899.1-2020', 'GB/T20899.2-2020', 'GB/T20899.3-2020']
        self.data_combobox_type = ['TAS-990F', 'TAS-991F', 'TAS-992F', 'TAS-993F']

    def load_ui(self, uifilename):
        loader = QUiLoader()
        uifile = QFile(uifilename)
        uifile.open(QFile.ReadOnly)
        self.ui = loader.load((uifile))

        # 获取comboBox_method
        self.combobox_method = self.ui.findChild(QComboBox, 'comboBox_method')
        self.combobox_method.addItems(self.data_combobox_method)

        # 获取combobox_type
        self.combobox_type = self.ui.findChild(QComboBox, 'comboBox_type')
        self.combobox_type.addItems(self.data_combobox_type)

        # 获取dail
        self.dial = self.ui.findChild(QDial, 'dial')
        self.dial.valueChanged.connect(self.dial_value_handle)

        # 获取lineEdit_dial
        self.lineEdit_dial = self.ui.findChild(QLineEdit, 'lineEdit_dial')

        # 获取slider1
        self.slider1 = self.ui.findChild(QSlider, 'horizontalSlider1')
        self.slider1.valueChanged.connect(self.slider1_value_handle)

        # 获取label1
        self.label1 = self.ui.findChild(QLabel, 'label1')

        # 获取slider2
        self.slider2 = self.ui.findChild(QSlider, 'horizontalSlider2')
        self.slider2.valueChanged.connect(self.slider2_value_handle)

        # 获取label2
        self.label2 = self.ui.findChild(QLabel, 'label2')

        # 获取配置ui中的layout
        verticalLayout = self.ui.findChild(QVBoxLayout, 'verticalLayout')

        # 计算数据矩阵大小
        col_cnt = len(self.data_list[0])
        row_cnt = len(self.data_list)
        table_widget = QTableWidget(row_cnt, col_cnt)

        # 设置表头
        table_widget.verticalHeader().hide()
        table_widget.setHorizontalHeaderLabels(self.data_header)
        font = QFont()
        font.setBold(True)
        table_widget.horizontalHeader().setFont(font)

        # 填充表格
        for i in range(row_cnt):
            for j in range(col_cnt):
                item = QTableWidgetItem(str(self.data_list[i][j]))
                table_widget.setItem(i, j, item)
        verticalLayout.addWidget(table_widget)

        uifile.close()
        return self.ui

    # 处理dial数据
    def dial_value_handle(self):
        dial_value = self.dial.value()
        self.lineEdit_dial.setText(str(float(dial_value / 10)))

    def slider1_value_handle(self):
        slider1_value = self.slider1.value()
        self.label1.setText(str(float(slider1_value)))

    def slider2_value_handle(self):
        slider2_value = self.slider2.value()
        self.label2.setText(str(float(slider2_value)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 设置配置文件和日志
    config = ConfigFactory(config_file='py_jfk.ini').get_config()
    logger = LoggerFactory(config_factory=config).get_logger()
    jfk = JFK(config=config, logger=logger)
    mainWindow = jfk.load_ui('py_jfk.ui')
    mainWindow.show()
    sys.exit(app.exec_())
