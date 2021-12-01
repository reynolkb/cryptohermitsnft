import React from 'react';

import rarityImage1 from '../../assets/rarity-item1.png';
import rarityImage2 from '../../assets/rarity-item2.png';
import rarityImage3 from '../../assets/rarity-item3.png';
import rarityImage4 from '../../assets/rarity-item4.png';
import rarityImage5 from '../../assets/rarity-item5.png';
import rarityImage6 from '../../assets/rarity-item6.png';
import rarityImage7 from '../../assets/rarity-item7.png';
import './rarity.css';

export default function Connect(props) {
	const items = [
		{ title: 'Common', color: '#999999', image: rarityImage1 },
		{ title: 'Uncommon', color: '#6DAE10', image: rarityImage2 },
		{ title: 'Rare', color: '#10A1BA', image: rarityImage3 },
		{ title: 'Epic', color: '#B049BD', image: rarityImage4 },
		{ title: 'Legendary', color: '#D57F38', image: rarityImage5 },
		{ title: 'Exotic', color: '#84ECEC', image: rarityImage6 },
		{ title: 'Mythic', color: '#F6D248', image: rarityImage7 },
	];
	return (
		<div className='page-rarity'>
			<p className='text-magento-border'>Rarity</p>
			<p className='text-normal-black' style={{ marginTop: 20, maxWidth: 970 }}>
				Each Bookworm NFT has a rarity ranging from common to mythic. The color of the book on the NFT corresponds with the rarity level. Below are some examples of NFTs you could get.
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
		</div>
	);
}
