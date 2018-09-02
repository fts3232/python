import Component from '../../Components/Component';
import Breadcrumb from '../../Components/Breadcrumb';
import Panel from '../../Components/Panel';
import Button from '../../Components/Button';
import {Link} from 'react-router-dom';
import {Textarea,Input} from '../../Components/Form';

class Add extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        let breadcrumb = [{'name': '账簿', 'path': '/CashBook'}, {'name': '添加', 'path': '/CashBook/Add'}];
        return (
            <div>
                <Breadcrumb data={breadcrumb}/>
                <Panel>
                    <form>
                        <Input label="日期"/>
                        <Input label="标签"/>
                        <Input label="类型"/>
                        <Input label="金额"/>
                        <Input label="标签"/>
                        <Textarea label="描述"></Textarea>
                        <Button type="info">添加</Button>
                        <Link to="/cashBook">
                            <Button>返回</Button>
                        </Link>
                    </form>
                </Panel>
            </div>
        )
    }
}

Add.childContextTypes = {};

Add.PropTypes = {}

Add.defaultProps = {}

//导出组件
export default Add;