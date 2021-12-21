"""
Nft utilities.
"""
import datetime
import json
import os
import sys
import traceback

import csv
from PIL import ImageFont, ImageDraw
import pymongo

import nftConfig


######################################## GLOBAL CONSTANTS, DO NOT CHANGE!! ########################################
# 'CollectionData' Field Names
_COLLECTION_DATA = "CollectionData"
FIELD_BASE_EXTERNAL_URL = "BaseExternalUri"  # Used for the metadata field 'external_url'
FIELD_BASE_IMAGE_URI = "BaseImageUri"  # Used for the metadata field 'image'
FIELD_COLLECTION_NAME = "CollectionName"
FIELD_IMAGE_TYPE = "ImageType"  # png, json, etc
FIELD_TOKENS_MINTED = "TokensMinted"  # The quantity of tokens that have been minted so far.
FIELD_TOTAL_TOKENS = "TotalTokens"  # The total quantity of tokens in the collection.

# 'Nfts' Collection Field Names
_COLLECTION_NFTS = "Nfts"
FIELD_IMAGE_BINARY_STRING = "ImageBinaryString"  # bson image data
FIELD_RARITY = "rarity"  # Common, Uncommon, Rare, Epic, etc.
FIELD_TOKEN_ID = "TokenId"  # The integer tokenId.
FIELD_TOKEN_IS_EXPOSABLE = "TokenIsExposable"  # The token is exposable to the outside world.
FIELD_TRAIT_COUNT = "trait_count"  # The quantity of traits that have non-Nothing attributes.
FIELD_TRAITS = "attributes"  # The json that describes the attributes for each trait.

# Mongo database name.
_MONGO_DATABASE_NAME = "Nfts"


######################################## GLOBAL VARIABLES ########################################
def _GetMongoClient():
    """
    Returns the mongoDB client.
    """
    if nftConfig.DATABASE_CONNECTION_STRING:
        # Atlas
        return pymongo.MongoClient(nftConfig.DATABASE_CONNECTION_STRING)

    # localhost
    return pymongo.MongoClient("localhost", nftConfig.DATABASE_LOCAL_PORT)


def _GetMongoDb():
    """
    Returns a handle to the mongoDB
    """
    with _GetMongoClient() as client:
        return client[_MONGO_DATABASE_NAME]


# Database Handle
_DB = _GetMongoDb()


############################## PUBLIC METHODS CALLED FROM THE FRONT-END (nft.py or app.py) ##############################
def GetImage(tokenId):
    """
    This will retrieve the imageType and imageBinaryString from the database.
      1. Then you can display the imageBinaryString as a png file on a web page:
         https://newbedev.com/displaying-a-byte-array-as-an-image-using-javascript
         https://stackoverflow.com/questions/20756042/how-to-display-an-image-stored-as-byte-array-in-html-javascript
      2. Or you can turn the binary string into a PIL image:
           from PIL import Image
           image = Image.open(io.BytesIO(imageBinaryString))
           image.show()
      3. Or you can save it as an actual .png file:
           with open(str(tokenId) + '.' + imageType, 'wb') as f:
             f.write(imageBinaryString)
    """
    # The tokenId might came in as '8.json', so convert it to the integer 8.
    if isinstance(tokenId, str):
        tokenId = int(tokenId.split(".")[0])

    # Get the document.
    doc = _DB[_COLLECTION_NFTS].find_one({FIELD_TOKEN_ID: tokenId})
    if doc is None:
        # Error (not fatal).  The tokenId is not in the database.
        return None, None

    if not doc[FIELD_TOKEN_IS_EXPOSABLE]:
        # Error (not fatal).  The metadata fot tokenId is not exposable.
        return None, None

    # Return the image.
    imageType = _DB[_COLLECTION_DATA].find_one({}, {"_id": 0, FIELD_IMAGE_TYPE: 1})[FIELD_IMAGE_TYPE]
    return imageType, doc[FIELD_IMAGE_BINARY_STRING]


def GetMetadata(tokenId):
    """
    Find the metadata associated with the tokenId.
    """
    # The tokenId might came in as '8.json', so convert it to the integer 8.
    if isinstance(tokenId, str):
        tokenId = int(tokenId.split(".")[0])

    # Get the document.
    doc = _DB[_COLLECTION_NFTS].find_one({FIELD_TOKEN_ID: tokenId})
    if doc is None:
        # Error (not fatal).  The tokenId is not in the database.
        return None

    if not doc[FIELD_TOKEN_IS_EXPOSABLE]:
        # Error (not fatal).  The metadata fot tokenId is not exposable.
        return None

    # Return the metadata.
    return GetDocMetadata(doc)


def GetTokensMinted():
    """
    Get the database FIELD_TOKENS_MINTED.
    """
    return _DB[_COLLECTION_DATA].find_one({}, {"_id": 0, FIELD_TOKENS_MINTED: 1})[FIELD_TOKENS_MINTED]


def GetTotalTokens():
    """
    Get the database FIELD_TOTAL_TOKENS.
       _DB[_COLLECTION_NFTS].count_documents({}) is the only 100% guaranteed way to get the correct number.
       But this is really slow because it is a query and loops through, counting each doc.
       So we store the actual count in the _COLLECTION_DATA in nftUtil.CreateMetadata().
    """
    return _DB[_COLLECTION_DATA].find_one({}, {"_id": 0, FIELD_TOTAL_TOKENS: 1})[FIELD_TOTAL_TOKENS]


def ProcessException():
    """
    Called for totally unexpected errors from an 'Except:' block where you need a stack trace.
    It's only called from the front-end app.py.
    """
    stackTrace = traceback.format_exc()
    return stackTrace


def SetTokensMinted(tokensMinted, password):
    """
    Set the database FIELD_TOKENS_MINTED with tokensMinted.
    """
    if password != nftConfig.FRONTEND_BACKEND_PASSWORD:
        return
    tokensMinted = int(tokensMinted)
    _DB[_COLLECTION_DATA].update_one({}, {"$set": {FIELD_TOKENS_MINTED: tokensMinted}})


########## PUBLIC METHODS CALLED FROM PROGRAMMER UTILITIES (nftInitializeDatabase.py, nftMakeImage.py, nftTestCases.py, nftReport.py) ##########
def ApplyCopyright(image):
    """
    Apply a copyright notice to the image.
    """
    # You cannot use ImageFont.load_default(), because that does not let you specify the font size.
    # So use a specific .ttf file.  You can find ttf files on a mac in either /System/Library/Fonts or /Library/Fonts.
    # https://stackoverflow.com/questions/58968752/loading-fonts-in-python-pillow-on-a-mac
    font = ImageFont.truetype("Roboto-Regular.ttf", size=8)  # You can use size=6, but it gets really fuzzy.
    text = "Copyright " + "\u00a9" + " 2021 BlockBot LLC, All Rights Reserved."
    imageDraw = ImageDraw.Draw(image)

    #   x = 2
    #   y = 986 is enough vertical room for 12-point font (or less)
    #   y = 987 is enough vertical room for 10-point font (or less)
    #   y = 988 is enough vertical room for  8-point font (or less)
    #   y = 990 is enough vertical room for  6-point font (or less)

    # Turn (62,63,64,255) into (22,23,24,255)
    # x = 2 Gets the white tile color, when most of the copyright is in the black tile.  So set x to 30 instead when determining the fill color.
    whiter = 40  # Increase to make copyright more visible (whiter), decrease to make copyright less visible.
    fill = []
    for f, rgba in enumerate(image.getpixel((30, 988))):
        fill.append(min(rgba + whiter, 254) if f < 3 else rgba)
    imageDraw.text(xy=(2, 988), text=text, fill=tuple(fill), font=font)

    return image


def BackupAndInitializeDatabase(nftDefinition, doBackup=True):
    """
    Rename the existing collection with a date/time stamp suffix as a backup, and then drop the existing collection.
    You can manually drop the backups later using db.collectionName.drop()
    """
    with _GetMongoClient() as client:
        if _MONGO_DATABASE_NAME in client.list_database_names():
            if doBackup:
                for collection in (_COLLECTION_NFTS, _COLLECTION_DATA):
                    if collection in _DB.list_collection_names():
                        # Make a backup copy of the collection with a date/time stamp as the suffix.
                        _DB[collection].rename(collection + "_" + _Now())
                        _DB[collection].drop()
            else:
                client.drop_database(_MONGO_DATABASE_NAME)

    # Add the one-and-only CollectionData document.
    _DB[_COLLECTION_DATA].insert_one(
        {
            FIELD_BASE_EXTERNAL_URL: nftDefinition["BaseExternalUri"],  # Used for 'external_url'
            FIELD_BASE_IMAGE_URI: nftDefinition["BaseImageUri"],  # Used for 'image'
            FIELD_COLLECTION_NAME: nftDefinition["Name"],
            FIELD_IMAGE_TYPE: nftDefinition["ImageType"],  # png, json, etc
            FIELD_TOKENS_MINTED: -1,
            FIELD_TOTAL_TOKENS: -1,
        }
    )

    # Create ascending (1) unique indexes.
    _DB[_COLLECTION_NFTS].create_index([(FIELD_TOKEN_ID, 1)], unique=True)


def CreateMetadata(nftDefinition):
    """
    1. Update the one-and-only doc in _COLLECTION_DATA with the following fields from nftDefinition:
       FIELD_BASE_EXTERNAL_URL: nftDefinition['BaseExternalUri'],
       FIELD_BASE_IMAGE_URI: nftDefinition['BaseImageUri'],
       FIELD_COLLECTION_NAME: nftDefinition['Name'],
    2. Update each Nfts doc with a possibly new value for FIELD_TOKEN_IS_EXPOSABLE based on nftDefinition['QuantityOfExposableTokens'].
    3. Regenerate all of the metadata files.
         These fields might change if the corresponding _COLLECTION_DATA (nftDefinition) has changed.
                   "description": "Bookworms token number 1, with a rarity of 'Epic'",
                   "external_url": "https://www.cryptohermitsnft.com/images/1.png",
                   "image": "https://www.cryptohermitsnft.com/images/1.png",
         But if someone has manually swapped the tokenIds in the database, then almost everything can change.
    """
    print()

    # 1. Change the _COLLECTION_DATA.  This will apply any changes that have been made to nftDefinition.
    _DB[_COLLECTION_DATA].update_one(
        {},
        {
            "$set": {
                FIELD_BASE_EXTERNAL_URL: nftDefinition["BaseExternalUri"],
                FIELD_BASE_IMAGE_URI: nftDefinition["BaseImageUri"],
                FIELD_COLLECTION_NAME: nftDefinition["Name"],
                # FIELD_IMAGE_TYPE: nftDefinition['ImageType'] Cannot update this field because all of the images have already been generated.
                FIELD_TOTAL_TOKENS: _DB[_COLLECTION_NFTS].count_documents({}),
            }
        },
    )

    # 2. Create all of the metadata files.
    allMetadatas = []
    for i, doc in enumerate(_DB[_COLLECTION_NFTS].find()):
        if i % 10 == 0:
            print("Writing Metadata", str(i))

        # Only expose a certain quantity of tokens.
        tokenIsExposable = doc[FIELD_TOKEN_ID] <= nftDefinition["QuantityOfExposableTokens"]
        _DB[_COLLECTION_NFTS].update_one({FIELD_TOKEN_ID: doc[FIELD_TOKEN_ID]}, {"$set": {FIELD_TOKEN_IS_EXPOSABLE: tokenIsExposable}})

        # Update the doc and then write out the metadata.
        doc[FIELD_TOKEN_IS_EXPOSABLE] = tokenIsExposable
        metadata = GetDocMetadata(doc)
        with open(os.path.join(nftDefinition["OutputMetadataFolder"], str(doc[FIELD_TOKEN_ID])) + ".json", "w") as f:
            json.dump(metadata, f)
        allMetadatas.append(metadata)

    # Write allMetadatas to a file.
    with open(os.path.join(nftDefinition["OutputMetadataFolder"], "_metadata.json"), "w") as f:
        json.dump(allMetadatas, f)
    print("Wrote", len(allMetadatas), "metadata files")


def FatalExit(message):
    """
    Print the fatal message and exit.  Should only be used in utilities that the programmer runs from the command line.
    """
    print(message)
    sys.exit(1)


def FormatPercent(nbr):
    """
    Format nbr into a percent string.
    """
    return str(round(100 * nbr, 2)) + "%"


def GetDocMetadata(doc):
    """
    Return the metadata for doc.
    """
    collectionDataDoc = _DB[_COLLECTION_DATA].find_one({})
    metadata = {
        "description": collectionDataDoc[FIELD_COLLECTION_NAME] + " token number " + str(doc[FIELD_TOKEN_ID]) + ", with a rarity of '" + doc[FIELD_RARITY] + "'",
        "external_url": collectionDataDoc[FIELD_BASE_EXTERNAL_URL] + str(doc[FIELD_TOKEN_ID]) + "." + collectionDataDoc[FIELD_IMAGE_TYPE],
        "image": collectionDataDoc[FIELD_BASE_IMAGE_URI] + str(doc[FIELD_TOKEN_ID]) + "." + collectionDataDoc[FIELD_IMAGE_TYPE],
        "name": str(doc[FIELD_TOKEN_ID]),
        "trait_count": doc[FIELD_TRAIT_COUNT],
        "rarity": doc[FIELD_RARITY],
        "attributes": doc[FIELD_TRAITS],
    }
    return metadata


def InsertOneDocument(doc):
    """
    Insert the document into the collection.
    """
    _DB[_COLLECTION_NFTS].insert_one(doc)


def IsExposable(tokenId):
    """
    Determine if the metadata for tokenId is exposable to the outside world.
    """
    return _DB[_COLLECTION_NFTS].find_one({FIELD_TOKEN_ID: tokenId})[FIELD_TOKEN_IS_EXPOSABLE]


def ReportNfts(filePath="AllNfts.csv", fieldNames=(FIELD_TOKEN_ID, FIELD_TOKEN_IS_EXPOSABLE, FIELD_RARITY, FIELD_TRAIT_COUNT, FIELD_TRAITS)):
    """
    Create a csv report to filePath containing fieldNames.
      filePath = The csv report output file.
      fieldNames = A list of fieldNames that will be the columns in the report.
    """
    qtyWritten = 0
    with open(filePath, "w", newline="") as fileHandle:
        csvWriter = csv.writer(fileHandle, quoting=csv.QUOTE_MINIMAL)
        csvWriter.writerow(fieldNames)  # headers
        for doc in _DB[_COLLECTION_NFTS].find():
            row = []
            for fieldName in fieldNames:
                row.extend(doc[fieldName] if fieldName in (FIELD_TRAITS,) else [doc[fieldName]])
            csvWriter.writerow(row)
            qtyWritten += 1
    print("Wrote", qtyWritten, "documents to", filePath)


def StringsMatch(a, b):
    """
    1. a can contain wildcards.
    2. if a starts with '!', that means not (reverse the truth).
    """
    a = a.upper()
    b = b.upper()
    if a.startswith("!"):
        reverseTruth = True
        a = a[1:]
    else:
        reverseTruth = False
    doesMatch = _match(a, b)
    return doesMatch if not reverseTruth else (not doesMatch)


def UpdateField(updates):
    """
    Update mongoDB with a list of field values.
        updates is a list of lists:
           0 = uniqueKeyFieldName
           1 = uniqueKeyFieldValue
           2 = fieldNameToUpdate
           3 = fieldValueToUpdate
        Example"
           data = [['TokenId', 21, 'TokenIsExposable', True], ['TokenId', 22, 'TraitCount', 12]]
    """
    for update in updates:
        search = {update[0]: (int(update[1]) if update[0] == FIELD_TOKEN_ID else update[1])}
        if _DB[_COLLECTION_NFTS].find_one(search):
            _DB[_COLLECTION_NFTS].update_one(search, {"$set": {update[2]: update[3]}})
            print(update)


def ValidateFolderName(folderName):
    """
    If folderName is not valid, then fail.
    """
    if folderName[-1] != "/":
        FatalExit(folderName + ' must end in a "/"')


def ValidateUniqueNames(thingList):
    """
    Validate that all names are unique.
    """
    names = set()
    for thing in thingList:
        name = thing["Name"]
        if name in names:
            FatalExit("Duplicate name " + name)
        names.add(name)


############################## PRIVATE METHODS ##############################


def _match(first, second):
    """
    From: https://www.geeksforgeeks.org/wildcard-character-matching/
    Returns True if the two given strings match.  The first string may contain wildcard characters
    """
    # If we reach at the end of both strings, we are done
    if len(first) == 0 and len(second) == 0:
        return True

    # Make sure that the characters after '*' are present
    # in second string. This function assumes that the first
    # string will not contain two consecutive '*'
    if len(first) > 1 and first[0] == "*" and len(second) == 0:
        return False

    # If the first string contains '?', or current characters
    # of both strings match
    if (len(first) > 1 and first[0] == "?") or (len(first) != 0 and len(second) != 0 and first[0] == second[0]):
        return _match(first[1:], second[1:])

    # If there is *, then there are two possibilities
    # a) We consider current character of second string
    # b) We ignore current character of second string.
    if len(first) != 0 and first[0] == "*":
        return _match(first[1:], second) or _match(first, second[1:])

    return False


def _Now():
    """
    Now.
    """
    return str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
