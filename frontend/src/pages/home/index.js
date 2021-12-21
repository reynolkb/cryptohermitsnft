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
			<img className='bookworm-gif' src='https://media.giphy.com/media/UtxHBMT3CrAqV2bw2Y/giphy.gif' alt='gif' />
			{/* <p className='text-normal-black para-home'> */}
			<p className='text-normal-black p-home'>
				The Bookworms are a collection of 5,555 NFTs sitting on top of the Ethereum blockchain costing 0.05 ETH each. After decades of down time and solitude, they are ready to make some
				noise. Free thinking has no political party. We heed to grandma's telltale wisdom of never judging a book by its cover.
			</p>
			<button className='btn-black' style={{ marginTop: 40 }} onClick={() => navigate('/rarity')}>
				LEARN MORE
			</button>
		</div>
	);
}
