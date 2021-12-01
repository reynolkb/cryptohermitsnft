import React, { Component } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTwitter, faDiscord } from '@fortawesome/free-brands-svg-icons';

import './Footer.css';

class Footer extends Component {
	render() {
		return (
			<footer id='footer'>
				<div className='footer-wrapper'>
					<p className='footer-text'>
						Copyright 2021. All rights reserved. <span style={{ textDecoration: 'underline' }}>cryptohermitsnft.com</span>
					</p>
					<br></br>
					<p>
						<FontAwesomeIcon icon={faTwitter} style={{ marginRight: 16 }} />
						<FontAwesomeIcon icon={faDiscord} />
					</p>
				</div>
			</footer>
		);
	}
}

export default Footer;
