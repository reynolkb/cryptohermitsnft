import React, { Component } from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
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

class App extends Component {
	render() {
		return (
			<BrowserRouter>
				<div className='App'>
					<ScrollToTop />
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
					{/* <Footer /> */}
				</div>
			</BrowserRouter>
		);
	}
}

export default App;
