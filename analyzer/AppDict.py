import json
import leancloud

__author__ = 'Jayvee'


class AppDict(leancloud.Object):
    """
    class of leancloud object, senz.analyzer.user.applist
    """

    @property
    def app(self):
        return self.get('app')

    @app.setter
    def app(self, value):
        return self.set('app', value)

    @property
    def label(self):
        return self.get('label')

    @label.setter
    def label(self, value):
        return self.set('label', value)

    @property
    def degree(self):
        return self.get('degree')

    @degree.setter
    def degree(self, value):
        return self.set('degree', value)


def push_data_to_leancloud(fin_path):
    """
    push app data to leancloud
    :param fin_path: json path
    :return: None
    """

    from config import token_config

    leancloud.init(token_config.LEANCLOUD_APP_ID, token_config.LEANCLOUD_APP_KEY)
    fin = open(fin_path, 'r')
    jsonobj = json.loads(fin.read())
    for single_app in jsonobj:
        appdict = AppDict()
        appdict.set('app', single_app['app'])
        appdict.set('degree', single_app['degree'])
        appdict.set('label', single_app['label'])
        appdict.save()
    print 'done!'


if __name__ == '__main__':
    push_data_to_leancloud(r'D:\CS\Git\Jobs\senz.analyzer.applist\analyzer\data\appdict.json')
