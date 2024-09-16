import os


appConfig = {'HOST': os.getenv('HOST', 'sandbox-iosxr-1.cisco.com'),
             'USR': os.getenv('USR', 'admin'),
             'PASSWD': os.getenv('PASSWD', 'C1sco12345'),
             }
