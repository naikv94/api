from multiprocessing import context
from pyexpat import model
from re import template
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView
from .forms import SignUpForm, UserForm, ProfileForm, CompanyForm, ContactForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import messages
from apps.userprofile.models import Profile
from .models import Company, Contact
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q


class HomeView(TemplateView):
    template_name = 'common/home.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'common/dashboard.html'
    login_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        
        # Add in a QuerySet of all the books
        context['book_list'] = self.request.user
        print('uid',self.request.user.id)
        companies = Company.objects.all()
        contacts = Contact.objects.all()
        if companies or contacts:
            context = {'companies':len(companies),'contacts':len(contacts)}
        return context


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('home')
    template_name = 'common/register.html'


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'common/profile.html'
    login_url = reverse_lazy('home')


class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    user_form = UserForm
    profile_form = ProfileForm
    template_name = 'common/profile-update.html'
    login_url = reverse_lazy('home')

    def post(self, request):

        post_data = request.POST or None
        file_data = request.FILES or None

        user_form = UserForm(post_data, instance=request.user)
        profile_form = ProfileForm(
            post_data, file_data, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully!')
            return HttpResponseRedirect(reverse_lazy('profile'))

        context = self.get_context_data(
            user_form=user_form,
            profile_form=profile_form
        )

        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class CompanyUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'common/companyUpdate.html'
    success_url = reverse_lazy('companies')
    login_url = reverse_lazy('home')
    success_message = 'Details updated sucessfully'

class CompanyDeleteView(LoginRequiredMixin, DeleteView):
    model = Company
    success_url = reverse_lazy('companies')
    login_url = reverse_lazy('home')
    template_name = 'common/confirm_delete.html'

class ContactUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = 'common/contactUpdate.html'
    success_url = reverse_lazy('contacts')
    login_url = reverse_lazy('home')
    success_message = 'Contact updated sucessfully'

class ContactDeleteView(LoginRequiredMixin,SuccessMessageMixin, DeleteView):
    model = Contact
    success_url = reverse_lazy('contacts')
    login_url = reverse_lazy('home')
    template_name = 'common/confirm_delete.html'
    success_message = 'Contact Deleted'

class ContactListView(LoginRequiredMixin,ListView,FormMixin):
    model = Contact
    login_url = reverse_lazy('home')
    template_name = 'common/contacts.html'
    paginate_by  = 4
    form_class = ContactForm

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            data = self.model.objects.filter(Q(name__icontains=query)| Q(company__name__icontains=query))
        else:
            data = self.model.objects.all()
        return data

    def post(self, request):
        self.object_list = self.get_queryset()
        post_data = request.POST or None
        contact_form = ContactForm(post_data)

        if contact_form.is_valid():
            contact_form.save()
            messages.success(request, 'Contact added successfully!')
            return HttpResponseRedirect(reverse_lazy('contacts'))
        context = self.get_context_data(form = contact_form)
        return self.render_to_response(context)

class CompanyListView(LoginRequiredMixin,ListView,FormMixin):
    model = Company
    login_url = reverse_lazy('home')
    template_name = 'common/companies.html'
    paginate_by  = 4
    form_class = CompanyForm

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            data = self.model.objects.filter(Q(name__icontains=query)| Q(country__icontains=query))
        else:
            data = self.model.objects.all()
        return data

    def post(self, request):
        self.object_list = self.get_queryset()
        post_data = request.POST or None
        company_form = CompanyForm(post_data)
        print('c user',self.request.user.id)
        if company_form.is_valid():
            print('form data', company_form)
            company_form.save()
            messages.success(request, 'Company added successfully!')
            return HttpResponseRedirect(reverse_lazy('companies'))
        context = self.get_context_data(form = company_form)
        return self.render_to_response(context)
