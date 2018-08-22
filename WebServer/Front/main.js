import App from './Components/App';
window.request = superagent;
//react-router

ReactDOM.render((
    <App />
), document.getElementsByTagName('section')[0]);