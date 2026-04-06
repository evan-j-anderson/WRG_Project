
import pandas as pd
import json
import os

def process_file(excel_file_path):
    # Load codes file (must be in same folder as app)
    codes = pd.read_csv('AvenueCodes.csv')

    mstr_code_list = codes['Master'].tolist()
    dct = {}

    for mstr_code in mstr_code_list:
        dct[mstr_code] = {}
        dct[mstr_code]['Master Code'] = mstr_code

        input_nums = [1,2,3]
        df = codes[codes['Master'] == mstr_code]

        input_lst = []
        if df.empty:
            input_lst = [None for _ in input_nums]
        else:
            row = df.iloc[0]
            for num in input_nums:
                col = 'Input ' + str(num)
                val = row.get(col, None)
                if pd.isna(val):
                    val = None
                input_lst.append(val)

        dct[mstr_code]['Input Codes'] = input_lst

    # Load uploaded Excel file
    df = pd.read_excel(excel_file_path, sheet_name='Report1', header=None)
    df.columns = ['ID', 'Category', 'PtD', 'Ptd%', 'YtD', 'YtD%']
    df = df.iloc[4:,]
    df = df.dropna(subset=['ID'])
    income_data = df

    # Calculate totals
    for mstr_code in dct:
        input_codes = dct[mstr_code]['Input Codes']
        total = 0
        for code in input_codes:
            if code is not None:
                row = income_data[income_data['ID'] == code]
                if not row.empty:
                    val = row.iloc[0]['PtD']
                    if pd.notna(val):
                        total += val
        dct[mstr_code]['PtD Total'] = total

    # Save outputs
    base = os.path.splitext(excel_file_path)[0]
    json_path = base + '_output.json'
    csv_path = base + '_output.csv'

    with open(json_path, 'w') as f:
        json.dump(dct, f, indent=4)

    finaldf = pd.DataFrame.from_dict(dct, orient='index')
    finaldf = finaldf.reset_index(drop=True).drop(columns=['Input Codes'])
    finaldf.to_csv(csv_path, index=False)

    return csv_path