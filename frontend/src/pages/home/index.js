import React from 'react';
import { useNavigate } from 'react-router-dom';
import coverPhotoTablet from '../../assets/desktop.jpeg';
import coverPhotoMobile from '../../assets/mobile.jpeg';

import './home.css';

export default function Home(props) {
	const navigate = useNavigate();
	return (
		<div className='default-layout'>
			<div className='content-wrapper'>
				<div className='page-home center-image'>
					<img src={coverPhotoTablet} className='cover-photo-tablet' alt='coverPhoto' />
					<img src={coverPhotoMobile} className='cover-photo-mobile' alt='coverPhoto' />
					<p className='text-magento-noborder mobile-header-text'>Crypto</p>
					<p className='text-cyan mobile-header-text'>Hermits</p>
					<p className='text-normal-black para-home'>
						Join the revolution of bookworms, self sufficient homesteaders, homeschoolers, fighters of free speech and leaders of ethical sustainable living.
					</p>
					<button className='btn-black' style={{ marginTop: 40 }} onClick={() => navigate('/about')}>
						ENTER
					</button>
					<br></br>
					<br></br>
				</div>
			</div>
		</div>
	);
}
