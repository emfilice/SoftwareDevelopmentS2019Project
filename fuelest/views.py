from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django import forms
from django.utils import timezone
from django.contrib import messages
from fuelest.forms import ProfileForm, AddressForm, QuoteForm
from django.contrib.auth.forms import UserCreationForm

from .models import UserInfo, Address, Quote

from datetime import date

class HomePageView(TemplateView):
    template_name = 'fuelest/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userprof = UserInfo.objects.filter(username=User.objects.get(username=self.request.user.username))
        profile_made = (len(userprof) != 0)
        context['profile_made'] = profile_made
        return context

class ProfileView(TemplateView):
    template_name = 'fuelest/profile.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        curuser = ""
        if self.request.user.is_authenticated:
            curuser = self.request.user.username
        userprof = UserInfo.objects.filter(username=User.objects.get(username=curuser))
        profile_made = True
        if len(userprof) == 0:
            profile_made = False
        context['profile_made'] = profile_made
        if profile_made:
            userprof = UserInfo.objects.get(username=User.objects.get(username=curuser))
            print(userprof)
            context['fullname'] = userprof.name
            useraddr = Address.objects.get(id=userprof.address.id)
            context['addr1'] = useraddr.address1
            context['addr2'] = useraddr.address2
            context['city'] = useraddr.city
            context['state'] = useraddr.state
            context['zip'] = useraddr.zip
        return context

class SuccessView(TemplateView):
    template_name = 'fuelest/quotesuccess.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userprof = UserInfo.objects.filter(username=User.objects.get(username=self.request.user.username))
        profile_made = (len(userprof) != 0)
        context['profile_made'] = profile_made
        return context


class QuoteListView(ListView):
    template_name = "fuelest/quotehist.html"
    paginate_by = 20
    model = Quote
    def get_queryset(self):
        return Quote.objects.filter(
            user=User.objects.get(username=self.request.user.username),
        )
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userprof = UserInfo.objects.filter(username=User.objects.get(username=self.request.user.username))
        profile_made = (len(userprof) != 0)
        context['profile_made'] = profile_made
        addr = Address.objects.get(id=UserInfo.objects.get(username=User.objects.get(username=self.request.user.username)).address.id)
        context['addr'] = addr
        return context

def profile_model(request):
    if request.method == "POST":
        profform = ProfileForm(request.POST)
        profile_valid = profform.is_valid()
        addrform = AddressForm(request.POST)
        addr_valid = addrform.is_valid()
        if addr_valid and profile_valid:
            if len(UserInfo.objects.filter(username=User.objects.get(username=request.user.username))) != 0:
                b = UserInfo.objects.get(username=User.objects.get(username=request.user.username))
                b.name = profform['name'].value()
                a = Address.objects.get(id=b.address.id)
                a.address1 = addrform['address1'].value()
                a.address2 = addrform['address2'].value()
                a.city = addrform['city'].value()
                a.state = addrform['state'].value()
                a.zip = addrform['zip'].value()
                a.save()
            else:
                a = addrform.save()
                b = profform.save(commit=False)
            b.username = User.objects.get(username=request.user.username)
            b.address = a
            b.save()
            return redirect("profile")
    else:
        profform = ProfileForm()
        addrform = AddressForm()
    return render(request, "fuelest/editprofile.html", {'profform': profform, 'addrform': addrform})

def register_model(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        form_valid = form.is_valid()
        if form_valid:
            a = form.save()
            return redirect("/")
    else:
        form = UserCreationForm()
    return render(request, "fuelest/register.html", {'form': form})

def calculate_price():
    price = 2.0
    return price

def quote_model(request):
    addr = Address.objects.get(id=UserInfo.objects.get(username=User.objects.get(username=request.user.username)).address.id)
    pr = calculate_price();
    userprof = UserInfo.objects.filter(username=User.objects.get(username=request.user.username))
    profile_made = (len(userprof) != 0)
    gal_err = ''
    date_err = ''
    pr_err = ''
    tot_err = ''
    gals = None
    del_date = None
    if request.method == "POST":
        gals = request.POST.get('gallons')
        del_date = request.POST.get('delivery_date')
        form_valid = True
        if gals in ['', None] or int(gals) <= 0:
            form_valid = False
            gal_err = "Please enter a positive integer."
        date_s = del_date
        if date_s == '':
            form_valid = False
            date_err = "Please enter a valid future date."
        else:
            try:
                dateT = date.fromisoformat(date_s)
                if dateT < date.today():
                    form_valid = False
                    date_err = "Please enter a valid future date."
            except ValueError:
                form_valid = False
                date_err = "Please enter a valid future date."
        if request.POST.get('pr') == '--':
            form_valid = False
            pr_err = "Please generate price before continuing."
        if request.POST.get('tot') == '--':
            form_valid = False
            tot_err = "Please generate price before continuing."
        if form_valid:
            a = form.save(commit=False)
            a.address = addr
            a.user = User.objects.get(username=request.user.username)
            a.price = pr
            a.total = a.gallons * a.price
            a.save()
            return redirect("quotesuccess")
    else:
        form = QuoteForm()
    print(pr_err)
    return render(request, "fuelest/fuelquote.html", {"addr": addr,
                                                        "pr": pr,
                                                        "profile_made": profile_made,
                                                        "gal_err": gal_err,
                                                        "date_err": date_err,
                                                        "pr_err": pr_err,
                                                        "tot_err": tot_err,
                                                        "gals": gals,
                                                        "del_date": del_date})
