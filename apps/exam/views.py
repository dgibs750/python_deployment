from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import User, Quote
from django.contrib import messages


def index(request):
    if 'login_token' not in request.session or request.session['login_token'] < 1:
        request.session['login_token'] = 0
        return render(request, 'exam/index.html')
    elif request.session['login_token'] > 0:
        return redirect('/quotes/')


def register_form(request):
    if 'login_token' not in request.session or request.session['login_token'] < 1:
        request.session['login_token'] = 0
        return render(request, 'exam/register_form.html')
    elif request.session['login_token'] > 0:
        return redirect('/quotes/')


def login(request):
    print(request.POST)
    if request.method == "POST":
        user = User.objects.login_validations(request.POST)
        if 'uid' in user:
            request.session['login_token'] = 1
            request.session['first_name'] = User.objects.get(id=int(user['uid'])).first_name
            request.session['last_name'] = User.objects.get(id=int(user['uid'])).last_name
            request.session['email'] = User.objects.get(id=int(user['uid'])).email
            request.session['type'] = 'logged in'
            request.session['uid'] = user['uid']
            print(request.session)
            return redirect('/quotes/')

        else:
            for key, value in user.items():
                messages.error(request, value)
            return redirect('/')


def add_user(request):
    print(request.POST)
    if request.method == 'POST':
        user = User.objects.reg_validations(request.POST)
        if 'uid' in user:
            request.session['login_token'] = 1
            request.session['first_name'] = User.objects.get(id=int(user['uid'])).first_name
            request.session['last_name'] = User.objects.get(id=int(user['uid'])).last_name
            request.session['email'] = User.objects.get(id=int(user['uid'])).email
            request.session['type'] = 'registered'
            request.session['uid'] = user['uid']
            print(request.session)
            return redirect('/quotes/')
        else:
            for key, value in user.items():
                messages.error(request, value)
            return redirect('/register_form/')


def dashboard(request):
    return render(request, 'exam/dashboard.html', {'quotes': Quote.objects.all()})


def userQuotes(request, num):
    x = {
        'name': User.objects.get(id=num).first_name +' '+User.objects.get(id=num).last_name,
        'uploaded': User.objects.get(id=num).quotes.all()
    }
    return render(request, 'exam/userQuotes.html', x)


def myAccount(request, num):
    return render(request, 'exam/profile.html')


def add_quote(request):
    if request.method == "POST":
        err = Quote.objects.quote_validations(request.POST)
        if not err:
            quote = Quote.objects.create(author=request.POST['author'], quote=request.POST['quote'], uploaded_by=User.objects.get(id=request.session['uid']))
            return redirect('/')
        else:
            for key, value in err.items():
                messages.error(request, value)
            return redirect('/')


def like(request, num):
    quote = Quote.objects.get(id=num)
    user = User.objects.get(id=request.session['uid'])
    quote.liked_by.add(user)
    return redirect('/')


def delete(request, num):
    Quote.objects.get(id=num).delete()
    return redirect('/')


def update(request):
    print(request.POST)
    if request.method == 'POST':
        user = User.objects.update_validations(request.POST)
        if 'pass' in user:
            x = User.objects.get(id=request.session['uid'])
            x.first_name = request.POST['first_name']
            x.last_name = request.POST['last_name']
            x.email = request.POST['email']
            x.save()
            request.session['first_name'] = User.objects.get(id=int(request.session['uid'])).first_name
            request.session['last_name'] = User.objects.get(id=int(request.session['uid'])).last_name
            request.session['email'] = User.objects.get(id=int(request.session['uid'])).email
            return redirect('/')
        else:
            for key, value in user.items():
                messages.error(request, value)
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)


def logout(request):
    request.session.flush()
    return redirect('/')
