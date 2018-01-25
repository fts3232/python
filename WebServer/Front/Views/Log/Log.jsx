import css from './Scss/Main.scss';
import Component from '../../Components/Component';
class Log extends Component {
	constructor(props){
		super(props);
    this.state = {
      'data':[],
      'toggle':false
    }
	}
  resetData(){
    this.setState({'data':[]})
  }
  appendData(msg){
    let data = this.state.data
    data.push(msg)
    this.setState({'data':data},()=>{
      $('.list').scrollTop( $('.list')[0].scrollHeight);
    })
  }
  toggle(){
    this.setState({'toggle':!this.state.toggle})
  }
  render() {
    return (
        <div className={this.classnames('log-wrapper',{'hidden':!this.state.toggle})}>
          <h3>运行记录</h3>
          <div className="list" ref='list'>
            {this.state.data.map((v)=>{
              return (<p>{v}</p>)
            })}
          </div>
          <div className="btn" onClick={this.toggle.bind(this)}>{this.state.toggle?'收回':'展开'}</div>
        </div>
    )
  }
}

Log.propTypes={//属性校验器，表示改属性必须是bool，否则报错
  
}
Log.defaultProps={
  
};//设置默认属性

//导出组件
export default Log;