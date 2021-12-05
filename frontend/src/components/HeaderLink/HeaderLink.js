import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

import './headerlink.css';

const navItems = [
	{ title: 'Home', link: '/' },
	{ title: 'Mint', link: '/mint-not-active' },
	{ title: 'About', link: '/about' },
	{ title: 'Rarity', link: '/rarity' },
	{ title: 'RoadMap', link: '/roadmap' },
	{ title: 'Team', link: '/team' },
	{ title: 'FAQ', link: '/faq' },
	{ title: 'Connect', link: '/connect' },
];

export default function HeaderLink(props) {
	const navigate = useNavigate();
	const location = useLocation();
	const activeMenu = location.pathname;
	return (
		<div className='header-link-wrapper'>
			<ul className='header-link-ul'>
				{navItems.map((item, index) => (
					<li key={`navitem-${index}`} onClick={() => navigate(item.link)}>
						{item.title}
						{item.link === activeMenu && <div className='header-link-bottom' />}
					</li>
				))}
			</ul>
		</div>
	);
}
