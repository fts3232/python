import css from './Scss/Main.scss';
class List extends React.Component {
	constructor(props){
		super(props);
        this.state = {
            data:[
                
            ],
            total:10,
            current:9,
        }
	}
    componentDidMount(){
        let _this = this;
        new Promise((resolve,reject)=>{
            request.get('http://localhost:8000/getData/?p=1&size=12')
                   .end(function(err, res){
                        if(res.ok){
                            resolve(JSON.parse(res.text))
                        }else{
                            reject(err)
                        }
                   })
        }).then((data)=>{
            _this.setState({'data':data},()=>{
                let _this = this
                let length = $('img').length
                let i = 0
                $('img').on('load',function(){
                    i += 1
                    if(i==length){
                        _this.waterfall()
                    }
                })
            })
            
        })
    }
    waterfall(){
        let items = $(this.refs.waterfall).find('.item')
        let length = items.length
        let width = 1000
        let cols = Math.floor(width / items.outerWidth());
        let rows_height = new Array();
        let space = 10
        let col = 0
        for(let i = 0;i<cols;i++){
            rows_height.push(0)
        }
        let left = 0
        for(let i = 0;i<length;i++){
            let row_height_min = Math.min.apply(this,rows_height)
            for(let i = 0;i<cols;i++){
                if(rows_height[i]==row_height_min){
                    col = i;
                    break;
                }
            }
            left = col * (items.outerWidth() + space)
            rows_height[col] += items.eq(i).outerHeight(true) + space
            items.eq(i).css({'position':'absolute','top':row_height_min,'left':left})
        }
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
                <div className="waterfall" ref='waterfall'>
                    {this.state.data.map((val)=>{
                        return (
                            <div className="item">
                                <img src={val.IMAGE}/>
                                <p className="title">{val.TITLE}</p>
                            </div>
                        )
                    })}
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