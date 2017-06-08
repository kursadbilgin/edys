# Local Django
from core.utils import default, admin


def set_up_app():
    # Groups
    print('\nGroups')

    try:
        default()
        print('* \033[1;32mDefault\033[1;37m')
    except:
        print('* \033[1;31mDefault\033[1;37m')

    try:
        admin()
        print('* \033[1;32mAdmin\033[1;37m')
    except:
        print('* \033[1;31mAdmin\033[1;37m')

#####################
