'''
Configuration parameters.
'''
import os
from dotenv import load_dotenv
load_dotenv()

################################################# STANDARD PROCESSING PARAMETERS #################################################
# Get the DATABASE_CONNECTION_STRING from the environment (.env or Heroku config)
DATABASE_CONNECTION_STRING = os.getenv('DATABASE_CONNECTION_STRING')

# The port for the localhost database.  Only relevant if DATABASE_CONNECTION_STRING is an empty string or None.
DATABASE_LOCAL_PORT = 27017

# False = Do not send emails, True = Do send emails
DO_SEND_EMAILS = False

# False = Do not write to the csv log file, True = Do write to the csv log file
DO_WRITE_LOG_FILE = False

# False = Do not write messages to the console, True = Do write messages to the console
DO_WRITE_TO_CONSOLE = False

# Send internal emails to these email addresses.  Only relevant if DO_SEND_EMAILS == True
SEND_TO_EMAIL_ADDRESSES = 'reynolds_johnd@yahoo.com' # , jjjkreynolds@gmail.com, kylereynolds789@gmail.com


################################################# NFT COLLECTION DEFINITIONS #################################################
NFT_DEFINITION_BOOKWORMS = {
    'Name': 'Bookworms',
    'Description' : 'A description of the bookworm collection that Bianca can come up with.',
    'Quantity' : 10000, # Quantity of NFT's to generate.  Set to a really high number if you want to generate the maximum number.
    'QuantityOfExposableTokens' : 10, # The initial quantity of tokens that will have their metadata exposable.

    # Update the database with the images.  Since the images are so large, it can be very slow to update a remote database.
    # So only turn this to True when you are 100% sure that the images are finalized.
    'UpdateDatabaseWithImages' : True,

    # Local folders for the input images and output images and output metadata.
    'InputImageFolder' : 'CryptoHermits/Bookworm/InputImages/', # input image files
    'OutputImageFolder' : 'CryptoHermits/Bookworm/OutputImages/', # output NFT images
    'OutputMetadataFolder' : 'CryptoHermits/Bookworm/OutputMetadata/', # output json metadata files
    'ImageExtension' : '.png', # .png, .jpg, etc.

    # Round 1 - Images and metadata are on Mongo via nftInitializeDatabase
    # the 'external_url' = 'BaseExternalUri' and 'image' = 'BaseImageUri'
    # Generate the images

    'BaseExternalUri' : 'https://www.cryptohermitsnft.com/images/',
    'BaseImageUri' : 'https://www.cryptohermitsnft.com/images/',

    # Round 2 - Images on Mongo, JSON on Mongo. Buyer views on OpenSea
    # Check Mongo and make sure Mongo returns correct metadata. Example: https://www.cryptohermitsnft.com/1.json should return the correct metadata for NFT 1
    # Launch smart contract and make base uri https://cryptohermitsnft.com/metadata/

    # Update BaseImageUri hash to hash of IPFS image folder
    # 'BaseExternalUri' : 'https://gateway.pinata.cloud/ipfs/QmVpkXZkWoTf9AQWzHcA4HZxjRRpJPoSUUekL2RX5sMbxd/',
    # 'BaseImageUri' : 'ipfs://QmVpkXZkWoTf9AQWzHcA4HZxjRRpJPoSUUekL2RX5sMbxd/',

    # Round 3 - Images on IPFS, JSON on IPFS. Sale is over and all NFTs are sold.
    # Update smart contract base uri to ipfs://QmYrVgtkHnXDw9KURzgSbmejgzpEcje6FV5AofEmBx98kz/

    'Traits' : (
        {'Name' : 'Base',
         'Attributes' : ({'Name' : 'Base Layer', 'FilePath' : '00_Base Layer.png', 'Probability' : 100},)},
        {'Name' : 'Floor',
         'Attributes' : ({'Name' : 'Wood-Floor', 'FilePath' : '01_Wood-Floor.png', 'Probability' : 100},)},
        {'Name' : 'Background',
         'Attributes' : ({'Name' : 'Brick-Wall', 'FilePath' : '02_Brick-Wall.png', 'Probability' : 100},)},
        {'Name' : 'Left Wall',
         'Attributes' : ({'Name' : 'GrayLeftWall', 'FilePath' : '03_Left-Wall.png', 'Probability' : 100},)},
        {'Name' : 'Lighting',
         'Attributes' : ({'Name' : 'Nothing', 'FilePath' : None, 'Probability' : 1},
                         {'Name' : 'Lava-Lamp', 'FilePath' : '04_Lava-Lamp.png', 'Probability' : 99},)},
        {'Name' : 'Chair',
         'Attributes' : ({'Name' : 'Tie-Dye', 'FilePath' : '05_Tie-Dye.png', 'Probability' : 100},)},
        {'Name' : 'Hairdos',
         'Attributes' : (
           {'Name' : 'Light-Mohawk', 'FilePath' : '06_Light-Mohawk.png', 'Probability' : 33.33},
           {'Name' : 'Medium-Mohawk', 'FilePath' : '06_Medium-Mohawk.png', 'Probability' : 33.33},
           {'Name' : 'Dark-Mohawk', 'FilePath' : '06_Dark-Mohawk.png', 'Probability' : 33.34},
          )
        },
        {'Name' : 'Outfits',
         'Attributes' : (
           {'Name' : 'Light-Robe', 'FilePath' : '07_Light-Robe.png', 'Probability' : 33.33},
           {'Name' : 'Medium-Robe', 'FilePath' : '07_Medium-Robe.png', 'Probability' : 33.33},
           {'Name' : 'Dark-Robe', 'FilePath' : '07_Dark-Robe.png', 'Probability' : 33.34},
          )
        },
        {'Name' : 'Book Titles',
         'Attributes' : ({'Name' : 'GreenBook', 'FilePath' : '08_Book.png', 'Probability' : 100},)},
        {'Name' : 'Shoes',
         'Attributes' : ({'Name' : 'BrownSlippers', 'FilePath' : '09_Slippers.png', 'Probability' : 100},)},
        {'Name' : 'Sideboard',
         'Attributes' : ({'Name' : 'BrownSideboard', 'FilePath' : '10_Sideboard.png', 'Probability' : 100},)},
        {'Name' : 'Sideboard Objects',
         'Attributes' : ({'Name' : 'Nothing', 'FilePath' : None, 'Probability' : 1},
                         {'Name' : 'GreenWineBottle', 'FilePath' : '11_Wine-Bottle.png', 'Probability' : 99},)},
        ),

    'Exclusions' : [
       # i don't want a mohawk with vuarnet sunglasses
       {'Hairdos' : 'Light-Mohawk', 'Outfits' : 'Medium-Robe'},
       {'Hairdos' : 'Light-Mohawk', 'Outfits' : 'Dark-Robe'},
       {'Hairdos' : 'Medium-Mohawk', 'Outfits' : 'Light-Robe'},
       {'Hairdos' : 'Medium-Mohawk', 'Outfits' : 'Dark-Robe'},
       {'Hairdos' : 'Dark-Mohawk', 'Outfits' : 'Light-Robe'},
       {'Hairdos' : 'Dark-Mohawk', 'Outfits' : 'Medium-Robe'},

       # i don't want zeke to have a wool scarf and a hoop earring
      #  {'Dog' : 'Zeke', 'Scarf' : 'WoolScarf', 'Earring' : 'hoop'}
    ],

    # these are the only traits i want to use for all 10,000 of the images
    #'Inclusions' : [
    #    {'Dog' : 'Buddy', 'LeftEarring' : 'CrossEarring20'},
    #    {'Dog' : 'Zeke', 'Scarf' : 'WoolScarf', 'RightEarring' : 'CrossEarring20'}]
    }


NFT_DEFINITION_DOGS = {
    'Name': 'CrazyDogs',
    'Description' : 'Crazy dogs with different traits.',
    'Quantity' : 20, #20, # 18290, # Quantity of NFT's to generate. 18291
    'QuantityOfExposableTokens' : 1, # The initial quantity of tokens that will have their metadata exposable.

    # Local folders for the input images and output images and output metadata.
    'InputImageFolder' : 'CrazyDogs/InputImages/', # Location of the input image files.
    'OutputImageFolder' : 'CrazyDogs/OutputImages/', # Location of the output NFTs and json metadata files.
    'OutputMetadataFolder' : 'CrazyDogs/OutputMetadata/', # Location of the output NFTs and json metadata files.
    'ImageExtension' : '.png',

    # Refer to the method CreateUris(nftDefinition) to understand how the following 2 fields are used.
    'BaseExternalUri' : 'https://www.cryptohermitsnft.com/',
    'BaseImageUri' : None,
    #'BaseExternalUri' : 'https://gateway.pinata.cloud/ipfs/Qmeuwa4V181ns6QknnZCdoEfp2yREcrB6neodDMHwCTG9o/',
    #'BaseImageUri' : 'ipfs://Qmeuwa4V181ns6QknnZCdoEfp2yREcrB6neodDMHwCTG9o/',

    'Traits' : (

        {'Name' : 'Dog',
         'Attributes' : ({'Name' : 'Buddy', 'FilePath' : 'body_dalmation.png', 'Offset' : (0, 0), 'Probability' : 90},
                         {'Name' : 'Zeke', 'FilePath' : 'body_dalmation_zeke.png', 'Offset' : (0, 0), 'Probability' : 10})},

        {'Name' : 'Sunglasses',
         'Attributes' : ({'Name' : 'Nothing', 'FilePath' : None, 'Probability' : 10},
                         {'Name' : 'CatEyes', 'FilePath' : 'sunglasses_cateyes.png', 'Offset' : (126, 24), 'Probability' : 40, 'Resize' : (80, 30)},
                         {'Name' : 'Rayban', 'FilePath' : 'sunglasses_rayban.png', 'Offset' : (126, 14), 'Probability' : 20, 'Resize' : (80, 30)},
                         {'Name' : 'Vuarnet', 'FilePath' : 'sunglasses_vuarnet.png', 'Offset' : (126, 24), 'Probability' : 30, 'Resize' : (80, 30)})},

        {'Name' : 'Scarf',
         'Attributes' : ({'Name' : 'Nothing', 'FilePath' : None, 'Probability' : 20},
                         {'Name' : 'ScandanavianScarf', 'FilePath' : 'scarf_scandinavian.png', 'Offset' : (142, 80), 'Probability' : 20, 'Resize' : (50, 120)}, # 146, 84
                         {'Name' : 'BlackScarf', 'FilePath' : 'scarf_black.png', 'Offset' : (142, 96), 'Probability' : 10, 'Resize' : (50, 120)},
                         {'Name' : 'PurpleScarf', 'FilePath' : 'scarf_purple.png', 'Offset' : (142, 96), 'Probability' : 20, 'Resize' : (50, 120)},

                         #{'Name' : 'MultiColorScarf', 'FilePath' : 'scarf_multi_color.png', 'Offset' : (142, 96), 'Probability' : 20, 'Resize' : (50, 120)},
                         {'Name' : 'MultiColorScarf1', 'FilePath' : 'scarf_multi_color.png', 'Offset' : (142, 96), 'Probability' : 1, 'Resize' : (50, 120)},
                         {'Name' : 'MultiColorScarf2', 'FilePath' : 'scarf_multi_color.png', 'Offset' : (142, 96), 'Probability' : 1, 'Resize' : (50, 120)},
                         {'Name' : 'MultiColorScarf3', 'FilePath' : 'scarf_multi_color.png', 'Offset' : (142, 96), 'Probability' : 1, 'Resize' : (50, 120)},
                         {'Name' : 'MultiColorScarf4', 'FilePath' : 'scarf_multi_color.png', 'Offset' : (142, 96), 'Probability' : 1, 'Resize' : (50, 120)},
                         {'Name' : 'MultiColorScarf5', 'FilePath' : 'scarf_multi_color.png', 'Offset' : (142, 96), 'Probability' : 1, 'Resize' : (50, 120)},
                         {'Name' : 'MultiColorScarf6', 'FilePath' : 'scarf_multi_color.png', 'Offset' : (142, 96), 'Probability' : 1, 'Resize' : (50, 120)},
                         {'Name' : 'MultiColorScarf7', 'FilePath' : 'scarf_multi_color.png', 'Offset' : (142, 96), 'Probability' : 1, 'Resize' : (50, 120)},
                         {'Name' : 'MultiColorScarf8', 'FilePath' : 'scarf_multi_color.png', 'Offset' : (142, 96), 'Probability' : 1, 'Resize' : (50, 120)},
                         {'Name' : 'MultiColorScarf9', 'FilePath' : 'scarf_multi_color.png', 'Offset' : (142, 96), 'Probability' : 1, 'Resize' : (50, 120)},
                         {'Name' : 'MultiColorScarf10', 'FilePath' : 'scarf_multi_color.png', 'Offset' : (142, 96), 'Probability' : 1, 'Resize' : (50, 120)},
                         {'Name' : 'MultiColorScarf11', 'FilePath' : 'scarf_multi_color.png', 'Offset' : (142, 96), 'Probability' : 1, 'Resize' : (50, 120)},
                         {'Name' : 'MultiColorScarf12', 'FilePath' : 'scarf_multi_color.png', 'Offset' : (142, 96), 'Probability' : 1, 'Resize' : (50, 120)},
                         {'Name' : 'MultiColorScarf13', 'FilePath' : 'scarf_multi_color.png', 'Offset' : (142, 96), 'Probability' : 1, 'Resize' : (50, 120)},
                         {'Name' : 'MultiColorScarf14', 'FilePath' : 'scarf_multi_color.png', 'Offset' : (142, 96), 'Probability' : 1, 'Resize' : (50, 120)},
                         {'Name' : 'MultiColorScarf15', 'FilePath' : 'scarf_multi_color.png', 'Offset' : (142, 96), 'Probability' : 1, 'Resize' : (50, 120)},
                         {'Name' : 'MultiColorScarf16', 'FilePath' : 'scarf_multi_color.png', 'Offset' : (142, 96), 'Probability' : 1, 'Resize' : (50, 120)},
                         {'Name' : 'MultiColorScarf17', 'FilePath' : 'scarf_multi_color.png', 'Offset' : (142, 96), 'Probability' : 1, 'Resize' : (50, 120)},
                         {'Name' : 'MultiColorScarf18', 'FilePath' : 'scarf_multi_color.png', 'Offset' : (142, 96), 'Probability' : 1, 'Resize' : (50, 120)},
                         {'Name' : 'MultiColorScarf19', 'FilePath' : 'scarf_multi_color.png', 'Offset' : (142, 96), 'Probability' : 1, 'Resize' : (50, 120)},
                         {'Name' : 'MultiColorScarf20', 'FilePath' : 'scarf_multi_color.png', 'Offset' : (142, 96), 'Probability' : 1, 'Resize' : (50, 120)},

                         {'Name' : 'WoolScarf', 'FilePath' : 'scarf_wool.png', 'Offset' : (142, 96), 'Probability' : 10, 'Resize' : (50, 120)})},

        {'Name' : 'LeftEarring',
         'Attributes' : ({'Name' : 'Nothing', 'FilePath' : None, 'Probability' : 80},
                         #{'Name' : 'CrossEarring', 'FilePath' : 'earring_cross.png', 'Offset' : (94, 35), 'Probability' : 20, 'Resize' : (40, 80)})},
                         {'Name' : 'CrossEarring01', 'FilePath' : 'earring_cross.png', 'Offset' : (94, 35), 'Probability' : 5, 'Resize' : (40, 80)},
                         {'Name' : 'CrossEarring03', 'FilePath' : 'earring_cross.png', 'Offset' : (94, 35), 'Probability' : 5, 'Resize' : (40, 80)},
                         {'Name' : 'CrossEarring05', 'FilePath' : 'earring_cross.png', 'Offset' : (94, 35), 'Probability' : 5, 'Resize' : (40, 80)},
                         {'Name' : 'CrossEarring20', 'FilePath' : 'earring_cross.png', 'Offset' : (94, 35), 'Probability' : 5, 'Resize' : (40, 80)})},

        {'Name' : 'RightEarring',
         'Attributes' : ({'Name' : 'Nothing', 'FilePath' : None, 'Probability' : 20},
                         #{'Name' : 'CrossEarring', 'FilePath' : 'earring_cross.png', 'Offset' : (201, 35), 'Probability' : 20, 'Resize' : (40, 80)})},
                         {'Name' : 'CrossEarring01', 'FilePath' : 'earring_cross.png', 'Offset' : (201, 35), 'Probability' : 4, 'Resize' : (40, 80)},
                         {'Name' : 'CrossEarring02', 'FilePath' : 'earring_cross.png', 'Offset' : (201, 35), 'Probability' : 4, 'Resize' : (40, 80)},
                         {'Name' : 'CrossEarring03', 'FilePath' : 'earring_cross.png', 'Offset' : (201, 35), 'Probability' : 4, 'Resize' : (40, 80)},
                         {'Name' : 'CrossEarring04', 'FilePath' : 'earring_cross.png', 'Offset' : (201, 35), 'Probability' : 4, 'Resize' : (40, 80)},
                         {'Name' : 'CrossEarring05', 'FilePath' : 'earring_cross.png', 'Offset' : (201, 35), 'Probability' : 4, 'Resize' : (40, 80)},
                         {'Name' : 'CrossEarring06', 'FilePath' : 'earring_cross.png', 'Offset' : (201, 35), 'Probability' : 4, 'Resize' : (40, 80)},
                         {'Name' : 'CrossEarring07', 'FilePath' : 'earring_cross.png', 'Offset' : (201, 35), 'Probability' : 4, 'Resize' : (40, 80)},
                         {'Name' : 'CrossEarring08', 'FilePath' : 'earring_cross.png', 'Offset' : (201, 35), 'Probability' : 4, 'Resize' : (40, 80)},
                         {'Name' : 'CrossEarring09', 'FilePath' : 'earring_cross.png', 'Offset' : (201, 35), 'Probability' : 4, 'Resize' : (40, 80)},
                         {'Name' : 'CrossEarring10', 'FilePath' : 'earring_cross.png', 'Offset' : (201, 35), 'Probability' : 4, 'Resize' : (40, 80)},
                         {'Name' : 'CrossEarring11', 'FilePath' : 'earring_cross.png', 'Offset' : (201, 35), 'Probability' : 4, 'Resize' : (40, 80)},
                         {'Name' : 'CrossEarring12', 'FilePath' : 'earring_cross.png', 'Offset' : (201, 35), 'Probability' : 4, 'Resize' : (40, 80)},
                         {'Name' : 'CrossEarring13', 'FilePath' : 'earring_cross.png', 'Offset' : (201, 35), 'Probability' : 4, 'Resize' : (40, 80)},
                         {'Name' : 'CrossEarring14', 'FilePath' : 'earring_cross.png', 'Offset' : (201, 35), 'Probability' : 4, 'Resize' : (40, 80)},
                         {'Name' : 'CrossEarring15', 'FilePath' : 'earring_cross.png', 'Offset' : (201, 35), 'Probability' : 4, 'Resize' : (40, 80)},
                         {'Name' : 'CrossEarring16', 'FilePath' : 'earring_cross.png', 'Offset' : (201, 35), 'Probability' : 4, 'Resize' : (40, 80)},
                         {'Name' : 'CrossEarring17', 'FilePath' : 'earring_cross.png', 'Offset' : (201, 35), 'Probability' : 4, 'Resize' : (40, 80)},
                         {'Name' : 'CrossEarring18', 'FilePath' : 'earring_cross.png', 'Offset' : (201, 35), 'Probability' : 4, 'Resize' : (40, 80)},
                         {'Name' : 'CrossEarring19', 'FilePath' : 'earring_cross.png', 'Offset' : (201, 35), 'Probability' : 4, 'Resize' : (40, 80)},
                         {'Name' : 'CrossEarring20', 'FilePath' : 'earring_cross.png', 'Offset' : (201, 35), 'Probability' : 4, 'Resize' : (40, 80)})},

        ),

    'Exclusions' : [
        {'Dog' : 'Buddy', 'Sunglasses' : 'Vuarnet'},
        {'Dog' : 'Zeke', 'Scarf' : 'WoolScarf', 'LeftEarring' : 'Nothing'}],

    #'Inclusions' : [
    #    {'Dog' : 'Buddy', 'LeftEarring' : 'CrossEarring20'},
    #    {'Dog' : 'Zeke', 'LeftEarring' : 'CrossEarring20'},
    #    {'Dog' : 'Zeke', 'Scarf' : 'WoolScarf', 'RightEarring' : 'CrossEarring20'}]
    }
