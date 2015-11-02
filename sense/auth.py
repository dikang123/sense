# coding=utf-8

import re
import hmac
import time
import traceback
import requests
from functools import wraps
from flask.ext.babel import gettext as _
from flask import g, session, redirect, current_app, request, render_template, jsonify

__author__ = 'comyn'

token_re = re.compile(r"\??\b_token=\w+&?")


class PermissionDeniedException(Exception):
    def __init__(self, permissions):
        super(Exception, self).__init__(_('permissions %(perm)s required', perm=' or '.join(permissions)))


class Auth(object):
    @classmethod
    def required(cls, permissions, error_resp_type="html"):
        if not (isinstance(permissions, list) or isinstance(permissions, tuple)):
            permissions = [permissions, ]

        def wrap(func):
            @wraps(func)
            def inner_wrap(*args, **kwargs):
                if hasattr(g, 'user'):
                    for p in set(g.user['permissions'].get(current_app.name, [])):
                        if str(p) in permissions:
                            return func(*args, **kwargs)
                if len(permissions) == 0:
                    return func(*args, **kwargs)
                msg = PermissionDeniedException(permissions).message
                if error_resp_type == "json":
                    return jsonify({"retcode": -1, "msg": msg, "result": "", "type": "str"})
                elif error_resp_type == "html":
                    return render_template("common/fail.html", message=msg)
                else:
                    return {"retcode": -1, "msg": msg, "result": "", "type": "str"}
            return inner_wrap

        return wrap

    @classmethod
    def validate(cls, permissions):
        if not current_app.config.get('SSO_ENABLE'):
            return True
        if not (isinstance(permissions, list) or isinstance(permissions, tuple)):
            permissions = [permissions, ]
        if hasattr(g, 'user'):
            for p in set(g.user['permissions'].get(current_app.name, [])):
                if str(p) in permissions:
                    return True
        return False

    @classmethod
    def load_user(cls):
        if not current_app.config.get('SSO_ENABLE'):
            g.user = current_app.config.get("LOCAL_USER")
            return

        if request.values.get("_token"):
            session["user_token"] = request.values.get("_token")
        if session.get('user_token'):
            url = '%s/account/info/%s?secret=%s&app=%d' % (current_app.config.get('SSO_URL'),
                                                           session.get('user_token'),
                                                           current_app.config.get('SSO_APP_SECRET'),
                                                           current_app.config.get('SSO_APP_ID'))
            try:
                req = requests.get(url)
                resp = req.json()
                if resp['status'] == 200:
                    g.user = resp
                    if token_re.findall(request.url):
                        return redirect(token_re.sub("", request.url))
                elif resp['status'] == 403:
                    return render_template("include/fail.html", message=resp["message"])
                else:
                    return redirect('%s/account/login?redirect=%s' % (
                        current_app.config.get('SSO_URL'),
                        request.url))
            except Exception, e:
                return redirect('%s/account/login?redirect=%s' % (
                    current_app.config.get('SSO_URL'), request.url))
        else:
            return redirect('%s/account/login?redirect=%s' % (
                current_app.config.get('SSO_URL'), request.url))

    @classmethod
    def load_api(cls):
        """
        """
        if not current_app.config.get('SSO_ENABLE'):
            g.user = current_app.config.get("LOCAL_USER")
            return
        #必须要提供三个头参数
        secretid = request.headers.get("x-secretid")
        timestamp = request.headers.get("x-timestamp")
        signature = request.headers.get("x-signature")
        if secretid and timestamp and signature:
            serv_timestamp = time.strftime('%s', time.localtime())
            delta = abs(int(serv_timestamp) - int(timestamp))
            if delta > 60:
                return jsonify(
                    {"retcode": -1,
                     "msg": "The timestamp you provide is difference to server up to 60s, please check your system time",
                     "result": "", "type": "str"})
            url = '%s/account/secret/%s' % (current_app.config.get('SSO_URL'), secretid)
            try:
                req = requests.get(url)
                resp = req.json()
                if resp['status'] == 200:
                    secret = resp["secret"]
                    query_keys = request.values.keys()
                    query_keys.sort()
                    query = []
                    for key in query_keys:
                        query.append("%s=%s" % (key, request.values[key]))
                    body = '&'.join(query)
                    #生成签名
                    serv_signature = hmac.new(str(secret["key"]), body).hexdigest()
                    if serv_signature != signature:
                        return jsonify({"retcode": -1, "msg": "x-signature is incrrect! ", "result": "", "type": "str"})
                    g.user = resp
                    if token_re.findall(request.url):
                        return redirect(token_re.sub("", request.url))
                else:
                    return jsonify({"retcode": -1, "msg": resp.get("message"), "result": "", "type": "str"})
            except Exception, e:
                current_app.logger.error(traceback.format_exc())
                return jsonify({"retcode": -1, "msg": e.message, "result": "", "type": "str"})
        else:
            return jsonify(
                {"retcode": -1, "msg": "x-secretid,x-timestamp and x-signature in headers is required", "result": "",
                 "type": "str"})
