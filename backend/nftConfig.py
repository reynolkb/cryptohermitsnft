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
    "TotalQuantity": 500,  # 10000  # Quantity of NFT's to generate.
    "QuantityOfExposableTokens": 5,  # The initial quantity of tokens that will have their metadata exposable.
    # Update the database with the images.  Since the images are so large, it can be very slow to update a remote database.
    # So only turn this to True when you are 100% sure that the images are finalized.
    "UploadImagesToDatabase": False,
    # Local folders for the input images and output images and output metadata.
    "AttributeImageFolder": "CryptoHermits/Bookworm/AttributeImages/",  # input image files
    "OutputImageFolder": "CryptoHermits/Bookworm/OutputImages/",  # output NFT images
    "OutputMetadataFolder": "CryptoHermits/Bookworm/OutputMetadata/",  # output json metadata files
    # The optional SignatureImages is a sub-folder contaiing full complete unique images.
    # So if there are 10 of them, and you have specified the above 'Quantity' = 990, then a total of 1000 NFTs will be produced.
    # They will be assigned a StatisticalRaity of 0, the highest Rarity (eg 'Mythic'), and a TraitCount of 1.
    # You will need to back into the first attribute[0] probability.
    # "SignatureImageFolder": "CryptoHermits/Bookworm/SignatureImages/",
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
                {"Name": "Checkered", "Probability": 1},
                {"Name": "Concrete", "Probability": 1},
                {"Name": "Grass", "Probability": 1},
                {"Name": "Shag_Rug", "Probability": 1},
                {"Name": "Wood_Floor", "Probability": 1},
            ),
        },
        # Level 1
        {
            "Name": "Left Wall",
            "Attributes": ({"Name": "Left_Wall", "Probability": 1},),
        },
        # Level 2
        {
            "Name": "Back Wall",
            "Attributes": (
                # {"Name": "Blank_Wall", "Probability": 1},
                {"Name": "Brick_Wall", "Probability": 1},
                {"Name": "Last_Supper_Wall", "Probability": 1},
                {"Name": "Marriage_Wall", "Probability": 1},
                {"Name": "Palm_Tree_Wall", "Probability": 1},
                {"Name": "Roses_Wall", "Probability": 1},
                {"Name": "TV_Wall", "Probability": 1},
            ),
        },
        # Level 3
        {
            "Name": "Decor",
            "Attributes": (
                # {"Name": "Nothing", "FilePath": None, "Probability": 1},
                {"Name": "Cannabis", "Probability": 1},
                {"Name": "Disco_Ball", "Probability": 1},
                {"Name": "Gun_Lamp", "Probability": 1},
                {"Name": "Lava_Lamp", "Probability": 1},
                {"Name": "Leg_Lamp", "Probability": 1},
                {"Name": "Torch", "Probability": 1},
            ),
        },
        # Level 4
        {
            "Name": "Chair",
            "Attributes": (
                {"Name": "Flag_Chair", "Probability": 1},
                {"Name": "Leather_Chair", "Probability": 1},
                {"Name": "Plaid_Chair", "Probability": 1},
                {"Name": "Polka_Dot_Chair", "Probability": 1},
                {"Name": "Shell_Chair", "Probability": 1},
                {"Name": "Tie_Dye_Chair", "Probability": 1},
            ),
        },
        # Level 5
        {
            "Name": "Hair",
            "Attributes": (
                {"Name": "Dark_Beehive", "Probability": 1},
                {"Name": "Dark_Box_Braids", "Probability": 1},  # Because excluding medium and light box_braids
                {"Name": "Dark_Buzzcut", "Probability": 1},
                {"Name": "Dark_Mohawk", "Probability": 1},
                {"Name": "Dark_Rainbow_Hair", "Probability": 1},
                {"Name": "Light_Beehive", "Probability": 1},
                {"Name": "Light_Box_Braids", "Probability": 1},
                {"Name": "Light_Buzzcut", "Probability": 1},
                {"Name": "Light_Mohawk", "Probability": 1},
                {"Name": "Light_Rainbow_Hair", "Probability": 1},
                {"Name": "Medium_Beehive", "Probability": 1},
                {"Name": "Medium_Box_Braids", "Probability": 1},
                {"Name": "Medium_Buzzcut", "Probability": 1},
                {"Name": "Medium_Mohawk", "Probability": 1},
                {"Name": "Medium_Rainbow_Hair", "Probability": 1},
                # A Mullet can be worn by any body, irrespective of skin tone.
                {"Name": "Mullet", "Probability": 1},
            ),
        },
        # Level 6
        {
            "Name": "Body",
            "Attributes": (
                {"Name": "Dark_Bell_Bottoms", "Probability": 1},
                {"Name": "Dark_Manwoman", "Probability": 1},
                {"Name": "Dark_Robe", "Probability": 1},
                {"Name": "Dark_Suit", "Probability": 1},
                {"Name": "Dark_Tracksuit", "Probability": 1},
                {"Name": "Light_Bell_Bottoms", "Probability": 1},
                {"Name": "Light_Manwoman", "Probability": 1},
                {"Name": "Light_Robe", "Probability": 1},
                {"Name": "Light_Suit", "Probability": 1},
                {"Name": "Light_Tracksuit", "Probability": 1},
                {"Name": "Medium_Bell_Bottoms", "Probability": 1},
                {"Name": "Medium_Manwoman", "Probability": 1},
                {"Name": "Medium_Robe", "Probability": 1},
                {"Name": "Medium_Suit", "Probability": 1},
                {"Name": "Medium_Tracksuit", "Probability": 1},
            ),
        },
        # Level 7
        {
            "Name": "Book Color",
            "Attributes": (
                # {"Name": "Mythic", "Probability": 1}, # Not applicable.  Mythic will be using the Signature Series images.
                {"Name": "Exotic", "Probability": 1},
                {"Name": "Legendary", "Probability": 1},
                {"Name": "Epic", "Probability": 1},
                {"Name": "Rare", "Probability": 1},
                {"Name": "Uncommon", "Probability": 1},
                {"Name": "Common", "Probability": 1},
            ),
        },
        # Level 8
        {
            "Name": "Book Title",
            "Attributes": (
                {"Name": "Comply_Or_Die", "Probability": 1},
                {"Name": "Don't_Shed_On_Me", "Probability": 1},
                {"Name": "How_To_Survive_The_Y2K", "Probability": 1},
                {"Name": "Men_On_The_Moon", "Probability": 1},
                {"Name": "Soul_Not_For_Sale", "Probability": 1},
                {"Name": "The_12_Steps_for_Social_Media_Addicts", "Probability": 1},
            ),
        },
        # Level 9
        {
            "Name": "Shoes",
            "Attributes": (
                # These shoes can be worn by any body.
                {"Name": "Boots", "Probability": 1},
                {"Name": "Converse", "Probability": 1},
                {"Name": "Socks_Slides", "Probability": 1},
                # These shoes can only be worn by a body with the matching clothes.  The skin tone of the body is irrelevant.
                {"Name": "Boots_Bell_Bottoms", "Probability": 1},
                {"Name": "Converse_Bell_Bottoms", "Probability": 1},
                {"Name": "Converse_Suit", "Probability": 1},
                {"Name": "Converse_Tracksuit", "Probability": 1},
                {"Name": "Dress_Shoes_Bell_Bottoms", "Probability": 1},
                {"Name": "Dress_Shoes_Robe_Manwoman", "Probability": 1},  # These can be worn both by a 'Robe' or 'Manwoman' body.
                {"Name": "Dress_Shoes_Suit", "Probability": 1},
                {"Name": "Dress_Shoes_Tracksuit", "Probability": 1},
                {"Name": "Socks_Slides_Bell_Bottoms", "Probability": 1},
                {"Name": "Socks_Slides_Suit", "Probability": 1},
                {"Name": "Socks_Slides_Tracksuit", "Probability": 1},
                # These shoes can only be worn by a dark body with the matching clothes.
                {"Name": "Dark_High_Heels_Bell_Bottoms", "Probability": 1},
                {"Name": "Dark_High_Heels_Robe_Manwoman", "Probability": 1},  # These can be worn both by a 'Robe' or 'Manwoman' body.
                {"Name": "Dark_High_Heels_Suit", "Probability": 1},
                {"Name": "Dark_High_Heels_Tracksuit", "Probability": 1},
                {"Name": "Dark_Slippers_Bell_Bottoms", "Probability": 1},
                {"Name": "Dark_Slippers_Robe_Manwoman", "Probability": 1},  # These can be worn both by a 'Robe' or 'Manwoman' body.
                {"Name": "Dark_Slippers_Suit", "Probability": 1},
                {"Name": "Dark_Slippers_Tracksuit", "Probability": 1},
                # These shoes can only be worn by a light body with the matching clothes.
                {"Name": "Light_High_Heels_Bell_Bottoms", "Probability": 1},
                {"Name": "Light_High_Heels_Robe_Manwoman", "Probability": 1},  # These can be worn both by a 'Robe' or 'Manwoman' body.
                {"Name": "Light_High_Heels_Suit", "Probability": 1},
                {"Name": "Light_High_Heels_Tracksuit", "Probability": 1},
                {"Name": "Light_Slippers_Bell_Bottoms", "Probability": 1},
                {"Name": "Light_Slippers_Robe_Manwoman", "Probability": 1},  # These can be worn both by a 'Robe' or 'Manwoman' body.
                {"Name": "Light_Slippers_Suit", "Probability": 1},
                {"Name": "Light_Slippers_Tracksuit", "Probability": 1},
                # These shoes can only be worn by a medium body with the matching clothes.
                {"Name": "Medium_High_Heels_Bell_Bottoms", "Probability": 1},
                {"Name": "Medium_High_Heels_Robe_Manwoman", "Probability": 1},  # These can be worn both by a 'Robe' or 'Manwoman' body.
                {"Name": "Medium_High_Heels_Suit", "Probability": 1},
                {"Name": "Medium_High_Heels_Tracksuit", "Probability": 1},
                {"Name": "Medium_Slippers_Bell_Bottoms", "Probability": 1},
                {"Name": "Medium_Slippers_Robe_Manwoman", "Probability": 1},  # These can be worn both by a 'Robe' or 'Manwoman' body.
                {"Name": "Medium_Slippers_Suit", "Probability": 1},
                {"Name": "Medium_Slippers_Tracksuit", "Probability": 1},
            ),
        },
        # Level 10
        {
            # You have to have the sideboard, otherwise there will be a hole in the left wall.
            "Name": "Sideboard",
            "Attributes": (
                # {"Name": "Nothing", "FilePath": None, "Probability": 1},
                {"Name": "Sideboard", "Probability": 1},
            ),
        },
        # Level 11
        {
            "Name": "Sideboard Object",
            "Attributes": (
                # {"Name": "Nothing", "FilePath": None, "Probability": 1},
                {"Name": "Beer_Bottle", "Probability": 1},
                {"Name": "Bong", "Probability": 1},
                {"Name": "Cigars", "Probability": 1},
                {"Name": "Coffee_Mug", "Probability": 1},
                {"Name": "Crypto_Hermit", "Probability": 1},  # This is hard-coded for the highest rarity level.
                {"Name": "Tumbler", "Probability": 1},
                {"Name": "Wine_Bottle", "Probability": 1},
            ),
        },
        # Level 12
        {
            "Name": "Rings",
            "Attributes": (
                {"Name": "Nothing", "FilePath": None, "Probability": 1},
                {"Name": "Wedding_Band", "Probability": 1},
            ),
        },
    ),
    "Rarities": (
        # Mythic: Comletely Custom
        {
            "Name": "Mythic",
            "Probability": 1,  # 1.0, 0.1 # 0.12,
            "FinalImageFolder": "CryptoHermits/Bookworm/SignatureImages/",
        },
        # Exotic: Force Sideboard Object to be "Crypto_Hermit"
        {
            "Name": "Exotic",
            "Probability": 4,  # 14, 14.9, 14.88,
            "Traits": (
                {"Name": "Book Color", "Inclusions": "Exotic"},
                {"Name": "Sideboard Object", "Inclusions": "Crypto_Hermit"},
            ),
        },
        # Legendary: Add Decor and Sideboard Object (except for "Nothing", "Crypto_Hermit")
        {
            "Name": "Legendary",
            "Probability": 9,
            "Traits": (
                {"Name": "Back Wall", "Inclusions": "Last_Supper_Wall"},
                {"Name": "Book Color", "Inclusions": "Legendary"},
                {"Name": "Sideboard Object", "Exclusions": "Crypto_Hermit"},
            ),
        },
        # Epic: Adding Floor
        {
            "Name": "Epic",
            "Probability": 14,
            "Traits": (
                {"Name": "Back Wall", "Inclusions": "Brick_Wall"},
                {"Name": "Book Color", "Inclusions": "Epic"},
                {"Name": "Sideboard Object", "Exclusions": "Crypto_Hermit"},
            ),
        },
        # Rare: Adding Wall
        {
            "Name": "Rare",
            "Probability": 19,
            "Traits": (
                {"Name": "Back Wall", "Inclusions": "Marriage_Wall"},
                {"Name": "Book Color", "Inclusions": "Rare"},
                {"Name": "Sideboard Object", "Exclusions": "Crypto_Hermit"},
            ),
        },
        # Uncommon: Adding Chair
        {
            "Name": "Uncommon",
            "Probability": 24,
            "Traits": (
                {"Name": "Back Wall", "Inclusions": "Palm_Tree_Wall"},
                {"Name": "Book Color", "Inclusions": "Uncommon"},
                {"Name": "Sideboard Object", "Exclusions": "Crypto_Hermit"},
            ),
        },
        # Common
        {
            "Name": "Common",
            "Probability": 29,
            "Traits": (
                {"Name": "Back Wall", "Inclusions": "TV_Wall"},
                {"Name": "Book Color", "Inclusions": "Common"},
                {"Name": "Sideboard Object", "Exclusions": "Crypto_Hermit"},
            ),
        },
    ),
    "Inclusions": (
        # --------------------------------- Hair/Body Inclusions ---------------------------------
        (("Hair", "Dark_*"), ("Body", "Dark_*")),
        (("Hair", "Light_*"), ("Body", "Light_*")),
        (("Hair", "Medium_*"), ("Body", "Medium_*")),
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
    "Exclusions": (
        ############### Boring/Plain Exclusions 12/06/21 ###############
        {"Back Wall": "TV_Wall", "Floor": "Concrete"},
        {"Back Wall": "TV_Wall", "Chair": "Leather_Chair"},
        {"Floor": "Concrete", "Chair": "Leather_Chair"},
        ############### John's Body/Hair Exclusions 12/06/21 ###############
        # The Dark_Beehive and Medium_Beehive scalp skin colors are both light.  They do not match their Dark_* and
        # Medium_* bodies.  The artist should darken their scalp skin tones, and possibly darken their hair color.
        {
            "Hair": (
                "Dark_Beehive",
                "Medium_Beehive",
            )
        },
        # The Light_Box_Braids and Medium_Box_Braids scalp is way too dark for their bodies.
        {
            "Hair": (
                "Light_Box_Braids",
                "Medium_Box_Braids",
            )
        },
        # The Buzz_Cuts all look good.
        # The Dark_Mohawk does not look natural on the Dark_* bodies.
        {"Hair": "Dark_Mohawk"},
        # The Dark_Rainbow_Hair does not look natural on the Dark_* bodies.
        {"Hair": "Dark_Rainbow_Hair"},
        ## The Mullet does not look natural on the Dark_* bodies.  Unless they dyed their hair.
        {"Hair": "Mullet", "Body": "Dark_*"},
        ############### John's Body/Shoe Exclusions 12/06/21 ###############
        # ## *_Bell_Bottoms
        # ##{"Body": "*_Bell_Bottoms", "Shoes": "*_High_Heels_*"},
        # # *_Manwoman
        # {
        #     "Body": "*_Manwoman",
        #     "Shoes": (
        #         "Converse*",
        #         "Dress_Shoes_*",
        #     ),
        # },
        # # *_Robe
        # {
        #     "Body": "*_Robe",
        #     "Shoes": (
        #         "Boots*",
        #         "Converse*",
        #         "Dress_Shoes_*",
        #         "*_High_Heels_*",
        #     ),
        # },
        # # *_Suit
        # {"Body": "*_Suit", "Shoes": ("Converse*", "*_High_Heels_*", "*_Slippers_*", "Socks_Slides_*")},
        # # *_Tracksuit
        # {
        #     "Body": "*_Tracksuit",
        #     "Shoes": (
        #         "Boots*",
        #         "Dress_Shoes_*",
        #         "*_High_Heels_*",
        #     ),
        # },
    ),
}
