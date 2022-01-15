#!/usr/bin/python3
from brownie import PetCollection
from scripts.Useful_scripts import fund_with_link


def main():
    pet_collectible = PetCollection[len(PetCollection) - 1]
    fund_with_link(pet_collectible.address)
