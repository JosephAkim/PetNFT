#!/usr/bin/python3
from brownie import  PetCollection, accounts, network, config
from metadata import metadata_sample
from scripts.Useful_scripts import get_petName


def main():
    print("Working on " + network.show_active())
    pet_collectible = PetCollection[len(PetCollection) - 1]
    breakpoint()
    number_of_pet_collectibles = pet_collectible.tokenCounter()
    print(number_of_pet_collectibles)
