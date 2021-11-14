async function main() {
  // MyNFT is a factory for instances of our NFT contract
  const CryptoHermits = await ethers.getContractFactory("CryptoHermits");

  // Start deployment, returning a promise that resolves to a contract object
  const cryptoHermits = await CryptoHermits.deploy(
    "CryptoHermits",
    "HERM",
    "https://cryptohermits.herokuapp.com/"
  );
  console.log("Contract deployed to address:", cryptoHermits.address);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
