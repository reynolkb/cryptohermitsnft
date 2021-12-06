import React from 'react';
import { useNavigate } from 'react-router-dom';

import './home.css';

export default function Home(props) {
	const navigate = useNavigate();
	return (
		<div className='page-home'>
			<div>
				<p className='text-magento-noborder mobile-header-text'>Crypto</p>
				<p className='text-cyan mobile-header-text'>Hermits</p>
			</div>
			<img className='bookworm-gif' src='https://media.giphy.com/media/iBcPKkUkxndjiQg9Oy/giphy.gif' alt='gif' />
			{/* <p className='text-normal-black para-home'> */}
			<button className='btn-black' style={{ marginTop: 40 }} onClick={() => navigate('/bookworms')}>
				BOOKWORMS
			</button>
		</div>
	);
}
