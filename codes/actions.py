# 作者: uranv
# 日期: 2024-12-13
# 发布于 https://github.com/uranv/Some-More-Jobs-CHS
#---------------------------------------------------
# 更新1 2024-12-14 15:00
# 配合 xlsx: inType 补充了 mayRequire
#---------------------------------------------------
import pandas as pd
import numpy as np
import codecs
import xml.etree.ElementTree as ET
import argparse
import os

# 从xlsx文件生成变动列表
def ChangeList(input_default, input_preset, output_csv = 'actions_from_xlsx.csv'):
    # 获取职业列表    Get sheet list
    with pd.ExcelFile(input_default) as f:
        sheet_list = f.sheet_names
    # 基础改动    Change in basic
    default = pd.read_excel(input_default, sheet_name=sheet_list[0], header=None).fillna(0)
    preset = pd.read_excel(input_preset, sheet_name=sheet_list[0], header=None).fillna(0)
    diff = (preset != default)
    different_indices = diff[diff].stack().index.tolist()
    # 生成新的CSV    Generate new CSV file
    with codecs.open(output_csv,"w", "utf-8-sig") as f:
        for item in different_indices:
            # change type | key | value | mayRequire
            if item[1] in [7,8]:
                if preset.iat[item] == 1:
                    f.write( str(preset.iat[0,item[1]])+','\
                        +str(preset.iat[item[0],0])+',True,'\
                        +str(preset.iat[item[0],9])+'\n')
                elif preset.iat[item] == 0:
                    f.write( str(preset.iat[0,item[1]])+','\
                        +str(preset.iat[item[0],0])+',False,'\
                        +str(preset.iat[item[0],9])+'\n')
            else:
                f.write( str(preset.iat[0,item[1]])+','\
                    +str(preset.iat[item[0],0])+','\
                    +str(preset.iat[item])+','\
                    +str(preset.iat[item[0],9])+'\n')
    # 工作分配改动    Change in Type
    for sheet in sheet_list[1:]:
        default = pd.read_excel(input_default, sheet_name=sheet, header=None).fillna(0)
        preset = pd.read_excel(input_preset, sheet_name=sheet, header=None).fillna(0)
        # 检查配置有效性    Check validity
        check = np.sum(np.array(preset)[3:,1:], axis=0)
        if np.where(check == 0)[0].size != 0:
            print( str(sheet)+'中有存在未分配工作类型！')
            return
        if np.where(check >1 )[0].size != 0:
            print( str(sheet)+'中有存在重复分配工作类型！')
            return
        # 寻找修改    Find changes
        diff = (preset != default)
        different_indices = diff[diff].stack().index.tolist()
        print(sheet, different_indices)
        # 继续CSV    Add to current CSV file
        with codecs.open(output_csv,"a", "utf-8-sig") as f:
            for item in different_indices:
                # 改变 priorityInType
                if item[0]==2: 
                    # SMJ_Numeric_priorityInType | workType | value | mayRequire
                    f.write( str(preset.iat[1,0])+','\
                            +str(preset.iat[0,item[1]])+','\
                            +str(preset.iat[item])+','\
                            +str(0)+'\n')
                # 改变 workType 分配
                elif item[0]>2 and preset.iat[item]==1: 
                    # SMJ_RadioButtons | workType | job key assigned | mayRequire
                    f.write( str(preset.iat[0,0])+','\
                            +str(preset.iat[0,item[1]])+','\
                            +str(preset.iat[item[0],0])+','\
                            +str(preset.iat[1,item[1]])+'\n')
    return

# 从变动列表生成xml actions
def BuildXml(input_csv, output_xml='actions_from_csv.xml'):
    df = pd.read_csv(input_csv)
    with codecs.open(output_xml,"w", "utf-8-sig") as f:
        f.write("<actions>\n")
        for i in range(df.shape[0]):
            if df.iat[i,3]=='0':
                f.write("  <li Class='XmlExtensions.Action.SetSetting'>\n")        
            else:
                f.write("  <li Class='XmlExtensions.Action.SetSetting' MayRequire='"+df.iat[i,3]+"'>\n")
            f.write("    <key>"+df.iat[i,0]+"."+df.iat[i,1]+"</key>\n    <value>"+df.iat[i,2]+"</value>\n  </li>\n")
        f.write("</actions>")
    return

# 从xml文件提取变动列表csv
def ExtractXml(input_xml, output_csv = 'actions_from_xml.csv'):
    results = []
    tree = ET.parse(input_xml)
    root = tree.getroot()
    for li in root.findall(".//li[@Class='XmlExtensions.Action.SetSetting']"):
        may_require = li.get("MayRequire", "0") 
        key_elem = li.find("key")
        value_elem = li.find("value")
        if key_elem is not None and key_elem.text and value_elem is not None and value_elem.text:
            key_text = key_elem.text.strip()
            value_text = value_elem.text.strip()
            key_parts = key_text.split(".", 1)
            if len(key_parts) == 2:
                key_part1, key_part2 = key_parts
                results.append([key_part1, key_part2, value_text, may_require])
    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False)
    return

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'mode',
        type=int,
        help='模式: 1. 从 XML 生成 CSV | 2. 从 CSV 生成 XML | 3. 从 XLSX 生成 CSV'
    )
    parser.add_argument('input', type=str, help='输入文件路径')
    parser.add_argument('-o', '--output', type=str, help='输出文件路径')
    parser.add_argument('-d', '--default', type=str, help='default.xlsx 文件路径，仅模式 3 使用')

    args = parser.parse_args()

    input_path = args.input
    output_path = args.output
    default_path = args.default

    if output_path is None:
        print('输出路径为空，输出文件将位于 C:\\Users\\username 目录下')
    if args.mode == 1:
        if os.path.splitext(input_path)[1]!='.xml':
            print("输入文件格式错误！(需要xml)")
        elif output_path:
                ExtractXml(input_path, output_path)
        else:
                ExtractXml(input_path)
    elif args.mode == 2:
        if os.path.splitext(input_path)[1]!='.csv':
            print("输入文件格式错误！(需要csv)")
        elif output_path:
            BuildXml(input_path, output_path)
        else:
            BuildXml(input_path)
    elif args.mode == 3:
        if default_path is None:
            print('需要输入 default.xlsx 路径')
        elif os.path.splitext(input_path)[1]!='.xlsx' or os.path.splitext(default_path)[1]!='.xlsx':
            print("输入文件格式错误！(需要xlsx)")
        else:
            if output_path:
                ChangeList(default_path, input_path, output_path)
            else:
                ChangeList(default_path, input_path)

if __name__ == "__main__":
    main()
