import React, { Component } from 'react';
import { HashRouter, Route, Routes } from 'react-router-dom';
import './App.css';
import ScrollToTop from './util/ScrollToTop';
import Home from './components/Home/Home';
import Minter from './components/Minter/Minter';
import Footer from './components/Footer/Footer';

class App extends Component {
	render() {
		return (
			<HashRouter>
				<div className='App'>
					<ScrollToTop />
					<Routes>
						<Route path='/' element={<Home />} />
						<Route path='/mint' element={<Minter />} />
					</Routes>
					<Footer />
				</div>
			</HashRouter>
		);
	}
}

export default App;
