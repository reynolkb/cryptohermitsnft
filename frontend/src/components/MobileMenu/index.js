import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBars, faTimes } from '@fortawesome/free-solid-svg-icons';
import { connect } from 'react-redux';

import './mobilemenu.css';

const navItems = [
	{ title: 'Home', link: '/' },
	{ title: 'Bookworms', link: '/bookworms' },
	{ title: 'Mint', link: '/mint-not-active' },
	{ title: 'About', link: '/about' },
	{ title: 'RoadMap', link: '/roadmap' },
	{ title: 'Team', link: '/team' },
	{ title: 'FAQ', link: '/faq' },
	{ title: 'Connect', link: '/connect' },
];

const MobileMenu = (props) => {
	const navigate = useNavigate();
	const location = useLocation();
	const activeMenu = location.pathname;
	// const [openMenu, setOpenMenu] = useState(false);

	function openMenu() {
		props.dispatch({ type: 'true' });
		document.getElementById('mobile-bars').classList.add('hide-mobile-bars');
		// var mobile = document.getElementById('mobile-bars');
		// console.log(mobile.classList);
	}

	function closeMenu() {
		props.dispatch({ type: 'false' });
		document.getElementById('mobile-bars').classList.remove('hide-mobile-bars');
	}

	function clickNavItemLink(item) {
		navigate(item.link);

		props.dispatch({ type: 'false' });
		document.getElementById('mobile-bars').classList.remove('hide-mobile-bars');
	}

	return (
		<div className='mobile-menu'>
			<FontAwesomeIcon icon={faBars} className='mobile-menu-opener' id='mobile-bars' color='#FFF' onClick={() => openMenu()} />
			{props.openMenuStatus && (
				<div className='mobile-menu-wrapper'>
					<FontAwesomeIcon icon={faTimes} className='mobile-menu-closer' color='#FFF' onClick={() => closeMenu()} />
					<ul className='mobile-link-ul'>
						{navItems.map((item, index) => (
							<li key={`navitem-${index}`} onClick={() => clickNavItemLink(item)}>
								{item.link === activeMenu && <div className='mobile-link-left' />}
								{item.title}
							</li>
						))}
					</ul>
				</div>
			)}
		</div>
	);
};

const mapStateToProps = (state) => ({
	openMenuStatus: state.openMenuStatus,
});

export default connect(mapStateToProps)(MobileMenu);
