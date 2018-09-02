import Component from '../Component';
import style from './scss/main.scss';

class Textarea extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        let {children, label, rows} = this.props;
        return (
            <div className="">
                <label className={this.classNames(style['label-control'], 'col-2')}>{label}</label>
                <textarea rows={rows} className={this.classNames(style['form-control'], 'col-10')}>{children}</textarea>
            </div>
        )
    }
}

Textarea.propTypes = {//属性校验器，表示改属性必须是bool，否则报错
    label: React.PropTypes.string,
    rows  : React.PropTypes.number
}
Textarea.defaultProps = {
    rows: 6
};//设置默认属性

//导出组件
export default Textarea;