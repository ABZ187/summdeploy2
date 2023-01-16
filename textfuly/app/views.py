import io

import razorpay
from gtts import gTTS
import pyttsx3
from .forms import RegisterForm
from django.conf import settings
from django.contrib import messages
from .Textsum import TextSummarizer
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from django.core.mail import EmailMessage
from reportlab.lib.pagesizes import letter
from django.contrib.auth.models import User
from .models import ColdCoffee, Subscription, NewsLetter, Profile
from django.shortcuts import render, redirect
# from .PremiumTextSum import TextSummarizer
from django.contrib.auth import authenticate, login
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from .forms import CoffeePaymentForm, SubscriptionForm
from .getData import GetData
# from .paraphraser import get_response
import uuid

global summary


# summarizer
@csrf_exempt
def index(request):
    if request.method == 'POST':
        if request.user.is_authenticated and Subscription.objects.filter(email=request.user.email).exists():
            subs=Subscription.objects.get(email=request.user.email)
            if subs.paid==True:
                return premium_work(request)
        else:
            return basic_work(request)
    return render(request, 'index.html', {'premium': False})

# paraphraser
def paraphraser(request):
    # text = request.POST.get('text')
    # result = get_response(text)

    return render(request, 'paraphraser.html')


# basic version
def basic_work(request):
    global summary
    uploaded_files = request.FILES.getlist('files')
    link = request.POST.get('url')
    text = request.POST.get('text')

    short = request.POST.get('short')
    medium = request.POST.get('medium')
    long = request.POST.get('long')

    if short:
        percentage = 20
    elif medium:
        percentage = 50
    elif long:
        percentage = 70
    else:
        percentage = 30

    if text:
        # word_count logic (text format)

        text_count = len(text.split(' '))

        if text_count > 1000:
            messages.info(request, 'Please try with word count less than 1000')
            return render(request, 'index.html', {'len': text_count})

        elif text_count <= 200:
            messages.info(request, 'Please try with a larger text')
            return render(request, 'index.html', {'len': text_count})

        else:

            summarizer = TextSummarizer(text, percentage)
            summary, summary_count = summarizer.get_summary()

            return render(request, 'index.html', {'summary': summary, 'count': summary_count,
                                                   'len': text_count})

    elif uploaded_files:

        for i in uploaded_files:
            if i.name.endswith("jpg"):
                messages.info(request, 'Jpg format is not supported in Non-Premium Version, please checkout '
                                       'premium features')
                return render(request, 'index.html')

        if len(uploaded_files) <= 5:
            text, word_count = GetData(uploaded_files).get_data()
            if word_count > 1000:
                messages.info(request, 'Please try with word count less than 1000')
                return render(request, 'index.html')

            elif word_count <= 200:
                messages.info(request, 'Please try with a larger text')
                return render(request, 'index.html')

            else:
                summarizer = TextSummarizer(text, percentage)
                summary, summary_count = summarizer.get_summary()
                return render(request, 'index.html', {'summary': summary, 'count': summary_count,
                                                       'text_len': word_count})
        else:
            messages.info(request, 'Supported file limit is 5')
            return render(request, 'index.html')

    elif link:

        if "youtube" in link:
            messages.info(request, 'YouTube links are not supported in Non-Premium Version, checkout premium version')
            return render(request, 'index.html')
        text, word_count = GetData(link).get_data()

        if word_count > 1000:
            messages.info(request, 'Please try with word count less than 1000')
            return render(request, 'index.html')

        elif word_count <= 200:
            messages.info(request, 'Could not fetch the data')
            return render(request, 'index.html')

        else:
            summarizer = TextSummarizer(text, percentage)
            summary, summary_count = summarizer.get_summary()
            return render(request, 'index.html', {'summary': summary, 'count': summary_count,
                                                   'text_len': word_count})

    else:
        return render(request, 'index.html')


# premium version
def premium_work(request):
    global summary
    uploaded_files = request.FILES.getlist('files')
    link = request.POST.get('url')
    text = request.POST.get('text')

    short = request.POST.get('short')
    medium = request.POST.get('medium')
    long = request.POST.get('long')

    if short:
        percentage = 20
    elif medium:
        percentage = 50
    elif long:
        percentage = 70
    else:
        percentage = 30

    if text:
        # word_count logic (text format)

        text_count = len(text.split(' '))

        if text_count > 5000:
            messages.info(request, 'You exceeded your word limit')
            return render(request, 'index.html', {'len': text_count})

        elif text_count <= 200:
            messages.info(request, 'Please try with a larger text')
            return render(request, 'index.html', {'len': text_count})

        else:
            summarizer = TextSummarizer(text, percentage)
            summary, summary_count = summarizer.get_summary()
            return render(request, 'index.html', {'summary': summary, 'count': summary_count,
                                                   'len': text_count})

    elif uploaded_files:
        # word_count logic (files format)

        if len(uploaded_files) <= 10:
            text, word_count = GetData(uploaded_files).get_data()
            if word_count > 8000:
                messages.info(request, 'You exceeded your word limit')
                return render(request, 'index.html')

            elif word_count <= 200:
                messages.info(request, 'Please try with a larger text')
                return render(request, 'index.html')

            else:
                summarizer = TextSummarizer(text, percentage)
                summary, summary_count = summarizer.get_summary()
                return render(request, 'index.html', {'summary': summary, 'count': summary_count,
                                                       'text_len': word_count})
        else:
            messages.info(request, 'Supported file limit is 10')
            return render(request, 'index.html')

    elif link:
        # word_count logic (link format)

        text, word_count = GetData([link]).get_data()

        if word_count > 8000:
            messages.info(request, 'You exceeded your word limit')
            return render(request, 'index.html')

        elif word_count <= 200:
            messages.info(request, 'Couldn\'t fetch the data')
            return render(request, 'index.html')

        else:
            summarizer = TextSummarizer(text, percentage)
            summary, summary_count = summarizer.get_summary()
            return render(request, 'index.html', {'summary': summary, 'count': summary_count,
                                                   'text_len': word_count})

    else:
        return render(request, 'index.html')


# pdf downloader
def downloadPdf(request):
    global summary
    try:
        # if request.user.is_authenticated:
        buf = io.BytesIO()    #premium bypass
        c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
        textObject = c.beginText(30, 680)
        textObject.setTextOrigin(inch, inch)
        c.setTitle("CybraneX summarizer")
        textObject.setFont("Helvetica", 10)
        words = summary.split(' ')
        lines = []
        i = 0
        while i < len(words):
            lines.append(' '.join(words[i:i + 14]))
            i += 15
        for j in lines:
            textObject.textLine(j)
        c.drawText(textObject)
        c.showPage()
        c.save()
        buf.seek(0)
        return FileResponse(buf, as_attachment=True, filename='summary.pdf')
        # else:
        #     messages.info(request, 'Please login to download pdf file for your summary')
        #     return render(request, 'index.html', {'summary': summary, 'count': len(summary.split(' '))})
    except:
        messages.info(request, 'Please add something to get summary')
        return redirect('home')


# engine = pyttsx3.init()
#
#
# def create_audio(request):
#     global summary
#     engine.say(summary)
#     engine.runAndWait()
#
#     return redirect('home')
#
#
# def stop_audio(request):
#     engine.stop()
#     return redirect('home')


# word counter
def counter(request):
    return render(request, 'index.html', {'count': len(summary.split(' '))})


# authentication
def register(request):

    # if request.user.is_authenticated:
    #     print("register4")
    #     return redirect('home')
    # else:
    #     print("register5",request.method)
        if request.method =='POST':
            form = RegisterForm(request.POST)
            if User.objects.filter(email=request.POST['email']).exists() or \
                    User.objects.filter(username=request.POST['username']).exists():

                messages.error(request, 'email/username already exists try again')
                return redirect('register')

            if form.is_valid():
                new_user = form.save()
                uid = uuid.uuid4()
                pro_obj = Profile(user=new_user, token=uid)
                pro_obj.save()

                send_verification_email(new_user.email, uid)

                newsLetter = NewsLetter(mail=request.POST['email'])
                # newsLetter.save()
                messages.success(request, 'Verification email has been sent to your emai id')
                return redirect("login")
            else:
                messages.error(request,'not valid info')
        else:
            form = RegisterForm()
        return render(request, 'registration/register.html', {'form': form})


def verify_email(request, token):
    pf = Profile.objects.filter(token=token).first()
    pf.verify = True
    pf.save()
    messages.success(request, 'Account has been verified, you can login now')
    return redirect('register')


def send_verification_email(email, token):
    message = f"Click the link to verify your email account http://127.0.0.1:8000/account-verification/{token}"
    template = "Verification Email"
    email = EmailMessage(
        template,
        message,
        settings.EMAIL_HOST_USER,
        [email],
    )
    email.fail_silently = False
    email.send()


def send_email(request, html_file, email_message):
    try:
        template = render_to_string(html_file, {'username': request.POST['username']})
        email = EmailMessage(
            f"{email_message} {request.POST['username']}",
            template,
            settings.EMAIL_HOST_USER,
            [request.POST['email']],
        )
        email.fail_silently = False
        email.send()

    except Exception:
        return


def login_page(request):
    # if request.user.is_authenticated:
    #     print('login')
    #     return redirect('home')
    # else:
        if 'login' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                pro = Profile.objects.get(user=user)
                if pro.verify:
                    login(request, user)
                    print('pro')
                    return redirect('home')
                else:
                    messages.info(request, 'Your account is not verified, please verify')
                    return redirect('login')
            else:
                messages.info(request, 'Username or password is not correct')

        context = {}
        return render(request, 'registration/login.html', context)


key_id = 'rzp_test_PXmmaKTVoIsrsT'
sec_key = 'QlVzo4M7ZEU5KZBCPLdfizX8'


# Buy me a Coffee
@csrf_exempt
def coffee_payment(request):
    # if request.user.is_authenticated:
        if request.method == "POST": #premium bypass3
            name = request.POST.get('name')
            amount = int(request.POST.get('amount')) * 100
            email = request.POST.get('email')
            # create Razorpay client
            client = razorpay.Client(auth=(key_id, sec_key))

            # create order
            response_payment = client.order.create(dict(amount=amount,
                                                        currency='INR')
                                                   )

            order_id = response_payment['id']
            order_status = response_payment['status']

            if order_status == 'created':
                cold_coffee = ColdCoffee(
                    name=name,
                    amount=amount,
                    email=email,
                    order_id=order_id
                )
                cold_coffee.save()
                response_payment['name'] = name

                form = CoffeePaymentForm(request.POST or None)
                return render(request, 'payment_index.html', {'form': form, 'payment': response_payment})
    # else:
    #     messages.info(request, 'Please login or register for your payment')
    #     return render(request, 'registration\login.html')
        form = CoffeePaymentForm()
        return render(request, 'payment_index.html', {'form': form})


@csrf_exempt
def payment_status(request):
    response = request.POST
    params_dict = {
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature']
    }

    # client instance
    client = razorpay.Client(auth=(key_id, sec_key))

    try:
        status = client.utility.verify_payment_signature(params_dict)
        cold_coffee = ColdCoffee.objects.get(order_id=response['razorpay_order_id'])
        cold_coffee.razorpay_payment_id = response['razorpay_payment_id']
        cold_coffee.paid = True
        cold_coffee.save()

        # sending confirmation email
        template = render_to_string('coffee_email_template.html', {'username': request.user.username})
        email = EmailMessage(
            f"Thank You for your support {request.user.username}",
            template,
            settings.EMAIL_HOST_USER,
            [request.user.email],
        )
        email.fail_silently = False
        email.send()

        return render(request, 'payment_status.html', {'status': True})
    except:
        return render(request, 'payment_status.html', {'status': False})


# premium
@csrf_exempt
def get_subscription(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            email = request.POST.get('email')
            amount = 299 * 100
            # create Razorpay client
            client = razorpay.Client(auth=(key_id, sec_key))

            # create order
            response_payment = client.order.create(dict(amount=299 * 100,
                                                        currency='INR')
                                                     )

            order_id = response_payment['id']
            order_status = response_payment['status']

            if order_status == 'created':
                subscription = Subscription(
                    email=email,
                    order_id=order_id
                )
                subscription.save()
                response_payment['email'] = email

                form = SubscriptionForm(request.POST or None)
                return render(request, 'sub_payment.html', {'form': form, 'payment': response_payment})
    else:
        messages.info(request, 'Please login or register for your payment')
        return render(request, 'index.html')
    form = SubscriptionForm()
    return render(request, 'sub_payment.html', {'form': form})


@csrf_exempt
def subscription_status(request):
    response = request.POST
    params_dict = {
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature']
    }
    # print(params_dict)
    # client instance
    client = razorpay.Client(auth=(key_id, sec_key))
    try:
        status = client.utility.verify_payment_signature(params_dict)
        subscription = Subscription.objects.get(order_id=response['razorpay_order_id'])
        subscription.razorpay_payment_id = response['razorpay_payment_id']
        subscription.paid = True
        subscription.save()

        # sending confirmation email
        template = render_to_string('premium_email_template.html', {'username': request.user.username})
        email = EmailMessage(
            f"Premium Summarizer Payment Success! {request.user.username}",
            template,
            settings.EMAIL_HOST_USER,
            [request.user.email],
        )
        email.fail_silently = False
        email.send()

        return render(request, 'subscription_status.html', {'status': True})
    except:
        return render(request, 'subscription_status.html', {'status': False})


def get_premium(request):
    return render(request, 'premium.html')
