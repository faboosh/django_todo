from rest_framework import permissions

class IsTodoListOwner(permissions.BasePermission):

    def has_permission(self, request, view, **kwargs):
        list_pk = view.kwargs['list_pk']
        queryset = view.get_queryset()

        todo_list = queryset.get(pk=list_pk)

        return view.request.user == todo_list.owner

class IsOwner(permissions.BasePermission):

    def has_permission(self, request, view, **kwargs):
        pk = view.kwargs['pk']
        queryset = view.get_queryset()

        obj = queryset.get(pk=pk)
        
        return obj.owner == request.user