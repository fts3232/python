import css from './Scss/Main.scss';
import Component from '../../Components/Component';
class Comic extends Component {
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
                let url = 'http://localhost:8000/getComic'
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
            <div ref="app" className="comic-list-page">
                {this.state.data.map((v)=>{
                    return (
                        <div className="item">
                            <a href={v.url}>
                                <div className="cover" style={{'background':'url('+v.cover+')'}}></div>
                                <div className="info-box">
                                    <h2 className="title">{v.title}</h2>
                                    <span className="episodes">{v.episodes}</span>
                                </div>
                            </a>
                        </div>
                    )
                })}
            </div>
        )
    }
}

Comic.childContextTypes = {
    component: React.PropTypes.any
};

Comic.PropTypes = {
    
}

Comic.defaultProps = {
    
}

//导出组件
export default Comic;