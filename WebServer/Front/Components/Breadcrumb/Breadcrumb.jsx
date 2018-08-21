import Component from '../Component';
import style from './scss/main.scss';
import {Link} from 'react-router-dom';

class Breadcrumb extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        let {data} = this.props;
        let {location} = this.context.router.route;
        return (
            <ul className={style.breadcrumb}>
                {data.map((v, i) => {
                    return (
                        <li className={location.pathname == v.path ? style.active : null}>
                            {location.pathname != v.path ? (<Link to={v.path}>{v.name}</Link>) : v.name}
                        </li>
                    );
                })}
            </ul>
        )
    }
}

Breadcrumb.propTypes = {//属性校验器，表示改属性必须是bool，否则报错
    data: React.PropTypes.array
}
Breadcrumb.defaultProps = {};//设置默认属性

Breadcrumb.contextTypes = {
    router: React.PropTypes.Object
}

//导出组件
export default Breadcrumb;