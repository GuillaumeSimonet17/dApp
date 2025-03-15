from .sepolia import get_user_balance, get_staked_balance, get_user_level, get_tokens_for_next_level
from django.contrib.auth.models import User
from .forms import SignUpForm  # Assure-toi que tu as un formulaire d'inscription
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import WalletAddressForm
from .models import UserProfile

def login_signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    login_form = AuthenticationForm()
    signup_form = SignUpForm()
    
    if request.method == "POST":
        if "login" in request.POST:  # Gestion de la connexion
            login_form = AuthenticationForm(data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('dashboard')  # Rediriger après la connexion
        
        elif "signup" in request.POST:  # Gestion de l'inscription
            signup_form = SignUpForm(request.POST)
            if signup_form.is_valid():

                username = signup_form.cleaned_data['username']
                email = signup_form.cleaned_data['email']
                password = signup_form.cleaned_data['password']
                confirm_pwd = signup_form.cleaned_data['confirm_pwd']
                if password != confirm_pwd:
                    print(signup_form.errors)
                    
                user = User.objects.create_user(username=username, email=email, password=password)
                
                login(request, user)
                
                return redirect('dashboard')
            else:
                print(signup_form.errors)
    
    return render(request, 'staking/login_signup.html', {'form': login_form, 'signup_form': signup_form})


@login_required(login_url='login_signup')  # Redirection vers login_signup si non connecté
def dashboard(request, user_address=None):
    user_profile = UserProfile.objects.get(user=request.user)
    wallet_address = user_profile.wallet_address

    if wallet_address:
        try:
            balance = get_user_balance(wallet_address)
            
            staked_balance = get_staked_balance(wallet_address)
            staked_balance_in_tokens = staked_balance / (10 ** 18)
            
            user_level = get_user_level(wallet_address)
            tokens_for_next_level = get_tokens_for_next_level(wallet_address) / (10 ** 18)
        except:
            return render(request, 'staking/dashboard.html', {
                'wallet_valid': False,
            })
        return render(request, 'staking/dashboard.html', {
            'wallet_valid': True,
            'balance': balance,
            'staked_balance': staked_balance_in_tokens,
            'user_level': user_level,
            'tokens_for_next_level': tokens_for_next_level,
        })
    else:
        return redirect('login_signup')


@login_required
def update_wallet_address(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user=request.user)

    if request.method == 'POST':
        form = WalletAddressForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        user_profile = UserProfile.objects.get(user=request.user)
        wallet_address = user_profile.wallet_address
        form = WalletAddressForm(instance=user_profile)

    return render(request, 'settings.html', {'form': form, 'wallet_address': wallet_address})
