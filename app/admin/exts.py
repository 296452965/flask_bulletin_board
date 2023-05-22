class ChartData(object):
    """
    数据封装类
    """
    def __init__(self, obj_list):
        self.obj_list = obj_list

    @property
    def line_data(self):
        """
        :return dic{'data':[],'labels':[]}
        data：问题数量 labels：时间
        """
        # obj_list_timeline = self.obj_list.order_by(date)
        dic = {
            'data': [],
            'labels': [],
        }
        for item in self.obj_list:
            date = item.date.isoformat()
            if date in dic['labels']:
                index = dic['labels'].index(date)
                dic['data'][index] += 1
            else:
                dic['data'].append(1)
                dic['labels'].append(date)
        return dic

    @property
    def bar_data(self):
        """
        :return dic{'data':[],'labels':[]}
        data：问题数量 labels：单位
        """
        dic = {
            'data': [],
            'labels': [],
        }
        for item in self.obj_list:
            unit_name = item.unit.unit_name
            if unit_name in dic['labels']:
                index = dic['labels'].index(unit_name)
                dic['data'][index] += 1
            else:
                dic['data'].append(1)
                dic['labels'].append(unit_name)
        return dic