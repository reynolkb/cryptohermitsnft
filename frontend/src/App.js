import React from 'react';
import { useNavigate, Route, Routes } from 'react-router-dom';
import './App.css';
import ScrollToTop from './util/ScrollToTop';
// import Home from './components/Home/Home';
import Home from './pages/home';
import About from './pages/about';
import Team from './pages/team';
import Connect from './pages/connect';
import Mint from './pages/mint';
import Rarity from './pages/rarity';
import Faq from './pages/faq';
import RoadMap from './pages/roadmap';
// import Minter from './components/Minter/Minter';
import HeaderLink from './components/HeaderLink/HeaderLink';
import Footer from './components/Footer/Footer';
import MobileMenu from './components/MobileMenu';
import logo from './assets/Crypto-Hermits-Logo-2-Small.png';

export default function App(props) {
	const navigate = useNavigate();

	return (
		<div className='App'>
			<div className='site-wrapper'>
				<ScrollToTop />
				<img src={logo} className='top-left-logo' alt='logo' onClick={() => navigate('/')} />
				<HeaderLink />
				<MobileMenu />
				<div className='default-layout'>
					<Routes>
						<Route path='/' element={<Home />} />
						<Route path='/about' element={<About />} />
						<Route path='/team' element={<Team />} />
						<Route path='/connect' element={<Connect />} />
						<Route path='/mint' element={<Mint />} />
						<Route path='/rarity' element={<Rarity />} />
						<Route path='/faq' element={<Faq />} />
						<Route path='/roadmap' element={<RoadMap />} />
					</Routes>
				</div>
			</div>
			<Footer />
		</div>
	);
}
