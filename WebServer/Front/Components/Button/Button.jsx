import Component from '../Component';
import style from './scss/main.scss';
import {Link} from 'react-router-dom';

class Button extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        let {children, type} = this.props
        return (
            <button className={this.classNames(style.btn, style["btn-" + type])}>{children}</button>
        )
    }
}

Button.propTypes = {//属性校验器，表示改属性必须是bool，否则报错
    type: React.PropTypes.string
}
Button.defaultProps = {
    type: 'default'
};//设置默认属性

//导出组件
export default Button;