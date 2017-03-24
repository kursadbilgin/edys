# Local Django
from core.utils import default, editor, assigned_editor, reviewer


def set_up_app():
    # Groups
    print('\nGroups')

    try:
        default()
        print('* \033[1;32mDefault\033[1;37m')
    except:
        print('* \033[1;31mDefault\033[1;37m')

    try:
        editor()
        print('* \033[1;32mEditor\033[1;37m')
    except:
        print('* \033[1;31mEditor\033[1;37m')

    try:
        assigned_editor()
        print('* \033[1;32mAssigned Editor\033[1;37m')
    except:
        print('* \033[1;31mAssigned Editor\033[1;37m')

    try:
        reviewer()
        print('* \033[1;32mReviewer\033[1;37m')
    except:
        print('* \033[1;31mReviewer\033[1;37m')

#####################
