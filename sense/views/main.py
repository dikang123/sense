# coding=utf-8

import json
import traceback
from ..auth import Auth
from flask import Blueprint, render_template, redirect, session, current_app, request


__author__ = 'Feng Lu'


main = Blueprint('main', __name__)
main.before_request(Auth.load_user)


@main.route("/")
def index():
    return render_template("index.html")

@main.route("/logout")
def logout():
    session.clear()
    return redirect('%s/account/logout?redirect=%s' % (current_app.config.get('SSO_URL'), request.referrer))