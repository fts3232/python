import css from './Scss/Header.scss';
import Component from '../../Components/Component';
class Header extends Component {
  	constructor(props){
  		super(props);
      this.state = {
        'canPlay':false
      }
  	}
    parent(){
        return this.context.component
    }
    search(){
        let val = $(this.refs.input).val()
        this.parent().search({'title':val})
    }
    scan(){
      this.parent().refs.log.resetData();
      this.parent().refs.log.setState({'toggle':true});
      this.parent().socketSend('scan');
    }
    spider(){
      this.parent().refs.log.resetData();
      this.parent().refs.log.setState({'toggle':true});
      this.parent().socketSend('spider');
    }
    getCanPlay(){
      if(this.parent().state.getData==false){
        let _this = this
        let status = !this.state.canPlay
        this.setState({'canPlay':status},()=>{
          _this.parent().setState({'canPlay':status,'data':[],'page':1,'end':false,rows_height:[]},()=>{
            _this.parent().getData()
          })
        })
      }
      
    }
    render() {
        return (
            <div className="header">
                <input ref='input'/>
                <button onClick={this.search.bind(this)}>搜索</button>
                <button onClick={this.scan.bind(this)}>扫描</button>
                <button onClick={this.spider.bind(this)}>爬取</button>
                <button className={this.classNames('switch',{'on':this.state.canPlay})} onClick={this.getCanPlay.bind(this)}>可播放</button>
            </div>
        )
    }
}

Header.contextTypes = {
  component: React.PropTypes.any
};

Header.PropTypes = {
    
}

Header.defaultProps = {
    
}

//导出组件
export default Header;