from django.shortcuts import render,redirect
from .models import School,Admin,Teacher,Student
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User     
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request,'classroom/home.html')

def s_login(request):
    context = {}
    if request.method=="POST":
        t_id = request.POST["stdnt_id"]
        username=request.POST["stdnt_uname"]
        password=request.POST["stdnt_pswd"]

        s = Student.objects.filter(school_id_id = t_id, email = username)
        if s.count() == 1:
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('dashboard')
            else:
                context['error'] = "Please provide valid credentials.."
                return render(request,'classroom/student_login.html',context)
        else:
            context['error'] = "You are not Student of this school"
            return render(request,'classroom/student_login.html',context)
    return render(request,'classroom/student_login.html')

@login_required(login_url='t_login')
def stdnt_registration(request):
    status = isTeacher(request)
    if status == True:
            
        context = {}
        if request.method == 'POST':
            f_name = request.POST['stdnt_fname']
            l_name = request.POST['stdnt_lname']
            contact = request.POST['stdnt_contct']
            standard = request.POST['stdnt_class']
            email = request.POST['stdnt_mail']
            password = request.POST['psw']

            c = User.objects.filter(username=email)

            if c.count() > 0:
                context['error'] = "This username/email exists already, Try another one"
                return render(request,'classroom/student_registration.html',context)
            else:
                stdnt = User.objects.create_user(username = email, email=email, password=password,first_name = f_name, last_name=l_name)
                stdnt.save()
                t_email = request.user.username
                s = Teacher.objects.get(email = t_email)

                student = Student(email = email, contact_number = contact, school_id = s.school_id,user = stdnt,standard=standard)
                student.save()
                return redirect('t_dash')
        return render(request,'classroom/student_registration.html',context)
    else:
        return redirect('home')


def t_login(request):
    context = {}
    if request.method=="POST":
        t_id = request.POST["i_id"]
        username=request.POST["t_uname"]
        password=request.POST["t_pswd"]

        s = Teacher.objects.filter(school_id_id = t_id,email = username)
        if s.count() == 1:
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('t_dash')
            else:
                context['error'] = "Please provide valid credentials.."
                return render(request,'classroom/teacher_login.html',context)
        else:
            context['error'] = "You are not Teacher of this school"
            return render(request,'classroom/teacher_login.html',context)

    return render(request,'classroom/teacher_login.html')

def a_login(request):
    context = {}
    if request.method=="POST":
        s_id = request.POST["s_id"]
        username=request.POST["username"]
        password=request.POST["password"]

        s = Admin.objects.get(school_id_id = s_id)
        if s.email == username:
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('a_dash')
            else:
                context['error'] = "Please provide valid credentials.."
                return render(request,'classroom/admin_login.html',context)
        else:
            context['error'] = "You are not Admin of this school"
            return render(request,'classroom/admin_login.html',context)

    return render(request,'classroom/admin_login.html',context)

@login_required(login_url='s_login')
def s_dash(request):
    context = {}
    context['message'] = "Welcome to E-School"
    return render(request,'classroom/dashboard.html',context)

@login_required(login_url='t_login')
def t_dash(request):
    return render(request,'classroom/t_dash.html')
@login_required(login_url='a_login')
def a_dash(request):
    return render(request,'classroom/a_dash.html')

@login_required(login_url='a_login')
def t_register(request):
    context = {}
    if request.method == 'POST':
        f_name = request.POST['t_fname']
        l_name = request.POST['t_lname']
        contact = request.POST['t_contct']
        email = request.POST['t_mail']
        password = request.POST['psw']

        c = User.objects.filter(username=email)

        if c.count() > 0:
            context['error'] = "This username/email exists already, Try another one"
            return render(request,'classroom/teacher_registration.html',context)
        else:
            t = User.objects.create_user(username = email, email=email, password=password,first_name = f_name, last_name=l_name)
            t.save()
            admin_email = request.user.username
            s = School.objects.get(email = admin_email)
            teacher = Teacher(email = email, contact_number = contact, school_id = s,user = t)
            teacher.save()
            return redirect('a_dash')

    return render(request,'classroom/teacher_registration.html')

def s_register(request):
    if request.method == 'POST':
        name = request.POST["s_name"]
        address = request.POST["s_addrs"]
        city = request.POST["s_city"]
        state = request.POST["s_state"]
        contact_number = request.POST["s_contct"]
        email = request.POST["s_mail"]
        password = request.POST["psw"]

        user = User.objects.create_user(username = email, email = email, password = password)
        user.save()

        login(request,user)


        school = School(name = name, email = email, address = address, 
                                        city = city, state = state, contact_number = contact_number)
        school.save()

        u = request.user
        s = School.objects.get(email = email)
        admin = Admin(user = u, school_id = s, email = email)
        admin.save()
        return render(request,'classroom/a_dash.html')
    return render(request,'classroom/register_school.html')

@login_required(login_url='/')
def session_logout(request):
    logout(request)
    return redirect('a_login')


def isTeacher(request):
    umail = request.user.username
    t = Teacher.objects.filter(email = umail)
    if t.count() == 1:
        return True
    else:
        return False
