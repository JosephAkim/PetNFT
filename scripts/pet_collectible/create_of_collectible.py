#!/usr/bin/python3
from brownie import PetCollection, accounts, config
from scripts.Useful_scripts import get_petName, fund_with_link
import time


def main():
    dev = accounts.add(config["wallets"]["from_key"])
    pet_collectible = PetCollection[len(PetCollection) - 1]
    fund_with_link(pet_collectible.address)
    transaction = pet_collectible.createPetCollectible("None", {"from": dev})
    print("Waiting on second transaction...")
    # wait for the 2nd transaction
    transaction.wait(1)
    time.sleep(35)
    requestId = transaction.events["requestedCollectible"]["requestId"]
    token_id = pet_collectible.requestIdToTokenId(requestId)
    pet = get_petName(pet_collectible.tokenIdToBreed(token_id))
    print("Pet of tokenId {} is {}".format(token_id, pet))
