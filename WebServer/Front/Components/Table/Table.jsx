import Component from '../Component';
import style from './scss/main.scss';

class Table extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        let {data, colunm, total, offset} = this.props;
        return (
            <div className={style['data-table']}>
                <table>
                    <thead>
                    <tr>
                        {Object.keys(colunm).map(key => {
                            return (<th>{key}</th>)
                        })}
                    </tr>
                    </thead>
                    <tbody>
                    {data.map((v, i) => {
                        return (
                            <tr>
                                {Object.values(colunm).map(key => {
                                    return (<td>{v[key]}</td>)
                                })}
                            </tr>
                        )
                    })}
                    </tbody>
                </table>
                <div className={style['data-info']}>
                    总共{total}条记录
                </div>
            </div>
        )
    }
}

Table.propTypes = {//属性校验器，表示改属性必须是bool，否则报错
    data  : React.PropTypes.array,
    colunm: React.PropTypes.Object
}
Table.defaultProps = {};//设置默认属性

//导出组件
export default Table;