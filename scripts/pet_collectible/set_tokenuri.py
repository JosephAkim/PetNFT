#!/usr/bin/python3
from brownie import  PetCollection, accounts, network, config
from metadata import metadata_sample
from scripts.Useful_scripts import get_petName, OPENSEA_FORMAT

#get the recent deployed contract
# loop through all the tokens that were deploed
# print
# loop through the list of collectibles again
# first we get the breed  


pets_metadata_dic = {
    "PUG": "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmdryoExpgEQQQgJPoruwGJyZmz6SqV4FRTX1i73CT3iXn?filename=1-SHIBA_INU.json",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmbBnUjyHHN7Ytq9xDsYF9sucZdDJLRkWz7vnZfrjMXMxs?filename=2-ST_BERNARD.json",
}

def main():
    print("Working on " + network.show_active())
    pet_collectible = PetCollection[len(PetCollection) - 1]
    number_of_pet_collectibles = pet_collectible.tokenCounter()
    print(
        "The number of tokens you've deployed is: "
        + str(number_of_pet_collectibles)
    )
    for token_id in range(number_of_pet_collectibles):
        breed = get_petName(pet_collectible.tokenIdToBreed(token_id))
        if not pet_collectible.tokenURI(token_id).startswith("https://"):
            print("Setting tokenURI of {}".format(token_id))
            set_tokenURI(token_id, pet_collectible,
                         pets_metadata_dic[breed])
        else:
            print("Skipping {}, we already set that tokenURI!".format(token_id))


def set_tokenURI(token_id, nft_contract, tokenURI):
    dev = accounts.add(config["wallets"]["from_key"])
    nft_contract.setTokenURI(token_id, tokenURI, {"from": dev})
    print(
        "Awesome! You can view your NFT at {}".format(
            OPENSEA_FORMAT.format(nft_contract.address, token_id)
        )
    )
    print('Please give up to 20 minutes, and hit the "refresh metadata" button')
