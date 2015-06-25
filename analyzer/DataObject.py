import json
import leancloud
from analyzer.MyExceptions import MsgException

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
    push local app data to leancloud
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


class FeedbackData(leancloud.Object):
    @property
    def labels(self):
        return self.get('labels')

    @property
    def applist(self):
        return self.get('applist')

    @labels.setter
    def labels(self, value):
        return self.set('labels', value)

    @applist.setter
    def applist(self, value):
        return self.set('applist', value)


def push_data_to_feedback(feedback_data):
    """
    define: feedback data contains a user's feedbacks,
    user's label and applist should be included in {Dict}-feedback_data
    :param feedback_data: format:{"labels":["label1","label2","label3"],"applist":["app1","app2","app3"]}
    :return:
    """
    from config import token_config

    leancloud.init(token_config.LEANCLOUD_APP_ID, token_config.LEANCLOUD_APP_KEY)
    try:
        labels = feedback_data['labels']
        applist = feedback_data['applist']
        fd = FeedbackData()
        if not isinstance(labels, list):
            raise MsgException('labels should be a list!')
        if not isinstance(applist, list):
            raise MsgException('applist should be a list!')
        if len(labels) == 0:
            raise MsgException('labels should not be empty!')
        if len(applist) == 0:
            raise MsgException('applist should not be empty!')

        fd.set('applist', applist)
        fd.set('labels', labels)
        fd.save()
    except KeyError, keyerror:
        # simply raise a exception
        raise keyerror


if __name__ == '__main__':
    # push_data_to_leancloud(r'D:\CS\Git\Jobs\senz.analyzer.applist\analyzer\data\appdict.json')
    ttt = {'labels': ['study', 'gender'], 'applist': ['test1', 'test2']}
    try:
        push_data_to_feedback(ttt)
    except KeyError, keyerror:
        print keyerror
    print 'done!'