# from django.contrib.auth.models import User, BaseUserManager
# from django.db import models

# class CustomUserManager(BaseUserManager):
#     def create_user(self, username, email, password=None):
#         if not email:
#             raise ValueError('The Email field must be set')
        
#         user = self.model(
#             username=username,
#             email=self.normalize_email(email)
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

# class CustomUser(User):
#     # username = models.CharField(max_length=100, unique=True)
#     # email = models.EmailField(unique=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
    
#     objects = CustomUserManager()
    
#     USERNAME_FIELD = 'username'
#     EMAIL_FIELD = 'email'
    
#     def __str__(self):
#         return self.username


