import Component from '../../Components/Component'
import Loader from '../../Components/Loader';
import style from './scss/main.scss';
import Header from '../Header';
import Footer from '../Footer';
import NavBar from '../NavBar';
import NotFound from '../NotFound'
import CashBook from '../CashBook';
import nav from '../../Config/nav.js';
const Router = ReactRouterDOM.Router;
const Route = ReactRouterDOM.Route;
const Redirect = ReactRouterDOM.Redirect;
const Switch = ReactRouterDOM.Switch;
const history = History.createBrowserHistory();

class App extends Component {
    constructor(props) {
        super(props);
    }

    componentDidMount() {

    }

    render() {
        return (
            <Router history={history}>
                <div className={style.app}>
                    <Header/>
                    <NavBar data={nav}/>
                    <div className={style['content-container']}>
                        <Switch>
                            <Route path="/" exact component={CashBook}/>
                            <Route exact path="/:path" component={Loader}/>
                            <Route component={NotFound}/>
                        </Switch>
                    </div>
                    <Footer/>
                </div>
            </Router>
        )
    }
}

App.propTypes = {//属性校验器，表示改属性必须是bool，否则报错

}
App.defaultProps = {};//设置默认属性

//导出组件
export default App;