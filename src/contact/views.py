# from django.shortcuts import render
#
# from .forms import ContactForm
#
#
# def contact(request):
#
#     form = ContactForm(request.POST or None)
#     if form.is_valid():
#         print(request.POST)
#
#     context = {
#         'form': form
#     }
#     return render(request, 'contact.html', context)