from rest_framework import permissions
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


DICT_METHODS = {
    'POST': 'add',
    'PUT': 'change',
    'DELETE': 'delete',
    'GET': 'view',
    'OPTIONS': 'view',
    'PATCH': 'view'
}

class CustomPermission(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        obj_content_type = ContentType.objects.get_for_model(view.queryset.model)
        app = obj_content_type.app_label
        model = obj_content_type.model
        if model == 'funcionario':
            pass

        #print('%s.%s_%s'%(app, DICT_METHODS[request.method.upper()], model))
        
        return user.has_perm('%s.%s_%s'%(app, DICT_METHODS[request.method.upper()], model))
