from constants import *
from web3 import Web3
from dotenv import load_dotenv
from web3.middleware import geth_poa_middleware
from eth_account import Account
import subprocess
import json

#Load environment variables
load_dotenv()
mnemonic = os.getenv('MNEMONIC', 'mix spot sign rally what endless chaos wall aisle elephant floor reason risk dumb change')

coins={}
#Calling Command line

#Initiate Web3 object
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)


private_key = os.getenv("PRIVATE_KEY")

account_one = Account.from_key(private_key)

#Derive Wallet based on the coin
def derive_wallet(coin):
    try:
        command=f'php ./derive -g --mnemonic="{mnemonic}" --cols=path,address,privkey,pubkey --format=jsonpretty --numderive=3 --coin={coin}'
        p=subprocess.Popen(command,stdout=subprocess.PIPE,shell=True)
        (output,err)=p.communicate()
        p_status=p.wait()
        coins[coin]=json.load(output)
    except expression as identifier:
        pass


def create_raw_tx(account, recipient, amount):
    gasEstimate = w3.eth.estimateGas(
        {"from": account.address, "to": recipient, "value": amount}
    )
    return {
        "from": account.address,
        "to": recipient,
        "value": amount,
        "gasPrice": w3.eth.gasPrice,
        "gas": gasEstimate,
        "nonce": w3.eth.getTransactionCount(account.address),
    }


def send_tx(account, recipient, amount):
    tx = create_raw_tx(account, recipient, amount)
    signed_tx = account.sign_transaction(tx)
    result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(result.hex())
    return result.hex()

send_tx(account_one,'0x812468f6730e6C0395120ddc563dED5477aCA219',330303308798789789)

