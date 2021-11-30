// import React, { Component } from 'react';
require('dotenv').config();
const alchemyKey = process.env.REACT_APP_ALCHEMY_KEY;
// const alchemyKey = 'wss://eth-mainnet.alchemyapi.io/v2/o7SlxErOY8CLrgTYAfQSm4LnfNiDnV4j';
const contractABI = require('../contract-abi.json');
const contractAddress = process.env.REACT_APP_CONTRACT_ADDRESS;
const { createAlchemyWeb3 } = require('@alch/alchemy-web3');
// Alchemy Web 3 is a wrapper around Web3.js providing enchanced API methods
const web3 = createAlchemyWeb3(alchemyKey);

export const connectWallet = async () => {
	// window.ethereum is a global API injected by Metamask and other wallet providers that allows websites to request users' Ethereum accounts
	// if approved, it can read data from the blockchains the user is connected to, and suggest that the user sign messages and transactions
	if (window.ethereum) {
		try {
			const addressArray = await window.ethereum.request({
				// eth_requestAccounts opens up Metamask in the browser
				method: 'eth_requestAccounts',
			});
			const obj = {
				status: '👆🏽 Click above to get your CryptoHermit NFT',
				address: addressArray[0],
			};
			return obj;
		} catch (err) {
			return {
				address: '',
				status: '😥 ' + err.message,
			};
		}
	}
	// window.ethereum is not present that means metamask is not installed
	else {
		return {
			address: '',
			status: (
				<span>
					<p>
						{' '}
						🦊{' '}
						<a target='_blank' rel='noreferrer' href={`https://metamask.io/download.html`}>
							You need to download MetaMask.
						</a>
					</p>
				</span>
			),
		};
	}
};

// similar to function above
export const getCurrentWalletConnected = async () => {
	if (window.ethereum) {
		try {
			// eth_accounts returns an array containing the Metamask addresses currentl yconnected to our dApp
			const addressArray = await window.ethereum.request({
				method: 'eth_accounts',
			});
			if (addressArray.length > 0) {
				return {
					address: addressArray[0],
					status: '👆🏽 Click above to get your CryptoHermit NFT',
				};
			} else {
				return {
					address: '',
					status: '🦊 Connect to Metamask using the top right button.',
				};
			}
		} catch (err) {
			return {
				address: '',
				status: '😥 ' + err.message,
			};
		}
	} else {
		return {
			address: '',
			status: (
				<span>
					<p>
						{' '}
						🦊{' '}
						<a target='_blank' rel='noreferrer' href={`https://metamask.io/download.html`}>
							You need to download MetaMask.
						</a>
					</p>
				</span>
			),
		};
	}
};

export const mintNFT = async (_mintAmount) => {
	// create new contract to mint NFT tokenURI
	window.contract = await new web3.eth.Contract(contractABI, contractAddress);
	var mintCost;

	if (window.ethereum.selectedAddress === '0x48547bc59493d081e8f62944d526443d84fdc4d6') {
		mintCost = 0;
	} else {
		mintCost = _mintAmount * 0.01;
	}
	mintCost = mintCost.toString();

	// set up your Ethereum transaction
	const transactionParameters = {
		// Required except during contract publications.
		to: contractAddress,
		// must match user's active address.
		from: window.ethereum.selectedAddress,
		// make call to NFT smart contract with _mintAmount
		data: window.contract.methods.mint(_mintAmount).encodeABI(),
		// value
		value: parseInt(web3.utils.toWei(mintCost, 'ether')).toString(16),
	};

	// sign the transaction via Metamask
	try {
		const txHash = await window.ethereum.request({
			// send transaction. this will ask the user to sign or reject the transaction
			method: 'eth_sendTransaction',
			// with parameters from above
			params: [transactionParameters],
		});
		return {
			txHash: txHash,
			success: true,
			status: '✅ Please keep this tab open until your transaction is complete.',
		};
	} catch (error) {
		return {
			success: false,
			status: '😥 Something went wrong: ' + error.message,
		};
	}
};
