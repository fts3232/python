import Component from '../Component';
import style from './scss/main.scss';

require('./font.js');

class IconButton extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        let {name} = this.props;
        return (
            <svg className={style.icon} aria-hidden="true">
                <use xlinkHref={"#icon-" + name}></use>
            </svg>
        )
    }
}

IconButton.propTypes = {//属性校验器，表示改属性必须是bool，否则报错
    name: React.PropTypes.string
}
IconButton.defaultProps = {};//设置默认属性

//导出组件
export default IconButton;