__author__ = 'lufeng'

import os
from sense import config
from sense.mountpoints import MOUNT_POINTS
from flask.ext.script import Manager, Shell
from sense.settings import create_app, configure_blueprints

env = os.getenv('APP_ENV')
if not env:
    env = "Development"
cfg = getattr(config, '%sConfig' % env)
if not cfg:
    raise RuntimeError("can not find config for Evn %s" % env)
app = create_app(conf=cfg)
app = configure_blueprints(app, MOUNT_POINTS)
manager = Manager(app)


if __name__ == '__main__':
    manager.run(default_command="runserver")