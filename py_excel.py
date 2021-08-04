import xlrd
import xlwt

# Excel报表处理
from py_config import ConfigFactory
from py_logging import LoggerFactory


class ExcelHandle:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.template = config.get('data', 'template')
        self.output = config.get('data', 'output')
        # 数据表的表头
        self.data_header = ['序号', '统一编号', '原始编号', '取样量 (g/ml)', '分析结果\n ω(Au)/10-6', '分析结果\n ω(Au)/10-6',
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

    # 数据替换处理函数
    def replace_handler(self, replacement: dict):

        # 读取excel源数据文件
        workbook = xlrd.open_workbook(self.template)
        sheet = workbook.sheet_by_index(0)

        # 创建新excel数据文件
        new_workbook = xlwt.Workbook()
        new_sheet = new_workbook.add_sheet('report')

        # sheet数据历遍
        for i in range(sheet.nrows):
            # 获取每个cell对象数据
            data = [sheet.cell_value(i, col) for col in range(sheet.ncols)]
            for index, value in enumerate(data):
                # 如果每个cell的value包含替换内容
                if value in replacement.keys():
                    # 替换数据
                    new_sheet.write(i, index, str(replacement.get(value)))
                else:
                    new_sheet.write(i, index, value)
        # 写入输出文件
        new_workbook.save(self.output)
        self.logger.info('The output file is %s' % self.output)

    # excel文件定位写入处理
    def inject_handler(self, data):
        # 合并数据集合
        # data = []
        # data.append(self.data_header)
        # for row in self.data_list:
        #     data.append(row)
        self.logger.info(data)

        # 创建新excel数据文件
        new_workbook = xlwt.Workbook()
        new_sheet = new_workbook.add_sheet('report')

        # 历遍数据并写入sheet
        for i, row in enumerate(data):
            for j, col in enumerate(row):
                new_sheet.write(i + 10, j, data[i][j])

        new_workbook.save(self.output)
        self.logger.info('The output file is %s' % self.output)


if __name__ == '__main__':
    # 设置配置文件和日志
    config = ConfigFactory(config_file='py_jfk.ini').get_config()
    logger = LoggerFactory(config_factory=config).get_logger()
    excel_handle = ExcelHandle(config=config, logger=logger)
    excel_handle.inject_handler()
    # replacement = {'aa': 'aa123', 'bb': 'bb123', 'cc': 'cc12345'}
    # excel_handle.replace_handler(replacement)
