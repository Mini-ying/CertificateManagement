from werkzeug.routing import BaseConverter

#定义正则转换器
class ReConverter(BaseConverter):
    def _init_(self,url_map,regex):
        super(ReConverter,self)._init_(url_map)
        #保存正则表达式
        self.regex=regex