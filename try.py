import xlwt
import xlrd

# Excel file can be in your local drive
# and if not, specify the exact path
sampleWorkbook = xlrd.open_workbook('old.xlsx')
originalSheet = sampleWorkbook.sheet_by_name('Test')

newWorkbookForTextReplacement = xlwt.Workbook()
newsheetForTextReplacement = newWorkbookForTextReplacement.add_sheet('Test')

replacementTextKeyPairs = {'Apple': 'Kiwi',
						'Oranges': 'Lemons',
						'Grapes': 'Papayas'}

# iterate over the rows of your sheet
# ncols - number of columns in the
# selected sheet, here it is for 'Test' sheet
# nrows - number of rows in the selected
# sheet, here it is for 'Test' sheet
for i in range(originalSheet.nrows):
	print(i)

	# Get the data of each column
	data = [originalSheet.cell_value(i, col)
			for col in range(originalSheet.ncols)]

	for index, value in enumerate(data):

		# If any key present in replacementTextKeyPairs
		# matches with excel column value, replace the
		# column with the value
		if value in replacementTextKeyPairs.keys():
			newsheetForTextReplacement.write(
				i, index, str(replacementTextKeyPairs.get(value)))
		else:
			newsheetForTextReplacement.write(i, index, value)

# Replaced text will be present in the new workbook
# with name sampleexcelwithreplacedtext.xls
newWorkbookForTextReplacement.save('sampleexcelwithreplacedtext.xls')
