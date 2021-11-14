const { expect } = require("chai");
const { ethers } = require("ethers");

describe("BitBirds", function () {
  it("Should return the right name and symbol", async function () {
    const BitBirds = await hre.ethers.getContractFactory("BitBirds");
    const bitBirds = await BitBirds.deploy("BitBirds", "BB");

    await bitBirds.deployed();
    expect(await bitBirds.name()).to.equal("BitBirds");
    expect(await bitBirds.symbol()).to.equal("BB");
  });
  it("signedTx from and to should equal public key and contract address", async function () {
    const BitBirds = await hre.ethers.getContractFactory("BitBirds");
    const bitBirds = await BitBirds.deploy("BitBirds", "BB");

    await bitBirds.deployed();

    const provider = new ethers.providers.JsonRpcProvider();
    const privateKey = '0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80';
    const signer = new ethers.Wallet(privateKey, provider);
    const publicKey = '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266';
    const tokenURI = 'https://gateway.pinata.cloud/ipfs/QmWBCpgGeTQJojTgEi6iSnxf8FhVdhKGiwL2cxJ4Ahaxjr';
    
    const _nonce = await signer.getTransactionCount("latest");

    bitBirds.on('printNewItemId', (newItemId) => {
      const _newItemId = newItemId;
      console.log(_newItemId);
    });

    let ABI = [
      "function mintNFT(address recipient, string memory tokenURI)"
    ];
    let iface = new ethers.utils.Interface(ABI);

    const _data = iface.encodeFunctionData("mintNFT", [publicKey, tokenURI]);
    const _contractAddress = bitBirds.address;

    // gasPrice is null since it's an EIP-1559 transaction
    const _gasPrice = await provider.getGasPrice();
    const _gasLimit = 500000;

    const tx = {
      from: publicKey,
      to: _contractAddress,
      nonce: _nonce,
      gasLimit: _gasLimit,
      gasPrice: _gasPrice,
      data: _data,
      value: ethers.utils.parseEther("0.05"),
    }

    const signedTx = await signer.sendTransaction(tx);
    expect(signedTx['from']).to.equal(publicKey);
    expect(signedTx['to']).to.equal(_contractAddress);
  });
  it("newItemId should be 1 since we are testing a new instance of the contract", async function () {
    const BitBirds = await hre.ethers.getContractFactory("BitBirds");
    const bitBirds = await BitBirds.deploy("BitBirds", "BB");

    await bitBirds.deployed();

    const provider = new ethers.providers.JsonRpcProvider();
    const privateKey = '0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80';
    const signer = new ethers.Wallet(privateKey, provider);
    const publicKey = '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266';
    const tokenURI = 'https://gateway.pinata.cloud/ipfs/QmWBCpgGeTQJojTgEi6iSnxf8FhVdhKGiwL2cxJ4Ahaxjr';
    
    const _nonce = await signer.getTransactionCount("latest");

    bitBirds.on('printNewItemId', (newItemId) => {
      const _newItemId = newItemId;
      console.log(_newItemId);
    });

    let ABI = [
      "function mintNFT(address recipient, string memory tokenURI)"
    ];
    let iface = new ethers.utils.Interface(ABI);

    const _data = iface.encodeFunctionData("mintNFT", [publicKey, tokenURI]);
    const _contractAddress = bitBirds.address;

    // gasPrice is null since it's an EIP-1559 transaction
    const _gasPrice = await provider.getGasPrice();
    const _gasLimit = 500000;

    const tx = {
      from: publicKey,
      to: _contractAddress,
      nonce: _nonce,
      gasLimit: _gasLimit,
      gasPrice: _gasPrice,
      data: _data,
      value: ethers.utils.parseEther("0.05"),
    }

    const signedTx = await signer.sendTransaction(tx);
    const txHash = signedTx['hash'];

    const txReceipt = await provider.waitForTransaction(txHash);
    let _newItemId = parseInt(txReceipt['logs'][1]['data'], 16);
    _newItemId = _newItemId.toString();

    expect(_newItemId).to.equal('1');
  });
  it("getBalance should return a balance of 0.05 eth", async function () {
    const BitBirds = await hre.ethers.getContractFactory("BitBirds");
    const bitBirds = await BitBirds.deploy("BitBirds", "BB");

    await bitBirds.deployed();

    const provider = new ethers.providers.JsonRpcProvider();
    const privateKey = '0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80';
    const signer = new ethers.Wallet(privateKey, provider);
    const publicKey = '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266';
    const tokenURI = 'https://gateway.pinata.cloud/ipfs/QmWBCpgGeTQJojTgEi6iSnxf8FhVdhKGiwL2cxJ4Ahaxjr';
    
    const _nonce = await signer.getTransactionCount("latest");

    bitBirds.on('printNewItemId', (newItemId) => {
      const _newItemId = newItemId;
      console.log(_newItemId);
    });

    let ABI = [
      "function mintNFT(address recipient, string memory tokenURI)"
    ];
    let iface = new ethers.utils.Interface(ABI);

    const _data = iface.encodeFunctionData("mintNFT", [publicKey, tokenURI]);
    const _contractAddress = bitBirds.address;

    // gasPrice is null since it's an EIP-1559 transaction
    const _gasPrice = await provider.getGasPrice();
    const _gasLimit = 500000;

    const tx = {
      from: publicKey,
      to: _contractAddress,
      nonce: _nonce,
      gasLimit: _gasLimit,
      gasPrice: _gasPrice,
      data: _data,
      value: ethers.utils.parseEther("0.05"),
    }

    await signer.sendTransaction(tx);
    let balance = await bitBirds.getBalance();
    balance = parseInt(balance['_hex'], 16);
    balance = balance.toString();
    expect(balance).to.equal("50000000000000000");
  });
  it("withdrawBalance should withdraw balance and contract balance should be 0", async function () {
    const BitBirds = await hre.ethers.getContractFactory("BitBirds");
    const bitBirds = await BitBirds.deploy("BitBirds", "BB");

    await bitBirds.deployed();

    const provider = new ethers.providers.JsonRpcProvider();
    const privateKey = '0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80';
    const signer = new ethers.Wallet(privateKey, provider);
    const publicKey = '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266';
    const tokenURI = 'https://gateway.pinata.cloud/ipfs/QmWBCpgGeTQJojTgEi6iSnxf8FhVdhKGiwL2cxJ4Ahaxjr';
    
    const _nonce = await signer.getTransactionCount("latest");

    bitBirds.on('printNewItemId', (newItemId) => {
      const _newItemId = newItemId;
      console.log(_newItemId);
    });

    let ABI = [
      "function mintNFT(address recipient, string memory tokenURI)"
    ];
    let iface = new ethers.utils.Interface(ABI);

    const _data = iface.encodeFunctionData("mintNFT", [publicKey, tokenURI]);
    const _contractAddress = bitBirds.address;

    // gasPrice is null since it's an EIP-1559 transaction
    const _gasPrice = await provider.getGasPrice();
    const _gasLimit = 500000;

    const tx = {
      from: publicKey,
      to: _contractAddress,
      nonce: _nonce,
      gasLimit: _gasLimit,
      gasPrice: _gasPrice,
      data: _data,
      value: ethers.utils.parseEther("0.05"),
    }

    await signer.sendTransaction(tx);
    await bitBirds.withdrawBalance();
    let contractBalance = await provider.getBalance(_contractAddress);
    contractBalance = parseInt(contractBalance['_hex'], 16);
    contractBalance = contractBalance.toString();
    expect(contractBalance).to.equal("0");
  });
});