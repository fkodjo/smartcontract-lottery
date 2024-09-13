from brownie import network, config, accounts, config, MockV3Aggregator, Contract, VRFCoordinatorMock, LinkToken

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-lottery"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development","ganache-local"]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])
    
contract_to_mack = {"eth_usd_price_feed": MockV3Aggregator, "vrf_coordinator": VRFCoordinatorMock, "link_token": LinkToken}

def get_contract(contract_name):
    """This function will grab the contract addresses from the brownie config 
    if defined, otherwise, it will deploy a mock version of that contract,and 
    return that mock contract.
        Args:
            contract_name (string)
        
        Returns:
            brownie.network.contract?ProjectContract: The lost recently deployed
            version of this contract.=
    """
    contract_type = contract_to_mack[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        # address
        # ABI
        contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi)
    return contract

DECIMALS = 8
STARTING_PRICE = 200000000000

def deploy_mocks(decimals=DECIMALS, initial_value=STARTING_PRICE):
    account = get_account()
    mock_price_feed = MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print("Deployed!")

def fund_with_link(contract_address, account=None, link_token=None, amount=250000000000000000): # 0.25 LINK
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    #link_token_contract = interface.LinkTokenInterface(link_token.address)
    #tx = link_token_contract.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("Fund contract!")
    print(tx)
    return tx

    
