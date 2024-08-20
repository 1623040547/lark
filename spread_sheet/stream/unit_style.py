from dataclasses import dataclass

from spread_sheet.stream.api_manager import ApiManager
from spread_sheet.stream.unit_sort import SheetUnitSort


@dataclass
class CiteColumn:
    table_id: str
    sheet_id: str
    column: int
    matrix: list

    def link_style(self, data, text):
        """
        :param data: 用于比较是否绑定超链接的数据
        :param text: 用于绑定超链接的文本
        :return: 超链接样式
        """
        if data is None or str(data) == "":
            return None
        sub_target = None
        for i in range(len(self.matrix)):
            if self.matrix[i][self.column] == data:
                return ApiManager.link_style(
                    text=str(text),
                    table_id=self.table_id,
                    sheet_id=self.sheet_id,
                    column=self.column,
                    row=i)
            elif self.matrix[i][self.column] != "" and str(data).__contains__(self.matrix[i][self.column]):
                sub_target = ApiManager.link_style(
                    text=str(text),
                    table_id=self.table_id,
                    sheet_id=self.sheet_id,
                    column=self.column,
                    row=i)
        return sub_target


class UnitStyle:
    def __init__(self, sorts: list[SheetUnitSort]):
        self.sorts = sorts
        self.set_pull_list_style()
        self.set_link_style()

    def set_pull_list_style(self):
        for sort in self.sorts:
            matrix = sort.layout.matrix
            pulls = sort.sheet_pulls
            for pull in pulls:
                x = pull.offset_x
                y = pull.offset_y
                for i in range(pull.height):
                    row = y + i
                    matrix[row][x] = ApiManager.pull_list_style(matrix[row][x])

    def set_link_style(self):
        for sort in self.sorts:
            try:
                param_cite = sort.layout.load.index_json['unit_style']['cite']
            except:
                continue
            param_cite_redirect = {}
            try:
                param_cite_redirect = sort.layout.load.index_json['unit_style']['cite_redirect']
            except:
                pass
            for key, value in param_cite.items():
                cites = self.find_link_column(value)
                index = sort.layout.head_index(key)
                for i in range(len(sort.layout.matrix[1:])):
                    i = i + 1
                    for cite in cites:
                        redirect_index = index
                        if param_cite_redirect.keys().__contains__(key):
                            redirect_index = sort.layout.head_index(param_cite_redirect[key])
                        link = cite.link_style(sort.layout.matrix[i][index], sort.layout.matrix[i][redirect_index])
                        if link is not None:
                            sort.layout.matrix[i][redirect_index] = link
                            break

    # index_name, head_name
    def find_link_column(self, cite_params: list[str]) -> list[CiteColumn]:
        cites = []
        for cite_param in cite_params:
            cite_index, cite_param = cite_param.split(':')[0], cite_param.split(':')[1]
            cite_index = cite_index.replace('@', '')
            for sort in self.sorts:
                if sort.layout.load.index_name == cite_index:
                    cites.append(
                        CiteColumn(
                            table_id=sort.layout.load.table_id,
                            sheet_id=sort.layout.sheet_id,
                            column=sort.layout.head_index(cite_param),
                            matrix=sort.layout.matrix
                        )
                    )
        return cites