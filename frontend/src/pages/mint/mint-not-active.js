import React from 'react';

import './mint-not-active.css';
import { connect } from 'react-redux';

const MintNotActive = (props) => {
	function exploreButtonClicked() {
		props.dispatch({ type: 'true' });
		document.getElementById('mobile-bars').classList.add('hide-mobile-bars');
	}

	return (
		<div className='page-mint'>
			<p className='text-magento-border'>Mint</p>
			<p className='text-normal-black para-about'>
				Our presale begins Wednesday, January 12th at 6pm ET. Public sale begins Friday, January 14th at 6pm ET. Each wallet can mint up to 5 NFTs. If your wallet address is whitelisted you
				can mint 5 NFTs during the presale and 5 NFTs during the public sale for a total of 10 NFTs.
			</p>
			<img className='bookworm-gif' src='https://media.giphy.com/media/iBcPKkUkxndjiQg9Oy/giphy.gif' alt='gif' />
			<button className='btn-black explore' style={{ marginTop: 40 }} onClick={() => exploreButtonClicked()}>
				EXPLORE
			</button>
		</div>
	);
};

const mapStateToProps = (state) => ({
	openMenuStatus: state.openMenuStatus,
});

export default connect(mapStateToProps)(MintNotActive);
