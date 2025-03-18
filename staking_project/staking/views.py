from .sepolia import get_user_balance, get_staked_balance, get_user_level, get_tokens_for_next_level, \
    stake_tokens_on_contract
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def home(request):
    return render(request, 'staking/home.html')


def dashboard_address(request, address):
    try:
        request.session['wallet_address'] = address  # Stocker l'adresse en session

        balance = get_user_balance(address)
        staked_balance = get_staked_balance(address)
        user_level = get_user_level(address)
        tokens_for_next_level = get_tokens_for_next_level(address)
        
        request.session['wallet_data'] = {
            'balance': float(balance),
            'staked_balance': float(staked_balance) / (10 ** 18),
            'user_level': int(user_level),  # Si c'est un entier
            'tokens_for_next_level': float(tokens_for_next_level) / (10 ** 18),
        }
    
    
    except Exception as e:
        print("Erreur:", e)
        request.session['wallet_valid'] = False
        return redirect('dashboard')

    request.session['wallet_valid'] = True
    return redirect('dashboard')

def dashboard(request):
    wallet_valid = request.session.get('wallet_valid', False)
    wallet_data = request.session.get('wallet_data', {})

    return render(request, 'staking/dashboard.html', {
        'wallet_valid': wallet_valid,
        **wallet_data,  # Injecter toutes les données dans le template
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
