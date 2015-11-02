#coding:utf-8

import os
from flask.ext.babel import gettext as _

__author__ = 'Feng Lu'


class Config(object):
    PAGE_SIZE = 30
    LOG_LEVEL = "INFO"
    DBSEARCH_LIMIT = 2000
    BABEL_DEFAULT_LOCALE = 'zh'
    ELASTICSEARCH_INDEX = "sense"
    LOCAL_USER = {"user": {"um": "loca_admin"}, "permissions": {"sense": ["super.admin"]}}
    os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
    change_babel = [_("id"), _("um"), _("do_type"), _("do_name"), _("do_version"), _("do_change"), _("do_time"),
                    _("do_ret")]
    change_type = [_('update'), _('create'), _('trash'), _('remove'), _('rollback'), _('restore')]

    APPNAME = "sense"
    MESSAGE_MAIL_QUEUE = "SENSE:MAIL:QUEUE"


class ProductionConfig(Config):
    SECRET_KEY = "sfhhjkdhfkjshk"
    SSO_URL = "http://passport.op.lufax.com"
    SSO_APP_SECRET = "QWCcwFKfSQHCYrmY"
    SSO_APP_ID = 17
    SSO_ENABLE = True

    #for watch save log
    REDIS_URL = "redis://192.168.111.212:6379/1"
    WATCH_QUEUE_NAME = "WATCH:LOG:QUEUE"

    CACHE_TYPE = "redis"
    #设置缓存连接
    CACHE_REDIS_URL = 'redis://192.168.111.212:6379/1'
    CACHE_KEY_PREFIX = "SENSE:"
    CACHE_DEFAULT_TIMEOUT = 3000
    CACHE_ENABLE = True
    ELASTICSEARCH_URL = "192.168.111.205:9200"

    PAGE_SIZE = 30
    DBSEARCH_LIMIT = 2000
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://op_sense:12qwaszx@192.168.111.115:3306/sense?charset=utf8'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_POOL_RECYCLE = 300


    CELERY_QUEUE = "sense"
    BROKER_URL = 'redis://192.168.111.212:6379'
    CELERY_RESULT_BACKEND = 'redis://192.168.111.212:6379'
    CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']

    #邮件配置
    ADMINS = ('lufeng044@pingan.com.cn',)
    MAIL_SUFFIX = 'pingan.com.cn'
    MAIL_SERVER = "192.168.93.12"
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_DEBUG = False
    MAIL_DEFAULT_SENDER = 'sense@lufax.com'

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = "sfhhjkdhfkjshk"
    SSO_URL = "http://0.0.0.0:8002"
    SSO_APP_SECRET = "sbc979g54n88w3408rmol"
    SSO_APP_ID = 3
    SSO_ENABLE = False

    #for watch save log
    REDIS_URL = "redis://127.0.0.1:6379/1"
    WATCH_QUEUE_NAME = "WATCH:LOG:QUEUE"

    CACHE_TYPE = "redis"
    CACHE_DEFAULT_TIMEOUT = 86400
    CACHE_REDIS_URL = 'redis://127.0.0.1:6379/1'
    CACHE_KEY_PREFIX = "SENSE:"
    CACHE_ENABLE = True

    ELASTICSEARCH_URL = "0.0.0.0:9200"

    PAGE_SIZE = 30
    DBSEARCH_LIMIT = 2000
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://sense:12qwaszx@127.0.0.1:3306/sense?charset=utf8'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_POOL_RECYCLE = 300

    CELERY_QUEUE = "sense"
    BROKER_URL = 'redis://127.0.0.1:6379/0'
    CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
    CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']

    ADMINS = ('lufeng4828@163.com', )

    MAIL_SUFFIX = 'mail.163.com'
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_DEBUG = False
    MAIL_USERNAME = 'lufax_opdev@163.com'
    MAIL_PASSWORD = 'xxxxxxxxxx'
    DEFAULT_MAIL_SENDER = 'lufax_opdev@163.com'
