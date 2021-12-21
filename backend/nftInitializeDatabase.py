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


def ApplyAttribute(baseImage, attribute, attributeImage):
    """
    Apply the attribute to the base image.
    """
    if attributeImage is not None:
        offset = attribute["Offset"] if "Offset" in attribute else (0, 0)
        baseImage.paste(attributeImage, offset, attributeImage)

    return baseImage


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


def AttributeFilePath(nftDefinition, attribute):
    """
    Return the effective attribute filePath.
    """
    if "FilePath" in attribute:
        return attribute["FilePath"]
    return attribute["Name"] + "." + nftDefinition["ImageType"]


def BuildPermutations(nftDefinition, finalImages, rarityQuantities):
    """
    Build the permutations, taking into account the exclusions and inclusions.
    """
    # Define working variables
    traits = nftDefinition["Traits"]
    rarities = nftDefinition["Rarities"]

    # Get the rarityAttributeDistributions
    rarityAttributeDistributions = GetRarityAttributeDistributions(nftDefinition)

    # Get the globalExclusions and globalInclusions
    globalExclusions = GetGlobalExclusions(nftDefinition)
    globalInclusions = GetGlobalInclusions(nftDefinition)

    # Build the permutations
    permutations = []  # running list
    permutationRarityIndexes = []  # running list
    for r, rarity in enumerate(rarities):
        if "FinalImageFolder" in rarity:
            if len(finalImages[r]) < rarityQuantities[r]:
                nftUtil.FatalExit("Insufficient quantity of finalImages: " + str(len(finalImages[r])) + " < " + str(rarityQuantities[r]))
            for i in range(rarityQuantities[r]):
                # The permutation will be a string of the finalImages index
                permutations.append(str(i))
                permutationRarityIndexes.append(r)
        else:
            rarityAttributeDistribution = rarityAttributeDistributions[r]
            for _ in range(rarityQuantities[r]):
                while True:
                    permutation = []
                    qualifyingPermutationFound = True
                    for t in range(len(traits)):
                        attributeDistribution = rarityAttributeDistribution[t]
                        attributeDistributionIndex = random.randint(0, len(attributeDistribution) - 1)
                        permutation.append(attributeDistribution[attributeDistributionIndex])
                        if not PermutationQualifiesInclusions(permutation, globalInclusions[t]) or PermutationQualifiesExclusions(permutation, globalExclusions[t]):
                            qualifyingPermutationFound = False
                            break
                    if qualifyingPermutationFound and permutation not in permutations:
                        permutations.append(permutation)
                        permutationRarityIndexes.append(r)
                        if len(permutations) % 1000 == 0:
                            print("Generating Permutations", len(permutations))
                        break

    return permutations, permutationRarityIndexes


##def CsvWritePermutations(permutations):
##    '''
##    Write out the permutations
##    '''
##    with open('permutations.csv', 'w', newline='') as file:
##        csvWriter = csv.writer(file)
##        for p in permutations:
##            if p[5] == 15: # mullet
##                csvWriter.writerow(p)


def DetermineAttributeProbabilities(traits, permutations):
    """
    Return the actual attributeProbabilities for non-SignatureSeries.
    """
    attributeProbabilities = []
    for trait in traits:
        attributeProbabilities.append([0] * len(trait["Attributes"]))
    qty = 0
    for permutation in permutations:
        qty += 1
        if not isinstance(permutation, str):  # Signature Series
            for t, a in enumerate(permutation):
                attributeProbabilities[t][a] += 1
    for attributeProbability in attributeProbabilities:
        for p, probability in enumerate(attributeProbability):
            attributeProbability[p] = probability / qty
    return attributeProbabilities


def DetermineRarityProbabilities(rarityQuantities):
    """
    Determine the probabilities for each rarity level.
    """
    total = sum(rarityQuantities)
    rarityPercentages = [(qty / total) for qty in rarityQuantities]
    return rarityPercentages


def DetermineRarityQuantities(nftDefinition):
    """
    Determine the quantity of NFTs for each rarity level.
    """
    rarities = nftDefinition["Rarities"]
    probabilityDistribution = ProbabilityDistribution(rarities)
    lenProbabilityDistribution = len(probabilityDistribution)

    quantityNeeded = nftDefinition["TotalQuantity"]  # 10000
    if quantityNeeded % lenProbabilityDistribution != 0:
        nftUtil.FatalExit("TotalQuantity " + str(quantityNeeded) + " must be a factor of " + str(lenProbabilityDistribution))
    quantityPerBucket = int(quantityNeeded / lenProbabilityDistribution)

    rarityQuantities = [0] * len(rarities)
    actualQuantity = 0
    for pd in probabilityDistribution:
        remainingQuantityNeeded = quantityNeeded - actualQuantity
        quantityToAllocate = min(quantityPerBucket, remainingQuantityNeeded)
        rarityQuantities[pd] += quantityToAllocate
        actualQuantity += quantityToAllocate
        if quantityNeeded < actualQuantity:
            nftUtil.FatalExit("Logic error in DetermineRarityQuantities()")
        if quantityNeeded == actualQuantity:
            break

    return rarityQuantities


def GetExclusionInclusionAttributeIndexes(attributeNameSpecifications, namedExclusionInclusion, traits, traitIndex):
    """
    Workhorse for getting the excluded/included attributeIndexes for the traitIndex
    """
    if isinstance(attributeNameSpecifications, str):
        attributeNameSpecifications = (attributeNameSpecifications,)
    attributeIndexes = []
    for attributeNameSpecification in attributeNameSpecifications:
        qtyFound = 0
        for a, attribute in enumerate(traits[traitIndex]["Attributes"]):
            if nftUtil.StringsMatch(attributeNameSpecification, attribute["Name"]):
                attributeIndexes.append(a)
                qtyFound += 1
        if qtyFound == 0:
            nftUtil.FatalExit("Typo in " + str(namedExclusionInclusion))
    return (traitIndex, attributeIndexes)


def GetGlobalExclusions(nftDefinition):
    """
    Get the global exclusions based on nftDefinition['Exclusions']
    """
    # exclusions contains an array for each trait level.
    traits = nftDefinition["Traits"]
    exclusions = [[] for _ in range(len(traits))]

    if "Exclusions" in nftDefinition:
        for namedExclusion in nftDefinition["Exclusions"]:
            exclusion = []
            maximumTraitIndex = -1
            for traitName, attributeNameSpecifications in namedExclusion.items():
                traitIndex = GetIndexByName(traits, traitName)
                if maximumTraitIndex < traitIndex:
                    maximumTraitIndex = traitIndex
                exclusion.append(GetExclusionInclusionAttributeIndexes(attributeNameSpecifications, namedExclusion, traits, traitIndex))

            exclusions[maximumTraitIndex].append(exclusion)

    return exclusions


def GetGlobalInclusions(nftDefinition):
    """
    Get the global inclusions based on nftDefinition['Inclusions']
    """
    traits = nftDefinition["Traits"]
    includes = [[] for _ in range(len(traits))]

    # for each inclusion or inclusion in the array
    if "Inclusions" in nftDefinition:
        for namedIncludes in nftDefinition["Inclusions"]:
            if len(namedIncludes) != 2:
                nftUtil.FatalExit("Inclusion must have exactly 2 elements: " + str(namedIncludes))
            include = []
            maximumTraitIndex = -1
            for namedInclude in namedIncludes:
                if len(namedInclude) != 2:
                    nftUtil.FatalExit("Inclusion must have exactly 2 elements: " + str(namedInclude))
                traitIndex = GetIndexByName(traits, namedInclude[0])
                if maximumTraitIndex < traitIndex:
                    maximumTraitIndex = traitIndex
                attributeNameSpecifications = namedInclude[1]
                include.append(GetExclusionInclusionAttributeIndexes(attributeNameSpecifications, namedInclude, traits, traitIndex))

            includes[maximumTraitIndex].append(include)

    return includes


def GetIndexByName(iterable, name):
    """
    Return the index of the iterable element where element['Name'] == name
    """
    for i, element in enumerate(iterable):
        if element["Name"] == name:
            return i
    return nftUtil.FatalExit("Could not find name " + name)


def GetRarityAttributeDistributions(nftDefinition):
    """
    For each rarity, build a list of valid trait attributes, taking into account the rarityExclusions and rarityInclusions.
    """
    # Set working variables
    traits = nftDefinition["Traits"]
    rarities = nftDefinition["Rarities"]

    # Get the rarityExcludes and rarityIncludes
    rarityExclusions = GetRarityExclusionsInclusions(traits, rarities, "Exclusions")
    rarityInclusions = GetRarityExclusionsInclusions(traits, rarities, "Inclusions")

    # rarityAttributeDistributions = [ [[0,1,2], [], ...], [[], [0,1,2], ...]
    rarityAttributeDistributions = [[] for _ in range(len(rarities))]

    for r, rarity in enumerate(rarities):
        if "Traits" not in rarity:
            continue
        for t, trait in enumerate(traits):
            traitProbabilityDistribution = ProbabilityDistribution(trait["Attributes"])
            traitAttributes = []  # all valid attributes for this trait
            for a in range(len(trait["Attributes"])):
                if rarityExclusions[r][t] and a in rarityExclusions[r][t]:
                    continue
                if rarityInclusions[r][t] and a not in rarityInclusions[r][t]:
                    continue
                # OK, we're on a valid attribute.  So now build the buckets from traitProbabilityDistributions
                traitAttributes.extend([a] * traitProbabilityDistribution.count(a))
            rarityAttributeDistributions[r].append(traitAttributes)

    return rarityAttributeDistributions


def GetRarityExclusionsInclusions(traits, rarities, exclusionsOrInclusions):
    """
    Get the inclusions for each rarity
    """
    rarityExclusionsInclusions = [[] for _ in range(len(rarities))]  # [None] * len(rarities)
    for r, rarity in enumerate(rarities):
        if "Traits" not in rarity:
            continue
        traitExclusionsInclusions = [[] for _ in range(len(traits))]  # [None] * len(traits)
        for trait in rarity["Traits"]:
            if exclusionsOrInclusions not in trait:
                continue
            traitIndex = GetIndexByName(traits, trait["Name"])
            attributeNameSpecifications = trait[exclusionsOrInclusions]
            attributeIndexes = GetExclusionInclusionAttributeIndexes(attributeNameSpecifications, trait, traits, traitIndex)
            traitExclusionsInclusions[attributeIndexes[0]] = attributeIndexes[1]
        rarityExclusionsInclusions[r] = traitExclusionsInclusions
    return rarityExclusionsInclusions


def LoadAttributeImages(nftDefinition):
    """
    Load the attribute images.
    """
    imageFolder = nftDefinition["AttributeImageFolder"]
    traits = nftDefinition["Traits"]
    images = [[] for _ in range(len(traits))]
    for t, trait in enumerate(traits):
        attributes = trait["Attributes"]
        images[t] = [None] * len(attributes)
        for a, attribute in enumerate(trait["Attributes"]):
            filePath = AttributeFilePath(nftDefinition, attribute)
            if filePath is None:
                continue  # This is valid.  It means that the attribute is not applied.
            filePath = os.path.join(imageFolder, trait["Name"], filePath)

            attributeImage = Image.open(filePath)
            ##attributeImage = attributeImage.convert("RGBA")
            ##if 'Resize' in attribute:
            ##    attributeImage = attributeImage.resize(attribute['Resize'])
            images[t][a] = attributeImage

    return images


def LoadFinalImages(rarities):
    """
    Load the rarity images.
    """
    images = [None] * len(rarities)
    for r, rarity in enumerate(rarities):
        if "FinalImageFolder" not in rarity:
            continue
        images[r] = []
        for filePath in glob.iglob(rarity["FinalImageFolder"] + "*"):
            # (simpleFileName, image)
            images[r].append((pathlib.Path(filePath).resolve().stem, Image.open(filePath)))

    return images


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


def PermutationQualifiesExclusions(permutation, excludess):
    """
    Return True if the permutation (0,3,2,4,2) matches at least one of the excludess.
    """
    # excludess = [  [(5, (0, 1, 2, 3, 4)), (6, (5, 6, 7, 8, 9))],  [(5, (0, 1, 2, 3, 4)), (6, (10, 11, 12, 13, 14))]  ]
    if excludess:
        for excludes in excludess:
            # excludes = [	(5, (0, 1, 2, 3, 4)), (6, (5, 6, 7, 8, 9)) ]
            # To qualify, the permutation must match all.
            allQualifies = True
            for exclude in excludes:
                # exclude = (5, (0, 1, 2, 3, 4))
                traitIndex = exclude[0]
                if permutation[traitIndex] not in exclude[1]:
                    allQualifies = False
                    break
            if allQualifies:
                return True
    return False


def PermutationQualifiesInclusions(permutation, includess):
    """
    Return True if the permutation (0,3,2,4,2) should be included.
    """
    for includes in includess:
        if permutation[includes[0][0]] in includes[0][1] and permutation[includes[1][0]] not in includes[1][1]:
            return False
    return True


def PreProcessing(nftDefinition):
    """
    Remove any old output files and then initialize the database.
    """
    # Maybe remove the current files from the output folder.
    for folderName in ("OutputImageFolder", "OutputMetadataFolder"):
        for file in os.scandir(nftDefinition[folderName]):
            os.remove(file.path)

    # Backup and initialize the database.
    nftUtil.BackupAndInitializeDatabase(nftDefinition)


def ProbabilityDistribution(thingList):
    """
    Create a probability distribution for the values in thingList.
    (3, 2, 4) -> [0, 0, 0, 1, 1, 2, 2, 2, 2]
    """
    # This will keep multyiplying times 10 until they are all integers.
    factor = 1
    while True:
        allAreIntegers = True
        for thing in thingList:
            probability = thing["Probability"] * factor
            if probability != int(probability):
                allAreIntegers = False
                factor *= 10
                if 100 < factor:
                    nftUtil.FatalExit("Probability " + str(probability) + " has too many decimals.")
                break
        if allAreIntegers:
            break

    probabilityDistribution = []
    for t, thing in enumerate(thingList):
        probability = int(thing["Probability"] * factor)
        probabilityDistribution.extend([t] * probability)

    return probabilityDistribution


def ProcessNftDefinition(nftDefinition):
    """
    Process the NFT definition.
    """
    startTime = time.time()

    # Validate the nftDefinition
    ValidateNftDefinition(nftDefinition)

    # Set working variables
    traits = nftDefinition["Traits"]
    rarities = nftDefinition["Rarities"]
    # totalQuantity = nftDefinition['TotalQuantity']

    # Load the images
    attributeImages = LoadAttributeImages(nftDefinition)
    finalImages = LoadFinalImages(rarities)

    # Determine the quantity of NFTs for each rarity level
    rarityQuantities = DetermineRarityQuantities(nftDefinition)
    rarityProbabilities = DetermineRarityProbabilities(rarityQuantities)

    # Get the permutations and permutationRarityIndexes.  This takes the majority of the time.
    permutations, permutationRarityIndexes = BuildPermutations(nftDefinition, finalImages, rarityQuantities)

    # Paranoid validation that there are no duplicate permutations in randomPermutations.
    ##randomPermutations.append(randomPermutations[1]) # This will force add a duplicate for testing.
    if not PermutationsAreUnique(permutations):
        nftUtil.FatalExit("\nFatal error!!!  Permutations are not unique.")

    attributeProbabilities = DetermineAttributeProbabilities(traits, permutations)

    # permutationsAndRarityIndexes become [ (permutation1, rarityIndex1), (permutation2, rarityIndex2), ...]
    permutationsAndRarityIndexes = []
    for p, permutation in enumerate(permutations):
        permutationsAndRarityIndexes.append((permutations[p], permutationRarityIndexes[p]))

    # The 'random' permutations tend to have the least rarest ones listed first just because they have a greater
    # likelihood of being chosen.  Plus they are in rarity order.  So shuffle them 5 times.
    for _ in range(5):
        random.shuffle(permutationsAndRarityIndexes)

    # The "Signature Series" probability for non-signature series images.
    # A bit of a kludge, we have to assume that signature series are the highest rarity level (0)
    signatureSeriesProbabilityForNonSignatureSeries = str(100 * (1 - rarityProbabilities[0])) + "%"

    # Remove any old output files and then initialize the database.
    PreProcessing(nftDefinition)

    print()
    for p, permutationAndRarityIndex in enumerate(permutationsAndRarityIndexes):
        permutation = permutationAndRarityIndex[0]
        rarityIndex = permutationAndRarityIndex[1]
        isFinalImage = isinstance(permutation, str)
        if isFinalImage:
            finalImage = finalImages[rarityIndex][int(permutation)]
            baseImage = finalImage[1]
            docTraits = [{"trait_type": "Signature Series", "value": finalImage[0], "probability": nftUtil.FormatPercent(rarityProbabilities[rarityIndex])}]
            traitCount = 1
        else:
            baseImage = attributeImages[0][permutation[0]]
            docTraits = []
            traitCount = 0
        baseImage = copy.copy(baseImage)
        extension = "." + nftDefinition["ImageType"]
        tokenId = p + 1
        doc = {
            nftUtil.FIELD_TOKEN_ID: tokenId,
            nftUtil.FIELD_TOKEN_IS_EXPOSABLE: None,
            nftUtil.FIELD_RARITY: rarities[rarityIndex]["Name"],
            nftUtil.FIELD_TRAIT_COUNT: traitCount,
            nftUtil.FIELD_TRAITS: docTraits,
            nftUtil.FIELD_IMAGE_BINARY_STRING: None,
        }  # Put this at the end because it is so huge.

        # Apply all attributes
        if not isFinalImage:
            for t, a in enumerate(permutation):
                trait = traits[t]
                attribute = trait["Attributes"][a]
                baseImage = ApplyAttribute(baseImage, attribute, attributeImages[t][a])
                # Something is only considered to be a "trait" if there is more than one choice.
                # For instance, the Left Wall and the Floor just have one value, so they are nor considered traits.
                if len(traits[t]["Attributes"]) != 1:
                    # If a traitImage is None (typically name = "Nothing"), then it should not be included in the
                    # trait count, although it still should be listed in the metadata.
                    if AttributeFilePath(nftDefinition, attribute) is not None:
                        traitCount += 1
                    doc[nftUtil.FIELD_TRAITS].append({"trait_type": trait["Name"], "value": attribute["Name"], "probability": nftUtil.FormatPercent(attributeProbabilities[t][a])})
            doc[nftUtil.FIELD_TRAIT_COUNT] = traitCount
            # Add the "Signature Series" attribute for non-SignatureSeries.
            doc[nftUtil.FIELD_TRAITS].append({"trait_type": "Signature Series", "value": None, "probability": signatureSeriesProbabilityForNonSignatureSeries})

        # Apply copyright statement
        ApplyCopyright(baseImage)

        # Save the images
        print("Generating Image", tokenId)
        if nftDefinition["UploadImagesToDatabase"]:
            buffer = io.BytesIO()
            baseImage.save(buffer, format=extension[1:])
            doc[nftUtil.FIELD_IMAGE_BINARY_STRING] = bson.Binary(buffer.getvalue())

        baseImage.save(os.path.join(nftDefinition["OutputImageFolder"], str(tokenId)) + extension)
        nftUtil.InsertOneDocument(doc)

    # Create the metadata and store the images
    nftUtil.CreateMetadata(nftDefinition)
    print("\nGenerated", len(permutations), "NFTs in", round(time.time() - startTime, 2), "seconds")

    # Dump the database out to 'AllNfts.csv'.
    nftUtil.ReportNfts()


def ValidateNftDefinition(nftDefinition):
    """
    Validate the NFT definition.
    """
    # Set working variables.
    traits = nftDefinition["Traits"]
    rarities = nftDefinition["Rarities"]

    # Validate the folder names and base URIs.
    for folderName in ("AttributeImageFolder", "BaseExternalUri", "BaseImageUri", "OutputImageFolder", "OutputMetadataFolder"):
        nftUtil.ValidateFolderName(nftDefinition[folderName])
    for rarity in rarities:
        if "FinalImageFolder" in rarity:
            nftUtil.ValidateFolderName(rarity["FinalImageFolder"])

    # Validate unique names
    nftUtil.ValidateUniqueNames(traits)
    for trait in traits:
        nftUtil.ValidateUniqueNames(trait["Attributes"])
    nftUtil.ValidateUniqueNames(rarities)
    for rarity in rarities:
        if "Traits" in rarity:
            nftUtil.ValidateUniqueNames(rarity["Traits"])

    # Validate that rarity probabilities add up to 100.  Otherwise too confusing.
    totalProbability = 0
    for rarity in rarities:
        probability = rarity["Probability"]
        if 0.001 <= probability <= 100:
            totalProbability += probability
        else:
            nftUtil.FatalExit("Rarity probability " + str(probability) + " must be between 0.001 and 100 inclusive.")
    if totalProbability != 100:
        nftUtil.FatalExit("Rarity probabilities toal " + str(totalProbability) + " != 100")


############################################### PROCESS #################################################
ProcessNftDefinition(nftConfig.NFT_DEFINITION_BOOKWORMS)
# ProcessNftDefinition(nftConfig.NFT_DEFINITION_DOGS)


########################################## OBSOLETE BELOW HERE ###########################################


# def GenerateQualifyingPermutations(nftDefinition):
#    '''
#    Get all possible qualifying permutations.
#    Filter out the 'Inclusions' and 'Exclusions' in nftDefinition with PermutationQualifies().
#    https://www.askpython.com/python-modules/python-itertools-module
#    '''
#    allExclusions = GetGlobalExclusions(nftDefinition)
#    allInclusions = GetGlobalInclusions(nftDefinition)
#    return PermutationLevels(nftDefinition, 0, [], allExclusions, allInclusions)

# def GenerateRandomPermutationsAndRarities(nftDefinition, signatureImages):
#    '''
#    Generate the randomPermutations and their associated randomRarities.
#    '''
#    # Generate all of the qualifying permutations, filtered with 'Include' and 'Exlcude'
#    startTime = time.time()
#    qualifyingPermutations = GenerateQualifyingPermutations(nftDefinition)
#    print('Generated', len(qualifyingPermutations), 'permutations in', round(time.time() - startTime, 2), 'seconds')

#    ##CsvWrite(qualifyingPermutations)

#    # go through qualifying permutations and creates rarities
#    # [0.0001, 0.0099, 0.0099, 0.9801]
#    print('\nCalculating statistical rarities...')
#    traits = nftDefinition['Traits']
#    rarityTraitIndex = GetRarityTrait(nftDefinition, returnIndex=True)
#    qualifyingRarities = [GetStatisticalRarity(permutation, traits, rarityTraitIndex) for permutation in qualifyingPermutations]

#    # Determine a qtyPerPermutationPerRarity that is sufficient to allow for the smallest permutaion rarity to have at least
#    # one entry in qualifyingPermutationsIntegers.  Anything over 500,000 makes it really slow!
#    #print('Determining probability tranch sizes...')
#    print('Allocating probability tranches...')
#    qtyPerPermutationPerRarity = 1
#    for rarity in qualifyingRarities:
#        # if 1 * 0.0001 < 1
#        if int(qtyPerPermutationPerRarity * rarity) < 1:
#            #  1 / 0.0001 = 10001
#            qtyPerPermutationPerRarity = int(1 / rarity) + 1
#    qtyPerPermutationPerRarity = min(qtyPerPermutationPerRarity, 500000)

#    # Create qualifyingPermutationsIntegers, which is a list of the qualifyingPpermutations indexes based on their rarity.
#    qualifyingPermutationsIntegers = []
#    iInteger = 0
#    for r, rarity in enumerate(qualifyingRarities):
#        # If qtyPerPermutationPerRarity * rarity < 1, then it would never get an entry added to qualifyingPermutationsIntegers.
#        # So set the qtyPerPermutationPerRarity to 1 so at least one entry will get added to qualifyingPermutationsIntegers.
#        # This means that very small rarities will have only one entry, and effecitively the same probability of being chosen.
#        useIncrement = max(1, int(qtyPerPermutationPerRarity * rarity))
#        for _ in range(iInteger, iInteger + useIncrement):
#            qualifyingPermutationsIntegers.append(r)
#        iInteger = iInteger + useIncrement
#        #if r % 100000 == 0:
#        #    print('Allocating probability tranches', r)

#    # Create the randomPermutations and randomRarities
#    randomPermutations = [] # A list of the permtations that have been generated
#    iGenerateds = [] # A list of the permutation indexes that have already been generated.
#    quantityToGenerate = min(len(qualifyingPermutations), nftDefinition['Quantity']) # The quantity that will be generated.
#    print('\nGenerating ' + str(quantityToGenerate) + ' random permutations...')
#    for _i in range(quantityToGenerate):
#        # Get a random permutation index from qualifyingPermutationsIntegers that does not already exist in iGenerateds.
#        # If you cannot find an unused random index, then clear out the iGenerateds from qualifyingPermutationsIntegers.
#        iGenerate = random.choice(qualifyingPermutationsIntegers)
#        if iGenerate in iGenerateds:
#            # Remove the iGenerateds from qualifyingPermutationsIntegers so you can get a unique iGenerate.
#            # This is really expensive, but list comprehension is by far the fastest because it only makes one pass.
#            # create a new array
#            # loop through qualifyingPermutationsIntegers
#            # if q is not in iGenerateds, copy to new list
#            # q = permutation 1, 2, 3 or 4 which is the index element of qualifyingPermutations [[0, 12, 5, 6, 2, 9, 0, ...], another permutation array]
#            qualifyingPermutationsIntegers = [q for q in qualifyingPermutationsIntegers if q not in iGenerateds]
#            iGenerateds = []
#            iGenerate = random.choice(qualifyingPermutationsIntegers)
#        iGenerateds.append(iGenerate)
#        randomPermutations.append(qualifyingPermutations[iGenerate])
#        if len(randomPermutations) % 1000 == 0:
#            print('Generating random permutations', len(randomPermutations)) #, len(qualifyingPermutationsIntegers))

#    # Paranoid validation that there are no duplicate permutations in randomPermutations.
#    ##randomPermutations.append(randomPermutations[1]) # This will force add a duplicate for testing.
#    if not PermutationsAreUnique(randomPermutations):
#        nftUtil.FatalExit('\nFatal error!!!  RandomPermutations are not unique.')

#    # Now add the extra 'Signature Series' files.
#    for filePath in signatureImages:
#        randomPermutations.append(filePath)

#    # The 'random' permutations tend to have the least rarest ones listed first just because thy have a greater likelihood of
#    # being chosen.  So shuffle them 5 times.
#    for _ in range(5):
#        random.shuffle(randomPermutations)

#    # Create randomRarities corresponding with randomPermutations
#    randomRarities = [GetStatisticalRarity(permutation, traits, rarityTraitIndex) for permutation in randomPermutations]

#    # Get the randomRarityIndex associated with each randomRarity
#    randomRarityIndexes = GenerateRarityIndexes(nftDefinition, randomRarities)

#    # When the permutations were created in PermutationLevels(), the 'IsRarityTrait' value in the permutation was just
#    # hard-coded to 0 (e.g. Mythic).  Because at the time, it was not known.  Now that it is known, we need to set it.
#    # If the permutation is a string, then that means that it is one of the Mythic "Signature Series", so we leave the
#    # permutation[rarityTraitIndex] == 0 (e.g. Mythic).
#    for p, permutation in enumerate(randomPermutations):
#        if not isinstance(permutation, str):
#            permutation[rarityTraitIndex] = randomRarityIndexes[p]

#    return randomPermutations, randomRarities, randomRarityIndexes

# def GenerateRarityIndexes(nftDefinition, rarities):
#    '''
#    Return a list of the rarityIndexes that corresponds exactly with the input rarities.
#    '''
#    rarityTrait = GetRarityTrait(nftDefinition)

#    # Get the rarityBreakPoints
#    sortedRarities = sorted(rarities)
#    rarityBreakPoints = []
#    cumulativeProbability = 0
#    for attribute in rarityTrait['Attributes']:
#        cumulativeProbability += attribute['Probability']
#        sortedRarityIndex = int(0.01 * cumulativeProbability * len(sortedRarities)) - 1
#        sortedRarityIndex = max(0, sortedRarityIndex) # cannot be < 0
#        sortedRarityIndex = min(sortedRarityIndex, len(sortedRarities) - 1) # cannot exceed the length of the array
#        rarityBreakPoints.append(sortedRarities[sortedRarityIndex])

#    rarityIndexes = []
#    for rarity in rarities:
#        for i, breakPoint in enumerate(rarityBreakPoints):
#            if rarity <= breakPoint:
#                rarityIndexes.append(i)
#                break

#    if len(rarityIndexes) != len(rarities):
#        nftUtil.FatalExit('len(rarityIndexes) != len(rarities)')

#    # Return a list of the rarityIndexes that corresponds exactly with rarities.
#    return rarityIndexes

# def GetRarityTrait(nftDefinition, returnIndex=False):
#    '''
#    sadasdas
#    '''
#    for t, trait in enumerate(nftDefinition['Traits']):
#        if 'IsRarityTrait' in trait and trait['IsRarityTrait']:
#            return t if returnIndex else trait
#    nftUtil.FatalExit('Cannot find IsRarityTrait')
#    return None # needed for lint

# def GetStatisticalRarity(permutation, traits, rarityTraitIndex):
#    '''
#    Get the statistical rarity, which is just the probabilities of each trait multiplied by one another.
#    '''
#    if isinstance(permutation, str):
#        # It is the filePath for one of the 'Signature Series' images.
#        return 0

#    #traits = nftDefinition['Traits']
#    # 1.0 = 100
#    statisticalRarity = 1.0
#    # a is the value and t is the index
#    # a is the index of the attributes array for each trait
#    for t, a in enumerate(permutation):
#        #if not IsRarityTrait(traits[t]):
#        if t != rarityTraitIndex: #not IsRarityTrait(traits[t]):
#            statisticalRarity *= 0.01 * traits[t]['Attributes'][a]['Probability']
#    # if two traits have probability of 0.01 it's 0.01 * 0.01
#    return statisticalRarity

# def LoadInputImages(nftDefinition):
#    '''
#    Load the input images.
#    '''
#    return None, None
# inputImageFolder = nftDefinition['AttributeImageFolder']

# inputImages = {} # keyed on full file path
# for trait in nftDefinition['Traits']:
#    for attribute in trait['Attributes']:
#        filePath = AttributeFilePath(nftDefinition, attribute)
#        if filePath is None:
#            continue # This is valid.  It means that the attribute is not applied.
#        filePath = os.path.join(inputImageFolder, trait['Name'], filePath)

#        attributeImage = Image.open(filePath)
#        ##attributeImage = attributeImage.convert("RGBA")
#        if 'Resize' in attribute:
#            attributeImage = attributeImage.resize(attribute['Resize'])
#        inputImages[filePath] = attributeImage

# signatureImages = {}
# if 'SignatureImageFolder' in nftDefinition:
#    for filePath in glob.iglob(nftDefinition['SignatureImageFolder'] + '*'):
#        signatureImages[filePath] = Image.open(filePath)

# return inputImages, signatureImages

# def PermutationLevels(nftDefinition, level, inPermutations, allExclusions, allInclusions):
#    '''
#    Recursive function for building the permutations for the traits level using inPermutaions as the starting point.
#    '''
#    # how many traits we have total in the nftConfig obj
#    traits = nftDefinition['Traits']
#    if level == len(traits):
#        return inPermutations # End of the line.  You are past the final level.

#    print('Generating permutations for', traits[level]['Name'])

#    # If we are on the rarityTrait level, then we only want one permutation, so we just pick 0.
#    # The actual value will be determined and overwritten once we actually know the rarity distribution.
#    rarityTraitIndex = GetRarityTrait(nftDefinition, returnIndex=True)
#    attributeRange = 1 if rarityTraitIndex == level else len(traits[level]['Attributes'])

#    # Get the inclusions and inclusions that are involved with this level.
#    exclusions = allExclusions[level]
#    inclusions = allInclusions[level]

#    outPermutations = []
#    if level == 0:
#        # range does 0 - 2 for 3 attributes
#        for a in range(attributeRange):
#            # appends attribute numbers to outPermutations array
#            # [[0, 0, 0,], []]
#            outPermutation = [a]
#            if not PermutationQualifiesInclusions(outPermutation, inclusions) or PermutationQualifiesExclusions(outPermutation, exclusions):
#                continue
#            outPermutations.append(outPermutation)
#    else:
#        # for each array in [[0, 0, 0, 0], [0, 0, 0, 1]]
#        # for loop within for loop multiplies the traits
#        for inPermutation in inPermutations:
#            # range of 0, 1 for 2 attributes

#            for a in range(attributeRange):
#                # make copy of [0, 0, 0]
#                # second round make copy of [0, 0, 0]
#                outPermutation = copy.copy(inPermutation)
#                # [0, 0, 0, 0]
#                # a is now 1 so we end up with [0, 0, 0, 1]
#                outPermutation.append(a)

#                if not PermutationQualifiesInclusions(outPermutation, inclusions) or PermutationQualifiesExclusions(outPermutation, exclusions):
#                    continue
#                # [[0, 0, 0, 0]]
#                # second round [[0, 0, 0, 0], [0, 0, 0, 1]]
#                # a new array will get created for each trait that has more then one attribute
#                outPermutations.append(outPermutation)

#    # Get the next level. runs function again
#    # [[0, 0, 0, 0, 0....], [0, 1]...]
#    return PermutationLevels(nftDefinition, level + 1, outPermutations, allExclusions, allInclusions)
