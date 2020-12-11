import sys,os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath('__file__')))
sys.path.append(BASE_DIR)

from test_program.core import core
#from test_program.conf import my_log_settings

if __name__ == '__main__':
    #my_log_settings.load_my_logging_cfg()
    core.run()