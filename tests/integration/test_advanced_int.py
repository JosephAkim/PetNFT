import pytest
from brownie import network, PetCollection
from scripts.Useful_scripts import (
    get_account,
    get_contract,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
import time


def test_can_create_advanced_collectible_integration(
    get_keyhash,
    chainlink_fee,
):
    # Arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for integration testing")
    pet_collectible = PetCollection.deploy(
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        get_keyhash,
        {"from": get_account()},
    )
    get_contract("link_token").transfer(
        pet_collectible.address, chainlink_fee * 3, {"from": get_account()}
    )
    # Act
    pet_collectible.createPetCollectible("None", {"from": get_account()})
    time.sleep(75)
    # Assert
    assert pet_collectible.tokenCounter() > 0
