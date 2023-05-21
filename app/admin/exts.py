class ChartData(object):
    def __init__(self, obj_list):
        self.obj_list = obj_list

    @property
    def line_data(self):
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

