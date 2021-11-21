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

# False = Do not send emails, True = Do send emails
DO_SEND_EMAILS = False

# False = Do not write to the csv log file, True = Do write to the csv log file
DO_WRITE_LOG_FILE = False

# False = Do not write messages to the console, True = Do write messages to the console
DO_WRITE_TO_CONSOLE = False

# Send internal emails to these email addresses.  Only relevant if DO_SEND_EMAILS == True
SEND_TO_EMAIL_ADDRESSES = "reynolds_johnd@yahoo.com"  # , jjjkreynolds@gmail.com, kylereynolds789@gmail.com


################################################# NFT COLLECTION DEFINITIONS #################################################
NFT_DEFINITION_BOOKWORMS = {
    "Name": "Bookworms",
    "Description": "A description of the bookworm collection that Bianca can come up with.",
    "ImageExtension": ".png",  # .png, .jpg, etc.
    "Quantity": 98,  # Quantity of NFT's to generate.  Set to a really high number if you want to generate the maximum number.
    "QuantityOfExposableTokens": 5,  # The initial quantity of tokens that will have their metadata exposable.
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
                {"Name": "Checkered", "Probability": 20},
                {"Name": "Concrete", "Probability": 20},
                {"Name": "Grass", "Probability": 20},
                {"Name": "Shag_Rug", "Probability": 20},
                {"Name": "Wood_Floor", "Probability": 20},
            ),
        },
        # Level 1
        {"Name": "Left Wall", "Attributes": ({"Name": "Left_Wall", "Probability": 100},)},
        # Level 2
        {
            "Name": "Back Wall",
            "Attributes": (
                {"Name": "Brick_Wall", "Probability": 17},
                {"Name": "Last_Supper_Wall", "Probability": 17},
                {"Name": "Marriage_Wall", "Probability": 17},
                {"Name": "Palm_Tree_Wall", "Probability": 17},
                {"Name": "Roses_Wall", "Probability": 16},
                {"Name": "TV_Wall", "Probability": 16},
            ),
        },
        # Level 3
        {
            "Name": "Lighting",
            "Attributes": (
                {"Name": "None", "FilePath": None, "Probability": 22},
                {"Name": "Cannabis", "Probability": 13},
                {"Name": "Disco_Ball", "Probability": 13},
                {"Name": "Gun_Lamp", "Probability": 13},
                {"Name": "Lava_Lamp", "Probability": 13},
                {"Name": "Leg_Lamp", "Probability": 13},
                {"Name": "Torch", "Probability": 13},
            ),
        },
        # Level 4
        {
            "Name": "Chair",
            "Attributes": (
                {"Name": "Flag_Chair", "Probability": 17},
                {"Name": "Leather_Chair", "Probability": 17},
                {"Name": "Plaid_Chair", "Probability": 17},
                {"Name": "Polka_Dot_Chair", "Probability": 17},
                {"Name": "Shell_Chair", "Probability": 16},
                {"Name": "Tie_Dye_Chair", "Probability": 16},
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
                {"Name": "Mythic", "FilePath": "BookColorMythic.png", "Probability": 2},
                {"Name": "Exotic", "FilePath": "BookColorExotic.png", "Probability": 3.4},
                {"Name": "Legendary", "FilePath": "BookColorLegendary.png", "Probability": 7.5},
                {"Name": "Epic", "FilePath": "BookColorEpic.png", "Probability": 12},
                {"Name": "Rare", "FilePath": "BookColorRare.png", "Probability": 17},
                {"Name": "Uncommon", "FilePath": "BookColorUncommon.png", "Probability": 25},
                {"Name": "Common", "FilePath": "BookColorCommon.png", "Probability": 33.1},
            ),
        },
        # Level 8
        {"Name": "Book Title", "Attributes": ({"Name": "_0002s_0000_Book", "Probability": 100},)},
        # Level 9
        {
            "Name": "Shoes",
            "Attributes": (
                # These shoes can be worn by any body.
                {"Name": "Boots", "Probability": 3.2},
                {"Name": "Converse", "Probability": 3.1},
                {"Name": "Slippers", "Probability": 3.1},
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
                {"Name": "None", "FilePath": None, "Probability": 23},
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
    # i don't want a certain mohawk with certain outfits (don't mix skin tones)
    "Exclusions": (
        {"Hair": "Dark_*", "Body": "Light_*"},
        {"Hair": "Dark_*", "Body": "Medium_*"},
        {"Hair": "Light_*", "Body": "Dark_*"},
        {"Hair": "Light_*", "Body": "Medium_*"},
        {"Hair": "Medium_*", "Body": "Dark_*"},
        {"Hair": "Medium_*", "Body": "Light_*"},
        {"Hair": "Dark_*", "Shoes": "Light_*"},
        {"Hair": "Dark_*", "Shoes": "Medium_*"},
        {"Hair": "Light_*", "Shoes": "Dark_*"},
        {"Hair": "Light_*", "Shoes": "Medium_*"},
        {"Hair": "Medium_*", "Shoes": "Dark_*"},
        {"Hair": "Medium_*", "Shoes": "Light_*"},
        {"Body": "Dark_*", "Shoes": "Light_*"},
        {"Body": "Dark_*", "Shoes": "Medium_*"},
        {"Body": "Light_*", "Shoes": "Dark_*"},
        {"Body": "Light_*", "Shoes": "Medium_*"},
        {"Body": "Medium_*", "Shoes": "Dark_*"},
        {"Body": "Medium_*", "Shoes": "Light_*"},
        {"Body": "*_Bell_Bottoms", "Shoes": "*_Robe_Manwoman"},
        {"Body": "*_Bell_Bottoms", "Shoes": "*_Suit"},
        {"Body": "*_Bell_Bottoms", "Shoes": "*_Tracksuit"},
        {"Body": "*_Manwoman", "Shoes": "*_Bell_Bottoms"},
        {"Body": "*_Manwoman", "Shoes": "*_Suit"},
        {"Body": "*_Manwoman", "Shoes": "*_Tracksuit"},
        {"Body": "*_Robe", "Shoes": "*_Bell_Bottoms"},
        {"Body": "*_Robe", "Shoes": "*_Suit"},
        {"Body": "*_Robe", "Shoes": "*_Tracksuit"},
        {"Body": "*_Suit", "Shoes": "*_Bell_Bottoms"},
        {"Body": "*_Suit", "Shoes": "*_Robe_Manwoman"},
        {"Body": "*_Suit", "Shoes": "*_Tracksuit"},
        {"Body": "*_Tracksuit", "Shoes": "*_Bell_Bottoms"},
        {"Body": "*_Tracksuit", "Shoes": "*_Robe_Manwoman"},
        {"Body": "*_Tracksuit", "Shoes": "*_Suit"},
    ),
    # These are the only traits I want to use for all 10,000 of the images
    #'Inclusions' : (
    #    {'Hair' : 'Dark_*', 'Body' : 'Dark_*', 'Sideboard Object' : 'Wine_Bottle', 'Chair' : 'Tie_Dye_Chair'},
    #    )
}
