
'''
程序自身业务配置 和 第三方平台配置
'''


REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 7,
}


YZX_API = 'https://open.ucpaas.com/ol/sms/sendsms'
YZX_VCODE_ARGS = {
    'appid': 'c153ca163aaa4b9a8d94568c3e8e8fa8',
    'sid': 'e8240184b714c40de8dbe13ccac48ed9',
    'token': '360d78f45a28edf2af141327848be433',
    'templateid': '534537',
    'mobile': None,
    'param': None,
}
'''七牛云'''

QN_ACCESS_KEY = 'AVFn8f1ve3AncfLNAfq5rhTddkKoaU2agS0Gkatz'
QN_SECRET_KEY = 'neViCpaWFPIyWZ_3cbBGUBdDitrhnyapu9C43dMr'
QN_BUCKET = 'gaoziyi'
QN_BASEURL = 'http://q7357yrqg.bkt.clouddn.com'