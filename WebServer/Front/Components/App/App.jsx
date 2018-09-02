import {Redirect, Route, Router, Switch} from 'react-router-dom';
import {createBrowserHistory} from 'history';

import Component from '../Component'
import Loader from '../Loader';
import style from './scss/main.scss';
import Header from '../../Views/Header';
import Footer from '../../Views/Footer';
import NavBar from '../../Views/NavBar';
import NotFound from '../../Views/NotFound'
import nav from '../../Config/nav.js';

const history = createBrowserHistory();

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
                            <Route path="/" exact render={() => (
                                <Redirect to="/cashBook"/>
                            )}/>
                            <Route exact strict path="/:controller/:action?" component={Loader}/>
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