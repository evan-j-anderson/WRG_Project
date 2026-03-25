
import pandas as pd
import numpy as np
import json

codes = pd.read_csv('AvenueCodes.csv')
# print(codes)

mstr_code_list = codes['Master'].tolist()
# print(mstr_code_list)
dct = {}
for mstr_code in mstr_code_list:
    dct[mstr_code] = {}
    dct[mstr_code]['Master Code'] = mstr_code
    # now we just need the other codes and the sum
    #identify wherethe master code is
    input_lst = []
    input_nums = [1,2,3]
    # find the row where 'Master' equals the current master code
    df = codes[codes['Master'] == mstr_code]
    if df.empty:
        # no matching row — use None placeholders
        input_lst = [None for _ in input_nums]
    else:
        row = df.iloc[0]
        for num in input_nums:
            col = 'Input ' + str(num)
            val = row.get(col, None)
            # convert NaN to None for cleanliness
            if pd.isna(val):
                val = None
            input_lst.append(val)
    dct[mstr_code]['Input Codes'] = input_lst
# print(dct)

#read income statement in
df = pd.read_excel('/workspaces/WRG_Project/Income_Statement_avenue24_Accrual (13).xlsx', sheet_name = 'Report1', header= None)
df.columns = ['ID', 'Category', 'PtD', 'Ptd%', 'YtD', 'YtD%']
df = df.iloc[4:,]
df = df.dropna(subset=['ID'])
income_data = df
# print(income_data)

#loop through master codes and sum up PtD values
for mstr_code in dct:
    input_codes = dct[mstr_code]['Input Codes']
    total = 0
    for code in input_codes:
        if code is not None:
            # find the row where 'ID' equals the current input code
            row = income_data[income_data['ID'] == code]
            if not row.empty:
                val = row.iloc[0]['PtD']
                if pd.notna(val):
                    total += val
    dct[mstr_code]['PtD Total'] = total

# print(dct)
with open('output.json', 'w') as f:
    json.dump(dct, f, indent=4)

finaldf = pd.DataFrame.from_dict(dct, orient='index')
finaldf = finaldf.reset_index(drop=True).drop(columns=['Input Codes'])
print(finaldf)
finaldf.to_csv('output.csv', index=False)