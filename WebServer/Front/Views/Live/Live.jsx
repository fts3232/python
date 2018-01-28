import css from './Scss/Main.scss';
import Component from '../../Components/Component';
class Live extends Component {
	constructor(props){
		super(props);
        this.state = {
            'data':[]
        }
	}
    getChildContext(){
        return {
          component: this
        };
    }
    getData(){
        let _this = this;
        this.setState({'getData':true},()=>{
            new Promise((resolve,reject)=>{
                let url = 'http://localhost:8000/getLive'
                request.get(url)
                       .end(function(err, res){
                            if(res.ok){
                                resolve(JSON.parse(res.text))
                            }else{
                                reject(err)
                            }
                       })
            }).then((data)=>{
                _this.setState({'data':data})
            })
        })
    }
    componentDidMount(){
        this.getData()
    }
    render() {
        let group = []
        let data = this.state.data
        let groupName = {
            'douyu':'斗鱼',
            'huya':'虎牙',
            'panda':'熊猫',
            'longzhu':'龙珠'
        }
        for(let i in data){
            let items = []
            for(let j in data[i]){
                let room_info = data[i][j][1]
                items.push(
                    <div className="item">
                        <a href={data[i][j][0]} target="_blank">
                            <img src={room_info.screenshot}/>
                            <span className={this.classNames('state',{'off':!room_info.state})}>{room_info.state?'正在直播':'已下播'}</span>
                            <div className="msg">
                                <p><span className="title">{room_info.room_name}</span></p>
                                <p>
                                    <span className="nickname">{room_info.nickname}</span>
                                    <span className="category">{room_info.category}</span>
                                </p>
                            </div>
                        </a>
                    </div>
                )
            }
            group.push(
                <div className="item-group">
                    <h3>{groupName[i]}</h3>
                    <div className="items">
                        {items}
                    </div>
                </div>
            )
        }
        return (
            <div ref="app" className="live-list-page">
                {group}
            </div>
        )
    }
}

Live.childContextTypes = {
    component: React.PropTypes.any
};

Live.PropTypes = {
    
}

Live.defaultProps = {
    
}

//导出组件
export default Live;