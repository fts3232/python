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
        let items = []
        let data = this.state.data
        for(let i in data){
            items.push(
                <div className="item">
                    <a href={i} target="_blank">
                        <img src={data[i].screenshot}/>
                        <span className={this.classNames('state',{'off':data[i].state=='回播' || data[i].state=='未在直播'})}>{data[i].state}</span>
                        <div className="msg">
                            <p><span className="title">{data[i].title}</span></p>
                            <p>
                                <span className="nickname">{data[i].nickname}</span>
                                <span className="category">{data[i].category}</span>
                            </p>
                        </div>
                    </a>
                </div>
            )
        }
        return (
            <div ref="app" className="list-page">
                {items}
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