import React, { Component } from 'react';
import './Connect.css';

class Connect extends Component {
	render() {
		return (
			<div className='section' id='Connect'>
				<h1>Connect</h1>
				<br></br>
				<br></br>
				<i className='fab fa-twitter fa-2x center' id='twitter'></i>
				<i className='fab fa-discord fa-2x center' id='discord'></i>
				<br></br>
				<br></br>
				<br></br>
				<p>
					Chat with us on Twitter and connect with friends on Discord who are just as intentional (and fed up) as you. We just want to be left alone and leave others alone. Let's find peace
					in solitary, together.
				</p>
			</div>
		);
	}
}

export default Connect;
