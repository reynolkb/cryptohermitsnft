'''
Create all image and metadata files for a collection, and load the database.
For Profiling run:
   python -m cProfile nftCreate.py >t.csv
'''
import copy
import io
import os
import random
import time
from PIL import Image

import bson
import nftConfig
import nftUtil


############################################# C O N S T A N T S #############################################
# Debug
DEBUG = False


def ApplyAttribute(nftDefinition, baseImage, attribute, inputImages):
    '''
    Apply the attribute to the base image.
    '''
    filePath = attribute['FilePath']
    if filePath is None:
        # This is valid.  It means that the attribute is not applied.
        return baseImage

    inputFolder = nftDefinition['InputImageFolder']
    offset = attribute['Offset'] if 'Offset' in attribute else (0, 0)
    inputImage = inputImages[os.path.join(inputFolder, filePath)]
    baseImage.paste(inputImage, offset, inputImage)

    return baseImage

def GenerateQualifyingPermutations(nftDefinition):
    '''
    Get all possible qualifying permutations.
    Filter out the 'Inclusions' and 'Exclusions' in nftDefinition with PermutationQualifies().
    https://www.askpython.com/python-modules/python-itertools-module
    '''
    # Recursively get all possible permutations.
    # pass in 0 and an empty array
    allPermutations = PermutationLevels(nftDefinition['Traits'], 0, [])

    # Filter by exclusions and inclusions.
    # nftDefiniton is entire NFT_DEFINITION_BOOKWORMS object in nftConfig.py
    exclusions = GetPermutationExclusionsInclusions(nftDefinition, 'Exclusions')
    inclusions = GetPermutationExclusionsInclusions(nftDefinition, 'Inclusions')
    # exclusions is turned into numeric list
    # exclusions = [[None, None, None, None, None, None, 0, None, ...], another exclusions arr]
    # for the qualifying permutations in allPermuations
    # if exclusions is None or qp is not in exclusions (we would want to include it)
    # loops through all possible permutations [[0, 12, 5, 6, 2, 9, 0, ...], another permutation array] there are no Nones
    # compares each possible permutation with each exclusions array. if they both have 0 at index 6 then do not include
    return [qp for qp in allPermutations if ((exclusions is None or not PermutationQualify(exclusions, qp)) and (inclusions is None or PermutationQualify(inclusions, qp)))]

def GenerateRandomPermutationsAndRarities(nftDefinition):
    '''
    Generate the randomPermutations and their associated randomRarities.
    '''
    # Generate all of the qualifying permutations, filtered with 'Include' and 'Exlcude'
    qualifyingPermutations = GenerateQualifyingPermutations(nftDefinition)
    # go through qualifying permutations and creates rarities
    # [0.0001, 0.0099, 0.0099, 0.9801]
    qualifyingRarities = [GetRawRarity(nftDefinition, permutation) for permutation in qualifyingPermutations]

    # Determine a qtyPerPermutationPerRarity that is sufficient to allow for the smallest permutaion rarity to have at least
    # one entry in qualifyingPermutationsIntegers.  Anything over 500,000 makes it really slow!
    qtyPerPermutationPerRarity = 1
    for rarity in qualifyingRarities:
        # if 1 * 0.0001 < 1
        if int(qtyPerPermutationPerRarity * rarity) < 1:
            #  1 / 0.0001 = 10001
            qtyPerPermutationPerRarity = int(1 / rarity) + 1
    qtyPerPermutationPerRarity = min(qtyPerPermutationPerRarity, 500000)

    # Create qualifyingPermutationsIntegers, which is a list of the qualifyingPpermutations indexes based on their rarity.
    qualifyingPermutationsIntegers = []
    iInteger = 0
    for r, rarity in enumerate(qualifyingRarities):
        # If qtyPerPermutationPerRarity * rarity < 1, then it would never get an entry added to qualifyingPermutationsIntegers.
        # So set the qtyPerPermutationPerRarity to 1 so at least one entry will get added to qualifyingPermutationsIntegers.
        # This means that very small rarities will have only one entry, and effecitively the same probability of being chosen.
        useIncrement = max(1, int(qtyPerPermutationPerRarity * rarity))
        for _ in range(iInteger, iInteger + useIncrement):
            qualifyingPermutationsIntegers.append(r)
        iInteger = iInteger + useIncrement

    # Create the randomPermutations and randomRarities
    randomPermutations = [] # A list of the permtations that have been generated
    iGenerateds = [] # A list of the permutation indexes that have already been generated.
    quantityToGenerate = min(len(qualifyingPermutations), nftDefinition['Quantity']) # The quantity that will be generated.
    for _i in range(quantityToGenerate):
        # Get a random permutation index from qualifyingPermutationsIntegers that does not already exist in iGenerateds.
        # If you cannot find an unused random index, then clear out the iGenerateds from qualifyingPermutationsIntegers.
        iGenerate = random.choice(qualifyingPermutationsIntegers)
        if iGenerate in iGenerateds:
            # Remove the iGenerateds from qualifyingPermutationsIntegers so you can get a unique iGenerate.
            # This is really expensive, but list comprehension is by far the fastest because it only makes one pass.

            # create a new array
            # loop through qualifyingPermutationsIntegers
            # if q is not in iGenerateds, copy to new list
            # q = permutation 1, 2, 3 or 4 which is the index element of qualifyingPermutations [[0, 12, 5, 6, 2, 9, 0, ...], another permutation array]
            qualifyingPermutationsIntegers = [q for q in qualifyingPermutationsIntegers if q not in iGenerateds]
            iGenerateds = []
            iGenerate = random.choice(qualifyingPermutationsIntegers)
        iGenerateds.append(iGenerate)
        randomPermutations.append(qualifyingPermutations[iGenerate])
        if  _i == 0 or len(randomPermutations) % 1000 == 0:
            print('Generating random permutations', len(randomPermutations), len(qualifyingPermutationsIntegers))

    # The 'random' permutations tend to have the least rarest ones listed first just because thy have a greater likelihood of
    # being chosen.  So randomize them even more... twice for good measure.
    random.shuffle(randomPermutations)
    random.shuffle(randomPermutations)

    # Create randomRarities corresponding with randomPermutations
    randomRarities = GenerateRandomRarities(nftDefinition, qualifyingPermutations, randomPermutations)

    return randomPermutations, randomRarities

def GenerateRandomRarities(nftDefinition, qualifyingPermutations, randomPermutations):
    '''
    Determine the rarities for all of the permutations in randomPermutations.
      1. qualifyingPermutations contains all posiible permutations except the ones that do not qualify due to Excludes and Includes.
         So the sum of the rarities of qualifyingPermutations will be less than 100.
      2. randomPermutations contains a subset of qualifyingPermutations.
         The quantity of randomPermutations equals the quantity specified by nftDefinition['Quantity']
         So the sum of the rarities of randomPermutations will also be less than 100.
      3. So We adjust the rarities of randomPermutations upwards by dividing them by sumOfQualifyingRaritiesRaw.
         This will yield randomRaritiesAdjusted.
      4. In theory, statistically speaking, randomRaritiesAdjusted is the correct answer.  But it is not explainable or supportable.
         So instead, we simply return randomRaritiesRaw.
    Example:
      sumOfQualifyingRaritiesRaw = 0.722
      sumOfRandomRaritiesRaw = 0.689 (If the total number of qualifying permutations was generated, then this would equal sumOfQualifyingRaritiesRaw.)
      sumOfrandomRaritiesAdjusted = 0.954 = 0.689/0.722 (If the total number of qualifying permutations was generated, then this would equal 100.)
    Reference:
      https://raritytools.medium.com/ranking-rarity-understanding-rarity-calculation-methods-86ceaeb9b98c
    '''
    randomRaritiesRaw = [GetRawRarity(nftDefinition, permutation) for permutation in randomPermutations]
    if DEBUG:
        sumOfRandomRaritiesRaw = sum(randomRaritiesRaw)
        qualifyingRaritiesRaw = [GetRawRarity(nftDefinition, permutation) for permutation in qualifyingPermutations]
        sumOfQualifyingRaritiesRaw = sum(qualifyingRaritiesRaw)
        randomRaritiesAdjusted = [(randomRarityRaw / sumOfQualifyingRaritiesRaw) for randomRarityRaw in randomRaritiesRaw]
        print('\npossibleQtyOfPermutations', PossibleQtyOfPermutations(nftDefinition), '\nqualifyingPermutations', len(qualifyingPermutations), 'sumOfQualifyingRaritiesRaw', sumOfQualifyingRaritiesRaw, '\nrandomPermutations', len(randomPermutations), 'sumOfRandomRaritiesRaw', sumOfRandomRaritiesRaw, 'sumOfRandomRaritiesAdjusted', sum(randomRaritiesAdjusted))
        #return randomRaritiesAdjusted # Too complicated.  Could never explain it to the user.

    return randomRaritiesRaw

def GetIndexByName(iterable, name):
    '''
    Return the index of the iterable element where element['Name'] == name
    '''
    for i, element in enumerate(iterable):
        if element['Name'] == name:
            return i
    return nftUtil.FatalExit('Could not find name ' + name)

def GetPermutationExclusionsInclusions(nftDefinition, excludeOrInclude):
    '''
    exclusionsInclusions = [[0,3,None,2], [None,1,None,4], ...]
    '''
    # if 'Exclusions' or 'Inclusions' is not in nftDefinition object then return none.
    # nftDefiniton is entire NFT_DEFINITION_BOOKWORMS object in nftConfig.py
    if excludeOrInclude not in nftDefinition:
        return None
    # array for exclusions or inclusions
    exclusionsInclusions = []
    traits = nftDefinition['Traits']
    # for each exclusion or inclusion in the array
    for namedExclusionInclusion in nftDefinition[excludeOrInclude]:
        # [None, None, None,...] 12 times since 12 is the length of the traits array
        exclusionInclusion = [None] * len(traits)
        # namedExclusionInclusion = {'Hairdos' : 'Mohawk', 'Sunglasses' : 'Vuarnet'}
        # since we want key and value you have to do .items()
        for key, value in namedExclusionInclusion.items():
            #print(key, value) 'Hairdos', 'Mohawk'
            # finds index of Hairdos
            traitIndex = GetIndexByName(traits, key)

            # finds index of Mohawk
            # NFT_DEFINITION_BOOKWORMS['Traits'][6]['Attributes'] is the iterable list of objects
            # value is Mohawk
            # attributeIndex = 0
            attributeIndex = GetIndexByName(traits[traitIndex]['Attributes'], value)

            # exclusionInclusion[6] = 0
            # exclusionInclusion[None, None, None, None, None, None, 0, None, ...] up to 12
            exclusionInclusion[traitIndex] = attributeIndex
        # exclusionsInclusions[[None, None, None, None, None, None, 0, None, ...], another exclusions arr]
        exclusionsInclusions.append(exclusionInclusion)
    return exclusionsInclusions

def GetRawRarity(nftDefinition, permutation):
    '''
    Get the raw rarity, which is just the probabilities of each trait multiplied by one another.
    '''
    traits = nftDefinition['Traits']
    # 1.0 = 100
    rarity = 1.0
    # a is the value and t is the index
    # a is the index of the attributes array for each trait
    for t, a in enumerate(permutation):
        rarity *= 0.01 * traits[t]['Attributes'][a]['Probability']
    # if two traits have probability of 0.01 it's 0.01 * 0.01
    return rarity

def LoadInputImages(nftDefinition):
    '''
    Load the input images.
    '''
    inputImages = {} # keyed on full file path
    for trait in nftDefinition['Traits']:
        for attribute in trait['Attributes']:
            filePath = attribute['FilePath']
            if filePath is None:
                continue # This is valid.  It means that the attribute is not applied.
            filePath = os.path.join(nftDefinition['InputImageFolder'], filePath)
            if filePath in inputImages:
                continue # Already have it loaded from a previous attribute with the same file.

            attributeImage = Image.open(filePath)
            if 'Resize' in attribute:
                attributeImage = attributeImage.resize(attribute['Resize'])
            inputImages[filePath] = attributeImage

    return inputImages

def PermutationLevels(traits, level, inPermutations):
    '''
    Recursive function for building the permutations for the traits level using inPermutaions as the starting point.
    '''
    # how many traits we have total in the nftConfig obj
    if level == len(traits):
        return inPermutations # End of the line.  You are past the final level.

    outPermutations = []
    if level == 0:
        # range does 0 - 2 for 3 attributes
        for a in range(len(traits[level]['Attributes'])):
            # appends attribute numbers to outPermutations array
            # [[0, 0, 0,], []]
            outPermutations.append([a])
    else:
        # for each array in [[0, 0, 0, 0], [0, 0, 0, 1]]
        # for loop within for loop multiplies the traits
        for inPermutation in inPermutations:
            # range of 0, 1 for 2 attributes
            for a in range(len(traits[level]['Attributes'])):
                # make copy of [0, 0, 0]
                # second round make copy of [0, 0, 0]
                outPermutation = copy.copy(inPermutation)
                # [0, 0, 0, 0]
                # a is now 1 so we end up with [0, 0, 0, 1]
                outPermutation.append(a)
                # [[0, 0, 0, 0]]
                # second round [[0, 0, 0, 0], [0, 0, 0, 1]]
                # a new array will get created for each trait that has more then one attribute
                outPermutations.append(outPermutation)

    # Get the next level. runs function again
    # [[0, 0, 0, 0, 0....], [0, 1]...]
    return PermutationLevels(traits, level + 1, outPermutations)

def PermutationQualify(excludesOrIncludes, permutation):
    '''
    Return True if the permutation (0,3,2,4,2) is in excludesOrIncludes (0,3,None,None,2)
    '''
    for qualify in excludesOrIncludes:
        doesQualify = True
        for i, e in enumerate(qualify):
            if e is not None and permutation[i] != qualify[i]:
                doesQualify = False
                break
        if doesQualify:
            return True
    return False

def PossibleQtyOfPermutations(nftdefinition):
    '''
    The total possible quantity of permutations, not taking into account Includes or Excludes.
    '''
    qty = 1
    for trait in nftdefinition['Traits']:
        qty *= len(trait['Attributes'])
    return qty

def PreProcessing(nftDefinition):
    '''
    Remove any old output files and then write the collection json.
    '''
    # Maybe remove the current files from the output folder.
    for folderName in ('OutputImageFolder', 'OutputMetadataFolder'):
        for file in os.scandir(nftDefinition[folderName]):
            os.remove(file.path)

    # Backup and initialize the database.
    nftUtil.BackupAndInitializeDatabase()

def ProcessNftDefinition(nftDefinition):
    '''
    Process the NFT definition.
    '''
    startTime = time.time()

    # Validate the nftDefinition
    ValidateNftDefinition(nftDefinition)

    # Load the images
    inputImages = LoadInputImages(nftDefinition)

    # Generate the randomPermutations and their associated randomRarities.
    randomPermutations, randomRarities = GenerateRandomPermutationsAndRarities(nftDefinition)

    if DEBUG:
        print('\n', round(time.time() - startTime, 2), 'seconds')
        input("\nPress Enter to continue...")

    # Remove any old output files, write the collection json, and .
    PreProcessing(nftDefinition)

    traits = nftDefinition['Traits']
    for p, permutation in enumerate(randomPermutations): # (0,0,1), (0,0,2)
        baseAttr = traits[0]['Attributes'][permutation[0]]
        baseImage = inputImages[os.path.join(nftDefinition['InputImageFolder'], baseAttr['FilePath'])]
        baseImage = copy.copy(baseImage)
        extension = nftDefinition['ImageExtension'] # os.path.splitext(baseAttr['FilePath'])[1]
        tokenId = p + 1
        doc = {nftUtil.FIELD_ID: tokenId,
               nftUtil.FIELD_COLLECTION_NAME: nftDefinition['Name'],
               nftUtil.FIELD_TOKEN_IS_EXPOSABLE: None, #(tokenId <= nftDefinition['QuantityOfExposableTokens']), # Only expose a certain quantity of tokens.
               nftUtil.FIELD_STATISTICAL_RARITY: round(randomRarities[p], 11),
               nftUtil.FIELD_IMAGE_TYPE: extension[1:],
               nftUtil.FIELD_IMAGE_URI: None,
               nftUtil.FIELD_EXTERNAL_URL: None,
               nftUtil.FIELD_TRAITS: [{'trait_type': traits[0]['Name'], 'value': baseAttr['Name'], 'probability' : str(baseAttr['Probability']) + '%'}],
               nftUtil.FIELD_TRANSACTIONS: [],
               nftUtil.FIELD_IMAGE_BINARY_STRING: None} # Put this at the end because it is so huge.

        # Apply all attributes
        for t, a in enumerate(permutation):
            if t == 0:
                continue # base
            trait = traits[t]
            attribute = trait['Attributes'][a]
            baseImage = ApplyAttribute(nftDefinition, baseImage, attribute, inputImages)
            doc[nftUtil.FIELD_TRAITS].append({'trait_type': trait['Name'], 'value': attribute['Name'], 'probability' : str(attribute['Probability']) + '%'})

        # Determine FIELD_IMAGE_BINARY_STRING
        if nftDefinition['UpdateDatabaseWithImages']:
            buffer = io.BytesIO()
            baseImage.save(buffer, format=extension[1:])
            doc[nftUtil.FIELD_IMAGE_BINARY_STRING] = bson.Binary(buffer.getvalue())

        print('Writing', tokenId)
        nftUtil.InsertOneDocument(doc)
        baseImage.save(os.path.join(nftDefinition['OutputImageFolder'], str(tokenId)) + extension)


    # Create the metadata and store the images
    nftUtil.CreateMetadata(nftDefinition)
    print('\nGenerated', len(randomPermutations), 'NFTs in', round(time.time() - startTime, 2), 'seconds')

def ValidateNftDefinition(nftDefinition):
    '''
    Validate the NFT definition.
    '''
    traitNames = set()
    traits = nftDefinition['Traits']
    for trait in traits:

        # Set working variables.
        traitName = trait['Name']

        # Make sure that none of the traits have duplicate names.
        if traitName in traitNames:
            nftUtil.FatalExit('Duplicate trait names ' + traitName)
        traitNames.add(traitName)

        # Validate this trait's attributes.
        attrNames = set()
        attrTotalProbabilities = 0
        traitAttributes = trait['Attributes']
        for attr in traitAttributes:
            attrName = attr['Name']
            if attrName in attrNames:
                nftUtil.FatalExit('Duplicate attribute names ' + attrName)
            attrNames.add(attrName)
            probability = attr['Probability']
            if 1 <= probability <= 100:
                attrTotalProbabilities += probability
            else:
                nftUtil.FatalExit(traitName + ' attribute probability ' + str(probability) + ' must be between 1 and 100 inclusive.')

        # Attributes probabilities for each trait must total to 100.
        if attrTotalProbabilities != 100:
            nftUtil.FatalExit(traitName + ' attribute probabilities ' + str(attrTotalProbabilities) + ' != 100')



############################################### PROCESS #################################################
ProcessNftDefinition(nftConfig.NFT_DEFINITION_BOOKWORMS) # nftConfig.NFT_DEFINITION_DOGS
