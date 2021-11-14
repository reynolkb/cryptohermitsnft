import React, { Component } from 'react';
import './Roadmap.css';

class Roadmap extends Component {
	render() {
		return (
			<div className='section' id='Roadmap'>
				<h1>Roadmap</h1>
				<br></br>
				<p>
					We are starting off with the bookworm
					collection and if we reach 100% we will
					begin working on the homesteader
					collection.
				</p>
				<br></br>
				<br></br>
				<h2>25%</h2>
				<p>Airdrop</p>
				<br></br>
				<br></br>
				<h2>50%</h2>
				<p>Donating $20,000 to an illiteracy program</p>
				<br></br>
				<br></br>
				<h2>75%</h2>
				<p>
					Merch - reading lights, bookmarks, lava
					lamps, blankets, mugs, teas
				</p>
				<br></br>
				<br></br>
				<h2>100%</h2>
				<p>
					Liquidity pool. All inclusive tropical
					vacation
				</p>
			</div>
		);
	}
}

export default Roadmap;
