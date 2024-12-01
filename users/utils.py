from django.core.mail import send_mail

def notify_farmer_approval(farmer_profile):
    send_mail(
        'Your account has been approved!',
        'You can now access all features of our platform.',
        'admin@yourplatform.com',
        [farmer_profile.user.email],
    )
