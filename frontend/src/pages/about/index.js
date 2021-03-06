import React from 'react';

import './about.css';
import { connect } from 'react-redux';

const About = (props) => {
	return (
		<div className='page-mint'>
			<p className='text-magento-border'>About</p>
			<p className='text-normal-black para-about'>
				After decades of down time and solitude, the CryptoHermits are ready to make some noise. Free thinking has no political party. We heed to grandma's telltale wisdom of never judging a
				book by its cover. We are modern day rebels who are overlooked and without credit. Join the revolution of bookworms, self-sufficient homesteaders, fighters of free speech and leaders
				of ethical, sustainable living. Collect art and make friends with those who are just as intentional (and probably fed up) as you. We just want to be left alone and leave others alone.
				Let's find peace in solitary, together.
			</p>
		</div>
	);
};

const mapStateToProps = (state) => ({
	openMenuStatus: state.openMenuStatus,
});

export default connect(mapStateToProps)(About);
