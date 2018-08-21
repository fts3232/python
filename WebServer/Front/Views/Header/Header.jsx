import style from './scss/main.scss';
import Component from '../../Components/Component';
import IconButton from '../../Components/IconButton';

const Link = ReactRouterDOM.Link

class Header extends Component {
    constructor(props) {
        super(props);
    }

    componentDidMount() {

    }

    render() {
        return (
            <div className={style.header}>
                <div className={style.left}>
                    <IconButton name="menu"/>
                </div>
            </div>
        )
    }
}

Header.propTypes = {//属性校验器，表示改属性必须是bool，否则报错

}
Header.defaultProps = {};//设置默认属性

//导出组件
export default Header;