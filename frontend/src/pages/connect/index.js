import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTwitter, faDiscord } from '@fortawesome/free-brands-svg-icons';

import './connect.css';

export default function Connect(props) {
	function openTwitter() {
		window.open('https://twitter.com/cryptohermits', '_blank');
	}

	function openDiscord() {
		window.open('https://discord.gg/kZcUJk4XTM', '_blank');
	}

	return (
		<div className='page-mint'>
			<p className='text-magento-border'>Connect</p>
			<p className='text-normal-black para-connect'>
				Let’s link on Twitter and connect with some new friends on Discord. Everyone is welcome! Only requirement is to be your true self and capable of regulating your emotions. We all don’t
				need to think alike to be friends! The world is beautiful because we are all different. *Also, we aren't keeping score, but there are bonus points if you have a rad conspiracy theory.
			</p>
			<p className='para-connect-icons'>
				<FontAwesomeIcon icon={faTwitter} className='connect-fa-twitter' color='#1D9BEF' onClick={openTwitter} />
				<FontAwesomeIcon icon={faDiscord} className='connect-fa-discord' color='#5766F2' onClick={openDiscord} />
			</p>
		</div>
	);
}
