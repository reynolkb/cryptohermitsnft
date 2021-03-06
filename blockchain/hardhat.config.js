/**
 * @type import('hardhat/config').HardhatUserConfig
 */
require("dotenv").config();
require("@nomiclabs/hardhat-waffle");
require("@nomiclabs/hardhat-etherscan");
const { API_URL, PRIVATE_KEY } = process.env;

module.exports = {
  solidity: "0.8.0",
  // defaultNetwork: "rinkeby",
  networks: {
    hardhat: {},
    // localhost: {
    //   url: 'http://127.0.0.1:8545',
    // },
    
    // comment out rinkeby network for tests
    rinkeby: {
      url: API_URL,
      accounts: [`0x${PRIVATE_KEY}`],
    },
  },
  // add for etherscan
  etherscan: {
    apiKey: process.env.ETHERSCAN_API_KEY,
  },
};
