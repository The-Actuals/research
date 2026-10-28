import sys, openpyxl
for f in sys.argv[1:]:
    wb = openpyxl.load_workbook(f, read_only=True)
    print('=====', f, wb.sheetnames)
    for ws in wb.worksheets:
        rows = list(ws.iter_rows(values_only=True))
        print('--', ws.title, len(rows), 'rows')
        for r in rows[:4]: print('  ', [c for c in r[:14]])
