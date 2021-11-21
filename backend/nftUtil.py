'''
Nft utilities.  All back-end.  See nft.py for front-end methods.
'''
import datetime
import json
import os
import smtplib
import sys
import traceback

import csv
import filelock
import pymongo

import nftConfig


######################################## GLOBAL CONSTANTS, DO NOT CHANGE!! ########################################
_EMPTY_STRING = ''

# Credentials for using gmail as our SMTP email server.
_GMAIL_USER = 'jjjkreynolds@gmail.com'
_GMAIL_APP_PASSWORD = 'pvyuqjfqwgmtpqae'

# 'Nfts' Collection Field Names
_COLLECTION_NFTS = 'Nfts'
FIELD_ID = '_id'
FIELD_COLLECTION_NAME = 'CollectionName'
FIELD_EXTERNAL_URL = 'external_url' # 'ExternalUrl'
FIELD_IMAGE_BINARY_STRING = 'ImageBinaryString' # bson image data
FIELD_IMAGE_TYPE = 'ImageType' # png, json, etc
FIELD_IMAGE_URI = 'image' # 'ImageUri'
FIELD_PERMUTATION = 'Permutation' # Numeric permutation of the attributes.
FIELD_RARITY = 'rarity' # Gold, Silver, Bronze
FIELD_STATISTICAL_RARITY = 'StatisticalRarity' # statistical_rarity
FIELD_TOKEN_IS_EXPOSABLE = 'TokenIsExposable'
FIELD_TRAIT_COUNT = 'trait_count' # The quantity of non-Nothing traits.
FIELD_TRAITS = 'attributes' # 'Traits'
FIELD_TRANSACTIONS = 'Transactions' # array

# 'Statistics' Collection Field Names
_COLLECTION_STATISTICS = 'Statistics'
FIELD_TOKENS_MINTED = 'TokensMinted'
FIELD_TOTAL_TOKENS = 'TotalTokens'

# Logging levels.
_LEVEL_DEBUG = 'DEBUG'
_LEVEL_INFO = 'INFO'   # Informational.  Like when an NFT is successfully sold.
_LEVEL_ERROR = 'ERROR'

# The name of the log file.
_LOG_FILE_NAME = 'NftLog.csv'

# Mongo database name.
_MONGO_DATABASE_NAME = 'Nfts'


######################################## GLOBAL VARIABLES ########################################
def _GetMongoClient():
    '''
    Returns the mongoDB client.
    '''
    if nftConfig.DATABASE_CONNECTION_STRING:
        # Atlas
        return pymongo.MongoClient(nftConfig.DATABASE_CONNECTION_STRING)

    # localhost
    return pymongo.MongoClient('localhost', nftConfig.DATABASE_LOCAL_PORT)

def _GetMongoDb():
    '''
    Returns a handle to the mongoDB
    '''
    with _GetMongoClient() as client:
        return client[_MONGO_DATABASE_NAME]

# Database Handle
_DB = _GetMongoDb()


############################## PUBLIC METHODS CALLED FROM THE FRONT-END (nft.py or app.py) ##############################
def GetImage(tokenId):
    '''
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
    '''
    # The tokenId might came in as '8.json', so convert it to the integer 8.
    if isinstance(tokenId, str):
        tokenId = int(tokenId.split(".")[0])

    # Get the document.
    doc = _DB[_COLLECTION_NFTS].find_one({FIELD_ID : tokenId})
    if doc is None:
        # Error (not fatal).  The tokenId is not in the database.
        _LogLine('The tokenId ' + str(tokenId) + ' does not exist.', _LEVEL_ERROR)
        return None, None

    if not doc[FIELD_TOKEN_IS_EXPOSABLE]:
        # Error (not fatal).  The metadata fot tokenId is not exposable.
        _LogLine('The tokenId ' + str(tokenId) + ' is not exposable.', _LEVEL_ERROR)
        return None, None

    # Log the action.
    _LogLine('Retrieved image for tokenId ' + str(tokenId), _LEVEL_INFO, tokenId)

    # Return the image.
    return doc[FIELD_IMAGE_TYPE], doc[FIELD_IMAGE_BINARY_STRING]

def GetMetadata(tokenId):
    '''
    Find the metadata associated with the tokenId.
    '''
    # The tokenId might came in as '8.json', so convert it to the integer 8.
    if isinstance(tokenId, str):
        tokenId = int(tokenId.split(".")[0])

    # Get the document.
    doc = _DB[_COLLECTION_NFTS].find_one({FIELD_ID : tokenId})
    if doc is None:
        # Error (not fatal).  The tokenId is not in the database.
        _LogLine('The tokenId ' + str(tokenId) + ' does not exist.', _LEVEL_ERROR)
        return None

    if not doc[FIELD_TOKEN_IS_EXPOSABLE]:
        # Error (not fatal).  The metadata fot tokenId is not exposable.
        _LogLine('The tokenId ' + str(tokenId) + ' is not exposable.', _LEVEL_ERROR)
        return None

    # Log the action.
    _LogLine('Retrieved metadata for tokenId ' + str(tokenId), _LEVEL_INFO, tokenId)

    # Return the metadata.
    return GetDocMetadata(doc)

def GetTokensMinted():
    '''
    Get the database FIELD_TOKENS_MINTED.
    '''
    return _DB[_COLLECTION_STATISTICS].find_one({}, {FIELD_ID: 0, FIELD_TOKENS_MINTED: 1})[FIELD_TOKENS_MINTED]

def GetTotalTokens():
    '''
    Get the database FIELD_TOTAL_TOKENS.
    '''
    return _DB[_COLLECTION_STATISTICS].find_one({}, {FIELD_ID: 0, FIELD_TOTAL_TOKENS: 1})[FIELD_TOTAL_TOKENS]

def ProcessException():
    '''
    Called for totally unexpected errors from an 'Except:' block where you need a stack trace.
    It's only called from the front-end nft.py.
    '''
    stackTrace = traceback.format_exc()
    _LogLine(message='Unexpected exception', level=_LEVEL_ERROR, secondaryMessage=stackTrace)
    return stackTrace

def SendEmail(arguments):
    '''
    Send email.
    '''
    if not nftConfig.DO_SEND_EMAILS:
        return

    # Get arguments.
    toAddresses = arguments['toAddresses'] # comma-delimited list of email adresses
    subject = arguments['subject'] # email subject
    body = arguments['body'] # email body
    tokenId = _GetArgumentOrDefault(arguments, 'tokenId', '') # the associated tokenId, if any
    ccAddresses = _GetArgumentOrDefault(arguments, 'ccAddresses', '') # comma-delimited list of email adresses
    bccAddresses = _GetArgumentOrDefault(arguments, 'bccAddresses', '') # comma-delimited list of email adresses

    # Construct the address lists.
    tos = toAddresses.split(',')
    tos += (ccAddresses.split(',') if ccAddresses else []) + (bccAddresses.split(',') if bccAddresses else [])
    toAllAddresses = []
    _ = [toAllAddresses.append(x.strip()) for x in tos if x.strip() not in toAllAddresses] # trim and remove duplicates

    # Construct the email text.
    emailText = _ConcatenateToString((
        'From: ', _GMAIL_USER, '\n',
        'To: ', toAddresses, '\n',
        ('CC: ' + ccAddresses + '\n' if ccAddresses else ''),
        'Subject: ', subject[:255], '\n',
        body))

    # Send the email.
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.ehlo()
            server.login(_GMAIL_USER, _GMAIL_APP_PASSWORD)
            server.sendmail(_GMAIL_USER, toAllAddresses, emailText)
            _LogLine(message='Sent email:  ' + subject, level=_LEVEL_DEBUG, tokenId=tokenId, sendEmail=False)
    except:
        # sendEmail = False, otherwise endless recusrive loop.
        _LogLine(message='Exception sending email', level=_LEVEL_ERROR, tokenId=tokenId, secondaryMessage=traceback.format_exc(), sendEmail=False)

def SetTokensMinted(tokensMinted):
    '''
    Set the database FIELD_TOKENS_MINTED with tokensMinted.
    '''
    tokensMinted = int(tokensMinted)
    _DB[_COLLECTION_STATISTICS].update_one({}, {'$set': {FIELD_TOKENS_MINTED: tokensMinted}})

def SetTotalTokens(totalTokens):
    '''
    Set the database FIELD_TOTAL_TOKENS with totalTokens.
    '''
    totalTokens = int(totalTokens)
    _DB[_COLLECTION_STATISTICS].update_one({}, {'$set': {FIELD_TOTAL_TOKENS: totalTokens}})

############################## PUBLIC METHODS CALLED ONLY FROM nftTestCases.py ##############################
def IsExposable(tokenId):
    '''
    Determine if the metadata for tokenId is exposable.
    '''
    return _DB[_COLLECTION_NFTS].find_one({FIELD_ID : tokenId})[FIELD_TOKEN_IS_EXPOSABLE]

def QuantityOfAllNfts():
    '''
    Get the total quantity of NFT documents.
    '''
    return _DB[_COLLECTION_NFTS].count_documents({})


################ PUBLIC METHODS CALLED FROM PROGRAMMER UTILITIES (nftInitializeDatabase.py, nftTestCases.py, nftReport.py) ################
def BackupAndInitializeDatabase(doBackup=True):
    '''
    Rename the existing collection with a time stamp as a backup, and then drop the existing collection.
    # You can manually drop the backups later using db.collectionName.drop()
    '''
    with _GetMongoClient() as client:
        if _MONGO_DATABASE_NAME in client.list_database_names():
            if doBackup:
                for collection in (_COLLECTION_NFTS, _COLLECTION_STATISTICS):
                    if collection in _DB.list_collection_names():
                        _DB[collection].rename(collection + '_' + _Now())
                        _DB[collection].drop()
            else:
                client.drop_database(_MONGO_DATABASE_NAME)

    _DB[_COLLECTION_STATISTICS].insert_one({FIELD_TOKENS_MINTED: -1, FIELD_TOTAL_TOKENS: -1})

    # Create ascending (1) unique indexes.  Not really necessary, but ensures integrity.
    ## Cannot do these because they could be None.
    ##_DB[_COLLECTION_NFTS].create_index([(FIELD_IMAGE_URI, 1)], unique=True)
    ##_DB[_COLLECTION_NFTS].create_index([(FIELD_EXTERNAL_URL, 1)], unique=True)

def CreateMetadata(nftDefinition):
    '''
    1. First, this will:
       a) Create the 'external_url' field based on the corresponding 'BaseExternalUri' field in the nftDefinition:

        'BaseExternalUri' : 'https://www.cryptohermitsnft.com/',
        'external_url' = https://www.cryptohermitsnft.com/1

        'BaseExternalUri' : 'https://gateway.pinata.cloud/ipfs/Qmeuwa4V181ns6QknnZCdoEfp2yREcrB6neodDMHwCTG9o/',
        'external_url' = https://gateway.pinata.cloud/ipfs/Qmeuwa4V181ns6QknnZCdoEfp2yREcrB6neodDMHwCTG9o/1.png

       b) Create the 'image' field based on the corresponding 'BaseImageUri' field in the nftDefinition:

        'BaseImageUri' : None,
        'image' = None

        'BaseImageUri' : 'ipfs://Qmeuwa4V181ns6QknnZCdoEfp2yREcrB6neodDMHwCTG9o/',
        'image' = ipfs://Qmeuwa4V181ns6QknnZCdoEfp2yREcrB6neodDMHwCTG9o/1.png

    2. It will then write out the full resulting metadata files with the updated 'external_url' and 'image' fields.
    '''
    print()
    allMetadatas = []
    for i, doc in enumerate(_DB[_COLLECTION_NFTS].find()):
        if i % 10 == 0:
            print('Writing Metadata', str(i)) #+ ('...' if i == 0 else ' ' + str(i)))

        # Only expose a certain quantity of tokens.
        tokenIsExposable = doc[FIELD_ID] <= nftDefinition['QuantityOfExposableTokens']

        # Determine externalUrl and imageUrl
        externalUrl = None
        imageUri = None
        for b, base in enumerate((nftDefinition['BaseExternalUri'], nftDefinition['BaseImageUri'])):
            if base is not None:
                if base[-1] != '/':
                    base += '/'
                newValue = base + str(doc[FIELD_ID]) + nftDefinition['ImageExtension']
                if b == 0:
                    externalUrl = newValue
                elif b == 1:
                    imageUri = newValue

        _DB[_COLLECTION_NFTS].update_one({FIELD_ID: doc[FIELD_ID]},
                                         {'$set' : {FIELD_TOKEN_IS_EXPOSABLE: tokenIsExposable,
                                                    FIELD_EXTERNAL_URL: externalUrl,
                                                    FIELD_IMAGE_URI: imageUri}})

        # Update the doc and then write out the metadata.
        doc[FIELD_TOKEN_IS_EXPOSABLE] = tokenIsExposable
        doc[FIELD_EXTERNAL_URL] = externalUrl
        doc[FIELD_IMAGE_URI] = imageUri
        metadata = GetDocMetadata(doc)
        with open(os.path.join(nftDefinition['OutputMetadataFolder'], str(doc[FIELD_ID])) + '.json', 'w') as f:
            json.dump(metadata, f)
        allMetadatas.append(metadata)

    # Write allMetadatas to a file.
    with open(os.path.join(nftDefinition['OutputMetadataFolder'], '_metadata.json'), 'w') as f:
        json.dump(allMetadatas, f)
    print('Wrote', len(allMetadatas), 'metadata files')

def FloatingPointEquivalent(fp1, fp2):
    '''
    Return True if fp1 ~= fp2
    '''
    return abs(fp1 - fp2) < 0.000000000001

def FatalExit(message):
    '''
    Print the fatal message and exit.  Should only be used in utilities that the programmer runs from the command line.
    '''
    print(message)
    sys.exit(1)

def GetDocMetadata(doc):
    '''
    Return the metadata for doc.  This is from the OpenSea standard:
    https://medium.com/code-sprout/upload-multiple-images-in-opensea-nft-d79dd7bb762b
    {
      "description": "Friendly OpenSea Creature that enjoys long swims in the ocean.",
      "external_url": "https://openseacreatures.io/3",
      "image": "https://storage.googleapis.com/opensea-prod.appspot.com/puffs/3.png",
      "name": "Dave Starbelly",
      "attributes": [ ... ],
    }
    '''
    metadata = {'description': doc[FIELD_COLLECTION_NAME] + ' token number ' + str(doc[FIELD_ID]) + ('' if doc[FIELD_RARITY] is None else ", with a rarity of '" + doc[FIELD_RARITY] + "'"),
                'external_url': doc[FIELD_EXTERNAL_URL],
                'image': doc[FIELD_IMAGE_URI],
                'name': str(doc[FIELD_ID]),
                #'statistical_rarity': doc[FIELD_STATISTICAL_RARITY],
                'trait_count': doc[FIELD_TRAIT_COUNT],
                'rarity': doc[FIELD_RARITY],
                'attributes': doc[FIELD_TRAITS]}
    if metadata['rarity'] is None:
        del metadata['rarity']
    return metadata

def InsertOneDocument(doc):
    '''
    Insert the document into the collection.
    '''
    _DB[_COLLECTION_NFTS].insert_one(doc)

def ReportFields(filePath, fieldNames):
    '''
    Create a csv report to filePath containing fieldNames.
      filePath = The csv report output file.
      fieldNames = A list of fieldNames that will be the columns in the report.
    '''
    qtyWritten = 0
    with open(filePath, 'w', newline='') as fileHandle:
        csvWriter = csv.writer(fileHandle, quoting=csv.QUOTE_MINIMAL)
        csvWriter.writerow(fieldNames) # headers
        for doc in _DB[_COLLECTION_NFTS].find():
            row = []
            for fieldName in fieldNames:
                #if fieldName == FIELD_STATISTICAL_RARITY:
                #    doc[fieldName] = f'{doc[fieldName]:.32f}' #.rstrip('0')
                row.extend(doc[fieldName] if fieldName in (FIELD_PERMUTATION, FIELD_TRANSACTIONS, FIELD_TRAITS) else [doc[fieldName]])
            csvWriter.writerow(row)
            qtyWritten += 1
    print('Wrote', qtyWritten, 'documents to', filePath)

def StringsMatch(a, b):
    '''
    1. a can contain wildcards.
    2. if a starts with '!', that means not (reverse the truth).
    '''
    a = a.upper()
    b = b.upper()
    if a.startswith('!'):
        reverseTruth = True
        a = a[1:]
    else:
        reverseTruth = False
    doesMatch = _match(a, b)
    return doesMatch if not reverseTruth else (not doesMatch)

def UpdateField(updates):
    '''
    updates is a list of lists:
       0 = uniqueKeyFieldName
       1 = uniqueKeyFieldValue
       2 = fieldNameToUpdate
       3 = fieldValueToUpdate
    Example"
       data = [['_id', 21, 'TokenIsExposable', True], ['_id', 22, 'external_url', None]]
    '''
    for update in updates:
        search = {update[0]: (int(update[1]) if update[0] == FIELD_ID else update[1])}
        if _DB[_COLLECTION_NFTS].find_one(search):
            _DB[_COLLECTION_NFTS].update_one(search, {'$set' : {update[2]: update[3]}})
            print(update)

############################## PRIVATE METHODS ##############################
def _ConcatenateToString(words):
    '''
    Return [words] concatenated into a string.
    '''
    #for w in range(len(words)):
    #    words[w] = str(words[w])
    words = [str(x) for x in words]
    return _EMPTY_STRING.join(words)

def _GetArgumentOrDefault(arguments, argumentName, defaultValue):
    '''
    Return the argumentValue for 'argumentName'.  If it does not exist, then return defaultValue.
    '''
    return arguments[argumentName] if (arguments and argumentName in arguments) else defaultValue

def _LogLine(message, level, tokenId=_EMPTY_STRING, secondaryMessage=_EMPTY_STRING, sendEmail=True):
    '''
    Log a message to Logger.
        message = Message
        level = _LEVEL_* constant
        tokenId = tokenId
        secondaryMessage = A secondary message.  Typically 'status' from the front-end.
        sendEmail = False if you don't want an email to be sent
    You cannot use any of the standard py logging modules because they keep files open once they are instantiated.
    And the cycling backups were a nightmare!  Plus, they were way too complicated.
    '''
    # Print to console.
    if nftConfig.DO_WRITE_TO_CONSOLE:
        print(('!!!! ' if level == _LEVEL_ERROR else _EMPTY_STRING) + message)

    # Double Quotes will mess up the csv log file.
    message = message.replace('"', _EMPTY_STRING).strip()
    secondaryMessage = secondaryMessage.replace('"', _EMPTY_STRING).strip()

    if nftConfig.DO_WRITE_LOG_FILE:
        # You definitely need this lock.  Otherwise multiple simultaneous processes writing to the log file will corrupt it.
        with filelock.FileLock(_LOG_FILE_NAME + '.lock', timeout=9):

            # Create a backup file.
            if os.path.exists(_LOG_FILE_NAME) and 500000 < os.path.getsize(_LOG_FILE_NAME):
                os.rename(_LOG_FILE_NAME, 'NftLog.' + _Now() + '.csv')

            # Write the header line.
            if not os.path.exists(_LOG_FILE_NAME):
                with open(_LOG_FILE_NAME, 'w+') as f:
                    f.write('Time,ProcessId,Level,Back-End Message,Secondary Message,NftId\n')

            # Write the detail line.
            with open(_LOG_FILE_NAME, 'a+') as f:
                detailLine = _ConcatenateToString((_Now(), ',', os.getpid(), ',', level, ',"', message, '","', secondaryMessage, '","', tokenId, '"\n'))
                f.write(detailLine)

    # Maybe send an email to alert for bad stuff.  This cannot be within the fileLock because it also calls _LogLine().
    if level == _LEVEL_ERROR and sendEmail:
        emailBody = _ConcatenateToString((
            'Hey Winnie and Wilson,\n\n',
            message, '\n\n',
            (secondaryMessage + '\n\n' if secondaryMessage else _EMPTY_STRING),
            'Hope you catch a lizard,\nBoo\n'))
        SendEmail({'toAddresses':nftConfig.SEND_TO_EMAIL_ADDRESSES, 'subject':message, 'body':emailBody, 'tokenId':tokenId})

def _match(first, second):
    '''
    From: https://www.geeksforgeeks.org/wildcard-character-matching/
    Returns True if the two given strings match.  The first string may contain wildcard characters
    '''
    # If we reach at the end of both strings, we are done
    if len(first) == 0 and len(second) == 0:
        return True

    # Make sure that the characters after '*' are present
    # in second string. This function assumes that the first
    # string will not contain two consecutive '*'
    if len(first) > 1 and first[0] == '*' and  len(second) == 0:
        return False

    # If the first string contains '?', or current characters
    # of both strings match
    if (len(first) > 1 and first[0] == '?') or (len(first) != 0 and len(second) != 0 and first[0] == second[0]):
        return _match(first[1:], second[1:])

    # If there is *, then there are two possibilities
    # a) We consider current character of second string
    # b) We ignore current character of second string.
    if len(first) != 0 and first[0] == '*':
        return _match(first[1:], second) or _match(first, second[1:])

    return False

def _Now():
    '''
    Now.
    '''
    return str(datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))


############################## HOUSEKEEPING ##############################
# Don't continue if you cannot access the log file.
if nftConfig.DO_WRITE_LOG_FILE:
    _LogLine('Initializing ' + _LOG_FILE_NAME + '...', _LEVEL_DEBUG)
