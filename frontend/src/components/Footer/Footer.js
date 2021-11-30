import React, { Component } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faTwitter, faDiscord } from '@fortawesome/free-brands-svg-icons'

import './Footer.css';

class Footer extends Component {
	render() {
		return (
			<div id='Footer'>
				<p className="footer-text">Copyright 2021. All rights reserved. <span style={{ textDecoration: 'underline' }}>cryptohermitsnft.com</span></p>
				<br></br>
				<p>
					<FontAwesomeIcon icon={faTwitter} style={{ marginRight: 16 }} />
					<FontAwesomeIcon icon={faDiscord} />
				</p>
				<br></br>
			</div>
		);
	}
}

export default Footer;
