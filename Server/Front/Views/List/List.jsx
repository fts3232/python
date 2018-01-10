import css from './Scss/Main.scss';
class List extends React.Component {
	constructor(props){
		super(props);
        this.state = {
            data:[
                {'img':'','title':'1221'},
                {'img':'','title':'1221'},
                {'img':'','title':'1221'},
                {'img':'','title':'1221'},
                {'img':'','title':'1221'},
                {'img':'','title':'1221'},
                {'img':'','title':'1221'},
                {'img':'','title':'1221'},
                {'img':'','title':'1221'},
                {'img':'','title':'1221'},
                {'img':'','title':'1221'},
            ],
            total:10,
            current:9,
        }
	}
    componentDidMount(){
        let _this = this;
        new Promise((resolve,reject)=>{
            request.post('/api/getUser')
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
    }
    createPagination(){
        let res = []
        let current = this.state.current
        let total = this.state.total
        if(total<=7){
            for(let i = 1;i<=total;i++){
                res.push(<span className="item">{i}</span>)
            }
        }else{
            
            if(total - 3 <= current){
                for(let i = current - 3;i<=total;i++){
                    res.push(<span className="item">{i}</span>)
                }
            }else{
                for(let i = current - 3;i<=current+3;i++){
                    res.push(<span className="item">{i}</span>)
                }
            }
        }
        
        
        return res
    }
    render() {
        return (
            <div className="list-page">
                <div className="waterfall">
                    {this.state.data.map((val)=>{
                        return (
                            <div className="item">
                                <img src={val.img}/>
                                <p className="title">{val.title}</p>
                            </div>
                        )
                    })}
                </div>
                <div className="pagination">
                    <button>上一页</button>
                    {this.createPagination()}
                    <button>下一页</button>
                </div>
            </div>
        )
    }
}

List.PropTypes = {

}

List.defaultProps = {
    
}

//导出组件
export default List;