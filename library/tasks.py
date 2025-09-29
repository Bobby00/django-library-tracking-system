from datetime import date
from celery import shared_task
from .models import Loan
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject='Book Loaned Successfully',
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass

def check_overdue_loans():
    try:
        queryset = Loan.objects.all()
        overdue_recipient_list = []
        for loan in queryset:
            if loan.due_date < date.today() and loan.is_returned == False:
                loan.append(overdue_recipient_list.append(loan.member.user.email))
            send_mail(
                subject='Overdue Book Loan Period',
                message=f'Hello {loan.member.user.username},\n\nYou have an overdue loan of book "{loan.book}".\nPlease return it!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[overdue_recipient_list],
                fail_silently=False,
            )
        return 'Email(s) sent sucessfully..'
    except Exception as e:
        return e
