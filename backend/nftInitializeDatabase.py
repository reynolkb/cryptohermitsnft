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
from PIL import Image  # , ImageFont, ImageDraw

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


def AttributeFilePath(nftDefinition, attribute):
    """
    Return the effective attribute filePath.
    """
    if "FilePath" in attribute:
        return attribute["FilePath"]
    return attribute["Name"] + "." + nftDefinition["ImageType"]


def BuildPermutations(nftDefinition, finalImages, rarityQuantities):
    """
    Build the list of permutations, taking into account the exclusions and inclusions.
    A permutation consists of a list of attributes represented by their index as they appear in nftDefinition.
    For instance a permutaion of (4,3,6) Would mean that the first trait would have have an attribute of 4,
    the second trait would have an attribute of 3, and the third trait would have an attribute of 6.
    """
    # Define working variables
    traits = nftDefinition["Traits"]
    rarities = nftDefinition["Rarities"]

    # Get the rarityAttributeDistributions.  They are a 3-dimensional array representing the attribute probability
    # within each trait within each rarity.  For instance, a specific rarity index might have a 2-dimensional
    # array as such: [ [0, 1, 1, 2], [0, 1, 1, 1, 2, 3, 3, 3], ...]
    # This would mean that for this specific rarity, for the first trait, the attibute 0 would have a probability of
    # 25%, the attribute 1 would have a probability of 50%, and the attribute 2 would have a probability of 25%.
    rarityAttributeDistributions = GetRarityAttributeDistributions(nftDefinition)

    # Get the globalExclusions and globalInclusions.
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
                    for attributeIndex in range(len(traits)):
                        if not FindQualifyingPermutationAttribute(permutation, attributeIndex, rarityAttributeDistribution[attributeIndex], globalInclusions, globalExclusions):
                            qualifyingPermutationFound = False
                            break
                    if qualifyingPermutationFound and permutation not in permutations:
                        permutations.append(permutation)
                        permutationRarityIndexes.append(r)
                        if len(permutations) % 1000 == 0:
                            print("Generating Permutations", len(permutations))
                        break

    return permutations, permutationRarityIndexes


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


def DetermineRarityQuantities(nftDefinition):
    """
    Determine the quantity of NFTs for each rarity level.
    """
    rarityQuantities = []  # The quantity of each rarity to generate.
    rProbabilities = []  # (0 = The rarity probability, 1 = The associated r index)
    totalQuantityNeeded = nftDefinition["TotalQuantity"]  # 10000
    remainingQuantityNeeded = totalQuantityNeeded
    for r, rarity in enumerate(nftDefinition["Rarities"]):
        probability = rarity["Percentage"]
        rProbabilities.append((probability, r))
        rarityQuantity = min(remainingQuantityNeeded, int(round(0.01 * probability * totalQuantityNeeded)))
        rarityQuantities.append(rarityQuantity)
        remainingQuantityNeeded -= rarityQuantity

    # remainingQuantityNeeded might still not be 0 due to rounding
    # So start allocating to the highest probability rarities first.
    rProbabilities.sort(reverse=True)
    while 0 < remainingQuantityNeeded:
        for rProbability in rProbabilities:  # sorted(rProbabilities, reverse=True):
            rarityQuantities[rProbability[1]] += 1
            remainingQuantityNeeded -= 1
            if remainingQuantityNeeded == 0:
                break

    return rarityQuantities


def FindQualifyingPermutationAttribute(permutation, traitIndex, attributeDistribution, globalInclusions, globalExclusions):
    """
    Find a valid attribute for traitIndex, and then append it to the permutation that is being built.
    """
    attributeFound = False
    for _ in range(3):  # 3 seems to be optimal.
        attributeDistributionIndex = random.randint(0, len(attributeDistribution) - 1)
        permutation.append(attributeDistribution[attributeDistributionIndex])
        if not PermutationQualifiesInclusions(permutation, globalInclusions[traitIndex]) or PermutationQualifiesExclusions(permutation, globalExclusions[traitIndex]):
            # The permutaion does not qualify based on globalInclusions and globalExclusions.
            # So pop it off and try again.
            permutation.pop()
            continue
        attributeFound = True
        break
    return attributeFound


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
        if "Traits" in rarity:
            for t, trait in enumerate(traits):
                traitProbabilityDistribution = ProbabilityDistribution(trait["Attributes"])
                traitAttributes = []  # all valid attributes for this trait
                for a in range(len(trait["Attributes"])):
                    if a in rarityExclusions[r][t]:
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
        if "Traits" in rarity:
            traitExclusionsInclusions = [[] for _ in range(len(traits))]  # [None] * len(traits)
            for trait in rarity["Traits"]:
                if exclusionsOrInclusions in trait:
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
    images = []
    for t, trait in enumerate(traits):
        # If the image is None, then it means that the attribute is not applied.
        images.append([None] * len(trait["Attributes"]))
        for a, attribute in enumerate(trait["Attributes"]):
            filePath = AttributeFilePath(nftDefinition, attribute)
            if filePath is not None:
                attributeImage = Image.open(os.path.join(imageFolder, trait["Name"], filePath))
                ##attributeImage = attributeImage.convert("RGBA")
                ##if 'Resize' in attribute:
                ##    attributeImage = attributeImage.resize(attribute['Resize'])
                images[t][a] = attributeImage

    return images


def LoadFinalImages(nftDefinition):
    """
    Load the rarity images.
    """
    rarities = nftDefinition["Rarities"]
    images = [None] * len(rarities)
    for r, rarity in enumerate(rarities):
        if "FinalImageFolder" in rarity:
            images[r] = []
            for filePath in glob.iglob(rarity["FinalImageFolder"] + "*." + nftDefinition["ImageType"]):
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
    factor = 1  ## 10
    while True:
        allAreIntegers = True
        for thing in thingList:
            probability = thing["Probability"] * factor
            if probability != int(probability):
                allAreIntegers = False
                factor *= 10
                if 100 < factor:  ## 1000
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
    finalImages = LoadFinalImages(nftDefinition)

    # Determine the quantity of NFTs for each rarity level
    rarityQuantities = DetermineRarityQuantities(nftDefinition)

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

    # A bit of a kludge, we have to assume that signature series are the highest rarity level (0)
    signatureSeriesProbability = nftUtil.FormatPercent(0.01 * rarities[0]["Percentage"])
    signatureSeriesProbabilityForNonSignatureSeries = nftUtil.FormatPercent(0.01 * (100 - rarities[0]["Percentage"]))

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
            docTraits = [{"trait_type": "Signature Series", "value": finalImage[0], "probability": signatureSeriesProbability}]
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
                if nftDefinition["UploadImagesToDatabase"] or nftDefinition["WriteImagesToDisk"]:
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
        nftUtil.ApplyCopyright(baseImage)

        # Save the images
        print("Generating Image", tokenId)
        if nftDefinition["UploadImagesToDatabase"]:
            buffer = io.BytesIO()
            baseImage.save(buffer, format=extension[1:])
            doc[nftUtil.FIELD_IMAGE_BINARY_STRING] = bson.Binary(buffer.getvalue())
        if nftDefinition["WriteImagesToDisk"]:
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

    # Validate that rarity percentages add up to 100.
    totalPercentage = 0
    for rarity in rarities:
        percentage = rarity["Percentage"]
        if 0.001 <= percentage <= 100:
            totalPercentage += percentage
        else:
            nftUtil.FatalExit("Rarity percentage " + str(percentage) + " must be between 0.001 and 100 inclusive.")
    if totalPercentage != 100:
        nftUtil.FatalExit("Rarity percentages toal " + str(totalPercentage) + " != 100")


############################################### PROCESS #################################################
ProcessNftDefinition(nftConfig.NFT_DEFINITION_BOOKWORMS)
# ProcessNftDefinition(nftConfig.NFT_DEFINITION_DOGS)
