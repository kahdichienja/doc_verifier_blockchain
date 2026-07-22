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
            return redirect("login")

        messages.warning(
            request, "Something went wrong, please fill in the form correctly"
        )
        return render(request, template_name, {"form": form})

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
        date_of_birth = request.POST.get("date_of_birth")
        profile_url = request.FILES.get("profile_url")

        institution_id = request.POST.get("institution_id")
        faculty_school = request.POST.get("faculty_school")
        date_of_graduation = request.POST.get("date_of_graduation")
        course = request.POST.get("course")
        student_reg_number = request.POST.get("student_reg_number")
        certificate_number = request.POST.get("certificate_number")
        classification = request.POST.get("classification")

        file_url = request.FILES.get("file_url")
        transcript_file = request.FILES.get("transcript_file")
        verified = True

        newBlock = DocumentBlockModel.objects.create(
            name=student_name,
            id_number=id_number,
            kra_pin=kra_pin,
            email_address=email_address,
            huduma_number=huduma_number,
            date_of_birth=date_of_birth,
            profile_url=profile_url,
            institution_id=institution_id,
            faculty_school=faculty_school,
            date_of_graduation=date_of_graduation,
            course=course,
            student_reg_number=student_reg_number,
            certificate_number=certificate_number,
            classification=classification,
            file_url=file_url,
            transcript_file=transcript_file,
            verified=verified,
        )

        write_block(
            student_name=newBlock.name,
            id_number=newBlock.id_number,
            kra_pin=newBlock.kra_pin,
            email_address=newBlock.email_address,
            huduma_number=newBlock.huduma_number,
            date_of_birth=newBlock.date_of_birth or "",
            profile_url=newBlock.profile_url.url if newBlock.profile_url else "",
            institution_name=newBlock.institution.institution_name,
            institution_id=newBlock.institution.id,
            faculty_school=newBlock.faculty_school or "",
            date_of_graduation=newBlock.date_of_graduation or "",
            course=newBlock.course or "",
            student_reg_number=newBlock.student_reg_number or "",
            certificate_number=newBlock.certificate_number or "",
            classification=newBlock.classification or "",
            file_url=newBlock.file_url.url if newBlock.file_url else "",
            transcript_url=newBlock.transcript_file.url if newBlock.transcript_file else "",
            verified=newBlock.verified,
        )

        messages.success(request, "Document Block Added Successfully!")
        return redirect("/dashboard/")

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