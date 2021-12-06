import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlusSquare, faMinusSquare } from '@fortawesome/free-regular-svg-icons';

import './faq.css';

export default function Faq(props) {
	const [qShow1, setQShow1] = useState(false);
	const [qShow2, setQShow2] = useState(false);
	const [qShow3, setQShow3] = useState(false);
	const [qShow4, setQShow4] = useState(false);
	const [qShow5, setQShow5] = useState(false);
	const [qShow6, setQShow6] = useState(false);
	const [qShow7, setQShow7] = useState(false);
	const [qShow8, setQShow8] = useState(false);

	return (
		<div className='page-mint' style={{ textAlign: 'left' }}>
			<p className='text-magento-border'>FAQ</p>
			<div className='faq-text-group'>
				{/* question 1 */}
				<div className='faq-text-question' onClick={() => setQShow1((prev) => !prev)}>
					<FontAwesomeIcon icon={qShow1 ? faMinusSquare : faPlusSquare} className='faq-text-plus' />
					<p className='text-faq-black'>What is a NFT?</p>
				</div>
				{qShow1 && (
					<p className='faq-text-answer'>
						NFT stands for “non-fungible token,” which refers to a unique digital asset that can’t be replaced with something else. The opposite is something that is “fungible”. For
						example, a dollar bill. One dollar bill can be swapped for another since they are identical. However, no two NFTs are the ever same.
					</p>
				)}
				{/* question 2 */}
				<div className='faq-text-question' onClick={() => setQShow2((prev) => !prev)}>
					<FontAwesomeIcon icon={qShow2 ? faMinusSquare : faPlusSquare} className='faq-text-plus' />
					<p className='text-faq-black'>What is required to mint a NFT?</p>
				</div>
				{qShow2 && <p className='faq-text-answer'>You must download MetaMask and fund your MetaMask wallet.</p>}
				{/* question 3 */}
				<div className='faq-text-question' onClick={() => setQShow3((prev) => !prev)}>
					<FontAwesomeIcon icon={qShow3 ? faMinusSquare : faPlusSquare} className='faq-text-plus' />
					<p className='text-faq-black'>How do I download MetaMask and fund my MetaMask wallet?</p>
				</div>
				{qShow3 && (
					<ol className='faq-text-answer'>
						<li className='space-list'>
							You need to{' '}
							<a href='https://metamask.io/download' target='_blank' rel='noreferrer'>
								download MetaMask.
							</a>
						</li>
						<li className='space-list'>
							<a href='https://www.coinbase.com/buy-ethereum' target='_blank' rel='noreferrer'>
								Buy Ethereum
							</a>{' '}
							from an exchange.
						</li>
						<li className='space-list'>
							<a href='https://www.coinbase.com/learn/tips-and-tutorials/how-to-send-crypto' target='_blank' rel='noreferrer'>
								Transfer
							</a>{' '}
							it to your MetaMask Wallet.
						</li>
					</ol>
				)}
				{/* question 4 */}
				<div className='faq-text-question' onClick={() => setQShow4((prev) => !prev)}>
					<FontAwesomeIcon icon={qShow4 ? faMinusSquare : faPlusSquare} className='faq-text-plus' />
					<p className='text-faq-black'>How do I mint a NFT?</p>
				</div>
				{qShow4 && (
					<p className='faq-text-answer'>
						Once you have MetaMask installed and Ethereum in your wallet you can <Link to='/mint-not-active'>click here</Link> to mint a NFT.
					</p>
				)}
				{/* question 5 */}
				<div className='faq-text-question' onClick={() => setQShow5((prev) => !prev)}>
					<FontAwesomeIcon icon={qShow5 ? faMinusSquare : faPlusSquare} className='faq-text-plus' />
					<p className='text-faq-black'>When can I mint a NFT?</p>
				</div>
				{qShow5 && <p className='faq-text-answer'>Our presale begins Wednesday, January 12th at 6pm ET. Public sale begins Friday, January 14th at 6pm ET.</p>}
				{/* question 6 */}
				<div className='faq-text-question' onClick={() => setQShow6((prev) => !prev)}>
					<FontAwesomeIcon icon={qShow6 ? faMinusSquare : faPlusSquare} className='faq-text-plus' />
					<p className='text-faq-black'>What do I receive when I mint a NFT?</p>
				</div>
				{qShow6 && (
					<p className='faq-text-answer'>
						Essentially, you are purchasing the token id which acts as a certificate for your NFT. Think of it like a certificate of ownership for a piece of art. The smart contract keeps
						track that your wallet owns a token id that corresponds to the NFT that you purchased.
					</p>
				)}
				{/* question 7 */}
				<div className='faq-text-question' onClick={() => setQShow7((prev) => !prev)}>
					<FontAwesomeIcon icon={qShow7 ? faMinusSquare : faPlusSquare} className='faq-text-plus' />
					<p className='text-faq-black'>What do you have planned for the future of CryptoHermits?</p>
				</div>
				{qShow7 && (
					<p className='faq-text-answer'>
						We have a lot planned once we reach 100% in sales for the bookworm collection. The next collection we are excited for is the homesteader collection. From there we hope to
						expand to other collections. We want to create a community of self-sufficient, independent thinkers who aren't afraid to fight censorship!
					</p>
				)}
				{/* question 8 */}
				<div className='faq-text-question' onClick={() => setQShow8((prev) => !prev)}>
					<FontAwesomeIcon icon={qShow8 ? faMinusSquare : faPlusSquare} className='faq-text-plus' />
					<p className='text-faq-black'>Can I buy on my mobile phone?</p>
				</div>
				{qShow8 && <p className='faq-text-answer'>Yes, simply download MetaMask for iOS or Android and visit our site using the MetaMask browser.</p>}
			</div>
		</div>
	);
}
