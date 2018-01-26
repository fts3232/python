import css from './Scss/Main.scss';
import Component from '../../Components/Component';
class Setting extends Component {
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
        return (
            <div ref="app" className="list-page">
                
            </div>
        )
    }
}

Setting.childContextTypes = {
    component: React.PropTypes.any
};

Setting.PropTypes = {
    
}

Setting.defaultProps = {
    
}

//导出组件
export default Setting;