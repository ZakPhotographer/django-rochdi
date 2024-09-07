from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Student
from course.models import Program

class Command(BaseCommand):
    help = 'Add students to the database'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, required=True, help='Username for the student')
        parser.add_argument('--first_name', type=str, required=True, help='First name of the student')
        parser.add_argument('--last_name', type=str, required=True, help='Last name of the student')
        parser.add_argument('--email', type=str, required=True, help='Email of the student')
        parser.add_argument('--phone', type=str, required=True, help='Phone number of the student')
        parser.add_argument('--address', type=str, required=True, help='Address of the student')
        parser.add_argument('--gender', type=str, required=True, help='Gender of the student (M/F)')
        parser.add_argument('--level', type=str, required=True, help='Level of the student (Bachelor/Master)')
        parser.add_argument('--program_id', type=int, required=True, help='ID of the program')
        parser.add_argument('--password', type=str, required=True, help='Password for the student')

    def handle(self, *args, **kwargs):
        User = get_user_model()

        username = kwargs['username']
        first_name = kwargs['first_name']
        last_name = kwargs['last_name']
        email = kwargs['email']
        phone = kwargs['phone']
        address = kwargs['address']
        gender = kwargs['gender']
        level = kwargs['level']
        program_id = kwargs['program_id']
        password = kwargs['password']

        try:
            program = Program.objects.get(id=program_id)
        except Program.DoesNotExist:
            self.stderr.write(self.style.ERROR(f'Program with ID {program_id} does not exist.'))
            return

        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
            gender=gender,
            password=password
        )

        # Set additional user attributes if necessary
        user.is_student = True  # or any other logic to set user attributes
        user.save()

        Student.objects.create(
            student=user,
            level=level,
            program=program
        )

        self.stdout.write(self.style.SUCCESS(f'Successfully added student {username}.'))
