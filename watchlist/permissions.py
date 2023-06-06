from rest_framework.permissions import BasePermission, IsAdminUser, SAFE_METHODS

class IsAdminOrReadOnly(IsAdminUser):
    """
    Permission class for 'Admin' user. Returns true for admin users or on 'GET' request only
    """    
    
    def has_permission(self, request, view):
        """
        Override the base class method to return true for admin users or on 'GET' requests only
        Args:
            request (Request): request object recieved from client side
            view (View): view object recieved from server side

        Returns:
            bool: true for SAFE_METHODS or staff users only
        """        
        
        if request.method in SAFE_METHODS:
            return True
        
        return bool(request.user and request.user.is_staff)
    
    
    
    class ReviewUserorReadOnly(BasePermission):
        """
        Permission class for 'Review' uers.
        Determines if the user making request is same who created the review or not?
        """      
        
        def has_object_permission(self, request, view, obj):
            """
            Override the base class method to return true for 'GET' requests or if request is made by same user only
            
            Args:
                request (Request): request object recieved from client side
                view (View): view object recieved from server side
                obj (Model): model object checked and used from server side

            Returns:
                bool: true for SAFE_METHODS or reviewer only
            """        
        
            if request.method in SAFE_METHODS:
                return True
            else:
                return obj.review_user == request.user