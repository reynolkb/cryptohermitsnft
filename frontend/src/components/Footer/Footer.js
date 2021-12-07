import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTwitter, faDiscord } from '@fortawesome/free-brands-svg-icons';

import './Footer.css';

export default function Footer(props) {
	function openTwitter() {
		window.open('https://twitter.com/cryptohermits', '_blank');
	}

	function openDiscord() {
		window.open('https://discord.gg/kZcUJk4XTM', '_blank');
	}

	return (
		<footer id='footer'>
			<div className='footer-wrapper'>
				<p className='footer-text'>&copy; 2021 BlockBot LLC</p>
				<br></br>
				<p>
					<FontAwesomeIcon className='social-hover' icon={faTwitter} style={{ marginRight: 16 }} onClick={openTwitter} />
					<FontAwesomeIcon className='social-hover' icon={faDiscord} onClick={openDiscord} />
				</p>
			</div>
		</footer>
	);
}
