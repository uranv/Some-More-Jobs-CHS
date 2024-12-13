# 快速修改生成简单预设
[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/uranv/Some-More-Jobs-CHS/blob/main/actions/readme.en.md)

原作者内置的预设通过'XmlExtensions.Action.SetSetting'完成，因此可以方便地从'Settings.xml'中提取出所有修改内容并整理到一个csv文件中。我们可以直接修改csv中的内容再重新生成<actions>...</actions>部分放回xml配置文件中。当然，如果修改内容很多的话，推荐直接在‘/configs/preset.xlsx'中修改并使用自动生成的actions内容以减少出错的可能。

---
```
  <li Class='XmlExtensions.Action.SetSetting' MayRequire='Ludeon.Rimworld.Ideology'>
    <key>SMJ_Checkbox.PlantCutting</key>
    <value>TRUE</value>
  </li>
```
每个'XmlExtensions.Action.SetSetting'都包涵以下四个部分：【1】'SMJ_Checkbox'指示修改类型，【2】'PlantCutting'为修改的项目，【3】'TRUE'为修改后的值，以及可以缺省的【4】MayRequire='Ludeon.Rimworld.Ideology'表示该项修改的依赖。用于修改的csv文件中四列按此处同样顺序，每一列中可以存在的修改内容请参考‘/configs/default.xlsx'。
