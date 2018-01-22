import List from './Views/List'
import NotFound from './Views/NotFound'
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
	        <Route path="/" exact component={List} />
	        <Route component={NotFound}/>
		</Switch>
	</Router>
), document.getElementsByTagName('section')[0]);