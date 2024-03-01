# This file manage simple cli for the project. This isn't standard
# TODO: create beauty and correct cli

# internal
from . import settings
from . import tools
# standard
import os


def choose_run_or_edit():
    options = """
    1: Run Project
    2: Edit Profile
    """
    print(options)

    while True:
        try:
            user_ans = int(input(': '))
            if user_ans == 1 or user_ans == 2:
                return user_ans
            else:
                raise ValueError

        except ValueError:
            print('insert valid value')


def choose_platform():
    explanation = 'choose your Platform\n'
    options = """
    1: Rubika
    2: Soroush
    """
    print(explanation)
    print(options)

    while True:
        try:
            user_ans = int(input(': '))
            if user_ans == 1:
                return 'rubika'
            elif user_ans == 2:
                return 'soroush'
            else:
                raise ValueError

        except ValueError:
            print('insert valid value')


def get_phonenumber(platform):
    description = 'Phone Number Format: 09** *** ** **'
    print(description)
    while True:
        phonenumber = input("give me your phonenumber: ")
        manage_phonenumber = tools.NumberFormats(phonenumber)
        if manage_phonenumber.check_phonenumber_format():
            break
        else:
            print("Invalid Phone Number")

    if platform == 'rubika':
        return manage_phonenumber.rubika_format()
    elif platform == 'soroush':
        return manage_phonenumber.soroush_format()
    else:
        return False


def base_project_dir():
    get_folder_text = "Please give me path of your base project"
    while True:
        print(get_folder_text)
        base_path = input(': ').strip()
        if not os.path.exists(base_path):
            print("your path doesn't exist")
            continue
        return base_path


def choose_base_or_profile():
    option = """
    1: Base Dir
    2: profile
    """
    print(option)

    while True:
        try:
            user_ans = int(input(': '))
            if user_ans == 1 or user_ans == 2:
                return user_ans
            else:
                raise ValueError

        except ValueError:
            print('insert valid value')


def edit_profile():
    get_profile_text = "Please give me your profile path"
    get_fname_text = "Please give me your first name"
    get_lname_text = "Please give me your last name"

    print(get_fname_text)
    fname = input(': ').strip()

    print(get_lname_text)
    lname = input(': ').strip()

    while True:
        print(get_profile_text)
        profile_path = input(': ').strip()
        if not os.path.exists(profile_path):
            print("your path doesn't exist")
            continue
        break

    return {"first name": fname, "last name": lname, 'profile path': profile_path}

