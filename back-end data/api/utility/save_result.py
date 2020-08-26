import xlsxwriter

def saveExcel(result, file_path):
    workbook = xlsxwriter.Workbook(file_path)
    for sheet_name in result.keys():
        data = result[sheet_name]
        worksheet = workbook.add_worksheet(sheet_name)
        if len(data) == 0:
            continue
        for i in range(len(data)):
            for j in range(len(data[0])):
                worksheet.write(i, j, data[i][j])
    workbook.close()
    print(file_path, 'saved!')