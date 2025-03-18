from web3 import Web3
import json
from django.conf import settings


TOKEN_CONTRACT_ADDRESS = settings.TOKEN_CONTRACT_ADDRESS
STAKING_CONTRACT_ADDRESS = settings.STAKING_CONTRACT_ADDRESS

TOKEN_ABI_PATH = 'staking/abi/fortytwo42_abi.json'
STAKING_ABI_PATH = 'staking/abi/stakingcontract_abi.json'

alchemy_url = settings.ALCHEMY_URL  # URL d'Alchemy
web3 = Web3(Web3.HTTPProvider(alchemy_url))
if web3.is_connected():
    print("Connexion réussie!")
else:
    print("Connexion échouée!")


# Charger l'ABI du contrat depuis un fichier
with open(TOKEN_ABI_PATH) as f:
    token_contract_abi = json.load(f)
with open(STAKING_ABI_PATH) as f:
    staking_contract_abi = json.load(f)

# Se connecter au contrat
token_contract = web3.eth.contract(address=TOKEN_CONTRACT_ADDRESS, abi=token_contract_abi)
staking_contract = web3.eth.contract(address=STAKING_CONTRACT_ADDRESS, abi=staking_contract_abi)

def get_user_balance(user_address):
    balance_wei = token_contract.functions.balanceOf(user_address).call()
    balance_tokens = web3.from_wei(balance_wei, 'ether')
    return balance_tokens

def get_staked_balance(user_address):
    staked_balance = staking_contract.functions.stakers(user_address).call()
    return staked_balance[0]

def get_user_level(user_address):
    try:
        user_level = staking_contract.functions.getUserLevel(user_address).call()
        return user_level
    except Exception as e:
        print(f"Erreur lors de l'appel à la fonction 'getUserLevel': {e}")
        return "Unknown"

def get_tokens_for_next_level(user_address):
    tokens_required = staking_contract.functions.tokensRequiredForNextLevel(user_address).call()
    return tokens_required

def stake_tokens_on_contract(user, wallet_address, amount):
    pass
#     print(f"stake_tokens_on_contract: {wallet_address}")
#     try:
#         approve_tx = staking_contract.functions.approve(TOKEN_CONTRACT_ADDRESS, amount).build_transaction({
#             "from": wallet_address,
#             "gas": 100000,
#             "gasPrice": web3.to_wei("50", "gwei"),
#             "nonce": web3.eth.get_transaction_count(wallet_address)
#         })
#
#         signed_approve_tx = web3.eth.account.sign_transaction(approve_tx, private_key=user.private_key)
#         web3.eth.send_raw_transaction(signed_approve_tx.rawTransaction)
#
#         web3.eth.wait_for_transaction_receipt(web3.to_hex(signed_approve_tx.hash))
#
#         tx = staking_contract.functions.stakeTokens(amount).build_transaction({
#             "from": wallet_address,
#             "gas": 200000,
#             "gasPrice": web3.to_wei("50", "gwei"),
#             "nonce": web3.eth.get_transaction_count(wallet_address)  # Nouveau nonce
#         })
#
#         signed_tx = web3.eth.account.sign_transaction(tx, private_key=user.private_key)
#         tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
#
#         return True, web3.to_hex(tx_hash)
#
#     except Exception as e:
#         print(f"Erreur staking: {e}")
#         return False, None
