# Build a translated preset or personalized preset fast and easy!

The inbuilt preset is implemented using a series of 'XmlExtensions.Action.SetSetting' commands. This structure allows us to conveniently extract all the changes into a CSV file with a more readable format, using 'extract_action.py' in this folder. One could edit this CSV file to make a translated version of the preset, or add some additional changes to the preset. Then the CSV file is used to generate the xml codes to be reinserted into the 'Settings.xml'.

In the case when lots of changes are made, it is recommended to directly edit the 'preset.xlsx'and use the automatically generated 'action.csv' to avoid possible errors.


原作者内置的预设通过'XmlExtensions.Action.SetSetting'完成，因此可以方便地从'Settings.xml'中提取出所有修改内容并整理到一个csv文件中。我们可以直接修改csv中的内容再重新生成<actions>...</actions>部分放回xml配置文件中。当然，如果修改内容很多的话，推荐直接在‘/configs/preset.xlsx'中修改并使用自动生成的actions内容以减少出错的可能。

---

```
  <li Class='XmlExtensions.Action.SetSetting' MayRequire='Ludeon.Rimworld.Ideology'>
    <key>SMJ_Checkbox.PlantCutting</key>
    <value>TRUE</value>
  </li>
```
Every 'XmlExtensions.Action.SetSetting' contains the following 4 parts：【1】'SMJ_Checkbox' for the type of the Setting, 【2】'PlantCutting' the key to change, 【3】'TRUE' changed value, and 【4】MayRequire='Ludeon.Rimworld.Ideology' for the dependency, which is omitted if empty. The generated CSV file has the same order for the four parts. For valid values for each part, please refer to ‘/configs/default.xlsx'.

每个'XmlExtensions.Action.SetSetting'都包涵以下四个部分：【1】'SMJ_Checkbox'指示修改类型，【2】'PlantCutting'为修改的项目，【3】'TRUE'为修改后的值，以及可以缺省的【4】MayRequire='Ludeon.Rimworld.Ideology'表示该项修改的依赖。用于修改的csv文件中四列按此处同样顺序，每一列中可以存在的修改内容请参考‘/configs/default.xlsx'。
