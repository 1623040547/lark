from dataclasses import dataclass
from spread_sheet.stream.api_manager import ApiManager
from spread_sheet.stream.unit_sort import SheetUnitSort


@dataclass
class SheetCrossColor:
    offset_x: int
    offset_y: int
    width: int
    height: int
    color: str


@dataclass
class SheetGlobalStyle:
    cross_colors: list[SheetCrossColor]
    sort: SheetUnitSort
    table_freeze: list[str]
    froze_column: bool
    froze_row: bool

    def index_json(self) -> dict:
        return self.sort.layout.load.index_json


class GlobalStyle:
    def __init__(self, sorts: list[SheetUnitSort]):
        self.sorts = sorts
        self.global_style = []
        for sort in sorts:
            self.global_style.append(
                SheetGlobalStyle(
                    cross_colors=[],
                    table_freeze=[],
                    sort=sort,
                    froze_column=False,
                    froze_row=False,
                )
            )
        self.set_unit_cross_color()
        self.set_global_cross_color()
        self.set_global_froze()

    def set_unit_cross_color(self):
        for global_style in self.global_style:
            sort = global_style.sort
            width = len(sort.layout.heads_name)
            offset_x = 0
            offset_y = 1
            ram = 0
            for mark in sort.unit_mark:
                if mark != 0:
                    ram = (ram + 1) % 2
                    height = mark
                    global_style.cross_colors.append(
                        SheetCrossColor(
                            offset_x=offset_x,
                            offset_y=offset_y,
                            width=width,
                            height=height,
                            color=ApiManager.ram_color(ram)
                        )
                    )
                offset_y += 1

    def set_global_cross_color(self):
        for global_style in self.global_style:
            sort = global_style.sort
            ram = 2
            for combine in sort.sheet_combines:
                if combine.is_global:
                    ram += 1
                    global_style.cross_colors.append(
                        SheetCrossColor(
                            offset_x=combine.offset_x,
                            offset_y=combine.offset_y,
                            width=combine.width,
                            height=combine.height,
                            color=ApiManager.ram_color(ram)
                        )
                    )

    def set_global_froze(self):
        for global_style in self.global_style:
            try:
                global_style.froze_column = \
                    global_style.index_json()['global_style']['froze_column']
            except:
                pass
            try:
                global_style.froze_row = global_style.index_json()['global_style'][
                    'froze_row']
            except:
                pass

    def set_table_freeze(self):
        for global_style in self.global_style:
            try:
                global_style.table_freeze = global_style.index_json()['freeze']
            except:
                pass
