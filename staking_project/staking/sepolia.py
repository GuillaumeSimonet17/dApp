from web3 import Web3
import json
from django.conf import settings

# Charger les informations du contrat à partir des settings
CONTRACT_ADDRESS = settings.CONTRACT_ADDRESS  # Adresse de ton contrat
ABI_PATH = 'staking/abi/fortytwo42_abi.json'  # Emplacement du fichier ABI

# Connexion à Sepolia via Alchemy
alchemy_url = settings.ALCHEMY_URL  # URL d'Alchemy
web3 = Web3(Web3.HTTPProvider(alchemy_url))

# Vérification de la connexion à Sepolia
if not web3.is_connected():
    raise Exception("Échec de la connexion à Sepolia via Alchemy")

# Charger l'ABI du contrat depuis un fichier
with open(ABI_PATH) as f:
    contract_abi = json.load(f)

# Se connecter au contrat
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

def get_user_balance(user_address):
    balance_wei = contract.functions.balanceOf(user_address).call()
    balance_tokens = web3.from_wei(balance_wei, 'ether')
    return balance_tokens

def get_staked_balance(user_address):
    staked_balance = contract.functions.stakers(user_address).call()
    return staked_balance[0]

def get_user_level(user_address):
    try:
        user_level = contract.functions.getUserLevel(user_address).call()
        return user_level
    except Exception as e:
        print(f"Erreur lors de l'appel à la fonction 'getUserLevel': {e}")
        return "Unknown"

def get_tokens_for_next_level(user_address):
    tokens_required = contract.functions.tokensRequiredForNextLevel(user_address).call()
    return tokens_required
