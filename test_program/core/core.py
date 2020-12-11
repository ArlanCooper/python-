import logging
import time
import os
from loguru import logger
from test_program.conf import settings
from test_program.lib import read_ini
#from test_program.conf import my_log_settings

# print(__name__)
config = read_ini.read(settings.config_path)
#logger = my_log_settings.load_my_logging_cfg()

#logger路径
work_dir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.dirname(work_dir)
logger.add(parent_dir+'/log/all.log')


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