import xlrd
import requests
from msgtask import MessageType
from mainloop import MainLoop
from workthreadpool import Work

url_temp = 'http://jwbm.jiangnan.edu.cn/jwzp/{stu_num}.jpg'
filename_temp = u'/Users/cailin/Desktop/stu_images/{stu_num}-{name}-{_class}.jpg'


def get_stu_numbers(filename):
    with xlrd.open_workbook(filename) as work_book:
        table = work_book.sheets()[0]
        for row_num in range(table.nrows):
            row = table.row_values(row_num)
            stu_num, name, _class = row[2], row[1], row[7]
            if stu_num:
                stu_num = str(int(stu_num))
                yield stu_num, filename_temp.format(stu_num=unicode(stu_num), name=name, _class=_class)


def get_url(stu_num):
    return url_temp.format(stu_num=str(int(stu_num)))


def get_data(url, filename):
    try:
        requests.adapters.DEFAULT_RETRIES = 5
        resp = requests.get(url)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {'args': (url, filename), 'msg': MessageType.ConnectionError}
    else:
        if resp.status_code == 200:
            content = resp.content
            with open(filename, 'w') as f:
                f.write(content)
            print 'success: {}'.format(url)
            return {'args': (url, filename), 'msg': MessageType.ConnectionSuccess}
        print 'resp code is not 200: {}'.format(url)
        return {'args': (url, filename), 'msg': MessageType.NotFound}


if __name__ == '__main__':
    # main_loop = MainLoop()


    # @main_loop.msg_map.register_msg_handler(MessageType.ConnectionError)
    # def FailCallback(*args):
    #     print 'get {0} failed'.format(args[0])
    #
    #
    # @main_loop.msg_map.register_msg_handler(MessageType.ConnectionSuccess)
    # def SuccCallback(*args):
    #     print 'get {0} successfully'.format(args[0])
    #
    #
    # @main_loop.msg_map.register_msg_handler(MessageType.NotFound)
    # def NotFoundCallback(*args):
    #     print '{} not found'.format(args[0])

    works = set([])
    for stu_num, filename in get_stu_numbers('/Users/cailin/Downloads/1.xls'):
        url = get_url(stu_num)
        work = Work(get_data, args=(url, filename))
        works.add(work)
    print 'row count: {}'.format(len(works))
    count = 0
    # for url, _ in groupby(works, key=lambda x: x.args[0]):
    #     count += 1
    #     s = [each for each in _]
    #     print url, len(s)
    #     main_loop.work_thread_mgr.add_work(s[0])
    # print 'total work: {}'.format(count)
    # main_loop.work_thread_mgr.wait_all_complete()
