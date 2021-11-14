import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import './FAQS.css';

class FAQS extends Component {
	render() {
		return (
			<div className='section' id='FAQS'>
				<h1>FAQS</h1>
				<br></br>
				<br></br>
				<h2>How do I download MetaMask and fund my MetaMask wallet?</h2>
				<p>
					1. You need to{' '}
					<a href='https://metamask.io/download' target='_blank'>
						download MetaMask
					</a>
					.
				</p>
				<p>
					2.{' '}
					<a href='https://www.coinbase.com/buy-ethereum' target='_blank'>
						Buy Ethereum
					</a>{' '}
					from an exchange.
				</p>
				<p>
					3.{' '}
					<a href='https://www.coinbase.com/learn/tips-and-tutorials/how-to-send-crypto' target='_blank'>
						Transfer it
					</a>{' '}
					to your MetaMask Wallet.
				</p>
				<br></br>
				<br></br>
				<h2>How do I mint an NFT?</h2>
				<p>
					Once you have MetaMask installed and Ethereum in your wallet you can <Link to='/mint'>click here</Link> to mint an NFT.
				</p>
				<br></br>
				<br></br>
				<h2>When can I mint an NFT?</h2>
				<p>You can officially mint an NFT on January 8th at 1:00 pm ET.</p>
				<br></br>
				<br></br>
				<h2>What do you have planned for the future of CryptoHermits?</h2>
				<p>
					We have a lot planned once we reach 100% in sales for the bookworm collection. The next collection we are excited for is the homesteader collection. From there we hope to expand to
					other collections. We want to create a community of self-sufficient, independent thinkers who aren't afraid to fight censorship!
				</p>
				<br></br>
				<br></br>
				<h2>Can I buy on my mobile phone?</h2>
				<p>Yes, simply download MetaMask for iOS or Android and visit our site using the MetaMask browser.</p>
			</div>
		);
	}
}

export default FAQS;
