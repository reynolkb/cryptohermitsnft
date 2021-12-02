import React from 'react';
import { useNavigate } from 'react-router-dom';
import coverPhotoTablet from '../../assets/desktop.jpeg';
import coverPhotoMobile from '../../assets/mobile.jpeg';

import './home.css';

export default function Home(props) {
	const navigate = useNavigate();
	return (
		<div className='page-home'>
			<div className='cover-photo-container'>
				<img src={coverPhotoTablet} className='cover-photo-tablet' alt='coverPhoto' />
				<img src={coverPhotoMobile} className='cover-photo-mobile' alt='coverPhoto' />
				<div className='centered'>
					<p className='text-magento-noborder mobile-header-text'>Crypto</p>
					<p className='text-cyan mobile-header-text'>Hermits</p>
					{/* <p className='text-normal-black para-home'> */}
					<button className='btn-black' style={{ marginTop: 40 }} onClick={() => navigate('/about')}>
						JOIN THE REVOLUTION
					</button>
				</div>
			</div>
		</div>
	);
}
