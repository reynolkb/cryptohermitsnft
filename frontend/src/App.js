import React from 'react';
import { useNavigate, Route, Routes } from 'react-router-dom';
import './App.css';
// import Home from './components/Home/Home';
import Home from './pages/home';
import About from './pages/about';
import Team from './pages/team';
import Connect from './pages/connect';
import Mint from './pages/mint/index';
import MintNotActive from './pages/mint/mint-not-active';
import Rarity from './pages/rarity';
import Faq from './pages/faq';
import RoadMap from './pages/roadmap';
// import Minter from './components/Minter/Minter';
import HeaderLink from './components/HeaderLink/HeaderLink';
import Footer from './components/Footer/Footer';
import MobileMenu from './components/MobileMenu';
import logo from './assets/Crypto-Hermits-Logo-2-Small.png';

// import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
// import { faArrowUp } from '@fortawesome/free-solid-svg-icons';

export default function App(props) {
	const navigate = useNavigate();

	// const [showButton, setShowButton] = useState(false);

	// const updateScrollState = (e) => {
	// 	const bottom = e.target.scrollHeight - e.target.scrollTop === e.target.clientHeight;
	// 	if (bottom) {
	// 		setShowButton(true);
	// 	} else {
	// 		setShowButton(false);
	// 	}
	// };

	// // This function will scroll the window to the top
	// const scrollToTop = () => {
	// 	document.getElementById('app').scrollTo({
	// 		top: 0,
	// 		behavior: 'smooth', // for smoothly scrolling
	// 	});
	// };

	return (
		<div className='App' id='app'>
			{/* <div className='App' id='app' onScroll={updateScrollState}> */}
			<div className='site-wrapper'>
				<nav className='navbar'>
					<div className='logo-wrapper'>
						<img className='logo' src={logo} alt='logo' onClick={() => navigate('/')} />
					</div>

					<HeaderLink />
				</nav>
				<nav className='navbar-mobile'>
					<div className='left-container-mobile'></div>
					<div className='logo-wrapper'>
						<img className='logo' src={logo} alt='logo' onClick={() => navigate('/')} />
					</div>
					<MobileMenu />
				</nav>
				<div className='default-layout'>
					<Routes>
						<Route path='/' element={<Home />} />
						{/* <Route path='/about' element={<About />} /> */}
						<Route path='/team' element={<Team />} />
						<Route path='/connect' element={<Connect />} />
						<Route path='/mint-not-active' element={<MintNotActive />} />
						<Route path='/mint' element={<Mint />} />
						<Route path='/rarity' element={<Rarity />} />
						<Route path='/faq' element={<Faq />} />
						<Route path='/roadmap' element={<RoadMap />} />
					</Routes>
				</div>
			</div>
			{/* {showButton && <FontAwesomeIcon icon={faArrowUp} className='back-to-top' color='#FFF' onClick={() => scrollToTop()} />} */}
			<Footer />
		</div>
	);
}
