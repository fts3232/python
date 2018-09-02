import Component from '../Component';
import style from './scss/main.scss';

class Panel extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        let {children} = this.props;
        return (
            <div className={style['panel']}>
                {children}
            </div>
        )
    }
}

Panel.propTypes = {//属性校验器，表示改属性必须是bool，否则报错

}
Panel.defaultProps = {};//设置默认属性

//导出组件
export default Panel;