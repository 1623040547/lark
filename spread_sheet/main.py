import sys

from spread_sheet.stream.config_reader import ConfigReader
from spread_sheet.stream.global_style import GlobalStyle
from spread_sheet.stream.mapping import SheetMapping
from spread_sheet.stream.unit_layout import UnitLayout
from spread_sheet.stream.unit_sort import SheetUnitSort, UnitSort
from spread_sheet.stream.unit_style import UnitStyle

# test_config_reader()
is_increment: bool = str(sys.argv[2]) == str(1)
sel_table_name: str = sys.argv[1]

# 读取配置
ConfigReader.read_config()
sorts: list[SheetUnitSort] = []
# 数据布局
for load in ConfigReader.loads:
    layout = UnitLayout(load)
    for lay in layout.layouts:
        sort = UnitSort(lay)
        sorts.append(sort.sheet_sort)
# 数据样式
UnitStyle(sorts=sorts)
g = GlobalStyle(sorts=sorts)
# API映射
SheetMapping(styles=g.global_style)
