
'''
1. Before this is run, you will need to update 'QuantityOfExposableTokens' and/or 'BaseExternalUri' and/or 'BaseImageUri'
   in the nftDefinition in nftConfig.py
2. Then when this is run, it will:
    a) Update the 'MetadataIsExposable', 'external_url', and 'image' mongoDB fields.
    b) Write out the resulting metadata files.
'''
import nftConfig
import nftUtil

nftUtil.CreateMetadata(nftConfig.NFT_DEFINITION_BOOKWORMS)