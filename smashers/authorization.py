from tastypie.authorization import ReadOnlyAuthorization


class DecisionAuthorization(ReadOnlyAuthorization):
    def create_list(object_list, bundle):
        return object_list
