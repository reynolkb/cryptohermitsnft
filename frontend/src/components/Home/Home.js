import React, { Component } from 'react';
import './Home.css';
import coverPhoto from './desktop.jpeg';
import coverPhotoMobile from './mobile.jpeg';
import About from '../About/About';
import Roadmap from '../Roadmap/Roadmap';
import Team from '../Team/Team';
import FAQS from '../FAQS/FAQS';
import Connect from '../Connect/Connect';
import Navbar from '../Navbar/Navbar';

class Home extends Component {
	render() {
		return (
			<div>
				<Navbar />
				<div id='Home'>
					<img src={coverPhoto} className='coverPhoto' alt='CryptoHermits Logo' />
					<img src={coverPhotoMobile} className='coverPhotoMobile' alt='CryptoHermits Logo Mobile' />
				</div>
				<About />
				<hr className='line-break' />
				<Roadmap />
				<hr className='line-break' />
				<Team />
				<hr className='line-break' />
				<FAQS />
				<hr className='line-break' />
				<Connect />
				<hr className='line-break' />
				<br></br>
				<br></br>
				<br></br>
				<br></br>
				<br></br>
			</div>
		);
	}
}

export default Home;
