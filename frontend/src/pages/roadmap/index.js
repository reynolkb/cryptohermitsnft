import React from 'react';

import './roadmap.css';

export default function RoadMap(props) {
	return (
		<div className='page-mint'>
			<p className='text-magento-border'>Roadmap</p>
			{/* <p className="text-normal-black" style={{ maxWidth: 542, marginTop: 35 }}> */}
			<p className='text-normal-black para-roadmap' style={{ maxWidth: 542, marginTop: 35 }}>
				We are starting off with the bookworm collection and if we reach 100% we will begin working on the homesteader collection. All bookworm holders will have presale access to the
				homesteader collection.
			</p>
			<div className='roadmap-step'>
				<p className='roadmap-percent'>25%</p>
				<ul>
					<li className='space-list'>All-inclusive remote tropical vacation for one random wallet address</li>
				</ul>
			</div>
			<div className='roadmap-step'>
				<p className='roadmap-percent'>50%</p>
				<ul>
					<li className='space-list'>All-inclusive remote tropical vacation for one random wallet address</li>
					<li className='space-list'>Airdrop Mythic NFT</li>
				</ul>
			</div>
			<div className='roadmap-step'>
				<p className='roadmap-percent'>75%</p>
				<ul>
					<li className='space-list'>All-inclusive remote tropical vacation for one random wallet address</li>
					<li className='space-list'>Donating $20,000 worth of books to an illiteracy program</li>
				</ul>
			</div>
			<div className='roadmap-step'>
				<p className='roadmap-percent'>100%</p>
				<ul>
					<li className='space-list'>All-inclusive remote tropical vacation for one random wallet address</li>
					<li className='space-list'>Airdrop Mythic NFT</li>
				</ul>
			</div>
		</div>
	);
}
