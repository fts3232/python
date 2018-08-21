import Component from '../../Components/Component';
import Table from '../../Components/Table';
import Pagination from '../../Components/Pagination';
import Breadcrumb from '../../Components/Breadcrumb';

class Main extends Component {
    constructor(props) {
        super(props);
        this.state = {}
    }

    render() {
        let data = [
            {'id': 1, 'date': '2018-09-20', 'type': '收入', 'amount': '200', 'description': '工资'},
            {'id': 2, 'date': '2018-09-20', 'type': '收入', 'amount': '200', 'description': '工资'},
            {'id': 3, 'date': '2018-09-20', 'type': '收入', 'amount': '200', 'description': '工资'},
        ];
        let colunm = {
            'ID': 'id',
            '日期': 'date',
            '类型': 'type',
            '金额': 'amount',
            '描述': 'description'
        };
        let totalPage = 6;
        let currentPage = 1;
        let total = 500;
        let pageSize = 10;
        let offset = (currentPage - 1) * pageSize;
        let breadcrumb = [{'name': '账簿', 'path': '/'}];
        return (
            <div>
                <Breadcrumb data={breadcrumb}/>
                <Table data={data} colunm={colunm} total={total} offset={offset}/>
                <Pagination total={totalPage} current={currentPage}/>
            </div>
        )
    }
}

Main.childContextTypes = {};

Main.PropTypes = {}

Main.defaultProps = {}

//导出组件
export default Main;