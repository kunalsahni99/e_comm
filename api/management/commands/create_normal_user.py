from api.models import User
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Creates application data'

    def handle(self, *args, **options):
        user = User.objects.create_user(username='kunal', 
                                        password='123456', 
                                        email='kunal.sahni1999@gmail.com')
        
        user.save()