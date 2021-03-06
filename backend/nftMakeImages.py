"""
Make images for the METADATAS
"""
import os
from PIL import Image, ImageFont, ImageDraw
import nftConfig

# Metadata for the images to make.
METADATAS = [
    # 1, Common
    {
        "attributes": [
            {
                "trait_type": "Floor",
                "value": "Wood_Floor",
            },
            {
                "trait_type": "Left Wall",
                "value": "Left_Wall",
            },
            {
                "trait_type": "Back Wall",
                "value": "TV_Wall",
            },
            {
                "trait_type": "Decor",
                "value": "Gun_Lamp",
            },
            {
                "trait_type": "Chair",
                "value": "Leather_Chair",
            },
            {
                "trait_type": "Hair",
                "value": "Light_Mohawk",
            },
            {
                "trait_type": "Body",
                "value": "Light_Robe",
            },
            {
                "trait_type": "Book Color",
                "value": "Common",
            },
            {
                "trait_type": "Book Title",
                "value": "Comply_Or_Die",
            },
            {
                "trait_type": "Shoes",
                "value": "Boots",
            },
            {
                "trait_type": "Sideboard",
                "value": "Sideboard",
            },
            {
                "trait_type": "Sideboard Object",
                "value": "Beer_Bottle",
            },
            {
                "trait_type": "Rings",
                "value": "Wedding_Band",
            },
        ]
    },
    # 2, Uncommon
    {
        "attributes": [
            {
                "trait_type": "Floor",
                "value": "Grass",
            },
            {
                "trait_type": "Left Wall",
                "value": "Left_Wall",
            },
            {
                "trait_type": "Back Wall",
                "value": "Palm_Tree_Wall",
            },
            {
                "trait_type": "Decor",
                "value": "Cannabis",
            },
            {
                "trait_type": "Chair",
                "value": "Tie_Dye_Chair",
            },
            {
                "trait_type": "Hair",
                "value": "Medium_Beehive",
            },
            {
                "trait_type": "Body",
                "value": "Medium_Manwoman",
            },
            {
                "trait_type": "Book Color",
                "value": "Uncommon",
            },
            {
                "trait_type": "Book Title",
                "value": "Soul_Not_For_Sale",
            },
            {
                "trait_type": "Shoes",
                "value": "Medium_High_Heels_Robe_Manwoman",
            },
            {
                "trait_type": "Sideboard",
                "value": "Sideboard",
            },
            {
                "trait_type": "Sideboard Object",
                "value": "Bong",
            },
            {
                "trait_type": "Rings",
                "value": "Nothing",
            },
        ]
    },
    # 3, Rare
    {
        "attributes": [
            {
                "trait_type": "Floor",
                "value": "Checkered",
            },
            {
                "trait_type": "Left Wall",
                "value": "Left_Wall",
            },
            {
                "trait_type": "Back Wall",
                "value": "Marriage_Wall",
            },
            {
                "trait_type": "Decor",
                "value": "Torch",
            },
            {
                "trait_type": "Chair",
                "value": "Flag_Chair",
            },
            {
                "trait_type": "Hair",
                "value": "Medium_Buzzcut",
            },
            {
                "trait_type": "Body",
                "value": "Medium_Tracksuit",
            },
            {
                "trait_type": "Book Color",
                "value": "Rare",
            },
            {
                "trait_type": "Book Title",
                "value": "Don't_Shed_On_Me",
            },
            {
                "trait_type": "Shoes",
                "value": "Medium_Slippers_Tracksuit",
            },
            {
                "trait_type": "Sideboard",
                "value": "Sideboard",
            },
            {
                "trait_type": "Sideboard Object",
                "value": "Cigars",
            },
            {
                "trait_type": "Rings",
                "value": "Wedding_Band",
            },
        ]
    },
    # 4, Epic
    {
        "attributes": [
            {
                "trait_type": "Floor",
                "value": "Concrete",
            },
            {
                "trait_type": "Left Wall",
                "value": "Left_Wall",
            },
            {
                "trait_type": "Back Wall",
                "value": "Brick_Wall",
            },
            {
                "trait_type": "Decor",
                "value": "Lava_Lamp",
            },
            {
                "trait_type": "Chair",
                "value": "Polka_Dot_Chair",
            },
            {
                "trait_type": "Hair",
                "value": "Light_Rainbow_Hair",
            },
            {
                "trait_type": "Body",
                "value": "Light_Suit",
            },
            {
                "trait_type": "Book Color",
                "value": "Epic",
            },
            {
                "trait_type": "Book Title",
                "value": "Men_On_The_Moon",
            },
            {
                "trait_type": "Shoes",
                "value": "Dress_Shoes_Suit",
            },
            {
                "trait_type": "Sideboard",
                "value": "Sideboard",
            },
            {
                "trait_type": "Sideboard Object",
                "value": "Tumbler",
            },
            {
                "trait_type": "Rings",
                "value": "Wedding_Band",
            },
        ]
    },
    # 5, Legendary
    {
        "attributes": [
            {
                "trait_type": "Floor",
                "value": "Shag_Rug",
            },
            {
                "trait_type": "Left Wall",
                "value": "Left_Wall",
            },
            {
                "trait_type": "Back Wall",
                "value": "Last_Supper_Wall",
            },
            {
                "trait_type": "Decor",
                "value": "Disco_Ball",
            },
            {
                "trait_type": "Chair",
                "value": "Shell_Chair",
            },
            {
                "trait_type": "Hair",
                "value": "Dark_Box_Braids",
            },
            {
                "trait_type": "Body",
                "value": "Dark_Bell_Bottoms",
            },
            {
                "trait_type": "Book Color",
                "value": "Legendary",
            },
            {
                "trait_type": "Book Title",
                "value": "How_To_Survive_The_Y2K",
            },
            {
                "trait_type": "Shoes",
                "value": "Converse_Bell_Bottoms",
            },
            {
                "trait_type": "Sideboard",
                "value": "Sideboard",
            },
            {
                "trait_type": "Sideboard Object",
                "value": "Wine_Bottle",
            },
            {
                "trait_type": "Rings",
                "value": "Nothing",
            },
        ]
    },
    # 6, Exotic
    {
        "attributes": [
            {
                "trait_type": "Floor",
                "value": "Grass",
            },
            {
                "trait_type": "Left Wall",
                "value": "Left_Wall",
            },
            {
                "trait_type": "Back Wall",
                "value": "Roses_Wall",
            },
            {
                "trait_type": "Decor",
                "value": "Leg_Lamp",
            },
            {
                "trait_type": "Chair",
                "value": "Plaid_Chair",
            },
            {
                "trait_type": "Hair",
                "value": "Mullet",
            },
            {
                "trait_type": "Body",
                "value": "Medium_Robe",
            },
            {
                "trait_type": "Book Color",
                "value": "Exotic",
            },
            {
                "trait_type": "Book Title",
                "value": "The_12_Steps_for_Social_Media_Addicts",
            },
            {
                "trait_type": "Shoes",
                "value": "Socks_Slides",
            },
            {
                "trait_type": "Sideboard",
                "value": "Sideboard",
            },
            {
                "trait_type": "Sideboard Object",
                "value": "Crypto_Hermit",
            },
            {
                "trait_type": "Rings",
                "value": "Wedding_Band",
            },
        ]
    },
]


def ApplyCopyright(image):
    """
    Apply a copyright notice to the image.
    """
    # You cannot use ImageFont.load_default(), because that does not let you specify the font size.
    # So use arial.ttf.  You can find ttf files on a mac in either /System/Library/Fonts or /Library/Fonts.
    # 6-point size seems to be the smallest allowable, but you need at least 10-point to decipher the copyright circle logo.
    # https://stackoverflow.com/questions/58968752/loading-fonts-in-python-pillow-on-a-mac
    # font = ImageFont.truetype('arial.ttf', size=10)
    font = ImageFont.truetype("Roboto-Regular.ttf", size=8)  # You can use size=6, but it gets really fuzzy.
    text = "Copyright " + "\u00a9" + " 2021 BlockBot LLC, All Rights Reserved."
    imageDraw = ImageDraw.Draw(image)

    # Set the xy placement and fill color.
    #   x = 2 Gets the white tile color, when most of the copyright is in the black tile.
    #         So set x to 20 instead.
    #   y = 986 is enough vertical room for 12-point font (or less)
    #   y = 987 is enough vertical room for 10-point font (or less)
    #   y = 988 is enough vertical room for  8-point font (or less)
    #   y = 990 is enough vertical room for  6-point font (or less)
    fill = image.getpixel((20, 988))  # Or 'white' to make it visible.
    imageDraw.text(xy=(2, 988), text=text, fill=fill, font=font)

    return image


############################################# MAIN CODE TO RUN ####################################
nftDefinition = nftConfig.NFT_DEFINITION_BOOKWORMS
attributeImageFolder = nftDefinition["AttributeImageFolder"]
for m, metadata in enumerate(METADATAS):
    for a, attribute in enumerate(metadata["attributes"]):
        attributeName = attribute["value"]
        if attributeName in ("None", "Nothing"):
            continue
        trait = attribute["trait_type"]
        filePath = os.path.join(attributeImageFolder, trait, attributeName) + ".png"
        if trait == "Book Color":
            bookColor = attributeName
        elif trait == "Back Wall":
            backWall = attributeName
        if a == 0:
            baseImage = Image.open(filePath)
        else:
            attributeImage = Image.open(filePath)
            baseImage.paste(attributeImage, (0, 0), attributeImage)
    ApplyCopyright(baseImage)
    filePath = os.path.join(str(m + 1) + "." + bookColor + "." + backWall + "." + ".png")
    print(filePath)
    baseImage.save(os.path.join(filePath))
