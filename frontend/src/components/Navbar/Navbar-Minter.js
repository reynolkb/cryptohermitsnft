import React, { Component } from 'react';
import { HashLink } from 'react-router-hash-link';
import './Navbar.css';
import logo from './Crypto-Hermits-Logo-2-Small.png';

class Navbar extends Component {
	state = { clicked: false };

	handleClick = () => {
		// whenver you click, change clicked state to opposite
		this.setState({ clicked: !this.state.clicked });
	};

	render() {
		return (
			<header className='parent-nav'>
				<nav className='NavbarItems'>
					<HashLink smooth to={'/#Home'}>
						<img src={logo} className='navbar-logo' alt='CryptoHermits Logo' />
					</HashLink>
					<HashLink className='menu-icon' smooth to={'/#Home'}>
						{/* if it's clicked, change menu icon into X, if it's not then be the bars */}
						{/* in other words, if you click the mobile nav bar then open and set icon to X */}
						<i className='fas fa-arrow-left'></i>
					</HashLink>
				</nav>
			</header>
		);
	}
}

export default Navbar;
