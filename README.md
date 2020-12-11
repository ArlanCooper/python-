Python 工程目录结构
===
[toc]

# 整体架构
```
project_name/
|
|_ _ _ _ bin/
|        |_ _ start.py       
|
|_ _ _ _ conf/
|        |_ _ config.ini
|        |_ _ my_log_settings.py
|        |_ _ settings.py
|
|_ _ _ _ core/
|        |_ _core.py
|
|_ _ _ _ db/
|        |_ _x.json
|        |_ _y.json
|
|_ _ _ _ doc/
|        |_ _README
|
|_ _ _ _ lib/
|        |_ _read_ini.py
|
|_ _ _ _ log/
|        |_ _all.log
|
|_ _ _ _ tests/
|        |_ _test.py
|
|_ _ _ _ requirements.txt
|
|
|_ _ _ _setup.py

```
简单说明:
- project_name/ : 存放项目的所有源代码。(1) 源代码中的所有模块、包都应该放在此目录。不要置于顶层目录。(2) 其子目录tests/存放单元测试代码； (3) 程序的入口最好命名为main.py。
- bin/ : 存放项目的一些可执行文件，当然你可以起名script/之类的也行。
- docs/: 存放一些文档,readme.md文档等
- core/:存放核心代码
- conf/:存放配置
- db/:存放数据
- setup.py/: 安装、部署、打包的脚本。
- lib/:存放自定义的模块与包
- tests/ : 存放测试代码
- requirements.txt: 存放软件依赖的外部Python包列表。

# 各个部分详解
## 关于README的内容
这个我觉得是每个项目都应该有的一个文件，目的是能简要描述该项目的信息，让读者快速了解这个项目。

它需要说明以下几个事项:

- 软件定位，软件的基本功能。
- 运行代码的方法: 安装环境、启动命令等。
- 简要的使用说明。
- 代码目录结构说明，更详细点可以说明软件的基本原理。
- 常见问题说明。

## 关于requirements.txt
这个文件存在的目的是:

1. 方便开发者维护软件的包依赖。将开发过程中新增的包添加进这个列表中，避免在 setup.py 安装依赖时漏掉软件包。
2. 方便读者明确项目使用了哪些Python包。

这个文件的格式是每一行包含一个包依赖的说明，通常是flask>=0.10这种格式，要求是这个格式能被pip识别，这样就可以简单的通过 pip install -r requirements.txt来把所有Python包依赖都装好了。

## 关于setup.py
一般来说，用setup.py来管理代码的打包、安装、部署问题。业界标准的写法是用Python流行的打包工具setuptools来管理这些事情。

这种方式普遍应用于开源项目中。不过这里的核心思想不是用标准化的工具来解决这些问题，而是说，一个项目一定要有一个安装部署工具，

能快速便捷的在一台新机器上将环境装好、代码部署好和将程序运行起来。

setup.py可以将这些事情自动化起来，提高效率、减少出错的概率。"复杂的东西自动化，能自动化的东西一定要自动化。"是一个非常好的习惯。

setuptools的文档比较庞大，刚接触的话，可能不太好找到切入点。学习技术的方式就是看他人是怎么用的，可以参考一下Python的一个Web框架，

flask是如何写的: setup.py当然，简单点自己写个安装脚本（deploy.sh）替代setup.py也未尝不可


# 项目举例

## bin/start.py
```python
import sys,os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath('__file__')))
sys.path.append(BASE_DIR)

from test_program.core import core
#from test_program.conf import my_log_settings

if __name__ == '__main__':
    #my_log_settings.load_my_logging_cfg()
    core.run()


```
## conf/config.ini
```
[DEFAULT]
user_timeout = 1000

[x]
password = 123
money = 10000000

[y]
password = 123456
money=1000

[z]
password = qwe123
money=10


```
## conf/settings.py
```python
import os
config_path=r'%s\%s' %(os.path.dirname(os.path.abspath(__file__)),'config.ini')
user_timeout=10
user_db_path=r'%s\%s' %(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'db')

```
## ~~conf/my_log_settings.py~~(因为有更好用的log模块，loguru，所以这个不使用)
```python
"""
logging配置
"""

import os
import logging.config

# 定义三种日志输出格式 开始

standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' \
                  '[%(levelname)s][%(message)s]' #其中name为getlogger指定的名字

simple_format = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'

id_simple_format = '[%(levelname)s][%(asctime)s] %(message)s'

# 定义日志输出格式 结束

logfile_dir = r'%s\log' %os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # log文件的目录

logfile_name = 'all2.log'  # log文件名

# 如果不存在定义的日志目录就创建一个
if not os.path.isdir(logfile_dir):
    os.mkdir(logfile_dir)

# log文件的全路径
logfile_path = os.path.join(logfile_dir, logfile_name)

# log配置字典
LOGGING_DIC = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': standard_format
        },
        'simple': {
            'format': simple_format
        },
    },
    'filters': {},
    'handlers': {
        #打印到终端的日志
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',  # 打印到屏幕
            'formatter': 'simple'
        },
        #打印到文件的日志,收集info及以上的日志
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
            'formatter': 'standard',
            'filename': logfile_path,  # 日志文件
            'maxBytes': 1024*1024*5,  # 日志大小 5M
            'backupCount': 5,
            'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
        },
    },
    'loggers': {
        #logging.getLogger(__name__)拿到的logger配置
        '': {
            'handlers': ['default', 'console'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
            'level': 'DEBUG',
            'propagate': True,  # 向上（更高level的logger）传递
        },
    },
}


def load_my_logging_cfg():
    logging.config.dictConfig(LOGGING_DIC)  # 导入上面定义的logging配置
    logger = logging.getLogger(__name__)  # 生成一个log实例
    logger.info('It works!')  # 记录该文件的运行状态

if __name__ == '__main__':
    load_my_logging_cfg()

```

## core/core.py
```python

import logging
import time
from loguru import logger
from test_program.conf import settings
from test_program.lib import read_ini
#from test_program.conf import my_log_settings

# print(__name__)
config = read_ini.read(settings.config_path)
#logger = my_log_settings.load_my_logging_cfg()
print(logger)

current_user={'user':None,'login_time':None,'timeout':int(settings.user_timeout)}
def auth(func):
    def wrapper(*args,**kwargs):
        if current_user['user']:
            interval=time.time()-current_user['login_time']
            if interval < current_user['timeout']:
                return func(*args,**kwargs)
        name = input('name>>: ')
        password = input('password>>: ')
        if config.has_section(name):
            if password == config.get(name,'password'):
                logger.info('登录成功')
                current_user['user']=name
                current_user['login_time']=time.time()
                return func(*args,**kwargs)
            else:
                logger.error('登录失败')
        else:
            logger.error('用户名不存在')

    return wrapper

@auth
def buy():
    print('buy...')

@auth
def run():

    print('''
购物
查看余额
转账
    ''')
    while True:
        choice = input('>>: ').strip()
        if not choice:break
        if choice == '1':
            buy()
```
## db/
```python
# x_json.json
#y_json.json

```

## lib/read_ini.py
```python
import configparser
def read(config_file):
    config=configparser.ConfigParser()
    config.read(config_file)
    return config

```

## log/all.log
```
all.log
```

整体上这个目录可以运行了。
