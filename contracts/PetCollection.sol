//SPDX-License-Identifier: MIT
pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract PetCollection is ERC721, VRFConsumerBase {
    uint256 public tokenCounter;
    //define the different breed at different state
    enum Pet{DOG, CAT, HORSE, FISH, RABBIT}
    // add other things
    mapping(bytes32 => address) public requestIdToSender;
    mapping(bytes32 => string) public requestIdToTokenURI;
    mapping(uint256 => Pet) public tokenIdToBreed;
    mapping(bytes32 => uint256) public requestIdToTokenId;
    //new best practice is to emmit event
    event requestedCollectible(bytes32 indexed requestId); 


    bytes32 internal keyHash;
    uint256 internal fee;
    
    //check the chainlink documentation
    //double inherited constructor
    constructor(address _VRFCoordinator, address _LinkToken, bytes32 _keyhash) public 
    VRFConsumerBase(_VRFCoordinator, _LinkToken)
    ERC721("Pets", "PET")
    {
        tokenCounter = 0;
        keyHash = _keyhash;
        fee = 0.1 * 10 ** 18;
    }

    // create collectible with tokenURI
    // defined where tokenURI came from in the scripts
    function createPetCollectible(string memory tokenURI) public returns (bytes32){
            bytes32 requestId = requestRandomness(keyHash, fee);
            requestIdToSender[requestId] = msg.sender;
            requestIdToTokenURI[requestId] = tokenURI;
            emit requestedCollectible(requestId);
    }
    
    function fulfillRandomness(bytes32 requestId, uint256 randomNumber) internal override {
        address petOwner = requestIdToSender[requestId];
        string memory tokenURI = requestIdToTokenURI[requestId];
        uint256 newItemId = tokenCounter;
        _safeMint(petOwner, newItemId);
        _setTokenURI(newItemId, tokenURI);
        Pet pet = Pet(randomNumber % 5); 
        tokenIdToBreed[newItemId] = pet;
        requestIdToTokenId[requestId] = newItemId;
        tokenCounter = tokenCounter + 1;
    }

    
    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: transfer caller is not owner nor approved"
        );
        _setTokenURI(tokenId, _tokenURI);
    }
}


