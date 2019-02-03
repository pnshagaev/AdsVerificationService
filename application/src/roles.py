from enum import Enum


def at_least_one_of_roles_in_roles_list(roles, roles_list):
    return True if len(set(roles).intersection(roles_list)) != 0 else False


class RolesTypes(Enum):
    user = 0
    administrator = 1
    superuser = 2


admin_roles = [RolesTypes.administrator.name, RolesTypes.superuser.name]

