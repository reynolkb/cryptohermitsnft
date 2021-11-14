import React, { Component } from 'react';
import { Link } from 'react-router-dom';
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
					<HashLink smooth to={'#Home'}>
						<img src={logo} className='navbar-logo' alt='CryptoHermits Logo' />
					</HashLink>
					<div className='menu-icon' onClick={this.handleClick}>
						{/* if it's clicked, change menu icon into X, if it's not then be the bars */}
						{/* in other words, if you click the mobile nav bar then open and set icon to X */}
						<i className={this.state.clicked ? 'fas fa-times' : 'fas fa-bars'}></i>
					</div>
					<ul className={this.state.clicked ? 'nav-menu active' : 'nav-menu'}>
						<HashLink smooth to={'#Home'} className='nav-links' onClick={this.handleClick}>
							Home
						</HashLink>
						<Link to='/mint' className='nav-links' onClick={this.handleClick}>
							Mint NFT
						</Link>
						<HashLink smooth to={'#About'} className='nav-links' onClick={this.handleClick}>
							About
						</HashLink>
						<HashLink smooth to={'#Roadmap'} className='nav-links' onClick={this.handleClick}>
							Roadmap
						</HashLink>
						<HashLink smooth to={'#Team'} className='nav-links' onClick={this.handleClick}>
							Team
						</HashLink>
						<HashLink smooth to={'#FAQS'} className='nav-links' onClick={this.handleClick}>
							FAQS
						</HashLink>
						<HashLink smooth to={'#Connect'} className='nav-links' onClick={this.handleClick}>
							Connect
						</HashLink>
					</ul>
				</nav>
			</header>
		);
	}
}

export default Navbar;
