import Component from '../Component';
import style from './scss/main.scss';

class Pagination extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        let {total, current} = this.props;
        let start, end;
        let li = [];
        start = current - 2 <= 0 ? 1 : current - 2;
        end = start + 4 > total ? total : start + 4;
        if (end - start < 5) {
            start = end - 4 <= 0 ? 1 : end - 4;
        }
        for (let i = start; i <= end; i++) {
            li.push(<li className={i == current ? style.active : null}><a>{i}</a></li>);
        }
        return (
            <div className={style.pagination}>
                <ul>
                    <li className={current == 1 ? 'disabled' : null}><a>上一页</a></li>
                    {li}
                    <li className={current == total ? 'disabled' : null}><a>下一页</a></li>
                </ul>
            </div>
        )
    }
}

Pagination.propTypes = {//属性校验器，表示改属性必须是bool，否则报错
    total  : React.PropTypes.number,
    current: React.PropTypes.number
}
Pagination.defaultProps = {};//设置默认属性

//导出组件
export default Pagination;