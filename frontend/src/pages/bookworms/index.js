import React from 'react';
import { useNavigate } from 'react-router-dom';

import common from '../../assets/common-nft.png';
import uncommon from '../../assets/uncommon-nft.png';
import rare from '../../assets/rare-nft.png';
import epic from '../../assets/epic-nft.png';
import legendary from '../../assets/legendary-nft.png';
import exotic from '../../assets/exotic-nft.png';
import mythic from '../../assets/mythic-nft.png';
import './rarity.css';

export default function Connect(props) {
	const items = [
		{ title: 'Common', color: '#999999', image: common },
		{ title: 'Uncommon', color: '#6DAE10', image: uncommon },
		{ title: 'Rare', color: '#10A1BA', image: rare },
		{ title: 'Epic', color: '#B049BD', image: epic },
		{ title: 'Legendary', color: '#D57F38', image: legendary },
		{ title: 'Exotic', color: '#84ECEC', image: exotic },
		{ title: 'Mythic', color: '#F6D248', image: mythic },
	];

	const navigate = useNavigate();

	return (
		<div className='page-bookworms'>
			<p className='text-magento-border'>Bookworms</p>
			<p className='text-normal-black p-bookworms' style={{ marginTop: 30, marginBottom: 20, maxWidth: 970 }}>
				Each of the 10,000 Bookworm NFTs have a rarity ranging from common to mythic and are built on the Ethereum blockchain. The color of the book on the NFT corresponds with the rarity
				level. Below are some examples of NFTs you could get.
			</p>
			<div className='rarity-wrapper'>
				{items.map((item, index) => (
					<div className='rarity-item' key={`rarity-${index}`}>
						<a href={item.image}>
							<img className='rarity-image' src={item.image} alt={item} />
						</a>
						<div className='rarity-text' style={{ color: item.color }}>
							{item.title}
						</div>
					</div>
				))}
			</div>
			<button className='btn-black' style={{ marginTop: 40 }} onClick={() => navigate('/mint-not-active')}>
				MINT
			</button>
		</div>
	);
}
