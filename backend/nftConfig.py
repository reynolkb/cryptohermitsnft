"""
Configuration parameters.
"""
import os
from dotenv import load_dotenv

load_dotenv()

################################################# STANDARD PROCESSING PARAMETERS #################################################
# Get the DATABASE_CONNECTION_STRING from the environment (.env or Heroku config)
DATABASE_CONNECTION_STRING = os.getenv("DATABASE_CONNECTION_STRING")

# The port for the localhost database.  Only relevant if DATABASE_CONNECTION_STRING is an empty string or None.
DATABASE_LOCAL_PORT = 27017

# Get the optional 'FRONTEND_BACKEND_HANDSHAKE' which will be required for external flask `apps.
FRONTEND_BACKEND_PASSWORD = os.getenv("FRONTEND_BACKEND_PASSWORD")

################################################# NFT COLLECTION DEFINITIONS #################################################
NFT_DEFINITION_BOOKWORMS = {
    "Name": "Bookworms",
    "Description": "A description of the bookworm collection that Bianca can come up with.",
    "ImageType": "png",  # png, jpg, etc.
    "Quantity": 98,  # Quantity of NFT's to generate.  Set to a really high number if you want to generate the maximum number.
    "QuantityOfExposableTokens": 10,  # The initial quantity of tokens that will have their metadata exposable.
    # Update the database with the images.  Since the images are so large, it can be very slow to update a remote database.
    # So only turn this to True when you are 100% sure that the images are finalized.
    "UpdateDatabaseWithImages": True,
    # Local folders for the input images and output images and output metadata.
    "AttributeImageFolder": "CryptoHermits/Bookworm/AttributeImages/",  # input image files
    "OutputImageFolder": "CryptoHermits/Bookworm/OutputImages/",  # output NFT images
    "OutputMetadataFolder": "CryptoHermits/Bookworm/OutputMetadata/",  # output json metadata files
    # The optional SignatureImages is a sub-folder contaiing full complete unique images.
    # So if there are 10 of them, and you have specified the above 'Quantity' = 990, then a total of 1000 NFTs will be produced.
    # They will be assigned a StatisticalRaity of 0, the highest Rarity (eg 'Mythic'), and a TraitCount of 1.
    # You will need to back into the first attribute[0] probability.
    "SignatureImageFolder": "CryptoHermits/Bookworm/SignatureImages/",
    # Round 1 - Images and metadata are on Mongo via nftInitializeDatabase
    # the 'external_url' = 'BaseExternalUri' and 'image' = 'BaseImageUri'
    # Generate the images
    "BaseExternalUri": "https://www.cryptohermitsnft.com/images/",
    "BaseImageUri": "https://www.cryptohermitsnft.com/images/",
    # Round 2 - Images on Mongo, JSON on Mongo. Buyer views on OpenSea
    # Check Mongo and make sure Mongo returns correct metadata. Example: https://www.cryptohermitsnft.com/1.json should return the correct metadata for NFT 1
    # Launch smart contract and make base uri https://cryptohermitsnft.com/metadata/
    # Update BaseImageUri hash to hash of IPFS image folder
    # 'BaseExternalUri' : 'https://gateway.pinata.cloud/ipfs/QmVpkXZkWoTf9AQWzHcA4HZxjRRpJPoSUUekL2RX5sMbxd/',
    # 'BaseImageUri' : 'ipfs://QmVpkXZkWoTf9AQWzHcA4HZxjRRpJPoSUUekL2RX5sMbxd/',
    # Round 3 - Images on IPFS, JSON on IPFS. Sale is over and all NFTs are sold.
    # Update smart contract base uri to ipfs://QmYrVgtkHnXDw9KURzgSbmejgzpEcje6FV5AofEmBx98kz/
    "Traits": (
        # Level 0
        {
            "Name": "Floor",
            "Attributes": (
                {"Name": "Checkered", "Probability": 18},
                {"Name": "Concrete", "Probability": 19},
                {"Name": "Grass", "Probability": 20},
                {"Name": "Shag_Rug", "Probability": 21},
                {"Name": "Wood_Floor", "Probability": 22},
            ),
        },
        # Level 1
        {"Name": "Left Wall", "Attributes": ({"Name": "Left_Wall", "Probability": 100},)},
        # Level 2
        {
            "Name": "Back Wall",
            "Attributes": (
                {"Name": "Brick_Wall", "Probability": 14},
                {"Name": "Last_Supper_Wall", "Probability": 15},
                {"Name": "Marriage_Wall", "Probability": 16},
                {"Name": "Palm_Tree_Wall", "Probability": 17},
                {"Name": "Roses_Wall", "Probability": 18},
                {"Name": "TV_Wall", "Probability": 20},
            ),
        },
        # Level 3
        {
            "Name": "Lighting",
            "Attributes": (
                {"Name": "Nothing", "FilePath": None, "Probability": 25},
                {"Name": "Cannabis", "Probability": 10},
                {"Name": "Disco_Ball", "Probability": 11},
                {"Name": "Gun_Lamp", "Probability": 12},
                {"Name": "Lava_Lamp", "Probability": 13},
                {"Name": "Leg_Lamp", "Probability": 14},
                {"Name": "Torch", "Probability": 15},
            ),
        },
        # Level 4
        {
            "Name": "Chair",
            "Attributes": (
                {"Name": "Flag_Chair", "Probability": 14},
                {"Name": "Leather_Chair", "Probability": 15},
                {"Name": "Plaid_Chair", "Probability": 16},
                {"Name": "Polka_Dot_Chair", "Probability": 17},
                {"Name": "Shell_Chair", "Probability": 18},
                {"Name": "Tie_Dye_Chair", "Probability": 20},
            ),
        },
        # Level 5
        {
            "Name": "Hair",
            "Attributes": (
                {"Name": "Dark_Beehive", "Probability": 6.25},
                {"Name": "Dark_Box_Braids", "Probability": 6.25},
                {"Name": "Dark_Buzzcut", "Probability": 6.25},
                {"Name": "Dark_Mohawk", "Probability": 6.25},
                {"Name": "Dark_Rainbow_Hair", "Probability": 6.25},
                {"Name": "Light_Beehive", "Probability": 6.25},
                {"Name": "Light_Box_Braids", "Probability": 6.25},
                {"Name": "Light_Buzzcut", "Probability": 6.25},
                {"Name": "Light_Mohawk", "Probability": 6.25},
                {"Name": "Light_Rainbow_Hair", "Probability": 6.25},
                {"Name": "Medium_Beehive", "Probability": 6.25},
                {"Name": "Medium_Box_Braids", "Probability": 6.25},
                {"Name": "Medium_Buzzcut", "Probability": 6.25},
                {"Name": "Medium_Mohawk", "Probability": 6.25},
                {"Name": "Medium_Rainbow_Hair", "Probability": 6.25},
                # A Mullet can be worn by any body, irrespective of skin tone.
                {"Name": "Mullet", "Probability": 6.25},
            ),
        },
        # Level 6
        {
            "Name": "Body",
            "Attributes": (
                {"Name": "Dark_Bell_Bottoms", "Probability": 6.67},
                {"Name": "Dark_Manwoman", "Probability": 6.67},
                {"Name": "Dark_Robe", "Probability": 6.67},
                {"Name": "Dark_Suit", "Probability": 6.67},
                {"Name": "Dark_Tracksuit", "Probability": 6.67},
                {"Name": "Light_Bell_Bottoms", "Probability": 6.67},
                {"Name": "Light_Manwoman", "Probability": 6.67},
                {"Name": "Light_Robe", "Probability": 6.67},
                {"Name": "Light_Suit", "Probability": 6.67},
                {"Name": "Light_Tracksuit", "Probability": 6.67},
                {"Name": "Medium_Bell_Bottoms", "Probability": 6.67},
                {"Name": "Medium_Manwoman", "Probability": 6.67},
                {"Name": "Medium_Robe", "Probability": 6.67},
                {"Name": "Medium_Suit", "Probability": 6.67},
                {"Name": "Medium_Tracksuit", "Probability": 6.62},
            ),
        },
        # Level 7 (RarityTrait)
        {
            "Name": "Book Color",
            "IsRarityTrait": True,
            "Attributes": (
                {"Name": "Mythic", "FilePath": "Mythic.png", "Probability": 2},
                {"Name": "Exotic", "FilePath": "Exotic.png", "Probability": 3.4},
                {"Name": "Legendary", "FilePath": "Legendary.png", "Probability": 7.5},
                {"Name": "Epic", "FilePath": "Epic.png", "Probability": 12},
                {"Name": "Rare", "FilePath": "Rare.png", "Probability": 17},
                {"Name": "Uncommon", "FilePath": "Uncommon.png", "Probability": 25},
                {"Name": "Common", "FilePath": "Common.png", "Probability": 33.1},  # 33.1
            ),
        },
        # Level 8
        {"Name": "Book Title", "Attributes": ({"Name": "Comply-Or-Die", "Probability": 100},)},
        # Level 9
        {
            "Name": "Shoes",
            "Attributes": (
                # These shoes can be worn by any body.
                {"Name": "Boots", "Probability": 3.2},  # 3.2
                {"Name": "Converse", "Probability": 6.2},
                {"Name": "Socks_Slides", "Probability": 3.1},
                # These shoes can only be worn by a body with the matching clothes.  The skin tone of the body is irrelevant.
                {"Name": "Boots_Bell_Bottoms", "Probability": 2.5},
                {"Name": "Converse_Bell_Bottoms", "Probability": 2.5},
                {"Name": "Converse_Suit", "Probability": 2.5},
                {"Name": "Converse_Tracksuit", "Probability": 2.5},
                {"Name": "Dress_Shoes_Bell_Bottoms", "Probability": 2.5},
                {"Name": "Dress_Shoes_Robe_Manwoman", "Probability": 2.5},  # These can be worn both by a 'Robe' or 'Manwoman' body.
                {"Name": "Dress_Shoes_Suit", "Probability": 2.5},
                {"Name": "Dress_Shoes_Tracksuit", "Probability": 2.5},
                {"Name": "Socks_Slides_Bell_Bottoms", "Probability": 2.5},
                {"Name": "Socks_Slides_Suit", "Probability": 2.5},
                {"Name": "Socks_Slides_Tracksuit", "Probability": 2.5},
                # These shoes can only be worn by a dark body with the matching clothes.
                {"Name": "Dark_High_Heels_Bell_Bottoms", "Probability": 2.5},
                {"Name": "Dark_High_Heels_Robe_Manwoman", "Probability": 2.5},  # These can be worn both by a 'Robe' or 'Manwoman' body.
                {"Name": "Dark_High_Heels_Suit", "Probability": 2.5},
                {"Name": "Dark_High_Heels_Tracksuit", "Probability": 2.5},
                {"Name": "Dark_Slippers_Bell_Bottoms", "Probability": 2.5},
                {"Name": "Dark_Slippers_Robe_Manwoman", "Probability": 2.5},  # These can be worn both by a 'Robe' or 'Manwoman' body.
                {"Name": "Dark_Slippers_Suit", "Probability": 2.5},
                {"Name": "Dark_Slippers_Tracksuit", "Probability": 2.5},
                # These shoes can only be worn by a light body with the matching clothes.
                {"Name": "Light_High_Heels_Bell_Bottoms", "Probability": 2.5},
                {"Name": "Light_High_Heels_Robe_Manwoman", "Probability": 2.5},  # These can be worn both by a 'Robe' or 'Manwoman' body.
                {"Name": "Light_High_Heels_Suit", "Probability": 2.5},
                {"Name": "Light_High_Heels_Tracksuit", "Probability": 2.5},
                {"Name": "Light_Slippers_Bell_Bottoms", "Probability": 2.5},
                {"Name": "Light_Slippers_Robe_Manwoman", "Probability": 2.5},  # These can be worn both by a 'Robe' or 'Manwoman' body.
                {"Name": "Light_Slippers_Suit", "Probability": 2.5},
                {"Name": "Light_Slippers_Tracksuit", "Probability": 2.5},
                # These shoes can only be worn by a medium body with the matching clothes.
                {"Name": "Medium_High_Heels_Bell_Bottoms", "Probability": 2.5},
                {"Name": "Medium_High_Heels_Robe_Manwoman", "Probability": 2.5},  # These can be worn both by a 'Robe' or 'Manwoman' body.
                {"Name": "Medium_High_Heels_Suit", "Probability": 2.5},
                {"Name": "Medium_High_Heels_Tracksuit", "Probability": 2.5},
                {"Name": "Medium_Slippers_Bell_Bottoms", "Probability": 2.5},
                {"Name": "Medium_Slippers_Robe_Manwoman", "Probability": 2.5},  # These can be worn both by a 'Robe' or 'Manwoman' body.
                {"Name": "Medium_Slippers_Suit", "Probability": 2.5},
                {"Name": "Medium_Slippers_Tracksuit", "Probability": 2.5},
            ),
        },
        # Level 10
        # You have to have the sideboard, otherwise there will be a hole in the left wall.
        {"Name": "Sideboard", "Attributes": ({"Name": "Sideboard", "Probability": 100},)},
        # Level 11
        {
            "Name": "Sideboard Object",
            "Attributes": (
                {"Name": "Nothing", "FilePath": None, "Probability": 23},
                {"Name": "Beer_Bottle", "Probability": 11},
                {"Name": "Bong", "Probability": 11},
                {"Name": "Cigars", "Probability": 11},
                {"Name": "Coffee_Mug", "Probability": 11},
                {"Name": "Crypto_Hermit", "Probability": 11},
                {"Name": "Tumbler", "Probability": 11},
                {"Name": "Wine_Bottle", "Probability": 11},
            ),
        },
    ),
    "Inclusions": (
        # If the hair is dark, then the body must be dark.
        (("Hair", "Dark_*"), ("Body", "Dark_*")),
        (("Hair", "Light_*"), ("Body", "Light_*")),
        (("Hair", "Medium_*"), ("Body", "Medium_*")),
        # If the body is dark, then the hair must be either dark or a Mullet.
        (("Body", "Dark_*"), ("Hair", ("Dark_*", "Mullet"))),
        (("Body", "Light_*"), ("Hair", ("Light_*", "Mullet"))),
        (("Body", "Medium_*"), ("Hair", ("Medium_*", "Mullet"))),
        # If the shoes are dark, then the body must be dark.
        (("Shoes", "Dark_*"), ("Body", "Dark_*")),
        (("Shoes", "Light_*"), ("Body", "Light_*")),
        (("Shoes", "Medium_*"), ("Body", "Medium_*")),
        # If the shoes are dark, then the hair must be either dark or a Mullet.
        (("Shoes", "Dark_*"), ("Hair", ("Dark_*", "Mullet"))),
        (("Shoes", "Light_*"), ("Hair", ("Light_*", "Mullet"))),
        (("Shoes", "Medium_*"), ("Hair", ("Medium_*", "Mullet"))),
        # --------------------------------- Body/Shoes Inclusions ---------------------------------
        # Dark_Bell_Bottoms
        (
            ("Body", "Dark_Bell_Bottoms"),
            ("Shoes", ("Boots_Bell_Bottoms", "Converse_Bell_Bottoms", "Dark_High_Heels_Bell_Bottoms", "Dark_Slippers_Bell_Bottoms", "Dress_Shoes_Bell_Bottoms", "Socks_Slides_Bell_Bottoms")),
        ),
        # Medium_Bell_Bottoms
        (
            ("Body", "Medium_Bell_Bottoms"),
            ("Shoes", ("Boots_Bell_Bottoms", "Converse_Bell_Bottoms", "Medium_High_Heels_Bell_Bottoms", "Medium_Slippers_Bell_Bottoms", "Dress_Shoes_Bell_Bottoms", "Socks_Slides_Bell_Bottoms")),
        ),
        # Light_Bell_Bottoms
        (
            ("Body", "Light_Bell_Bottoms"),
            ("Shoes", ("Boots_Bell_Bottoms", "Converse_Bell_Bottoms", "Light_High_Heels_Bell_Bottoms", "Light_Slippers_Bell_Bottoms", "Dress_Shoes_Bell_Bottoms", "Socks_Slides_Bell_Bottoms")),
        ),
        # Dark_Manwoman
        (
            ("Body", "Dark_Manwoman"),
            ("Shoes", ("Boots", "Converse", "Dark_High_Heels_Robe_Manwoman", "Dark_Slippers_Robe_Manwoman", "Dress_Shoes_Robe_Manwoman", "Socks_Slides")),
        ),
        # Medium_Manwoman
        (
            ("Body", "Medium_Manwoman"),
            ("Shoes", ("Boots", "Converse", "Medium_High_Heels_Robe_Manwoman", "Medium_Slippers_Robe_Manwoman", "Dress_Shoes_Robe_Manwoman", "Socks_Slides")),
        ),
        # Light_Manwoman
        (
            ("Body", "Light_Manwoman"),
            ("Shoes", ("Boots", "Converse", "Light_High_Heels_Robe_Manwoman", "Light_Slippers_Robe_Manwoman", "Dress_Shoes_Robe_Manwoman", "Socks_Slides")),
        ),
        # Dark_Robe
        (
            ("Body", "Dark_Robe"),
            ("Shoes", ("Boots", "Converse", "Dark_High_Heels_Robe_Manwoman", "Dark_Slippers_Robe_Manwoman", "Dress_Shoes_Robe_Manwoman", "Socks_Slides")),
        ),
        # Medium_Robe
        (
            ("Body", "Medium_Robe"),
            ("Shoes", ("Boots", "Converse", "Medium_High_Heels_Robe_Manwoman", "Medium_Slippers_Robe_Manwoman", "Dress_Shoes_Robe_Manwoman", "Socks_Slides")),
        ),
        # Light_Robe
        (
            ("Body", "Light_Robe"),
            ("Shoes", ("Boots", "Converse", "Light_High_Heels_Robe_Manwoman", "Light_Slippers_Robe_Manwoman", "Dress_Shoes_Robe_Manwoman", "Socks_Slides")),
        ),
        # Dark_Suit
        (
            ("Body", "Dark_Suit"),
            ("Shoes", ("Boots", "Converse_Suit", "Dark_High_Heels_Suit", "Dark_Slippers_Suit", "Dress_Shoes_Suit", "Socks_Slides_Suit")),
        ),
        # Medium_Suit
        (
            ("Body", "Medium_Suit"),
            ("Shoes", ("Boots", "Converse_Suit", "Medium_High_Heels_Suit", "Medium_Slippers_Suit", "Dress_Shoes_Suit", "Socks_Slides_Suit")),
        ),
        # Light_Suit
        (
            ("Body", "Light_Suit"),
            ("Shoes", ("Boots", "Converse_Suit", "Light_High_Heels_Suit", "Light_Slippers_Suit", "Dress_Shoes_Suit", "Socks_Slides_Suit")),
        ),
        # Dark_Tracksuit
        (
            ("Body", "Dark_Tracksuit"),
            ("Shoes", ("Boots", "Converse_Tracksuit", "Dark_High_Heels_Tracksuit", "Dark_Slippers_Tracksuit", "Dress_Shoes_Tracksuit", "Socks_Slides_Tracksuit")),
        ),
        # Medium_Tracksuit
        (
            ("Body", "Medium_Tracksuit"),
            ("Shoes", ("Boots", "Converse_Tracksuit", "Medium_High_Heels_Tracksuit", "Medium_Slippers_Tracksuit", "Dress_Shoes_Tracksuit", "Socks_Slides_Tracksuit")),
        ),
        # Light_Tracksuit
        (
            ("Body", "Light_Tracksuit"),
            ("Shoes", ("Boots", "Converse_Tracksuit", "Light_High_Heels_Tracksuit", "Light_Slippers_Tracksuit", "Dress_Shoes_Tracksuit", "Socks_Slides_Tracksuit")),
        ),
    ),
    # Kyle says these are incorrect.
    # "Exclusions": (
    #     {"Body": "*_Bell_Bottoms", "Shoes": "*_Robe_Manwoman"},
    #     {"Body": "*_Bell_Bottoms", "Shoes": "*_Suit"},
    #     {"Body": "*_Bell_Bottoms", "Shoes": "*_Tracksuit"},
    #     {"Body": "*_Manwoman", "Shoes": "*_Bell_Bottoms"},
    #     {"Body": "*_Manwoman", "Shoes": "*_Suit"},
    #     {"Body": "*_Manwoman", "Shoes": "*_Tracksuit"},
    #     {"Body": "*_Robe", "Shoes": "*_Bell_Bottoms"},
    #     {"Body": "*_Robe", "Shoes": "*_Suit"},
    #     {"Body": "*_Robe", "Shoes": "*_Tracksuit"},
    #     {"Body": "*_Suit", "Shoes": "*_Bell_Bottoms"},
    #     {"Body": "*_Suit", "Shoes": "*_Robe_Manwoman"},
    #     {"Body": "*_Suit", "Shoes": "*_Tracksuit"},
    #     {"Body": "*_Tracksuit", "Shoes": "*_Bell_Bottoms"},
    #     {"Body": "*_Tracksuit", "Shoes": "*_Robe_Manwoman"},
    #     {"Body": "*_Tracksuit", "Shoes": "*_Suit"},
    # ),
}
