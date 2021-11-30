import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBars, faTimes } from '@fortawesome/free-solid-svg-icons';

import './mobilemenu.css';

const navItems = [
	{ title: 'Home', link: '/' },
	{ title: 'Mint NFT', link: '/mint' },
	{ title: 'About', link: '/about' },
	{ title: 'Rarity', link: '/rarity' },
	{ title: 'RoadMap', link: '/roadmap' },
	{ title: 'Team', link: '/team' },
	{ title: "FAQ's", link: '/faq' },
	{ title: 'Connect', link: '/connect' },
];

export default function MobileMenu() {
	const navigate = useNavigate();
	const location = useLocation();
	const activeMenu = location.pathname;
	const [openMenu, setOpenMenu] = useState(false);

	function handleMobileBarClick(status) {
		setOpenMenu(status);

		if (status) {
			document.getElementById('mobile-bars').classList.add('hide-mobile-bars');
			// var mobile = document.getElementById('mobile-bars');
			// console.log(mobile.classList);
		} else {
			document.getElementById('mobile-bars').classList.remove('hide-mobile-bars');
		}
	}

	return (
		<div className='mobile-menu'>
			<FontAwesomeIcon icon={faBars} className='mobile-menu-opener' id='mobile-bars' color='#FFF' onClick={() => handleMobileBarClick(true)} />
			{openMenu && (
				<div className='mobile-menu-wrapper'>
					<FontAwesomeIcon icon={faTimes} className='mobile-menu-closer' color='#FFF' onClick={() => handleMobileBarClick(false)} />
					<ul className='mobile-link-ul'>
						{navItems.map((item, index) => (
							<li key={`navitem-${index}`} onClick={() => navigate(item.link)}>
								{item.link === activeMenu && <div className='mobile-link-left' />}
								{item.title}
							</li>
						))}
					</ul>
				</div>
			)}
		</div>
	);
}
