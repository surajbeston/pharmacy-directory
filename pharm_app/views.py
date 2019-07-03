from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.template.context_processors import csrf
from pharm_app.forms import  pharma_signup_form, pharma_signin_form, activation_form, medicine_form, composition_form, user_form
from .models import pharma, signin_info, activation_info, download_record, medicine_info, medicine_composition, keys_key

from pytz import timezone
from django.utils.encoding import smart_str
from datetime import datetime, timedelta
import hashlib, binascii, os
import random, string

import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

from twilio.rest import Client

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup

def medicine_search(request):
    if request.method == "POST":
        form = user_form(request.POST)
        if form.is_valid():
            search_medicine = request.POST['medicine'].lower()
            medicine_obj = medicine_info.objects.get(medicine = search_medicine)
            #getting all the compositions of the given medicine
            compositions = medicine_obj.medicine_composition_set.all()
            clone_compositions = compositions
            arr_score = []
            arr_medicine = []
            arr_medicine_name = []
            if len(compositions) < 1:
                return HttpResponse("The medicine you serached could not be found. Check the characters again or go for a new lookup.")
            for composition in compositions:
                #getting the similar compositions objects relating to different medicines
                comp_medicines = medicine_composition.objects.filter(composition = composition.composition)
                medicines = []
                for comp_medicine in comp_medicines:
                    #getting different medicines to the given composition
                    medicines.append(medicine_info.objects.get(id = comp_medicine.medicine_id))
                for medicine in medicines:
                    if medicine.medicine in arr_medicine_name:
                        continue
                    if medicine.medicine == search_medicine:
                        continue
                    #all compositions of a medicine
                    med_compositions = medicine.medicine_composition_set.all()
                    total_score = 0
                    #iterating through original composition
                    for clone_composition in clone_compositions:
                        clone_composition_text = clone_composition.composition
                        is_there  = False
                        #iterating through the picked medicine
                        for med_composition in med_compositions:
                            med_composition_text = med_composition.composition
                            if clone_composition_text == med_composition_text:
                                weightage_difference = clone_composition.weightage - med_composition.weightage
                                if weightage_difference < 0:
                                    weightage_difference = weightage_difference * -1
                                total_score = total_score + weightage_difference
                                is_there  = True
                                break
                        if is_there == "False":
                            total_score = total_score + clone_composition.weightage

                    arr_medicine.append(medicine)
                    arr_score.append(total_score)
                    arr_medicine_name.append(medicine.medicine)
            for i in range(len(arr_medicine)):
                for j in range(len(arr_medicine)-1):
                    if arr_score[j] > arr_score[j+1]:
                        score_moderator = arr_score[j]
                        medicine_moderator = arr_medicine[j]
                        medicine_name_moderator = arr_medicine_name[j]

                        arr_score[j] = arr_score[j+1]
                        arr_medicine[j] = arr_medicine[j+1]
                        arr_medicine_name[j] = arr_medicine_name[j+1]

                        arr_score[j+1] = score_moderator
                        arr_medicine[j+1] = medicine_moderator
                        arr_medicine_name[j+1] = medicine_name_moderator
            print(arr_medicine_name)
            composition_arr = []
            for medicine in arr_medicine_name:
                med_obj = medicine_info.objects.get(medicine = medicine)
                comps = med_obj.medicine_composition_set.all()
                composition_arr.append(comps)
            for compositions in composition_arr:
                for composition in compositions:
                    print(composition.composition)
            dict = user_form(request.POST)
            dict = {'form': form}
            dict.update(csrf(request))
            dict.update({'medicines': composition_arr})
            return render_to_response('search_medicine.html', dict, RequestContext(request))
        else:
            print(form.errors)
            return HttpResponse("Form Validation Failed. Check logs for details.")
    else:
        form = user_form()
        dict = {'form':form}
        dict.update(csrf(request))
        return render_to_response("search_medicine.html", dict, RequestContext(request))

def home(request):
    print("reached here 1")
    pharma = request.session['pharmaceutical']
    if request.method == "POST":
        print("reached here 2")
        form = medicine_form(request.POST, request.FILES)
        if form.is_valid():
            form_medicine = request.POST['medicine'].lower()
            objs = medicine_info.objects.all()
            for obj in objs:
                if obj.medicine == form_medicine:
                    return HttpResponse("Medicine with this name is already registered.")
            print("Reached here 3")
            file = request.FILES["file"]
            f = ''
            for chunk in file.chunks():
                f = f + chunk.decode()
            print("Reached here 4")
            print(f)
            id = decrypter(f, request.session['pharmaceutical'])
            if id != "Key Did Not Match":
                obj = medicine_info()
                obj.identification = id
                obj.medicine = form_medicine
                obj.info = 'By: ' +pharma
                obj.save()
                key = ''
                token = ''
                all_char = string.ascii_letters + string.digits*4
                all_digits = string.digits
                for a in range(100):
                    key = key + all_char[random.randrange(92)]
                    token =token + all_digits[random.randrange(10)]
                obj = keys_key()
                obj.key = key
                obj.token = token
                obj.save()
                request.session['key'] = key
                request.session['medicineEntry_key'] = token
                request.session['medicine'] = form_medicine
                return redirect("/add-composition/"+key)
            else:
                return HttpResponse("File seems to be invalid")
        else:
            print(form.errors)
            return HttpResponse("Form validation failed. Check logs for errors.")
    elif request.method == 'GET':
        form = medicine_form()
        dict = {'form': form, 'pharma': pharma}
        dict.update(csrf(request))
        return render_to_response('pharma_home.html', dict, RequestContext(request))

def add_composition(request, key):
    pharma = request.session['pharmaceutical']
    obj = keys_key.objects.get(key = key)
    if request.session['medicineEntry_key'] == obj.token:
        if request.method == "POST":
            form = composition_form(request.POST)
            if form.is_valid():
                obj = form.save(commit = False)
                med_obj = medicine_info.objects.get(medicine = request.session['medicine'])
                comp = obj.composition
                obj.medicine = med_obj
                obj.composition = comp.lower()
                obj.save()
                return redirect("/add-composition/"+request.session['key'])
            else:
                print(form.errors)
                return HttpResponse("The form submitted was invalid.")
        else:
            form = composition_form()
            print(form)
            dict = {'form': form, 'medicine': request.session['medicine'], 'key': request.session['key']}
            print(dict)
            dict.update(csrf(request))
            return render_to_response('add_composition.html', dict, RequestContext(request))
    else:
        return HttpResponse("Link seems to be tampered.")

def delete(request, key):
    try:
        pharma = request.session['pharmaceutical']
        obj = keys_key.objects.get(key = key)
        if request.session['medicineEntry_key'] == obj.token:
            obj = medicine_info.objects.get(medicine = request.session["medicine"])
            print(obj)
            obj.delete()
            del request.session['medicineEntry_key'], request.session['medicine']
            return redirect("/home")
        else:
            return HttpResponse("The link has been tampered.")
    except:
        return redirect("/signin-pharma")

def finish(request, key):
    try:
        pharma = request.session['pharmaceutical']
        obj = keys_key.objects.get(key = key)
        if request.session['medicineEntry_key'] == obj.token:
            obj = medicine_info.objects.get(medicine = request.session["medicine"])
            obj.added_composition = True
            obj.save()
            del request.session['medicineEntry_key'], request.session['medicine']
            return redirect("/home")
        else:
            return HttpResponse("The link has been tampered.")
    except:
        return redirect("/signin-pharma")

def signup_pharma(request):
    if request.method == "POST":
        form = pharma_signup_form(request.POST)
        if form.is_valid():
            all_pharma = pharma.objects.all()
            data = request.POST
            for pharm in all_pharma:
                if data.get("email") == pharm.email:
                    return HttpResponse("Email is already registered.")
                if data.get("mobile") == pharm.mobile:
                    return HttpResponse("Mobile is already registered.")
                if data.get("organization_name") == pharm.organization_name:
                    return HttpResponse("Organization Name is already registered.")
            a = form.save(commit = False)
            a.password = hash_password(data.get("password"))
            a.entry_id = entry_id_generator()
            a.encryption_key = encryption_key_generator(a.password)
            filename_ini = ''
            for char in data.get("organization_name"):
                if char != " ":
                    filename_ini = filename_ini + char
                else:
                    break
            a.authentication_file = filename_ini + '.pharma'
            encrypter(a.encryption_key, a.entry_id, filename_ini)
            a.save()
            credentials = activation_initiator(data.get("organization_name"))
            send_sms(credentials[0], data.get("mobile"))
            send_email(data.get("email"), data.get("organization_name"), credentials[1])
            return HttpResponse("We have sent an email with a link to your mailing address, also we have sent a code to your mobile. You should use those to verify yourself.")
        else:
            print (form.errors)
            return HttpResponse('Form validation failed. Check logs for more detail.')
    else:
        form = pharma_signup_form()
        dict = {'form': form}
        dict.update(csrf(request))
        return render_to_response("pharma_signup.html", dict, RequestContext(request))

def signin_pharma(request):
    if request.method == "POST":
        form = pharma_signin_form(request.POST)
        if form.is_valid():
            user = pharma.objects.get(email = request.POST.get("email"))
            print(user.organization_name)
            print(request.POST.get("password"))
            if verify_password(user.password, request.POST.get("password")) == True:
                request.session['pharmaceutical'] = user.organization_name
                request.session.set_expiry(1800)
                return redirect('/home')
            else:
                return HttpResponse("Not Verified.")
            return HttpResponse('On with test.')
        else:
            print (form.errors)
            return HttpResponse('Form validation failed. Check logs for more detail.')
    else:
        form = pharma_signin_form()
        dict = {'form': form}
        dict.update(csrf(request))
        return render_to_response("pharma_signin.html", dict, RequestContext(request))

def activate(request, activation_code):
    if request.method == "GET":
        objs = activation_info.objects.all()
        for obj in objs:
            if obj.link_randcode == activation_code:
                form = activation_form()
                dict = {'name' : obj.pharmaceutical.organization_name, 'form': form}
                dict.update(csrf(request))
                return render_to_response('code_activation.html', dict, RequestContext(request))
        return HttpResponse("The link is tampered.")
    elif request.method == "POST":
        form = activation_form(request.POST)
        if form.is_valid():
            obj = activation_info.objects.get(link_randcode = activation_code)
            if str(obj.pin) == request.POST.get("pin"):
                print("Entered here")
                name = obj.pharmaceutical.organization_name
                obj = pharma.objects.get(organization_name = name)
                filename = obj.authentication_file
                file_path = 'authentication_files/'
                file_name = file_path + filename
                obj.activated = True
                obj.save()
                key = ''
                all_char = string.ascii_letters +string.digits * 4
                for a in range(100):
                    key = key + all_char[random.randrange(92)]
                obj = download_record()
                obj.key = key
                obj.filename = filename
                obj.file_path = file_name
                tz = timezone('Asia/Kathmandu')
                obj.expiry_datetime = datetime.now(tz) + timedelta(minutes = 5)
                obj.save()
                return redirect('/auth_download/' + key)

            else:
                form = activation_form()
                dict = {'name' : obj.pharmaceutical.organization_name, 'form': form, 'message': 'PIN was incorrect.'}
                dict.update(csrf(request))
                return render_to_response('code_activation.html', dict, RequestContext(request))
        else:
            print(form.errors)
            return HttpResponse("The form data was not valid. Check logs for additional information.")

def auth_download(request, key):
    if request.method == "POST":
        obj = download_record.objects.get(key=key)
        tz = timezone('Asia/Kathmandu')
        time =  obj.expiry_datetime - datetime.now(tz)
        print(obj.expiry_datetime)
        print(datetime.now(tz))
        print(time.seconds)
        if time.seconds >= 1 and time.seconds <= 360 and obj.downloaded == False:
            with open(obj.file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type='application/force-download')
                response['Content-Disposition'] = 'attachment; filename= %s' % smart_str(obj.filename)
                obj.downloaded = True
                obj.save()
                return response
        else:
            return HttpResponse("The download file expired. Contact the team to revive the file.")
    else:
        dict = {}
        dict.update(csrf(request))
        return render_to_response("auth_download.html", dict, RequestContext(request))

def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                salt, 150000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(stored_password, provided_password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  150000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

def entry_id_generator():
    entry_id = ''
    all_char = string.ascii_letters + string.digits * 3
    for char in range(random.randrange(20, 100)):
        entry_id = entry_id + all_char[random.randrange(82)]
    return entry_id

def encryption_key_generator(password_hash):
    password_provided = password_hash
    password = password_provided.encode()
    salt = b'Ter@Mel0'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=150000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password)).decode()
    return key

def encrypter(key, message, filename):
    f = Fernet(key.encode())
    encrypted = f.encrypt(message.encode())
    encrypted = encrypted.decode()
    with open('authentication_files/'+filename + '.pharma', 'w' ) as f:
        f.write(encrypted)

def decrypter(encrypted, pharm):
    obj = pharma.objects.get(organization_name = pharm)
    try:
        f = Fernet(obj.encryption_key.encode())
        decrypted = f.decrypt(encrypted.encode())
        return decrypted.decode()
    except:
        return "Key Did Not Match"

def activation_initiator(org_name):
    digits = string.digits
    all_characters = string.ascii_letters + string.digits * 3
    pin = ''
    randcode = ''
    for a in range(6):
        pin = pin + digits[random.randrange(10)]
    for a in range(50):
        randcode = randcode + all_characters[random.randrange(82)]
    pharm = pharma.objects.get(organization_name = org_name)
    obj = activation_info()
    obj.pharmaceutical = pharm
    obj.pin = pin
    obj.link_randcode = randcode
    obj.save()
    return [pin, randcode]

def send_sms(pin, mobile):
    account_sid = 'ACcf401c612d39d28e0d1e374ef541df27'
    auth_token = '7eb29117c4053bedddac350df49aafec'
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                         body=pin,
                         from_='+12055649922',
                         to='+9779819604815'
                     )
    print(message.sid)

def send_email(receiver_email, username, link_ext):
    sender_email = "surajbeston@gmail.com"
    receiver_email = "getsurajjha@gmail.com"
    password = "6874@@&&Neb"
    message = MIMEMultipart("alternative")
    message["Subject"] = "Activate your Quiz Nepal Account."
    message["From"] = sender_email
    message["To"] = receiver_email

    report_file = open('activate.html')
    html = report_file.read()

    soup = BeautifulSoup(html, features="html.parser")
    p_tag = soup.p
    new_tag = soup.new_tag("b")
    new_tag.string = username
    p_tag.b.replace_with(new_tag)
    a_tag = soup.a
    print(link_ext)
    a_tag['href'] = a_tag['href'].replace("blaw", link_ext)
    html= str(soup)

    message.attach(MIMEText(html, "html"))
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
    report_file.close()
