from tastypie.authorization import ReadOnlyAuthorization
from tastypie.exceptions import Unauthorized


class DecisionAuthorization(ReadOnlyAuthorization):
    def create_list(object_list, bundle):
        return object_list

class UserAuthorization(ReadOnlyAuthorization):
    def delete_detail(object_list, bundle):
        userprofile = bundle.request.user.userprofile
        if bundle.obj.pk != userprofile.pk:
            raise Unauthorized('This is not your account!')
        else:
            return True
