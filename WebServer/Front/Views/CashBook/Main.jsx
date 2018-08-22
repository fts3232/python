import Component from '../../Components/Component';
import Table from '../../Components/Table';
import Pagination from '../../Components/Pagination';
import Breadcrumb from '../../Components/Breadcrumb';
import Panel from '../../Components/Panel';
import Button from '../../Components/Button';
import {Link} from 'react-router-dom';

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
        let total = 500;
        let breadcrumb = [{'name': '账簿', 'path': '/cashBook'}];
        let currentPage = parseInt(this.getParams('page'));
        return (
            <div>
                <Breadcrumb data={breadcrumb}/>
                <Panel>
                    <div className="margin-bottom-10">
                        <Link to="/cashBook/add">
                            <Button type="info">添加</Button>
                        </Link>
                    </div>
                    <Table data={data} colunm={colunm} total={total}/>
                    <Pagination total={total} currentPage={currentPage}/>
                </Panel>
            </div>
        )
    }
}

Main.PropTypes = {}

Main.defaultProps = {}

//导出组件
export default Main;