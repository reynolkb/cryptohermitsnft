import React from 'react';
import { useNavigate } from 'react-router-dom';
import DefaultPage from '../../components/DefaultPage/DefaultPage';

import './home.css';

export default function Home(props) {
	const navigate = useNavigate();
	return (
		<DefaultPage>
			<div className='page-home center-image'>
				<p className='text-magento-noborder'>Crypto</p>
				<p className='text-cyan'>Hermits</p>
				<p className='text-normal-black para-home'>
					Join the revolution of bookworms, self sufficient homesteaders, homeschoolers, fighters of free speech and leaders of ethical sustainable living.
				</p>
				<button className='btn-black' style={{ marginTop: 40 }} onClick={() => navigate('/about')}>
					ENTER
				</button>
				<br></br>
				<br></br>
			</div>
		</DefaultPage>
	);
}
