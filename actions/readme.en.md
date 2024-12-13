# Build a translated preset or personalized preset fast and easy!
[![zh-cn](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/uranv/Some-More-Jobs-CHS/blob/main/actions/readme.md)
[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/uranv/Some-More-Jobs-CHS/blob/main/actions/readme.en.md)
The inbuilt preset is implemented using a series of 'XmlExtensions.Action.SetSetting' commands. This structure allows us to conveniently extract all the changes into a CSV file with a more readable format, using 'extract_action.py' in this folder. One could edit this CSV file to make a translated version of the preset, or add some additional changes to the preset. Then the CSV file is used to generate the xml codes to be reinserted into the 'Settings.xml'.

In the case when lots of changes are made, it is recommended to directly edit the 'preset.xlsx'and use the automatically generated 'action.csv' to avoid possible errors.

---
```
  <li Class='XmlExtensions.Action.SetSetting' MayRequire='Ludeon.Rimworld.Ideology'>
    <key>SMJ_Checkbox.PlantCutting</key>
    <value>TRUE</value>
  </li>
```
Every 'XmlExtensions.Action.SetSetting' contains the following 4 parts：【1】'SMJ_Checkbox' for the type of the Setting, 【2】'PlantCutting' the key to change, 【3】'TRUE' changed value, and 【4】MayRequire='Ludeon.Rimworld.Ideology' for the dependency, which is omitted if empty. The generated CSV file has the same order for the four parts. For valid values for each part, please refer to ‘/configs/default.xlsx'.
