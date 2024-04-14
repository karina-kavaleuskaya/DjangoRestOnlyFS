from celery import shared_task
import time
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from only_app.models import Stock, Product
import io
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
from django.db.models import Count
import tempfile


@shared_task
def some_task():
    time.sleep(5)
    return 'Aboba'


@shared_task
def check_order_and_send_mails():
    stocks = Stock.objects.filter(if_notif_sent=False)

    for stock in stocks:
        user_email = stock.product.user.email

        send_mail(
            'Product sold',
            f'Your product has been sold!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_email],
        )

        stock.if_notif_sent = True
        stock.save()


@shared_task
def generate_sales_report():
    user_emails = Product.objects.values_list('user__email', flat=True).distinct()

    for user_email in user_emails:
        products = (
            Product.objects
            .filter(user__email=user_email)
            .annotate(stock_count=Count('stock'))
        )

        if products.exists():
            pdf_buffer = io.BytesIO()
            c = canvas.Canvas(pdf_buffer)

            c.setFont('Helvetica', 16)
            c.drawString(50, 750, 'Stock Report')

            c.setFont('Helvetica', 12)
            c.drawString(50, 700, f'User: {user_email}')

            product_names = [product.name for product in products]
            stock_counts = [product.stock_count for product in products]

            plt.figure(figsize=(8, 6))
            plt.bar(product_names, stock_counts)
            plt.xlabel('Product')
            plt.ylabel('Sales count')
            plt.title('Sales Analytics')
            plt.xticks(rotation='vertical')
            plt.tight_layout()

            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                plt.savefig(temp_file.name, format='png')

            # Включение графика в PDF-файл
            c.drawImage(temp_file.name, 50, 400, width=500, height=300)

            c.save()

            email_subject = 'Sales Report'
            email_body = 'Your month sales report!.'
            email_from = settings.DEFAULT_FROM_EMAIL
            email_to = [user_email]

            email = EmailMessage(email_subject, email_body, email_from, email_to)
            email.attach('sales_report.pdf', pdf_buffer.getvalue(), 'application/pdf')
            email.send()