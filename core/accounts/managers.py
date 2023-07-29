from django.contrib.auth.models import BaseUserManager




class UserManager(BaseUserManager):
    def create_user(self, *args, **kwargs):
        if not kwargs['phone_number']:
            raise ValueError('user must have phone number')

        if not kwargs['email']:
            raise ValueError('user must havee email')
        
        user = self.model(phone_number = kwargs['phone_number'], email = self.normalize_email(kwargs['email']), full_name = kwargs['full_name'])
        user.set_password(kwargs['password'])
        user.save(using=self._db)
        return user

    def create_superuser(self, *args, **kwargs):
        user = self.create_user(*args, **kwargs)
        user.is_admin = True
        user.save(using=self._db)
        return user