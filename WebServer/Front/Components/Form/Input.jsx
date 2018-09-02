import Component from '../Component';
import style from './scss/main.scss';

class Input extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        let {children, label, type} = this.props;
        return (
            <div className={style['form-group']}>
                <label className={this.classNames(style['label-control'], 'col-2')}>{label}</label>
                <input type={type} className={this.classNames(style['form-control'], 'col-10')}/>
            </div>
        )
    }
}

Input.propTypes = {//属性校验器，表示改属性必须是bool，否则报错
    label: React.PropTypes.string,
    type : React.PropTypes.string,
}
Input.defaultProps = {
    type: 'text'
};//设置默认属性

//导出组件
export default Input;