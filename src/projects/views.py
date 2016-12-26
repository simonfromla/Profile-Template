from contact.forms import ContactForm
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect


#If going to qs, must import model to qs
from .models import Project, Image


# Create your views here.

def projects_home(request):

    # order by active and neg -publish date
    # queryset_list = Project.objects.order_by("-timestamp")
    # if request.user.is_staff or request.user.is_superuser:
    #     queryset_list = Project.objects.all()
    # context = {
    #     'project_list': queryset_list
    # }

    # instance = get_object_or_404(Project, slug=slug)


    # pic_qs = Image.objects.get(name__icontains='head')
    currentUrl = request.get_full_path()

    form = ContactForm(request.POST or None)
    if form.is_valid():
        # print(request.POST)
        # dont just straight up grab data by using 'request.POST' - insecure. Clean it.
        # print(form.cleaned_data['comment'])
        form_email = form.cleaned_data['email']
        form_comment = form.cleaned_data['comment']
        form_full_name = form.cleaned_data['name']
        subject = 'Site contact form'
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email, 'retsnomis@gmail.com']
        message = '%s:\n%s\nvia %s' %(
            form_full_name,
            form_comment,
            form_email)
        send_mail(
            subject,
            message,
            from_email,
            to_email,
            fail_silently=True)

        messages.success(request, 'Message Submitted\nI\'ll be getting back to you shortly.')
        return HttpResponseRedirect('/')
    # else:
    #     return redirect('/#contact')

        # return HttpResponseRedirect(instance.objects.get_absolute_url())


    recent_projects = []
    for i in range(0, 6):
        try:
            recent_projects.append(Project.objects.order_by('-timestamp')[i])
        except IndexError:
            break
    context = {
        'projects': recent_projects,
        'form': form,
        'currentUrl': currentUrl,
        # 'pic': pic_qs,
    }
    return render(request, 'projects_home.html', context)


def project_detail(request, slug):
    instance = get_object_or_404(Project, slug=slug)

    form = ContactForm(request.POST or None)
    if form.is_valid():
        print(request.POST)

    context = {
        'instance':instance,
        'form': form
    }
    return render(request, 'project_detail.html', context)
