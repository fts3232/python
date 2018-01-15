import css from './Scss/Main.scss';
import Dialog from '../Dialog';
import Header from '../Header';
class List extends React.Component {
	constructor(props){
		super(props);
        this.state = {
            data:[],
            search:'',
            rows_height:[],
            end:false,
            page:1,
        }
	}
    getData(){
        let _this = this;
        let page = _this.state.page
        let search = _this.state.search
        new Promise((resolve,reject)=>{
            request.get('http://localhost:8000/getData/?p='+page+'&size=24&search='+search)
                   .end(function(err, res){
                        if(res.ok){
                            resolve(JSON.parse(res.text))
                        }else{
                            reject(err)
                        }
                   })
        }).then((data)=>{
            if(data!=''){
                data = _this.state.data.concat(data)
                _this.setState({'data':data,page:page + 1},()=>{
                    let _this = this
                    let length = $('.waterfall .item:not(.active) img').length
                    let i = 0
                    $('.waterfall .item:not(.active) img').on('load error',function(){
                        i += 1
                        if(i==length){
                            let items = $(_this.refs.waterfall).find('.item:not(.active)')
                            page==1 ? _this.waterfall(items):_this.updateWaterfall(items)
                        }
                    })
                })
            }else{
                _this.setState({'end':true})
            }
        })
    }
    componentDidMount(){
        let _this = this
        this.getData()
        $(window).resize(()=>{
            this.setState({rows_height:[]},()=>{
                let items = $(_this.refs.waterfall).find('.item')
                _this.waterfall(items)
            })
            
        })
        $(window).scroll(()=>{
            let scrollTop = $(window).scrollTop()
            let scrollHeight = $('html').get(0).scrollHeight
            let height = $(window).height()
            if(scrollHeight <= height + scrollTop && !_this.state.end){
                _this.getData()
            }
        })
    }
    waterfall(items){
        let space =  this.props.space
        let width = $('body').width() - space * 2
        let cols = Math.floor(width / (items.outerWidth() +space));
        $(this.refs.app).css({'width':cols * (items.outerWidth() + space)})
        let rows_height = this.state.rows_height
        for(let i = 0;i<cols;i++){
            rows_height.push(0)
        }
        this.updateWaterfall(items)
    }
    updateWaterfall(items){
        let rows_height = this.state.rows_height
        let col = 0
        let left = 0
        let length = items.length
        let cols = rows_height.length
        let space = this.props.space
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
        this.setState({rows_height:rows_height})
        items.addClass('active')

    }
    onClick(val){
        let obj = this.refs.dialog
        obj.show()
        obj.setState({data:val})
    }
    search(data){
        let _this = this
        this.setState({'search':data,'data':[],'page':1,'end':false,rows_height:[]},()=>{
            _this.getData()
        })
    }
    top(){
        $('html').animate({'scrollTop':0})
    }
    render() {
        return (
            <div ref="app" className="list-page">
                <Header search={this.search.bind(this)}/>
                <div className="waterfall" ref='waterfall'>
                    {this.state.data.map((val)=>{
                        return (
                            <div className="item" onClick={this.onClick.bind(this,val)}>
                                <img src={val.IMAGE}/>
                                <p className="title">
                                    {val.TITLE}
                                    {val.PLAY?(
                                        <span className="can-play">可播放</span>
                                    ):null}
                                </p>
                                
                            </div>
                        )
                    })}
                </div>
                <Dialog ref='dialog'/>
                <div className="top" onClick={this.top.bind(this)}>Top</div>
            </div>
        )
    }
}

List.PropTypes = {
    space:React.PropTypes.number
}

List.defaultProps = {
    space:10
}

//导出组件
export default List;