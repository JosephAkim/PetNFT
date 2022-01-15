#!/usr/bin/python3
import os
import requests
import json
from brownie import PetCollection, network
from metadata import metadata_sample
from scripts.Useful_scripts import get_petName
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

pet_to_image_uri = {
    "DOG": "https://ipfs.io/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU?filename=dog.png",
    "CAT": "https://ipfs.io/ipfs/QmfTW4a8gqRPMUP8D3Y74Cs1Tyu53yJLS9upNMJUsTFRxT?filename=cat.jpg",
    "HORSE": "https://ipfs.io/ipfs/QmcXbWMD33ro1tQYGjPUbwpJsG13omKqJXcLodW9HGBTVh?filename=horse.png",
    "FISH": "https://ipfs.io/ipfs/QmT5DYbvAWokYkGTMUQ6D6vmQVVdQRAzDjvvBgYhZ1cEZj?filename=fish.png",
    "RABBIT": "https://ipfs.io/ipfs/QmWfFL6YmCdEvDBHPJJeHiwZ4YkydAuzRgkFaWusPfwoBx?filename=rabbit.png"
}


def main():
    print("Working on " + network.show_active())
    pet_collectible = PetCollection[len(PetCollection) - 1]
    number_of_pet_collectibles = pet_collectible.tokenCounter()
    print(
        "The number of tokens you've deployed is: "
        + str(number_of_pet_collectibles)
    )
    write_metadata(number_of_pet_collectibles, pet_collectible)


def write_metadata(token_ids, nft_contract):
    for token_id in range(token_ids):
        collectible_metadata = metadata_sample.metadata_template
        pet = get_petName(nft_contract.tokenIdToPet(token_id))
        metadata_file_name = (
            "./metadata/{}/".format(network.show_active())
            + str(token_id)
            + "-"
            + pet
            + ".json"
        )
        if Path(metadata_file_name).exists():
            print(
                "{} already found, delete it to overwrite!".format(
                    metadata_file_name)
            )
        else:
            print("Creating Metadata file: " + metadata_file_name)
            collectible_metadata["name"] = get_petName(
                nft_contract.tokenIdToPet(token_id)
            )
            collectible_metadata["description"] = "An adorable {}!".format(
                collectible_metadata["name"]
            )
            image_to_upload = None
            if os.getenv("UPLOAD_IPFS") == "true":
                image_path = "./img/{}.png".format(
                    pet.lower().replace('_', '-'))
                image_to_upload = upload_to_ipfs(image_path)
            image_to_upload = (
                pet_to_image_uri[pet] if not image_to_upload else image_to_upload
            )
            collectible_metadata["image"] = image_to_upload
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_ipfs(metadata_file_name)

# curl -X POST -F file=@metadata/rinkeby/0-SHIBA_INU.json http://localhost:5001/api/v0/add


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = (
            os.getenv("IPFS_URL")
            if os.getenv("IPFS_URL")
            else "http://localhost:5001"
        )
        response = requests.post(ipfs_url + "/api/v0/add",
                                 files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        image_uri = "https://ipfs.io/ipfs/{}?filename={}".format(
            ipfs_hash, filename)
        print(image_uri)
    return image_uri
