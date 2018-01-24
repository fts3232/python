import NotFound from './Views/NotFound'
import Home from './Views/Home';
import Loader from './Components/Loader';
window.request = superagent;
//react-router
const Router = ReactRouterDOM.Router;
const Route = ReactRouterDOM.Route;
const Redirect = ReactRouterDOM.Redirect;
const Switch = ReactRouterDOM.Switch;
const history = History.createBrowserHistory();

ReactDOM.render((
	<Router history={history}>
		<Switch>
	        <Route path="/" exact component={Home} />
            <Route exact path="/:path" component={Loader} />
	        <Route component={NotFound}/>
		</Switch>
	</Router>
), document.getElementsByTagName('section')[0]);