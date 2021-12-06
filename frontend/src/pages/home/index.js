import React from 'react';
import { useNavigate } from 'react-router-dom';

import './home.css';

export default function Home(props) {
	const navigate = useNavigate();
	return (
		<div className='page-home'>
			<div>
				<p className='text-magento-noborder mobile-header-text'>Crypto</p>
				<p className='text-cyan mobile-header-text'>Hermits</p>
			</div>
			<img className='bookworm-gif' src='https://media.giphy.com/media/iBcPKkUkxndjiQg9Oy/giphy.gif' alt='gif' />
			{/* <p className='text-normal-black para-home'> */}
			<p className='text-normal-black p-home'>
				The Bookworms are a collection of 10,000 NFTs sitting on top of the Ethereum blockchain costing 0.05 ETH each. After decades of down time and solitude, they are ready to make some
				noise. Free thinking has no political party. We heed to grandma's telltale wisdom of never judging a book by its cover. We are modern day rebels who are overlooked and without credit.
				Join the CryptoHermit revolution of bookworms, self-sufficient homesteaders, fighters of free speech and leaders of ethical, sustainable living. Collect art and make friends with those
				who are just as intentional (and probably fed up) as you. We just want to be left alone and leave others alone. Let's find peace in solitary, together.
			</p>
			<button className='btn-black' style={{ marginTop: 40 }} onClick={() => navigate('/rarity')}>
				LEARN MORE
			</button>
		</div>
	);
}
