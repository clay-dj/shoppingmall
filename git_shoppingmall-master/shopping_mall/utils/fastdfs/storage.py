#自定义存储模块必须继承django.core.files.storage中的Storage类
#然后在重写_open()和_save()两个方法
#最后通过url方法返回本机ip地址和端口号
from django.core.files.storage import Storage
from shopping_mall import settings
class FastDFSStorage(Storage):
    """自定义文件存储系统，修改存储的方案"""
    # def __init__(self, fdfs_base_url=None):
    #     """
    #     构造方法，可以不带参数，也可以携带参数
    #     :param base_url: Storage的IP
    #     """
    #     self.fdfs_base_url = fdfs_base_url or settings.FDFS_BASE_URL

    def _open(self, name, mode='rb'):
        pass


    def _save(self, name, content):
        pass


    def url(self, name):
        """
        返回name所指文件的绝对URL
        :param name: 要读取文件的引用:group1/M00/00/00/wKhnnlxw_gmAcoWmAAEXU5wmjPs35.jpeg
        :return: http://192.168.103.158:8888/group1/M00/00/00/wKhnnlxw_gmAcoWmAAEXU5wmjPs35.jpeg
        """
        # return 'http://192.168.103.158:8888/' + name
        # return 'http://image.meiduo.site:8888/' + name
        return "http://192.168.254.142:8888/" + name