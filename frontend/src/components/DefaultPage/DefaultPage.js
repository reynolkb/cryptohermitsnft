import React from 'react';
import { useNavigate } from 'react-router-dom';
import './defaultpage.css';
import logo from '../../assets/Crypto-Hermits-Logo-2-Small.png';
import HeaderLink from '../HeaderLink/HeaderLink';
import Footer from '../Footer/Footer';
import MobileMenu from '../MobileMenu';

export default function DefaultPage(props) {
	const navigate = useNavigate();
	return (
		<div className='default-layout'>
			{/* <div className='default-background-wrapper'>
				<div className='header-gradient' />
				<div className='center-image' alt='CryptoHermits Logo' />
				<div className='footer-gradient' />
			</div> */}
			<div className='content-wrapper'>
				<img src={logo} className='top-left-logo' alt='logo' onClick={() => navigate('/')} />
				<HeaderLink />
				<MobileMenu />
				{/* DefaultPage is set as root element of each page, so all children of page are passed to DefaultPage component as "children" property of "props" object. React supports this function as default. */}
				<div className='child-wrapper'>{props.children}</div>
				<Footer />
			</div>
		</div>
	);
}
