"""
Create all image and metadata files for a collection, and load the database.
For Profiling run:
   python -m cProfile nftInitializeDatabase.py >t.csv
"""
import copy
import glob
import io
import os
import pathlib
import random
import time
from PIL import Image, ImageFont, ImageDraw

import bson
import nftConfig
import nftUtil


############################################# C O N S T A N T S #############################################
# Debug
DEBUG = False


def ApplyAttribute(nftDefinition, baseImage, trait, attribute, inputImages):
    """
    Apply the attribute to the base image.
    """
    filePath = AttributeFilePath(nftDefinition, attribute)
    if filePath is None:
        # This is valid.  It means that the attribute is not applied.
        return baseImage
    # else:
    #    filePath = os.path.join(trait['Name'], filePath)

    inputFolder = nftDefinition["AttributeImageFolder"]
    offset = attribute["Offset"] if "Offset" in attribute else (0, 0)
    inputImage = inputImages[os.path.join(inputFolder, trait["Name"], filePath)]
    baseImage.paste(inputImage, offset, inputImage)

    return baseImage


def ApplyCopyright(image):
    """
    Apply a copyright notice to the image.
    """
    # You cannot use ImageFont.load_default(), because that does not let you specify the font size.
    # So use arial.ttf.  You can find ttf files on a mac in either /System/Library/Fonts or /Library/Fonts.
    # 6-point size seems to be the smallest allowable, but you need at least 10-point to decipher the copyright circle logo.
    # https://stackoverflow.com/questions/58968752/loading-fonts-in-python-pillow-on-a-mac
    font = ImageFont.truetype("Roboto-Regular.ttf", size=10)
    text = "\u00a9" + " 2021 BlockBot LLC"
    imageDraw = ImageDraw.Draw(image)

    # Set the xy placement and fill color.
    #   y = 986 is enough vertical room for 12-point font (or less)
    #   y = 987 is enough vertical room for 10-point font (or less)
    xy = (2, 987)
    fill = image.getpixel(xy)  # Or 'white' to make it visible.
    imageDraw.text(xy=xy, text=text, fill=fill, font=font)

    return image


def AttributeFilePath(nftDefinition, attribute):
    """
    asdsada
    """
    if "FilePath" in attribute:
        return attribute["FilePath"]
    return attribute["Name"] + nftDefinition["ImageExtension"]


def GenerateQualifyingPermutations(nftDefinition):
    """
    Get all possible qualifying permutations.
    Filter out the 'Inclusions' and 'Exclusions' in nftDefinition with PermutationQualifies().
    https://www.askpython.com/python-modules/python-itertools-module
    """
    exclusions = GetPermutationExclusionsInclusions(nftDefinition, "Exclusions")
    inclusions = GetPermutationExclusionsInclusions(nftDefinition, "Inclusions")
    return PermutationLevels(nftDefinition, 0, [], exclusions, inclusions)


def GenerateRandomPermutationsAndRarities(nftDefinition, signatureImages):
    """
    Generate the randomPermutations and their associated randomRarities.
    """
    # Generate all of the qualifying permutations, filtered with 'Include' and 'Exlcude'
    startTime = time.time()
    qualifyingPermutations = GenerateQualifyingPermutations(nftDefinition)
    print("Generated", len(qualifyingPermutations), "permutations in", round(time.time() - startTime, 2), "seconds")

    # go through qualifying permutations and creates rarities
    # [0.0001, 0.0099, 0.0099, 0.9801]
    print("\nCalculating statistical rarities...")
    traits = nftDefinition["Traits"]
    rarityTraitIndex = GetRarityTrait(nftDefinition, returnIndex=True)
    qualifyingRarities = [GetStatisticalRarity(permutation, traits, rarityTraitIndex) for permutation in qualifyingPermutations]

    # Determine a qtyPerPermutationPerRarity that is sufficient to allow for the smallest permutaion rarity to have at least
    # one entry in qualifyingPermutationsIntegers.  Anything over 500,000 makes it really slow!
    # print('Determining probability tranch sizes...')
    print("Allocating probability tranches...")
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
        # if r % 100000 == 0:
        #    print('Allocating probability tranches', r)

    # Create the randomPermutations and randomRarities
    randomPermutations = []  # A list of the permtations that have been generated
    iGenerateds = []  # A list of the permutation indexes that have already been generated.
    quantityToGenerate = min(len(qualifyingPermutations), nftDefinition["Quantity"])  # The quantity that will be generated.
    print("\nGenerating " + str(quantityToGenerate) + " random permutations...")
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
        if len(randomPermutations) % 1000 == 0:
            print("Generating random permutations", len(randomPermutations))  # , len(qualifyingPermutationsIntegers))

    # Paranoid validation that there are no duplicate permutations in randomPermutations.
    ##randomPermutations.append(randomPermutations[1]) # This will force add a duplicate for testing.
    if not PermutationsAreUnique(randomPermutations):
        nftUtil.FatalExit("\nFatal error!!!  RandomPermutations are not unique.")

    # Now add the extra 'Signature Series' files.
    for filePath in signatureImages:
        randomPermutations.append(filePath)

    # The 'random' permutations tend to have the least rarest ones listed first just because thy have a greater likelihood of
    # being chosen.  So shuffle them 5 times.
    for _ in range(5):
        random.shuffle(randomPermutations)

    # Create randomRarities corresponding with randomPermutations
    randomRarities = [GetStatisticalRarity(permutation, traits, rarityTraitIndex) for permutation in randomPermutations]

    # Get the randomRarityIndex associated with each randomRarity
    randomRarityIndexes = GenerateRarityIndexes(nftDefinition, randomRarities)

    # When the permutations were created, the 'IsRarityTrait' value in the permutation was just hard-coded to 0 (e.g. Mythic)
    # This is because it is not known until now.  So now we must set it.
    for p, permutation in enumerate(randomPermutations):
        if not isinstance(permutation, str):
            permutation[rarityTraitIndex] = randomRarityIndexes[p]

    return randomPermutations, randomRarities, randomRarityIndexes


def GenerateRarityIndexes(nftDefinition, rarities):
    """
    Return a list of the rarityIndexes that corresponds exactly with the input rarities.
    """
    rarityTrait = GetRarityTrait(nftDefinition)

    # Get the rarityBreakPoints
    sortedRarities = sorted(rarities)
    rarityBreakPoints = []
    cumulativeProbability = 0
    for attribute in rarityTrait["Attributes"]:
        cumulativeProbability += attribute["Probability"]
        sortedRarityIndex = int(0.01 * cumulativeProbability * len(sortedRarities)) - 1
        sortedRarityIndex = max(0, sortedRarityIndex)  # cannot be < 0
        sortedRarityIndex = min(sortedRarityIndex, len(sortedRarities) - 1)  # cannot exceed the length of the array
        rarityBreakPoints.append(sortedRarities[sortedRarityIndex])

    rarityIndexes = []
    for rarity in rarities:
        for i, breakPoint in enumerate(rarityBreakPoints):
            if rarity <= breakPoint:
                rarityIndexes.append(i)
                break

    if len(rarityIndexes) != len(rarities):
        nftUtil.FatalExit("len(rarityIndexes) != len(rarities)")

    # Return a list of the rarityIndexes that corresponds exactly with rarities.
    return rarityIndexes


def GetAttributeIndexes(traits, traitName, attributeNameSpecification):
    """
    Return qualifying (traitIndex, (attributeIndexes))
      traitName = 'Hair' (5)
      attributeNameSpecification = 'Dark_*'
    """
    attributeIndexes = []
    traitIndex = GetIndexByName(traits, traitName)
    for a, attribute in enumerate(traits[traitIndex]["Attributes"]):
        attributeName = attribute["Name"]
        if nftUtil.StringsMatch(attributeNameSpecification, attributeName):
            attributeIndexes.append(a)
    return (traitIndex, tuple(attributeIndexes))


def GetExclusionsInclusionsForLevel(allExclusionsInclusions, level):
    """
    In order to qualify, the exclusion must:
      1. Contain level.
      2. All others must be <= level.
    """
    if not allExclusionsInclusions:
        return None
    exclusionsInclusions = []
    for exclusionInclusion in allExclusionsInclusions:
        greaterThanLevel = False
        containsLevel = False
        for ex in exclusionInclusion:
            if level == ex[0]:
                containsLevel = True
            elif level < ex[0]:
                greaterThanLevel = True
                break
        if containsLevel and not greaterThanLevel:
            exclusionsInclusions.append(exclusionInclusion)
    return tuple(exclusionsInclusions)


def GetIndexByName(iterable, name):
    """
    Return the index of the iterable element where element['Name'] == name
    """
    for i, element in enumerate(iterable):
        if element["Name"] == name:
            return i
    return nftUtil.FatalExit("Could not find name " + name)


def GetPermutationExclusionsInclusions(nftDefinition, excludeOrInclude):
    """
    exclusionsInclusions = [[0,3,None,2], [None,1,None,4], ...]
    """
    # if 'Exclusions' or 'Inclusions' is not in nftDefinition object then return none.
    # nftDefiniton is entire NFT_DEFINITION_BOOKWORMS object in nftConfig.py
    if excludeOrInclude not in nftDefinition:
        return None
    # array for exclusions or inclusions
    exclusionsInclusions = []
    traits = nftDefinition["Traits"]
    # for each exclusion or inclusion in the array
    for namedExclusionInclusion in nftDefinition[excludeOrInclude]:
        exclusionInclusion = []
        # namedExclusionInclusion = {'Hairdos' : 'Mohawk', 'Sunglasses' : 'Vuarnet'}
        # since we want key and value you have to do .items()
        for key, value in namedExclusionInclusion.items():
            exclusionInclusion.append(GetAttributeIndexes(traits, key, value))
        exclusionsInclusions.append(tuple(exclusionInclusion))
    return exclusionsInclusions


def GetRarityTrait(nftDefinition, returnIndex=False):
    """
    sadasdas
    """
    for t, trait in enumerate(nftDefinition["Traits"]):
        if "IsRarityTrait" in trait and trait["IsRarityTrait"]:
            return t if returnIndex else trait
    nftUtil.FatalExit("Cannot find IsRarityTrait")
    return None  # needed for lint


def GetStatisticalRarity(permutation, traits, rarityTraitIndex):
    """
    Get the statistical rarity, which is just the probabilities of each trait multiplied by one another.
    """
    if isinstance(permutation, str):
        # It is the filePath for one of the 'Signature Series' images.
        return 0

    # traits = nftDefinition['Traits']
    # 1.0 = 100
    statisticalRarity = 1.0
    # a is the value and t is the index
    # a is the index of the attributes array for each trait
    for t, a in enumerate(permutation):
        # if not IsRarityTrait(traits[t]):
        if t != rarityTraitIndex:  # not IsRarityTrait(traits[t]):
            statisticalRarity *= 0.01 * traits[t]["Attributes"][a]["Probability"]
    # if two traits have probability of 0.01 it's 0.01 * 0.01
    return statisticalRarity


# def IsRarityTrait(trait):
#    '''
#    Return True if this trait is a rarity trait.
#    '''
#    return 'IsRarityTrait' in trait and trait['IsRarityTrait']


def LoadInputImages(nftDefinition):
    """
    Load the input images.
    """
    inputImageFolder = nftDefinition["AttributeImageFolder"]

    inputImages = {}  # keyed on full file path
    for trait in nftDefinition["Traits"]:
        for attribute in trait["Attributes"]:
            filePath = AttributeFilePath(nftDefinition, attribute)
            if filePath is None:
                continue  # This is valid.  It means that the attribute is not applied.
            filePath = os.path.join(inputImageFolder, trait["Name"], filePath)

            attributeImage = Image.open(filePath)
            if "Resize" in attribute:
                attributeImage = attributeImage.resize(attribute["Resize"])
            inputImages[filePath] = attributeImage

    signatureImages = {}
    if "SignatureImageFolder" in nftDefinition:
        for filePath in glob.iglob(nftDefinition["SignatureImageFolder"] + "*"):
            signatureImages[filePath] = Image.open(filePath)

    return inputImages, signatureImages


def PermutationsAreUnique(permutations):
    """
    Validate that each permutation in permutations is unique.
      permutations = [ [3,2,8,1,4], [2,4,7,1,3], ...]
    """
    # A set() is a unique set of keys.  Like a dictionary of keys without values.
    permutationStrings = set()

    # Add each permutation (as a string) to permutationStrings.  False will be returned if a duplicate is encountered.
    for permutation in permutations:
        permutationString = ""
        for p in permutation:
            permutationString += str(p) + "_"
        if permutationString in permutationStrings:
            # Duplicate permutation, not unique.
            return False
        permutationStrings.add(permutationString)

    # All permutations are unique.
    return True


def PermutationLevels(nftDefinition, level, inPermutations, allExclusions, allInclusions):
    """
    Recursive function for building the permutations for the traits level using inPermutaions as the starting point.
    """
    # how many traits we have total in the nftConfig obj
    traits = nftDefinition["Traits"]
    if level == len(traits):
        return inPermutations  # End of the line.  You are past the final level.

    print("Generating permutations for", traits[level]["Name"])

    # If we are on the rarityTrait level, then we only want one permutation, so we just pick 0.
    # The actual value will be determined and overwritten once we assign the rarity.
    rarityTraitIndex = GetRarityTrait(nftDefinition, returnIndex=True)
    attributeRange = 1 if rarityTraitIndex == level else len(traits[level]["Attributes"])

    # To make things much faster, only get the exclusions and inclusions that are involved with this level.
    exclusions = GetExclusionsInclusionsForLevel(allExclusions, level)
    inclusions = GetExclusionsInclusionsForLevel(allInclusions, level)

    outPermutations = []
    if level == 0:
        # range does 0 - 2 for 3 attributes
        for a in range(attributeRange):
            # appends attribute numbers to outPermutations array
            # [[0, 0, 0,], []]
            outPermutation = [a]
            if exclusions and PermutationQualifies(outPermutation, exclusions):
                continue
            if inclusions and not PermutationQualifies(outPermutation, inclusions):
                continue
            outPermutations.append(outPermutation)
    else:
        # for each array in [[0, 0, 0, 0], [0, 0, 0, 1]]
        # for loop within for loop multiplies the traits
        for inPermutation in inPermutations:
            # range of 0, 1 for 2 attributes

            for a in range(attributeRange):
                # make copy of [0, 0, 0]
                # second round make copy of [0, 0, 0]
                outPermutation = copy.copy(inPermutation)
                # [0, 0, 0, 0]
                # a is now 1 so we end up with [0, 0, 0, 1]
                outPermutation.append(a)
                if exclusions and PermutationQualifies(outPermutation, exclusions):
                    continue
                if inclusions and not PermutationQualifies(outPermutation, inclusions):
                    continue
                # [[0, 0, 0, 0]]
                # second round [[0, 0, 0, 0], [0, 0, 0, 1]]
                # a new array will get created for each trait that has more then one attribute
                outPermutations.append(outPermutation)

    # Get the next level. runs function again
    # [[0, 0, 0, 0, 0....], [0, 1]...]
    return PermutationLevels(nftDefinition, level + 1, outPermutations, allExclusions, allInclusions)


def PermutationQualifies(permutation, excludeOrIncludess):
    """
    Return True if the permutation (0,3,2,4,2) matches at least one of the excludeOrIncludess.
    """
    maximumPermutationIndex = len(permutation) - 1

    # excludeOrIncludess = [  [(5, (0, 1, 2, 3, 4)), (6, (5, 6, 7, 8, 9))],  [(5, (0, 1, 2, 3, 4)), (6, (10, 11, 12, 13, 14))]  ]
    for excludeOrIncludes in excludeOrIncludess:
        # excludeOrIncludes = [	(5, (0, 1, 2, 3, 4)), (6, (5, 6, 7, 8, 9)) ]
        # To qualify, the permutation must match all.
        allQualifies = True
        for excludeOrInclude in excludeOrIncludes:
            # excludeOrInclude = (5, (0, 1, 2, 3, 4))
            # If permutation[5] == 0, 1, 2, 3 or 4 then subQualifies = True
            traitIndex = excludeOrInclude[0]
            if maximumPermutationIndex < traitIndex or permutation[traitIndex] not in excludeOrInclude[1]:
                allQualifies = False
                break
        if allQualifies:
            return True
    return False


def PreProcessing(nftDefinition):
    """
    Remove any old output files and then initialize the database.
    """
    # Maybe remove the current files from the output folder.
    for folderName in ("OutputImageFolder", "OutputMetadataFolder"):
        for file in os.scandir(nftDefinition[folderName]):
            os.remove(file.path)

    # Backup and initialize the database.
    nftUtil.BackupAndInitializeDatabase()


def ProcessNftDefinition(nftDefinition):
    """
    Process the NFT definition.
    """
    startTime = time.time()

    # Validate the nftDefinition
    ValidateNftDefinition(nftDefinition)

    # Load the images
    inputImages, signatureImages = LoadInputImages(nftDefinition)

    # Generate the randomPermutations and their associated randomRarities and their associated randomRarityIndexes
    randomPermutations, randomRarities, randomRarityIndexes = GenerateRandomPermutationsAndRarities(nftDefinition, signatureImages)

    # Validate that the highest rarity percentage is correct.
    rarityTraitAttributes = GetRarityTrait(nftDefinition)["Attributes"]
    if "SignatureImageFolder" in nftDefinition:
        specifiedSignaturePercent = rarityTraitAttributes[0]["Probability"]
        actualSignaturePercent = 100 * len(signatureImages) / len(randomPermutations)
        if 0.02 < abs(specifiedSignaturePercent - actualSignaturePercent):
            nftUtil.FatalExit("Your math is wrong: " + str(specifiedSignaturePercent) + " != " + str(actualSignaturePercent))

    # Remove any old output files and then initialize the database.
    PreProcessing(nftDefinition)

    print("\nInitial processing took", round(time.time() - startTime, 2), "seconds")
    if DEBUG:
        input("Press Enter to continue...")
    print()

    traits = nftDefinition["Traits"]
    for p, permutation in enumerate(randomPermutations):  # (0,0,1), (0,0,2)
        isSignatureSeries = isinstance(permutation, str)
        if isSignatureSeries:
            # baseAttr = None
            baseImage = signatureImages[permutation]
            # docTraits = None
            docTraits = [{"trait_type": "Signature Series", "value": pathlib.Path(permutation).resolve().stem, "probability": specifiedSignaturePercent}]
        else:
            baseAttr = traits[0]["Attributes"][permutation[0]]
            baseImage = inputImages[os.path.join(nftDefinition["AttributeImageFolder"], traits[0]["Name"], AttributeFilePath(nftDefinition, baseAttr))]
            docTraits = [{"trait_type": traits[0]["Name"], "value": baseAttr["Name"], "probability": str(baseAttr["Probability"]) + "%"}]
        baseImage = copy.copy(baseImage)
        extension = nftDefinition["ImageExtension"]
        rarity = rarityTraitAttributes[randomRarityIndexes[p]]["Name"]
        tokenId = p + 1
        doc = {
            nftUtil.FIELD_ID: tokenId,
            nftUtil.FIELD_COLLECTION_NAME: nftDefinition["Name"],
            nftUtil.FIELD_TOKEN_IS_EXPOSABLE: None,
            nftUtil.FIELD_STATISTICAL_RARITY: f"{randomRarities[p]:.32f}".rstrip("0"),  # Must store a string because Mongo loses precision for floating point numbers.
            nftUtil.FIELD_RARITY: rarity,
            nftUtil.FIELD_IMAGE_TYPE: extension[1:],
            nftUtil.FIELD_IMAGE_URI: None,
            nftUtil.FIELD_EXTERNAL_URL: None,
            nftUtil.FIELD_TRAIT_COUNT: 1,  # This default will be used for isSignatureSeries.
            nftUtil.FIELD_PERMUTATION: permutation,
            nftUtil.FIELD_TRAITS: docTraits,  # [{'trait_type': traits[0]['Name'], 'value': baseAttr['Name'], 'probability' : str(baseAttr['Probability']) + '%'}],
            ##nftUtil.FIELD_TRANSACTIONS: [],
            nftUtil.FIELD_IMAGE_BINARY_STRING: None,
        }  # Put this at the end because it is so huge.

        # Apply all attributes
        if not isSignatureSeries:
            traitCount = 1  # Base
            for t, a in enumerate(permutation):
                if t == 0:
                    continue  # base
                trait = traits[t]
                attribute = trait["Attributes"][a]
                baseImage = ApplyAttribute(nftDefinition, baseImage, trait, attribute, inputImages)
                if AttributeFilePath(nftDefinition, attribute) is not None:
                    traitCount += 1
                doc[nftUtil.FIELD_TRAITS].append({"trait_type": trait["Name"], "value": attribute["Name"], "probability": str(attribute["Probability"]) + "%"})
            doc[nftUtil.FIELD_TRAIT_COUNT] = traitCount

        # Apply copyright statement
        ApplyCopyright(baseImage)

        # Determine FIELD_IMAGE_BINARY_STRING
        if nftDefinition["UpdateDatabaseWithImages"]:
            buffer = io.BytesIO()
            baseImage.save(buffer, format=extension[1:])
            doc[nftUtil.FIELD_IMAGE_BINARY_STRING] = bson.Binary(buffer.getvalue())

        print("Writing Image", tokenId)
        nftUtil.InsertOneDocument(doc)
        baseImage.save(os.path.join(nftDefinition["OutputImageFolder"], str(tokenId)) + extension)

    # Create the metadata and store the images
    nftUtil.CreateMetadata(nftDefinition)
    print("\nGenerated", len(randomPermutations), "NFTs in", round(time.time() - startTime, 2), "seconds")


def ValidateNftDefinition(nftDefinition):
    """
    Validate the NFT definition.
    """
    traitNames = set()
    traits = nftDefinition["Traits"]
    for trait in traits:

        # Set working variables.
        traitName = trait["Name"]

        # Make sure that none of the traits have duplicate names.
        if traitName in traitNames:
            nftUtil.FatalExit("Duplicate trait names " + traitName)
        traitNames.add(traitName)

        # Validate this trait's attributes.
        attrNames = set()
        attrTotalProbabilities = 0
        traitAttributes = trait["Attributes"]
        for attr in traitAttributes:
            attrName = attr["Name"]
            if attrName in attrNames:
                nftUtil.FatalExit("Duplicate attribute names " + attrName)
            attrNames.add(attrName)
            probability = attr["Probability"]
            if 0.0001 <= probability <= 100:
                attrTotalProbabilities += probability
            else:
                nftUtil.FatalExit(traitName + " attribute probability " + str(probability) + " must be between 0.0001 and 100 inclusive.")
        if not nftUtil.FloatingPointEquivalent(attrTotalProbabilities, 100):
            nftUtil.FatalExit(traitName + " attribute probabilities " + str(attrTotalProbabilities) + " != 100")

    # I could only get multiple Inclusions to work if they all had exactly the same trait levels.
    # I think the only way to really do robust inclusions is to wait until ALL possible permutaions have been generated,
    # and then check for multiple exclusions, but that would not be feasible.  So to keep it simple and understandable,
    # only allow for one Inclusion.
    if "Inclusions" in nftDefinition and 1 < len(nftDefinition["Inclusions"]):
        nftUtil.FatalExit("Can only specify one inclusion.")


############################################### PROCESS #################################################
ProcessNftDefinition(nftConfig.NFT_DEFINITION_BOOKWORMS)
# ProcessNftDefinition(nftConfig.NFT_DEFINITION_DOGS)
