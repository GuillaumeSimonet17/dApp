from .sepolia import get_user_balance, get_staked_balance, get_user_level, get_tokens_for_next_level, \
    stake_tokens_on_contract
from django.contrib.auth.models import User
from .forms import SignUpForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import WalletAddressForm
from .models import UserProfile
from .forms import LoginForm
from django.contrib import messages


def login_signup(request):
    message = None
    
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    login_form = LoginForm()
    signup_form = SignUpForm()
    
    if request.method == "POST":
        if "login" in request.POST:
            login_form = LoginForm(data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('dashboard')
            else:
                print(login_form.errors)
                message = []
                for field in login_form.errors:
                    for error in login_form.errors[field]:
                        message.append(error)
        
        elif "signup" in request.POST:  # Gestion de l'inscription
            signup_form = SignUpForm(request.POST)
            if signup_form.is_valid():
                
                username = signup_form.cleaned_data['username']
                email = signup_form.cleaned_data['email']
                password = signup_form.cleaned_data['password']
                confirm_password = signup_form.cleaned_data['confirm_password']
                if password != confirm_password:
                    print(signup_form.errors)
                
                user = User.objects.create_user(username=username, email=email, password=password)
                UserProfile.objects.create(user=user)
                
                login(request, user)
                
                return redirect('dashboard')
            else:
                print(signup_form.errors)
                message = []
                for field in signup_form.errors:
                    for error in signup_form.errors[field]:
                        message.append(error)
    
    return render(request, 'staking/login_signup.html',
                  {'form': login_form, 'signup_form': signup_form, 'message': message})


@login_required(login_url='login_signup')  # Redirection vers login_signup si non connecté
def dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)
    wallet_address = user_profile.wallet_address
    try:
        
        balance = get_user_balance(wallet_address)
        
        staked_balance = get_staked_balance(wallet_address)
        
        staked_balance_in_tokens = staked_balance / (10 ** 18)

        user_level = get_user_level(wallet_address)
        tokens_for_next_level = get_tokens_for_next_level(wallet_address) / (10 ** 18)
    except:
        return render(request, 'staking/dashboard.html', {
            'username': user_profile.user.username,
            'wallet_valid': False,
        })
    return render(request, 'staking/dashboard.html', {
        'username': user_profile.user.username,
        'wallet_valid': True,
        'balance': balance,
        'staked_balance': staked_balance_in_tokens,
        'user_level': user_level,
        'tokens_for_next_level': tokens_for_next_level,
    })

# TODO : verif dans le back c'est cool mais faut que le user signe sur metamask dans le front avant de staker

def stake_tokens(request):
    if request.method == "POST":
        amount = request.POST.get("amount")

        if not amount or float(amount) <= 0:
            messages.error(request, "Veuillez entrer un montant valide.")
            return redirect("dashboard")

        user_profile = UserProfile.objects.get(user=request.user)
        wallet_address = user_profile.wallet_address

        user_balance = get_user_balance(wallet_address)
        if user_balance < float(amount):
            messages.error(request, "Fonds insuffisants pour staker ce montant.")
            return redirect("dashboard")

        success, tx_hash = stake_tokens_on_contract(request.user, wallet_address, int(amount))

        if success:
            messages.success(request, f"Vous avez staké {amount} tokens avec succès ! (TX: {tx_hash})")
        else:
            messages.error(request, "Échec du staking. Veuillez réessayer.")

    return redirect("dashboard")


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
