import os


# Base Dir
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
                    )
)


DRIVER_FOLDER = os.path.join(BASE_DIR, 'driver')
DRIVER = os.listdir(DRIVER_FOLDER)[0]
DRIVER_FILE = os.path.join(DRIVER_FOLDER, DRIVER)

# Construct the path to the user's home folder
HOME_FOLDER = os.path.join('C:\\', 'Users', os.getlogin())

CHROME_PATH = os.path.join(HOME_FOLDER, 'AppData', 'Local', 'Google', 'Chrome', 'User Data')
BASE_CHROME_NAME = 'User Data'
INSTANCE_CHROME_NAME = 'Chrome'
INSTANCE_PATH = os.path.join(HOME_FOLDER, 'Desktop', 'Chrome')

PROFILES_FOLDER = os.path.join(BASE_DIR, 'profiles')

# logins
LOGIN_EITAA = 'https://web.eitaa.com/'
LOGIN_BALE = 'https://web.bale.ai/login'
LOGIN_IGAP = 'https://web.igap.net/'
LOGIN_RUBIKA = 'https://web.rubika.ir/'
LOGIN_SOROUSH = 'https://web.splus.ir/'

# registered platforms
REGISTERED_PLATFORM = ['soroush', 'rubika']

# config file
CONFIG_FILE = 'configs.json'
CONFIG_PATH = os.path.join(BASE_DIR, CONFIG_FILE)
