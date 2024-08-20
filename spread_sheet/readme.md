# Lark - Spread Sheet

对于飞书电子表格API的一种使用方式,将Json格式的数据展示到飞书电子表格之上，
为了完整运行此项目，你需要完成如下一些配置（以下用python表示json文件,方便注解）：

- 文档中用到的宏定义     
  - INDEX_KEY=index
  - DATA_KEY=data
  - TEST_KEY=test
  - EVENTS_INDEX_KEY=events_index
  - EVENTS_KEY=events
  - IS_INCREMENT=1


- 配置`spread_sheet/config.json`

```python
json = {
    # 提供注册飞书应用后提供的AppId
    "app_id": "",
    # 提供注册飞书应用后提供的AppSecret
    "app_secret": "",
    # 提供索引文件的路径（后续解释）
    "index_path": "./INDEX_KEY",
    # 提供数据文件的路径（后续解释）
    "data_path": "./DATA_KEY",
    # 数据文件与索引文件的后缀名
    "file_suffix": ".json",
    # 对于需要将数据转换到电子表格的集合进行定义
    "table": [
      {
        # 电子表格的table_id(具体见文档中sheet_id：https://open.feishu.cn/document/server-docs/docs/sheets-v3/overview)
        "table_id": "",
        # 数据文件所在文件夹名称（建议填写为表名称或项目名称）
        "name": "TEST_KEY",
        # 一个索引文件对应一类数据文件
        "loads": {
          # 索引文件对应数据文件，即将数据文件按索引文件规定格式转换为电子表格
          "EVENTS_INDEX_KEY": "EVENTS_KEY",
        }
      }
    ]
  }
```

- 在`spread_sheet/data/TEST_KEY/EVENTS_KEY.json`中存放你的数据

  - 方式一：此方式在电子表格中生成一张表单,该表单的名称是`INDEX_KEY.json`中的`sheet_name`的`value`值
  ```python
  json = {
    "data":[
      {
          "event_name": "你好",
          "event_desc": "世界",
          "param_list": [
              {
                  "param_name": "你好",
                  "param_type": "String",
                  "param_desc": "这是一个'你好'的字符串",
                  "param_must_write": "不是",
                  "param_check": ""
              }
          ],
          "event_trigger": "",
          "locations": "",
          "panels": "",
          "event_plate": ""    
      }
    ] 
  }
  ```
  - 方式二：此方式可以在电子表格中生成多张表单,这些表单的名称通过以下方法找到:    
    将`INDEX_KEY.json`中的`sheet_name`的`value`值取出(假设为`version`)，
    在数据文件中找寻最外层key值为`version`的键值对，该键值对的`value`值为表单的名称
  ```python
  json = [
    {
    "version": "0.0.1",
    "data": [{
          "event_name": "你好",
          "event_desc": "世界",
          "param_list": [
              {
                  "param_name": "你好",
                  "param_type": "String",
                  "param_desc": "这是一个'你好'的字符串",
                  "param_must_write": "不是",
                  "param_check": ""
              }
          ],
          "event_trigger": "",
          "locations": "",
          "panels": "",
          "event_plate": ""    
       }]
    }
  ]  
  ```
- 定义你所需要的索引文件（表格样式）

此处以 `spread_sheet/index/EVENTS_INDEX_KEY.json`为例：
```python
json = {
  # 电子表格中表单的名称
  # 此处可以直接指定表单的名称，此时数据结构应采用`方式一`
  # 也可以指定表单名称所在的`key`值，此时数据结构应采用`方式二`
  "sheet_name": "",
  # 对电子表格表头的定义：
  # 这里的`key`值对应数据文件中json的key值，
  # 这里的`value`值对应电子表格中的第一行各列名，
  # 请注意这里的`param_list`，它表明了一个数据列表该如何表达，
  # 但我们不允许数据列表的嵌套
  "data_head": {
    "event_name": "事件名",
    "event_desc": "事件描述",
    "param_list": {
      "param_name": "参数名",
      "param_type": "参数数据类型",
      "param_desc": "参数描述",
      "param_must_write": "是否必填",
      "param_check": "参数类型检查"
    },
    "event_trigger": "事件触发时机",
    "locations": "事件触发位置",
    "panels": "打点平台",
    "event_plate": "功能模块"
  },
  # 数据单元样式,数据单元只在数据文件中，
  # json数据中key值为`data`下的各列表子项,
  # 此处操作范围不会超出数据单元在电子表格中占据的长宽
  "unit_style": {
    # 合并纵向单元格，因为允许`param_list`这样的单元内列表存在，
    # 一个数据单元可以有多列，但其中部分列数据可能只有一行，
    # 此处允许对它们进行合并操作
    "combine": [
      "event_name",
      "event_desc",
      "locations",
      "panels"
    ],
    # 将某列设置为下拉列表，此时会统计数据文件中该列的所有值，
    # 为了美观，数据不为空的单元格才会设置下拉列表
    "pull_list": [
      "param_type",
      "panels",
      "locations",
      "param_must_write"
    ],
    # 相同引用
    # 获取其它数据文件中的某些数据列的所有数据
    # 与当前文件中的指定列中每个单元格的数据进行比较，
    # 若数据相同，则引用此单元格
    "cite": {
      "param_name": [
        "@param_index:param_name",
        "@union_param_index:param_name"
      ]
    },
    # 引用重定向，将在`param_name`上生效的超链接转移到`param_type`上
    # 而判断是否具备引用关系时，仍使用`param_name`进行判断
    "cite_redirect": {
      "param_name": "param_type"
    }
  },
  # 全局样式
  "global_style": {
    # 给布局在表单中数据单元设置交替的两种背景色
    "cross_color": True,
    # 冻结首行
    "froze_row": True,
    # 冻结首列
    "froze_column": True,
    # 根据取值合并某一数据列
    "combine": [
      "event_plate"
    ],
    # 若以下表单名称已存在，则不再对其进行创建
    "freeze": [
      "0.0.0"
    ]
  }
}

```

- 运行main.dart
```shell

  # 
  # IS_INCREMENT: 电子表格中已存在的表单不会清空重建，其它情况下遇到冲突表单会清空后重建
  # path/to/python3 path/to/spread_sheet/main.py TEST_KEY 1 
  path/to/python3 path/to/spread_sheet/main.py TEST_KEY IS_INCREMENT 
```

<br>
<br>
<br>
<br>
<br>
<br>




