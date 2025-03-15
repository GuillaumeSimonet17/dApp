from django.shortcuts import render, redirect
from .sepolia import get_user_balance, get_staked_balance, get_user_level, get_tokens_for_next_level


def login(request):
    if request.method == 'POST':
        user_address = request.POST.get('user_address')
        if user_address:
            return redirect('dashboard', user_address=user_address)
        else:
            return render(request, 'staking/login.html',
                          {'error': 'Adresse invalide, veuillez réessayer.'})
    
    return render(request, 'staking/login.html')


def dashboard(request, user_address=None):
    if user_address:
        balance = get_user_balance(user_address)
        
        staked_balance = get_staked_balance(user_address)
        staked_balance_in_tokens = staked_balance / (10 ** 18)
        
        user_level = get_user_level(user_address)
        tokens_for_next_level = get_tokens_for_next_level(user_address) / (10 ** 18)
        
        return render(request, 'staking/dashboard.html', {
            'balance': balance,
            'staked_balance': staked_balance_in_tokens,
            'user_level': user_level,
            'tokens_for_next_level': tokens_for_next_level,
        })
    else:
        return redirect('login')
