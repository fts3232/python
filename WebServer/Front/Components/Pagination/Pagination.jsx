import Component from '../Component';
import style from './scss/main.scss';
import {Link} from 'react-router-dom'

class Pagination extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        let {total, size, maxShowPage, currentPage} = this.props;
        maxShowPage = maxShowPage - 1;
        if(isNaN(currentPage)){
            currentPage = 1;
        }
        let totalPage = Math.ceil(total / size);
        let start, end;
        let li = [];
        start = currentPage - 2 <= 0 ? 1 : currentPage - 2;
        end = start + maxShowPage > totalPage ? totalPage : start + maxShowPage;
        if (end - start < maxShowPage) {
            start = end - maxShowPage <= 0 ? 1 : end - maxShowPage;
        }
        for (let i = start; i <= end; i++) {
            li.push(<li className={i == currentPage ? style.active : null}><Link to={"?page=" + i}>{i}</Link></li>);
        }
        return (
            <div className={style.pagination}>
                <ul>
                    <li className={currentPage == 1 ? style.disabled : null}><Link to={"?page=" + (currentPage - 1)}>上一页</Link></li>
                    {li}
                    <li className={currentPage == totalPage ? style.disabled : null}><Link to={"?page=" + (currentPage + 1)}>下一页</Link></li>
                </ul>
            </div>
        )
    }
}

Pagination.propTypes = {//属性校验器，表示改属性必须是bool，否则报错
    total   : React.PropTypes.number,
    size: React.PropTypes.number,
    maxShowPage: React.PropTypes.number,
    currentPage: React.PropTypes.number
}
Pagination.defaultProps = {
    size: 10,
    maxShowPage: 5
};//设置默认属性

//导出组件
export default Pagination;