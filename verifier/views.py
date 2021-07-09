from django.shortcuts import render
from documentverifier.block import (
    write_block,
    get_finger_print_data,
    check_integrity,
    BLOCKDIR,
)
from .forms import *
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Q
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
def registerView(request):

    template_name = "auth/register.html"

    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}! Now Login")
            form.save()
            return redirect("/login/")
        else:
            messages.warning(
                request, f"Something went wrong please fil in the form correctly"
            )
            form.save()
            return redirect("/registration/")

    else:
        form = UserRegisterForm()

    return render(request, template_name, {"form": form})


def loginView(request):

    template_name = "auth/login.html"
    if request.user.is_authenticated:
        return redirect("/dashboard/")
    if request.method == "POST":

        form = UserLoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            # str_relace = str.replace(username, '/', f'')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f"login was successful")
            return redirect("/dashboard/")
        else:
            messages.warning(
                request, f"login Error !!!! Provide Correct Username And Password"
            )
            return redirect("/")
    else:
        form = UserLoginForm()

    return render(request, template_name, {"form": form})


@login_required(login_url="/login/")
def dashboard(request):
    context = {}

    res = check_integrity()
    context["res"] = res

    context["count_docs"] = len(res)

    template_name = "pages/dashboard.html"
    return render(request, template_name, context)


@login_required(login_url="/login/")
def add_block_doc(request):
    template_name = "pages/addBlock.html"
    context = {}
    qs = Institution.objects.all()

    context["qs"] = qs

    if request.method == "POST":
        sirname = request.POST.get("sirname")
        othername = request.POST.get("othername")

        student_name = f"{sirname} {othername}"
        id_number = request.POST.get("id_number")
        kra_pin = request.POST.get("kra_pin")
        email_address = request.POST.get("email_address")
        huduma_number = request.POST.get("huduma_number")
        profile_url = request.FILES["profile_url"]
        # institution_name = request.POST.get("institution_name")
        institution_id = request.POST.get("institution_id")
        date_of_graduation = request.POST.get("date_of_graduation")
        course = request.POST.get("course")
        file_url = request.FILES["file_url"]
        verified = True

        # print(request.POST)
        # print(request.FILES)

        DocumentBlockModel.objects.create(
            name=student_name,
            id_number=id_number,
            kra_pin=kra_pin,
            email_address=email_address,
            huduma_number=huduma_number,
            profile_url=profile_url,
            institution_id=institution_id,
            date_of_graduation=date_of_graduation,
            course=course,
            file_url=file_url,
            verified=verified,
        )

        newBlock = DocumentBlockModel.objects.latest("id")

        write_block(
            student_name= newBlock.name,
            id_number=newBlock.id_number,
            kra_pin=newBlock.kra_pin,
            email_address=newBlock.email_address,
            huduma_number=newBlock.huduma_number,
            profile_url= newBlock.profile_url.url,
            institution_name=newBlock.institution.institution_name,
            institution_id=newBlock.institution.id,
            date_of_graduation= newBlock.date_of_graduation,
            course= newBlock.course,
            file_url=  newBlock.file_url.url,
            verified= newBlock.verified,
        )

    return render(request, template_name, context)


def verify(request):

    template_name = "pages/verify.html"

    context = {}

    if request.method == "POST":
        hash_finger_pring = request.POST.get("hash_finger_pring")

        res = get_finger_print_data(hash_finger_pring=hash_finger_pring)

        context["res"] = res

    return render(request, template_name, context)


def homepage(request):

    template_name = "pages/homepage.html"

    # print(BLOCKDIR)

    return render(request, template_name, context={})



def loguotView(request): 
    logout(request)  
    messages.success(request, f'You Have logout !!!')
    return redirect('/login/')