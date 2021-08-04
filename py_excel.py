import xlrd
import xlwt

# Excel报表处理
from py_config import ConfigFactory
from py_logging import LoggerFactory


class ExcelHandle:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    # 数据处理函数
    def handler(self, replacement: dict):
        # read Excel file and sheet by name
        workbook = xlrd.open_workbook('source.xls')
        sheet = workbook.sheet_by_name('test')

        new_workbook = xlwt.Workbook()
        new_sheet = new_workbook.add_sheet('test2')

        for i in range(sheet.nrows):
            print(i)
            data = [sheet.cell_value(i, col) for col in range(sheet.ncols)]
            for index, value in enumerate(data):
                if value in replacement.keys():
                    new_sheet.write(i, index, str(replacement.get(value)))
                else:
                    new_sheet.write(i, index, value)
        new_workbook.save('example.xls')


if __name__ == '__main__':
    # 设置配置文件和日志
    config = ConfigFactory(config_file='py_jfk.ini').get_config()
    logger = LoggerFactory(config_factory=config).get_logger()
    excel_handle = ExcelHandle(config=config, logger=logger)
    replacement = {'abcd': 'defc'}
    excel_handle.handler(replacement)
