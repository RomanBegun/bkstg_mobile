import sys
from src.api.urls.api_urls import *


class TestEnvironment(object):

    def __init__(self):

        super().__init__()
        self.base_url = ''

    def set_env_from_arg(self):

        argv_len = len(sys.argv)
        env_args = sys.argv[argv_len - 1]

        if argv_len > 3:
            # Take url part from --tc=env:url CL parameter
            env_url = env_args.split(':', 1)[1]

            # Lock tests from running on Prod
            if env_url == PROD_ENV_URL:
                sys.exit("Tests should not be run on Production environment.")

            self.base_url = env_url

        else:
            self.base_url = MASTER_ENV_URL
        print('Server: %s' % self.base_url, '\n')
