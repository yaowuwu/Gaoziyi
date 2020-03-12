from qiniu import Auth, put_file
from swiper import conf


def upload_to_qncloud(filepath, filename):
    # 构建鉴权对象
    qn_Auth = Auth(conf.QN_ACCESS_KEY, conf.QN_SECRET_KEY)
    # 生成上传 Token，可以指定过期时间等
    token = qn_Auth.upload_token(conf.QN_BUCKET, filename, 3600)
    # 要上传文件的本地路径
    put_file(token, filename, filepath)
    # 拼接文件的链接
    file_url = '%s/%s' % (conf.QN_BASEURL, filename)
    return file_url


