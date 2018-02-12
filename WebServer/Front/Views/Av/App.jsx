import css from './Scss/Main.scss';
import Dialog from './Dialog.jsx';
import Header from './Header.jsx';
import Log from './Log.jsx';
import Tag from './Tag.jsx';
import Component from '../../Components/Component';
class App extends Component {
	constructor(props){
		super(props);
        this.state = {
            data:[],
            title:false,
            rows_height:[],
            end:false,
            page:1,
            getData:false,
            star:false,
            tag:false,
            canPlay:false,
        }
	}
    getData(){
        let _this = this;
        let page = _this.state.page
        if(_this.state.getData==false){
            this.setState({'getData':true},()=>{
                new Promise((resolve,reject)=>{
                    let url = 'http://localhost:8000/getData?p='+page+'&size=24'
                    if(_this.state.canPlay == true)
                        url += '&canPlay=1'
                    if(_this.state.title != false)
                        url += '&title=' + _this.state.title
                    else if(_this.state.star != false)
                        url += '&star=' + _this.state.star
                    else if(_this.state.tag != false)
                        url += '&tag=' + _this.state.tag

                    request.get(url)
                           .end(function(err, res){
                                if(typeof res != 'undefined' && res.ok){
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
                        if(_this.state.canPlay == true && _this.state.title !=false || _this.state.star !=false || _this.state.tag !=false){
                            _this.setState({'end':true,'getData':false})
                        }else{
                            _this.setState({'getData':false})
                        }
                    }else{
                        _this.setState({'end':true,'getData':false})
                    }
                }).catch((err)=>{
                    _this.setState({'end':true,'getData':false})
                })
            })
        }
    }
    componentDidMount(){
        let _this = this
        let socket = new WebSocket('ws://localhost:8000/socket')
        // 打开Socket 
        socket.onopen = function(event) { 
          console.log('连接成功')
            // 监听消息
            socket.onmessage = function(event) { 
                let data = JSON.parse(event.data)
                if(data.event=='scan' || data.event=='spider'){
                    _this.refs.log.appendData(data.msg)
                }else if(data.event=='play' && data.msg=='打开失败'){
                    alert(data.msg)
                }
            }; 
        }
       
        // 监听Socket的关闭
        socket.onclose = function(event) { 
          console.log('Client notified socket has closed',event); 
          // 关闭Socket.... 
          //socket.close() 
        }; 
        this.socket = socket
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
    socketSend(event,msg=''){
        let data = JSON.stringify({'event':event,'msg':msg})
        this.socket.send(data)
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
        if(typeof data.title !='undefined'){
            this.setState({'title':data.title,'tag':false,'star':false,'data':[],'page':1,'end':false,rows_height:[]},()=>{
                _this.getData()
            })
        }else if(typeof data.star !='undefined'){
            this.setState({'star':data.star,'tag':false,'title':false,'data':[],'page':1,'end':false,rows_height:[]},()=>{
                _this.getData()
            })
        }else if(typeof data.tag !='undefined'){
            this.setState({'tag':data.tag,'star':false,'title':false,'data':[],'page':1,'end':false,rows_height:[]},()=>{
                _this.getData()
            })
        }
    }
    top(){
        $('html').animate({'scrollTop':0})
    }
    getChildContext(){
        return {
          component: this
        };
    }
    render() {
        return (
            <div ref="app" className="list-page">
                <Header />
                <div className="waterfall" ref='waterfall'>
                    {this.state.data.map((val)=>{
                        return (
                            <div className="item" onClick={this.onClick.bind(this,val)}>
                                <img src={val.IMAGE} title={val.IMAGE == ''?'暂无图片':val.TITLE}/>
                                <div className="box">
                                    <p className="title">
                                        {val.TITLE}
                                    </p>
                                    <div className="tag">
                                        {val.PLAY?(
                                            <span className="can-play">可播放</span>
                                        ):null}
                                        {val.LINK.length > 0?(
                                            <span className="can-download">可下载</span>
                                        ):null}
                                    </div>
                                     <div className="info">
                                        <span className="identifier">{val.IDENTIFIER}</span>
                                        <span className="publish-time">{val.PUBLISH_TIME}</span>
                                    </div>
                                </div>
                            </div>
                        )
                    })}
                </div>
                <Dialog ref='dialog'/>
                <Log ref='log'/>
                <Tag ref='tag'/>
                <div className="top" onClick={this.top.bind(this)}>Top</div>
            </div>
        )
    }
}

App.childContextTypes = {
    component: React.PropTypes.any
};

App.PropTypes = {
    space:React.PropTypes.number
}

App.defaultProps = {
    space:10
}

//导出组件
export default App;