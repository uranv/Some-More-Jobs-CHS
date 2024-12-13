# 生成自定义xml预设

$\qquad$使用此文件夹内的‘actions.py’生成方便编辑的csv文件，再从csv文件生成可插入'Settings.xml'的预设。也可以通过修改此文件夹内的’preset.xlsx‘表格文件，直观地完成所有设置，再从修改后的‘preset.xlsx’生成修改的csv并进一步生成可插入‘Settings.xml’的预设。

```shell
usage: actions.py [-h] [-o OUTPUT] [-d DEFAULT] mode input

positional arguments:
  mode                  模式: 1. 从 XML 生成 CSV | 2. 从 CSV 生成 XML | 3. 从 XLSX 生成 CSV
  input                 输入文件路径

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        输出文件路径
  -d DEFAULT, --default DEFAULT
                        default.xlsx 文件路径，仅模式 3 使用
```

## 'actions.py'包含以下三种模式：

#### 1. 从 XML 生成 CSV

从XML文件中提取用于定义预设的'XmlExtensions.Action.SetSetting'，将其修改内容输出到CSV文件中。一个示例输入为：

```shell
python 'actions.py' 1 'Settings.xml' -o 'actions_from_xml.csv'
```

其中" -o 'actions_from_xml.csv' "可省略，此时程序将自动在'C:\\Users\\username'目录生成名为'actions_from_xml.csv'的输出文件。如果选择指定输出路径，请务必包含到具体文件名和后缀。

#### 2. 从 CSV 生成 XML

从CSV文件生成XML代码，一个示例输入为：

```shell
python 'actions.py' 2 'actions.csv'
```

如果不指定输出路径。程序将自动在'C:\\Users\\username'目录生成名为'actions_from_csv.xml'的输出文件。



生成的文件可以插入'./RimWorld/Mods/some more jobs chs/1.5/Defs/Settings.xml'中，具体位置为下列代码框中注释之间，使用时可以直接在文本中查找注释内容快速到达位置。

><!--以下为作者预设-->
>
><!--以下为预设1-->
>
><!--以下为预设2-->

```xml
<li Class="XmlExtensions.Setting.ApplyActions">
  <label>使用模组作者预设(需先重置设置)</label>
<!--以下为作者预设-->

<!--以上为作者预设-->
</li>
```

```xml
<li Class="XmlExtensions.Setting.SplitColumn">
  <leftCol>
    <li Class="XmlExtensions.Setting.ApplyActions">
      <label>自定义预设1</label>
<!--以下为预设1-->

<!--以上为预设1-->
    </li>
  </leftCol>
  <rightCol>
    <li Class="XmlExtensions.Setting.ApplyActions">
      <label>自定义预设2</label>
<!--以下为预设2-->

<!--以上为预设2-->
    </li>
  </rightCol>
</li>
```

将程序生成代码正确地插入到'Settings.xml'后，即可在游戏中通过对应按键一键应用自己的设定。当然，每次应用新的设置都需要先**重置所有设置**，并且应用后需要**重启游戏**来让新的设置生效。

<img src="D:\Documents\GitHub\Some-More-Jobs-CHS\codes\Preview.jpg" alt="Preview" style="zoom:50%;" />

#### 3. 从 XLSX 生成 CSV

通过修改‘preset.xlsx'，也可以生成记录了所有修改的csv文件，此时生成的csv文件便可以作为**2. 从 CSV 生成 XML**中的输入，进一步生成xml代码插入模组设置。一个示例输入为：

```
python 'actions.py' 3 'preset.xlsx' -d 'default.xlsx'
```

值得注意的是，虽然[-d DEFAULT]是可选参数，但是在模式3中程序要求此参数才能正确工作，因此**使用模式3时必须包含'default.xlsx'的路径**。如果不指定输出路径。程序将自动在'C:\\Users\\username'目录生成名为'actions_from_xlsx.csv'的输出文件。



关于xlsx文件内的修改内容，将在下一小节与xml格式一同说明。

## 修改内容说明

从XML文件中提取用于定义预设的'XmlExtensions.Action.SetSetting'，将其修改内容输出到中。程序在'Settings.xml'中提取所有'XmlExtensions.Action.SetSetting'操作，一个典型的‘Action.SetSetting’具有如下结构：

```xml
<li Class='XmlExtensions.Action.SetSetting' MayRequire='Ludeon.Rimworld.Ideology'>
  <key>SMJ_Checkbox.PlantCutting</key>
  <value>TRUE</value>
</li>
```

其中key，value和MayRequire(可以缺省，此时记录为0)被提取并录入到输出csv中，输出数据被查分为四部分：

1. SMJ_Checkbox记录此项定义的类型，其他可能值包含：
   + SMJ_Textbox_labelShort：工作名称，显示在底部菜单的工作栏中。
   + SMJ_Textbox_pawnLabel，SMJ_Textbox_gerundLabel，SMJ_Textbox_verb：在其他位置显示的工作名称，一般可直接设定为与labelShort相同值；需要去分时，pawnLabel为职业名称(ex.教师)，SMJ_Textbox_gerundLabel为进行时的动作(ex.正在教授/教授)，SMJ_Textbox_verb为动作(ex.教授)。
   + SMJ_Textbox_description：工作描述，鼠标放置于工作界面内labelShort的展开说明见面中的内容。
   + SMJ_Numeric_naturalPriority：工作的默认优先级，在工作见界面内从左到右以此降低，合法值为0~9999。
   + SMJ_Checkbox_alwaysStartActive：判断是否启用新增加的工作(即key为SMJ_...的工作)，默认为布尔值True/False，表格内接受1/0。特别地，-1表示该项目不能更改。
   + SMJ_RadioButtons：用于设定某一工作项目的分配情况，合法值为各个工作key，例如Doctor/SMJ_Doctor1/etc.。表格内单项工作按原版分配至的工作，分布在对应命名的sheet中，1表示该项工作单项(列标题)被分配至该工作(行标题)。
   + SMJ_Numeric_priorityInType：表示对应工作单项的优先级。
2. PlantCutting记录此项定义的内容；此处可以是工作，即表格Basic中第一例Key的内容，也可以是单项工作，即其他sheet第一行的内容。
3. \<value\>TRUE\</value\>记录此项定义改变后的值，每种设定的合法值如第一条中说明。
4. MayRequire='Ludeon.Rimworld.Ideology'描述此设定依赖的dlc或其他mod，当且仅当检测到启用对应模组时这项设定才会被应用。

#### 示例文件

'actions.py'生成和读取的csv文件中便是由上述四种数据按同样顺序构成组成的。示例文件包含本目录下的：src_action.xml(原模组Settings.xml的预设部分)；程序生成的src_action.csv；包含本人翻译的src_action_chs.csv；以及程序生成的src_action_chs.xml。



default.xlsx记录了模组中的**默认设定，请勿修改其内容**。自定义设置时，请**仅修改preset.xlsx中未锁定格子的内容**。若出于任何原因需要修改被保护部分，密码为123。



