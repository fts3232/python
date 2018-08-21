import style from './scss/main.scss';
import Component from '../../Components/Component';
import img from './images/404-error.png';

const Link = ReactRouterDOM.Link;

class NotFound extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className={style['not-found']}>
                <img src={img} />
                <h2>PAGE NOT FOUND</h2>
                <h3>WE COULDN’T FIND THIS PAGE</h3>
                <Link to="/" className={style.back}>Back To Home</Link>
            </div>
        )
    }
}

NotFound.propTypes = {//属性校验器，表示改属性必须是bool，否则报错
}
NotFound.defaultProps = {};//设置默认属性

//导出组件
export default NotFound;