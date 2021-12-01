(this["webpackJsonpnft-minter"]=this["webpackJsonpnft-minter"]||[]).push([[0],{265:function(e,t,n){},266:function(e,t,n){},267:function(e,t,n){},269:function(e,t,n){},275:function(e,t,n){},277:function(e,t,n){},279:function(e,t,n){},283:function(e){e.exports=JSON.parse('[{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"},{"internalType":"string","name":"_initBaseURI","type":"string"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"_newTokenId","type":"uint256"}],"name":"printNewTokenId","type":"event"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"baseExtension","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"baseURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"cost","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"maxMintAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"maxSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_mintAmount","type":"uint256"}],"name":"mint","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bool","name":"_state","type":"bool"}],"name":"pause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"_newBaseExtension","type":"string"}],"name":"setBaseExtension","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"_newBaseURI","type":"string"}],"name":"setBaseURI","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_newCost","type":"uint256"}],"name":"setCost","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_newmaxMintAmount","type":"uint256"}],"name":"setmaxMintAmount","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"index","type":"uint256"}],"name":"tokenByIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"tokenOfOwnerByIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_owner","type":"address"}],"name":"walletOfOwner","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"withdraw","outputs":[],"stateMutability":"payable","type":"function"}]')},294:function(e,t){},315:function(e,t){},317:function(e,t){},394:function(e,t){},396:function(e,t){},405:function(e,t){},407:function(e,t){},432:function(e,t){},437:function(e,t){},439:function(e,t){},446:function(e,t){},459:function(e,t){},521:function(e,t){},557:function(e,t,n){},558:function(e,t,n){},559:function(e,t,n){},560:function(e,t,n){},561:function(e,t,n){},562:function(e,t,n){},563:function(e,t,n){"use strict";n.r(t);var a=n(1),s=n.n(a),r=n(94),i=n.n(r),o=(n(265),n(11));n(266);function c(){var e=Object(o.e)().pathname;return Object(a.useEffect)((function(){window.scrollTo(0,0)}),[e]),null}var l=n.p+"static/media/desktop.2043187a.jpeg",u=n.p+"static/media/mobile.9191d20d.jpeg",p=(n(267),n(0));function d(e){var t=Object(o.f)();return Object(p.jsxs)("div",{className:"page-home center-image",children:[Object(p.jsx)("img",{src:l,className:"cover-photo-tablet",alt:"coverPhoto"}),Object(p.jsx)("img",{src:u,className:"cover-photo-mobile",alt:"coverPhoto"}),Object(p.jsx)("p",{className:"text-magento-noborder mobile-header-text",children:"Crypto"}),Object(p.jsx)("p",{className:"text-cyan mobile-header-text",children:"Hermits"}),Object(p.jsx)("p",{className:"text-normal-black para-home",children:"Join the revolution of bookworms, self sufficient homesteaders, homeschoolers, fighters of free speech and leaders of ethical sustainable living."}),Object(p.jsx)("button",{className:"btn-black",style:{marginTop:40},onClick:function(){return t("/about")},children:"ENTER"})]})}n(269);var m=n(70),b=Object(m.b)((function(e){return{openMenuStatus:e.openMenuStatus}}))((function(e){return Object(p.jsxs)("div",{className:"page-mint",children:[Object(p.jsx)("p",{className:"text-magento-border",style:{marginTop:"2vh"},children:"About Us"}),Object(p.jsx)("p",{className:"text-normal-black para-about",children:"After decades of down time and solitude, the CryptoHermits are ready to make some noise. Free thinking has no political party. We heed to grandma's telltale wisdom of never judging a book by its cover. We are modern day rebels who are overlooked and without credit. Join the revolution of bookworms, self-sufficient homesteaders, fighters of free speech and leaders of ethical, sustainable living. Collect art and make friends with those who are just as intentional (and probably fed up) as you. We just want to be left alone and leave others alone. Let's find peace in solitary, together."}),Object(p.jsx)("button",{className:"btn-black explore",style:{marginTop:40},onClick:function(){return e.dispatch({type:"true"}),void document.getElementById("mobile-bars").classList.add("hide-mobile-bars")},children:"EXPLORE"})]})}));n(275);function y(e){return Object(p.jsxs)("div",{className:"page-mint",children:[Object(p.jsx)("p",{className:"text-magento-border",style:{marginTop:"2vh"},children:"Team"}),Object(p.jsx)("p",{className:"text-title-black para-founder",children:"Founder"}),Object(p.jsx)("p",{className:"text-normal-black para-team",children:"We are a married couple whose aim is to stay anonymous. Thus proving who we are in terms of controversial societal categories like gender, race, and political affiliations do not matter. Our beliefs and character define us. The elites do not get to divide us unless we consent to prioritizing our differences compared to our similarities. We are all together on this beautiful planet; join the rebellion of hermits. This is the way."}),Object(p.jsx)("p",{className:"text-title-black para-artist",children:"Artist"}),Object(p.jsx)("p",{className:"text-normal-black para-artist-content",children:"Jeremy Webster"})]})}var j=n(22),h=n(71);n(277);function f(e){return Object(p.jsxs)("div",{className:"page-mint",children:[Object(p.jsx)("p",{className:"text-magento-border",style:{marginTop:"2vh"},children:"Connect"}),Object(p.jsx)("p",{className:"text-normal-black para-connect",children:"Let\u2019s link on Twitter and connect with some new friends on Discord. Everyone is welcome! Only requirement is to be your true self and capable of regulating your emotions. We all don\u2019t need to think alike to be friends! The world is beautiful because we are all different. *Also, we aren't keeping score, but there are bonus points if you have a rad conspiracy theory."}),Object(p.jsxs)("p",{className:"para-connect-icons",children:[Object(p.jsx)(j.a,{icon:h.b,className:"connect-fa-twitter",color:"#1E9BF0"}),Object(p.jsx)(j.a,{icon:h.a,className:"connect-fa-discord",color:"#404EED"})]})]})}var x=n(19),O=n.n(x),w=n(43),g=n(20),v=n(80);n(279);n(280).config();var k=n(283),T="0x7ca700F227a824c51913BEa8597708663A33e532",N=(0,n(141).createAlchemyWeb3)("https://eth-rinkeby.alchemyapi.io/v2/NGxwRcG2EtrikJ029J4wdMQ1cK6KxUnv"),M=function(){var e=Object(w.a)(O.a.mark((function e(){var t,n;return O.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(!window.ethereum){e.next=14;break}return e.prev=1,e.next=4,window.ethereum.request({method:"eth_requestAccounts"});case 4:return t=e.sent,n={status:"\ud83d\udc46\ud83c\udffd Click above to get your CryptoHermit NFT",address:t[0]},e.abrupt("return",n);case 9:return e.prev=9,e.t0=e.catch(1),e.abrupt("return",{address:"",status:"\ud83d\ude25 "+e.t0.message});case 12:e.next=15;break;case 14:return e.abrupt("return",{address:"",status:Object(p.jsx)("span",{children:Object(p.jsxs)("p",{children:[" ","\ud83e\udd8a"," ",Object(p.jsx)("a",{target:"_blank",rel:"noreferrer",href:"https://metamask.io/download.html",children:"You need to download MetaMask."})]})})});case 15:case"end":return e.stop()}}),e,null,[[1,9]])})));return function(){return e.apply(this,arguments)}}(),F=function(){var e=Object(w.a)(O.a.mark((function e(){var t;return O.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(!window.ethereum){e.next=17;break}return e.prev=1,e.next=4,window.ethereum.request({method:"eth_accounts"});case 4:if(!((t=e.sent).length>0)){e.next=9;break}return e.abrupt("return",{address:t[0],status:"\ud83d\udc46\ud83c\udffd Click above to get your CryptoHermit NFT"});case 9:return e.abrupt("return",{address:"",status:"\ud83e\udd8a Connect to Metamask using the top right button."});case 10:e.next=15;break;case 12:return e.prev=12,e.t0=e.catch(1),e.abrupt("return",{address:"",status:"\ud83d\ude25 "+e.t0.message});case 15:e.next=18;break;case 17:return e.abrupt("return",{address:"",status:Object(p.jsx)("span",{children:Object(p.jsxs)("p",{children:[" ","\ud83e\udd8a"," ",Object(p.jsx)("a",{target:"_blank",rel:"noreferrer",href:"https://metamask.io/download.html",children:"You need to download MetaMask."})]})})});case 18:case"end":return e.stop()}}),e,null,[[1,12]])})));return function(){return e.apply(this,arguments)}}(),A=function(){var e=Object(w.a)(O.a.mark((function e(t){var n,a,s;return O.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,new N.eth.Contract(k,T);case 2:return window.contract=e.sent,n=(n="0x48547bc59493d081e8f62944d526443d84fdc4d6"===window.ethereum.selectedAddress?0:.01*t).toString(),a={to:T,from:window.ethereum.selectedAddress,data:window.contract.methods.mint(t).encodeABI(),value:parseInt(N.utils.toWei(n,"ether")).toString(16)},e.prev=6,e.next=9,window.ethereum.request({method:"eth_sendTransaction",params:[a]});case 9:return s=e.sent,e.abrupt("return",{txHash:s,success:!0,status:"\u2705 Please keep this tab open until your transaction is complete."});case 13:return e.prev=13,e.t0=e.catch(6),e.abrupt("return",{success:!1,status:"\ud83d\ude25 Something went wrong: "+e.t0.message});case 16:case"end":return e.stop()}}),e,null,[[6,13]])})));return function(t){return e.apply(this,arguments)}}(),C="haXer22293",I=(0,n(141).createAlchemyWeb3)("https://eth-rinkeby.alchemyapi.io/v2/NGxwRcG2EtrikJ029J4wdMQ1cK6KxUnv");function E(e){var t=Object(a.useState)(""),n=Object(g.a)(t,2),s=n[0],r=n[1],i=Object(a.useState)("loading..."),o=Object(g.a)(i,2),c=o[0],l=o[1],u=Object(a.useState)("loading..."),d=Object(g.a)(u,2),m=d[0],b=d[1],y=Object(a.useState)(""),h=Object(g.a)(y,2),f=h[0],x=h[1],k=Object(a.useState)(""),T=Object(g.a)(k,2),N=T[0],E=T[1],B=Object(a.useState)(""),S=Object(g.a)(B,2),q=S[0],_=S[1],R=Object(a.useState)(""),W=Object(g.a)(R,2),H=W[0],L=W[1],J=Object(a.useRef)(),P=Object(a.useRef)();function U(){window.ethereum?window.ethereum.on("accountsChanged",(function(e){e.length>0?(r(e[0]),x("\ud83d\udc46\ud83c\udffd Click above to get your BitBird NFT")):(r(""),x("\ud83e\udd8a Connect to Metamask using the top right button."))})):(document.getElementById("mintButton").disabled=!0,x(Object(p.jsxs)("p",{children:[" ","\ud83e\udd8a"," ",Object(p.jsx)("a",{target:"_blank",rel:"noreferrer",href:"https://metamask.io/download.html",children:"You need to download MetaMask."})]})))}Object(a.useEffect)((function(){function e(){return(e=Object(w.a)(O.a.mark((function e(){var t,n,a;return O.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,F();case 2:return t=e.sent,n=t.address,a=t.status,r(n),x(a),U(),e.next=10,fetch("https://www.cryptohermitsnft.com/getTokensMinted",{method:"GET"});case 10:return J.current=e.sent,e.next=13,J.current.json();case 13:return J.current=e.sent,J.current=J.current.tokensMinted,l(J.current),e.next=18,fetch("https://www.cryptohermitsnft.com/getTotalTokens",{method:"GET"});case 18:return P.current=e.sent,e.next=21,P.current.json();case 21:P.current=e.sent,P.current=P.current.totalTokens,b(P.current);case 24:case"end":return e.stop()}}),e)})))).apply(this,arguments)}!function(){e.apply(this,arguments)}()}),[]);var Y=function(){var e=Object(w.a)(O.a.mark((function e(){var t;return O.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,M();case 2:t=e.sent,x(t.status),r(t.address);case 5:case"end":return e.stop()}}),e)})));return function(){return e.apply(this,arguments)}}();function G(e){return D.apply(this,arguments)}function D(){return(D=Object(w.a)(O.a.mark((function e(t){return O.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.abrupt("return",new Promise((function(e){setTimeout(e,t)})));case 1:case"end":return e.stop()}}),e)})))).apply(this,arguments)}function Q(e){return e.toString().replace(/\B(?=(\d{3})+(?!\d))/g,",")}var K=function(){var e=Object(w.a)(O.a.mark((function e(){var t,n,a,s,r,i,o,c,u,p,d,m;return O.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(E(" "),_(" "),L(" "),""!==(r=document.getElementById("mintAmount").value)){e.next=7;break}return alert("mint amount cannot be empty"),e.abrupt("return");case 7:if(!(r>3)){e.next=10;break}return alert("mint amount cannot be greater than 3"),e.abrupt("return");case 10:return document.getElementById("mintButton").innerHTML="loading Metamask...",e.next=13,A(r);case 13:if(s=e.sent,t=s.txHash,n=s.success,a=s.status,!n){e.next=24;break}document.getElementById("mintButton").innerHTML="pending transaction...",E("Check out your pending transaction on Etherscan in a new tab while you wait."),_("https://rinkeby.etherscan.io/tx/".concat(t)),L("Pending Transaction"),e.next=27;break;case 24:return document.getElementById("mintButton").innerHTML="Mint NFT",x(a),e.abrupt("return");case 27:x(a),i=0;case 29:if(!(i<175)){e.next=47;break}return e.next=32,I.eth.getTransactionReceipt(t);case 32:if(null!==(o=e.sent)){e.next=43;break}return e.next=36,G(5e3);case 36:return c=(c=5*(i+1)).toString(),console.log("".concat(c," seconds has passed for the pending transaction")),e.abrupt("continue",44);case 43:return e.abrupt("break",47);case 44:i++,e.next=29;break;case 47:if(console.log(o),!o.status){e.next=81;break}if(p=[],console.log(o.logs),!(o.logs.length<3)){e.next=67;break}return d=parseInt(o.logs[1].data,16),p.push(d),u=p.length-1,e.next=58,fetch("https://www.cryptohermitsnft.com/setTokensMinted/".concat(Q(p[u]),"/").concat(C),{method:"PUT"});case 58:return J=e.sent,e.next=61,J.json();case 61:J=e.sent,l(J.tokensMinted),E("Your transaction is completed, please view your NFT on Open Sea once the metadata is revealed. Your token id is ".concat(p,".")),L("Completed Transaction"),e.next=78;break;case 67:for(m=1;m<=o.logs.length;m+=2)d=parseInt(o.logs[m].data,16),p.push(d);return u=p.length-1,e.next=71,fetch("https://www.cryptohermitsnft.com/setTokensMinted/".concat(Q(p[u]),"/").concat(C),{method:"PUT"});case 71:return J=e.sent,e.next=74,J.json();case 74:J=e.sent,l(J.tokensMinted),E("Your transaction is completed, please view your NFTs on Open Sea once the metadata is revealed. Your token ids are ".concat(p,".")),L("Completed Transaction");case 78:document.getElementById("mintButton").innerHTML="Mint NFT",e.next=85;break;case 81:document.getElementById("transactionStatus").style.color="red",E("Please click the link below for the reason your transaction failed."),_("https://rinkeby.etherscan.io/tx/".concat(t)),L("Failed Transaction");case 85:document.getElementById("mintButton").innerHTML="Mint NFT";case 86:case"end":return e.stop()}}),e)})));return function(){return e.apply(this,arguments)}}();return Object(p.jsxs)("div",{className:"page-mint",children:[Object(p.jsx)("p",{className:"text-magento-border",style:{marginTop:"2vh"},children:"Mint Nft"}),Object(p.jsxs)("p",{className:"text-normal-black",style:{marginTop:30},children:["Tokens Minted ",c,"/",m]}),Object(p.jsx)("p",{className:"text-normal-black",style:{marginTop:30},children:"Get your random cryptohermit nft below, All nfts are 0.01 Eth!"}),Object(p.jsx)("p",{className:"text-normal-black",style:{marginTop:30},children:"Number of Nfts to mint (3 max per wallet)"}),Object(p.jsxs)("div",{className:"mint-select-wrapper",children:[Object(p.jsxs)("select",{name:"mintAmount",id:"mintAmount",className:"mint-amount",children:[Object(p.jsx)("option",{value:"1",children:"1"}),Object(p.jsx)("option",{value:"2",children:"2"}),Object(p.jsx)("option",{value:"3",children:"3"})]}),Object(p.jsx)(j.a,{icon:v.b,className:"mint-icon-down",onClick:function(){return document.getElementById("mintAmount").click()}})]}),Object(p.jsxs)("div",{className:"mint-button-wrapper",children:[Object(p.jsx)("button",{id:"walletButton",className:"btn-cyan mint-connect",onClick:Y,children:s.length>0?"Connected: "+String(s).substring(0,6)+"..."+String(s).substring(38):"Connect Wallet"})," ",Object(p.jsx)("br",{id:"button-separator"}),Object(p.jsx)("button",{id:"mintButton",className:"btn-magento",onClick:K,children:"MINT NFT"})]}),Object(p.jsx)("p",{id:"status",className:"text-normal-black",children:f}),Object(p.jsx)("br",{}),Object(p.jsx)("br",{}),Object(p.jsxs)("p",{id:"transactionStatus",className:"text-normal-black",children:[N,Object(p.jsx)("br",{}),Object(p.jsx)("a",{href:"".concat(q),target:"_blank",rel:"noreferrer",children:H})]})]})}I.eth.handleRevert=!0;var B=n.p+"static/media/rarity-item1.ee61c9e9.png",S=n.p+"static/media/rarity-item2.cbab8e30.png",q=n.p+"static/media/rarity-item3.a1d63472.png",_=n.p+"static/media/rarity-item4.fcc07954.png",R=n.p+"static/media/rarity-item5.91c7037c.png",W=n.p+"static/media/rarity-item6.3924b2e9.png",H=n.p+"static/media/rarity-item7.5407e39b.png";n(557);function L(e){var t=[{title:"Common",color:"#6E6E6E",image:B},{title:"Uncommon",color:"#737531",image:S},{title:"Rare",color:"#3477B9",image:q},{title:"Epic",color:"#9546A4",image:_},{title:"Legendary",color:"#A75B19",image:R},{title:"Exotic",color:"#268A8F",image:W},{title:"Mythic",color:"#976F01",image:H}];return Object(p.jsxs)("div",{className:"page-rarity",children:[Object(p.jsx)("p",{className:"text-magento-border",style:{marginTop:"2vh"},children:"Rarity"}),Object(p.jsx)("p",{className:"text-normal-black",style:{marginTop:20,maxWidth:970},children:"Each Bookworm NFT has a rarity ranging from common to mythic. The color of the book on the NFT corresponds with the rarity level. Below are some examples of NFTs you could get."}),Object(p.jsx)("div",{className:"rarity-wrapper",children:t.map((function(e,t){return Object(p.jsxs)("div",{className:"rarity-item",children:[Object(p.jsx)("img",{className:"rarity-image",src:e.image,alt:e}),Object(p.jsx)("div",{className:"rarity-text",style:{color:e.color},children:e.title})]},"rarity-".concat(t))}))})]})}var J=n(42),P=n(34);n(558);function U(e){var t=Object(a.useState)(!1),n=Object(g.a)(t,2),s=n[0],r=n[1],i=Object(a.useState)(!1),o=Object(g.a)(i,2),c=o[0],l=o[1],u=Object(a.useState)(!1),d=Object(g.a)(u,2),m=d[0],b=d[1],y=Object(a.useState)(!1),h=Object(g.a)(y,2),f=h[0],x=h[1],O=Object(a.useState)(!1),w=Object(g.a)(O,2),v=w[0],k=w[1];return Object(p.jsxs)("div",{className:"page-mint",children:[Object(p.jsx)("p",{className:"text-magento-border",style:{marginTop:"2vh"},children:"FAQ"}),Object(p.jsxs)("div",{className:"faq-text-group",children:[Object(p.jsxs)("div",{className:"faq-text-question",onClick:function(){return r((function(e){return!e}))},children:[Object(p.jsx)(j.a,{icon:s?P.a:P.b,className:"faq-text-plus"}),Object(p.jsx)("p",{className:"text-faq-black",children:"How do I download MetaMask and fund my MetaMask wallet?"})]}),s&&Object(p.jsxs)("ol",{className:"faq-text-answer",children:[Object(p.jsxs)("li",{className:"space-list",children:["You need to"," ",Object(p.jsx)("a",{href:"https://metamask.io/download",target:"_blank",rel:"noreferrer",children:"download MetaMask."})," "]}),Object(p.jsxs)("li",{className:"space-list",children:[Object(p.jsx)("a",{href:"https://www.coinbase.com/buy-ethereum",target:"_blank",rel:"noreferrer",children:"Buy Ethereum"})," ","from an exchange."," "]}),Object(p.jsxs)("li",{className:"space-list",children:[Object(p.jsx)("a",{href:"https://www.coinbase.com/learn/tips-and-tutorials/how-to-send-crypto",target:"_blank",rel:"noreferrer",children:"Transfer"})," ","it to your MetaMask Wallet."]})]}),Object(p.jsxs)("div",{className:"faq-text-question",onClick:function(){return l((function(e){return!e}))},children:[Object(p.jsx)(j.a,{icon:c?P.a:P.b,className:"faq-text-plus"}),Object(p.jsx)("p",{className:"text-faq-black",children:"How do I mint an NFT?"})]}),c&&Object(p.jsxs)("p",{className:"faq-text-answer",children:["Once you have MetaMask installed and Ethereum in your wallet you can ",Object(p.jsx)(J.b,{to:"/mint",children:"click here"})," to mint an NFT."]}),Object(p.jsxs)("div",{className:"faq-text-question",onClick:function(){return b((function(e){return!e}))},children:[Object(p.jsx)(j.a,{icon:m?P.a:P.b,className:"faq-text-plus"}),Object(p.jsx)("p",{className:"text-faq-black",children:"When can I mint an NFT?"})]}),m&&Object(p.jsx)("p",{className:"faq-text-answer",children:"You can officially mint an NFT on January 8th at 1:00 pm ET."}),Object(p.jsxs)("div",{className:"faq-text-question",onClick:function(){return x((function(e){return!e}))},children:[Object(p.jsx)(j.a,{icon:f?P.a:P.b,className:"faq-text-plus"}),Object(p.jsx)("p",{className:"text-faq-black",children:"What do you have planned for the future of CryptoHermits?"})]}),f&&Object(p.jsx)("p",{className:"faq-text-answer",children:"We have a lot planned once we reach 100% in sales for the bookworm collection. The next collection we are excited for is the homesteader collection. From there we hope to expand to other collections. We want to create a community of self-sufficient, independent thinkers who aren't afraid to fight censorship!"}),Object(p.jsxs)("div",{className:"faq-text-question",onClick:function(){return k((function(e){return!e}))},children:[Object(p.jsx)(j.a,{icon:v?P.a:P.b,className:"faq-text-plus"}),Object(p.jsx)("p",{className:"text-faq-black",children:"Can I buy on my mobile phone?"})]}),v&&Object(p.jsx)("p",{className:"faq-text-answer",children:"Yes, simply download MetaMask for iOS or Android and visit our site using the MetaMask browser."})]})]})}n(559);function Y(e){return Object(p.jsxs)("div",{className:"page-mint",children:[Object(p.jsx)("p",{className:"text-magento-border",style:{marginTop:"2vh"},children:"Roadmap"}),Object(p.jsx)("p",{className:"text-normal-black para-team",style:{maxWidth:542,marginTop:35},children:"We are starting off with the bookworm collection and if we reach 100% we will begin working on the homesteader collection. All bookworm holders have pre-sale access to the homesteader collection."}),Object(p.jsxs)("div",{className:"roadmap-step",children:[Object(p.jsx)("p",{className:"roadmap-percent",children:"25%"}),Object(p.jsx)("ul",{children:Object(p.jsx)("li",{className:"space-list",children:"All inclusive tropical vacation for one random wallet address"})})]}),Object(p.jsxs)("div",{className:"roadmap-step",children:[Object(p.jsx)("p",{className:"roadmap-percent",children:"50%"}),Object(p.jsxs)("ul",{children:[Object(p.jsx)("li",{className:"space-list",children:"All inclusive tropical vacation for one random wallet address"}),Object(p.jsx)("li",{className:"space-list",children:"Airdrop Mythic one of one NFT"})]})]}),Object(p.jsxs)("div",{className:"roadmap-step",children:[Object(p.jsx)("p",{className:"roadmap-percent",children:"75%"}),Object(p.jsxs)("ul",{children:[Object(p.jsx)("li",{className:"space-list",children:"All inclusive tropical vacation for one random wallet address"}),Object(p.jsx)("li",{className:"space-list",children:"Donating $20,000 worth of books to an illiteracy program"})]})]}),Object(p.jsxs)("div",{className:"roadmap-step",children:[Object(p.jsx)("p",{className:"roadmap-percent",children:"100%"}),Object(p.jsxs)("ul",{children:[Object(p.jsx)("li",{className:"space-list",children:"All inclusive tropical vacation for one random wallet address"}),Object(p.jsx)("li",{className:"space-list",children:"Airdrop Mythic one of one NFT"})]})]})]})}n(560);var G=[{title:"Home",link:"/"},{title:"Mint NFT",link:"/mint"},{title:"About",link:"/about"},{title:"Rarity",link:"/rarity"},{title:"RoadMap",link:"/roadmap"},{title:"Team",link:"/team"},{title:"FAQ's",link:"/faq"},{title:"Connect",link:"/connect"}];function D(e){var t=Object(o.f)(),n=Object(o.e)().pathname;return Object(p.jsx)("div",{className:"header-link-wrapper",children:Object(p.jsx)("ul",{className:"header-link-ul",children:G.map((function(e,a){return Object(p.jsxs)("li",{onClick:function(){return t(e.link)},children:[e.title,e.link===n&&Object(p.jsx)("div",{className:"header-link-bottom"})]},"navitem-".concat(a))}))})})}var Q=n(8),K=n(9),X=n(15),z=n(14),$=(n(561),function(e){Object(X.a)(n,e);var t=Object(z.a)(n);function n(){return Object(Q.a)(this,n),t.apply(this,arguments)}return Object(K.a)(n,[{key:"render",value:function(){return Object(p.jsx)("footer",{id:"footer",children:Object(p.jsxs)("div",{className:"footer-wrapper",children:[Object(p.jsxs)("p",{className:"footer-text",children:["Copyright 2021. All rights reserved. ",Object(p.jsx)("span",{style:{textDecoration:"underline"},children:"cryptohermitsnft.com"})]}),Object(p.jsx)("br",{}),Object(p.jsxs)("p",{children:[Object(p.jsx)(j.a,{icon:h.b,style:{marginRight:16}}),Object(p.jsx)(j.a,{icon:h.a})]})]})})}}]),n}(a.Component)),V=(n(562),[{title:"Home",link:"/"},{title:"Mint NFT",link:"/mint"},{title:"About",link:"/about"},{title:"Rarity",link:"/rarity"},{title:"RoadMap",link:"/roadmap"},{title:"Team",link:"/team"},{title:"FAQ's",link:"/faq"},{title:"Connect",link:"/connect"}]),Z=Object(m.b)((function(e){return{openMenuStatus:e.openMenuStatus}}))((function(e){var t=Object(o.f)(),n=Object(o.e)().pathname;return Object(p.jsxs)("div",{className:"mobile-menu",children:[Object(p.jsx)(j.a,{icon:v.a,className:"mobile-menu-opener",id:"mobile-bars",color:"#FFF",onClick:function(){return e.dispatch({type:"true"}),void document.getElementById("mobile-bars").classList.add("hide-mobile-bars")}}),e.openMenuStatus&&Object(p.jsxs)("div",{className:"mobile-menu-wrapper",children:[Object(p.jsx)(j.a,{icon:v.c,className:"mobile-menu-closer",color:"#FFF",onClick:function(){return e.dispatch({type:"false"}),void document.getElementById("mobile-bars").classList.remove("hide-mobile-bars")}}),Object(p.jsx)("ul",{className:"mobile-link-ul",children:V.map((function(a,s){return Object(p.jsxs)("li",{onClick:function(){return function(n){t(n.link),e.dispatch({type:"false"}),document.getElementById("mobile-bars").classList.remove("hide-mobile-bars")}(a)},children:[a.link===n&&Object(p.jsx)("div",{className:"mobile-link-left"}),a.title]},"navitem-".concat(s))}))})]})]})})),ee=n.p+"static/media/Crypto-Hermits-Logo-2-Small.54b58327.png";function te(e){var t=Object(o.f)();return Object(p.jsxs)("div",{className:"App",children:[Object(p.jsxs)("div",{className:"site-wrapper",children:[Object(p.jsx)(c,{}),Object(p.jsx)("img",{src:ee,className:"top-left-logo",alt:"logo",onClick:function(){return t("/")}}),Object(p.jsx)(D,{}),Object(p.jsx)(Z,{}),Object(p.jsx)("div",{className:"default-layout",children:Object(p.jsxs)(o.c,{children:[Object(p.jsx)(o.a,{path:"/",element:Object(p.jsx)(d,{})}),Object(p.jsx)(o.a,{path:"/about",element:Object(p.jsx)(b,{})}),Object(p.jsx)(o.a,{path:"/team",element:Object(p.jsx)(y,{})}),Object(p.jsx)(o.a,{path:"/connect",element:Object(p.jsx)(f,{})}),Object(p.jsx)(o.a,{path:"/mint",element:Object(p.jsx)(E,{})}),Object(p.jsx)(o.a,{path:"/rarity",element:Object(p.jsx)(L,{})}),Object(p.jsx)(o.a,{path:"/faq",element:Object(p.jsx)(U,{})}),Object(p.jsx)(o.a,{path:"/roadmap",element:Object(p.jsx)(Y,{})})]})})]}),Object(p.jsx)($,{})]})}var ne=function(e){e&&e instanceof Function&&n.e(3).then(n.bind(null,566)).then((function(t){var n=t.getCLS,a=t.getFID,s=t.getFCP,r=t.getLCP,i=t.getTTFB;n(e),a(e),s(e),r(e),i(e)}))},ae=n(257),se={openMenuStatus:!1},re=Object(ae.a)((function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:se,t=arguments.length>1?arguments[1]:void 0;switch(t.type){case"true":return{openMenuStatus:!0};case"false":return{openMenuStatus:!1};default:return e}}));i.a.render(Object(p.jsx)(s.a.StrictMode,{children:Object(p.jsx)(m.a,{store:re,children:Object(p.jsx)(J.a,{children:Object(p.jsx)(te,{})})})}),document.getElementById("root")),ne()}},[[563,1,2]]]);
//# sourceMappingURL=main.8a1ad7fa.chunk.js.map