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
			<p className='text-normal-black para-about'>Our presale is opening Wednesday, January 12th at 6pm ET. Please explore our site in the meantime.</p>
			<img className='bookworm-gif' src='https://media.giphy.com/media/GBbJOa0QP6HEBK2WXW/giphy.gif' alt='gif' />
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
