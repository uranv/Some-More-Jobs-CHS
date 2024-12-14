import pandas as pd
# paths
csv_file = 'src_action_chs.csv'
excel_file = 'preset.xlsx'
output_file = "modified.xlsx"
csv_list = pd.read_csv(csv_file)
modified_sheets = {}

with pd.ExcelFile(excel_file) as f:
    for i in range( len(csv_list['0']) ):
        sheet_name = csv_list.iat[i, 0]
        # 迭代df
        try:
            df = modified_sheets[sheet_name]
            #print('Exist sheet')
        except KeyError:
            #print('New sheet')
            df = f.parse(sheet_name=sheet_name, header=None)
            # 设置索引
            df.iat[0, 0] = None
            df.columns = df.iloc[0, :]
            df = df.iloc[1:, :]
            df.index = df.iloc[:, 0]
            df = df.iloc[:, 1:]

        # 对应值
        row = csv_list.iat[i, 2]  # 行名称
        col = csv_list.iat[i, 1]  # 列名称
        value = csv_list.iat[i, 3]  # 修改值
        dependency = csv_list.iat[i,4]  # 依赖
        
        # 修改值
        if row in df.index and col in df.columns:
            df.at[row, col] = value
            # print(str(i)+'. 【基本修改】'+sheet_name+': '+col+'.'+row+'='+value)
        elif col == 'SMJ_RadioButtons' and value in df.index and row in df.columns:
            df.at[value, row] = 1
            # print(str(i)+'. 【工作分配】'+sheet_name+': '+row+'-->'+value+'=1')
        elif col in df.index and row in df.columns:
            df.at[col, row] = value
            # print(str(i)+'. 【单项修改】'+sheet_name+': '+col+'.'+row+'='+value)
        else:
            print(f"{i}. <警告> 在 {sheet_name} 中未找到行 {row} 或列 {col}")
        
        # 修改依赖
        if dependency != '0':
            if sheet_name == 'Basic' and row in df.index and 'MayRequire' in df.columns:
                df.at[row, 'MayRequire'] = dependency
                # print(str(i)+'. 【基本依赖】'+sheet_name+': MayRequire.'+row+'='+dependency)
            elif  'MayRequire' in df.index and row in df.columns:
                df.at['MayRequire', row] = dependency
                # print(str(i)+'. 【单项依赖】'+sheet_name+': MayRequire.'+col+'='+dependency)
            elif 'MayRequire' not in df.index and 'MayRequire' not in df.columns:
                print(f"{i}. <警告> 在 {sheet_name} 中未找到 MayRequire 位置")
        else:
            continue
            # print(f"{i}. 依赖未改变")
            
        # 记录修改
        modified_sheets[sheet_name] = df
        
# 输出
with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
    for sheet, modified_df in modified_sheets.items():
        modified_df.to_excel(writer, sheet_name=sheet, index=True)
                
print(f"所有修改已保存到 {output_file}")
