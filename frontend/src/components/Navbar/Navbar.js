import React, { Component } from 'react';
import { BrowserRouter, Link, Route, Routes } from 'react-router-dom';
import './Navbar.css';
import logo from './Crypto-Hermits-Logo-2-Small.png';
import Home from '../Home/Home';
import Minter from '../Minter/Minter';

class Navbar extends Component {
	state = { clicked: false };

	handleClick = () => {
		// whenver you click, change clicked state to opposite
		this.setState({ clicked: !this.state.clicked });
	};

	render() {
		return (
			<BrowserRouter>
				<div>
					<header className='parent-nav'>
						<nav className='NavbarItems'>
							<a href='/#Home'>
								<img src={logo} className='navbar-logo' alt='CryptoHermits Logo' />
							</a>
							<div className='menu-icon' onClick={this.handleClick}>
								{/* if it's clicked, change menu icon into X, if it's not then be the bars */}
								{/* in other words, if you click the mobile nav bar then open and set icon to X */}
								<i className={this.state.clicked ? 'fas fa-times' : 'fas fa-bars'}></i>
							</div>
							<ul className={this.state.clicked ? 'nav-menu active' : 'nav-menu'}>
								<a href='/#Home' className='nav-links' onClick={this.handleClick}>
									Home
								</a>
								<Link to='/mint' className='nav-links' onClick={this.handleClick}>
									Mint NFT
								</Link>
								<a href='/#About' className='nav-links' onClick={this.handleClick}>
									About
								</a>
								<a href='/#Roadmap' className='nav-links' onClick={this.handleClick}>
									Roadmap
								</a>
								<a href='/#Team' className='nav-links' onClick={this.handleClick}>
									Team
								</a>
								<a href='/#Connect' className='nav-links' onClick={this.handleClick}>
									Connect
								</a>
							</ul>
						</nav>
					</header>
					<Routes>
						<Route path='/' element={<Home />} />
						<Route path='/mint' element={<Minter />} />
					</Routes>
				</div>
			</BrowserRouter>
		);
	}
}

export default Navbar;
