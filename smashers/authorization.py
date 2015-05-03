from tastypie.authorization import ReadOnlyAuthorization
from tastypie.exceptions import Unauthorized


class DecisionAuthorization(ReadOnlyAuthorization):
    def create_list(self, object_list, bundle):
        return object_list

class UserAuthorization(ReadOnlyAuthorization):

    def _is_this_me(self, bundle):
        userprofile = bundle.request.user.userprofile
        print bundle.obj
        print userprofile
        print bundle.obj.pk == userprofile.pk
        if bundle.obj.pk != userprofile.pk:
            raise Unauthorized('This is not your account!')
        else:
            return True

    def delete_detail(self, object_list, bundle):
        return self._is_this_me(bundle)

    def update_detail(self, object_list, bundle):
        return self._is_this_me(bundle)
