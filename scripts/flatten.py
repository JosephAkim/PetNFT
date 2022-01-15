#!/usr/bin/python3
from brownie import PetCollection, accounts, network, config, interface
import json


def main():
    flatten()


def flatten():
    file = open("./PetCollection_flattened.json", "w")
    json.dump(PetCollection.get_verification_info(), file)
    file.close()
