# internal
from src import manage_folders
from src.login_bot import *
from src import settings
from src import tools
from src.cli import *


def main():
    try:
        configs = tools.load_json(settings.CONFIG_PATH)
    except FileNotFoundError:
        data = edit_profile()
        data['base dir'] = base_project_dir()
        tools.write_json(settings.CONFIG_PATH, data)
        main()
    configs_data = (configs['first name'], configs['last name'], configs['profile path'])

    run_or_edit = choose_run_or_edit()
    if run_or_edit == 1:
        base_dir = tools.load_json(settings.CONFIG_PATH)['base dir']
        platform = choose_platform()

        if platform == 'rubika':
            while True:
                folders = manage_folders.Folders(base_dir)
                folders.create_base_folder()
                phonenumber = get_phonenumber(platform)
                print(folders.base_folder)
                rubika = RubikaLogin(phonenumber, *configs_data, folders.base_folder)
                rubika.main()
                print('successfully profile created!')
        elif platform == 'soroush':
            while True:
                folders = manage_folders.Folders(base_dir)
                folders.create_base_folder()
                phonenumber = get_phonenumber(platform)
                soroush = SoroushLogin(phonenumber, *configs_data, folders.base_folder)
                soroush.main()
                print('successfully profile created!')

    elif run_or_edit == 2:
        what_do = choose_base_or_profile()
        if what_do == 1:
            base_dir = base_project_dir()
            data = tools.load_json(settings.CONFIG_PATH)
            data['base dir'] = base_dir
            tools.write_json(settings.CONFIG_PATH, data)
        else:
            base_dir = tools.load_json(settings.CONFIG_PATH)
            data = edit_profile()
            data['base dir'] = base_dir['base dir']
            tools.write_json(settings.CONFIG_PATH, data)
        main()


if __name__ == '__main__':
    main()
