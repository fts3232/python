import Component from '../../Components/Component'
import style from './scss/main.scss';
import {Link} from 'react-router-dom';

class NavBar extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        let {location} = this.context.router.route;
        let {data} = this.props;
        return (
            <div className={style['nav-bar']}>
                <ul>
                    {data.map((v, i) => {
                        let className = null;
                        if(location.pathname.toLowerCase() == v.path.toLowerCase() || location.pathname.toLowerCase().indexOf(v.path.toLowerCase()) != -1){
                            className = style.active;
                        }
                        return (
                            <li className={className}>
                                <Link to={v.path}>{v.name}</Link>
                            </li>
                        );
                    })}
                </ul>
            </div>
        )
    }
}

NavBar.propTypes = {//属性校验器，表示改属性必须是bool，否则报错
    data: React.PropTypes.array
}

NavBar.defaultProps = {};//设置默认属性

//导出组件
export default NavBar;