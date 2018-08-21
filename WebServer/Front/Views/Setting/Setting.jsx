import Component from '../../Components/Component';

class Setting extends Component {
    constructor(props) {
        super(props);
        this.state = {
            'data': []
        }
    }

    getChildContext() {
        return {
            component: this
        };
    }

    componentDidMount() {

    }

    createDB(type) {
        let _this = this;
        new Promise((resolve, reject) => {
            let url = 'http://localhost:8000/setting/createDB'
            request.get(url)
                .end(function (err, res) {
                    if (typeof res != 'undefined' && res.ok) {
                        resolve(JSON.parse(res.text))
                    } else {
                        reject(err)
                    }
                })
        }).then((data) => {
            alert(data.msg)
        })
    }

    render() {
        return (
            <div ref="app" className="setting-page">
                <h3>JavBus</h3>
                <button onClick={this.createDB.bind(this, 'javbus')}>创建数据库</button>
                <h3>账本</h3>
                <button onClick={this.createDB.bind(this, 'cashbook')}>创建数据库</button>
            </div>
        )
    }
}

Setting.childContextTypes = {
    component: React.PropTypes.any
};

Setting.PropTypes = {}

Setting.defaultProps = {}

//导出组件
export default Setting;