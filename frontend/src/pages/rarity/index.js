import React from 'react'

import DefaultPage from '../../components/DefaultPage/DefaultPage'
import rarityImage1 from '../../assets/rarity-item1.png';
import rarityImage2 from '../../assets/rarity-item2.png';
import rarityImage3 from '../../assets/rarity-item3.png';
import rarityImage4 from '../../assets/rarity-item4.png';
import rarityImage5 from '../../assets/rarity-item5.png';
import rarityImage6 from '../../assets/rarity-item6.png';
import rarityImage7 from '../../assets/rarity-item7.png';
import './rarity.css';

export default function Connect(props) {
  const items = [
    {title: 'Common', color: '#6E6E6E', image: rarityImage1},
    {title: 'Uncommon', color: '#737531', image: rarityImage2},
    {title: 'Rare', color: '#3477B9', image: rarityImage3},
    {title: 'Epic', color: '#9546A4', image: rarityImage4},
    {title: 'Legendary', color: '#A75B19', image: rarityImage5},
    {title: 'Exotic', color: '#268A8F', image: rarityImage6},
    {title: 'Mythic', color: '#976F01', image: rarityImage7}
  ]
  return (
    <DefaultPage>
      {/* <div className="rarity-custom-backend" /> */}
      <div className="page-rarity">
        <p className="text-magento-border" style={{ marginTop: '2vh' }}>Rarity</p>
        <p className="text-normal-black" style={{ marginTop: 20, maxWidth: 970 }}>
          Each Bookworm NFT has a rarity ranging from common to mythic. 
          The color of the book on the NFT corresponds with the rarity level. Below are some examples of NFTs you could get.
        </p>
        <div className="rarity-wrapper">
          {items.map((item, index) => 
            <div className="rarity-item" key={`rarity-${index}`}>
              <img className="rarity-image" src={item.image} alt={item} />
              <div className="rarity-text" style={{ color: item.color }}>{item.title}</div>
            </div>
          )}
        </div>
      </div>
    </DefaultPage>
  )
}