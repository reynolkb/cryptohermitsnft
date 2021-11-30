import React from 'react';
import DefaultPage from '../../components/DefaultPage/DefaultPage';

import './roadmap.css';

export default function RoadMap(props) {
	return (
		<DefaultPage>
			<div className='page-mint'>
				<p className='text-magento-border' style={{ marginTop: '2vh' }}>
					Roadmap
				</p>
				{/* <p className="text-normal-black" style={{ maxWidth: 542, marginTop: 35 }}> */}
				<p className='text-normal-black para-team' style={{ maxWidth: 542, marginTop: 35 }}>
					We are starting off with the bookworm collection and if we reach 100% we will begin working on the homesteader collection. All bookworm holders have pre-sale access to the
					homesteader collection.
				</p>
				<div className='roadmap-step'>
					<p className='roadmap-percent'>25%</p>
					<p>All inclusive tropical vacation for one random wallet address</p>
				</div>
				<div className='roadmap-step'>
					<p className='roadmap-percent'>50%</p>
					<p>All inclusive tropical vacation for one random wallet address</p>
					<p>Airdrop Mythic one of one NFT</p>
				</div>
				<div className='roadmap-step'>
					<p className='roadmap-percent'>75%</p>
					<p>All inclusive tropical vacation for one random wallet address</p>
					<p>Donating $20,000 worth of books to an illiteracy program</p>
				</div>
				<div className='roadmap-step'>
					<p className='roadmap-percent'>100%</p>
					<p>All inclusive tropical vacation for one random wallet address</p>
					<p>Airdrop Mythic one of one NFT</p>
				</div>
			</div>
		</DefaultPage>
	);
}
