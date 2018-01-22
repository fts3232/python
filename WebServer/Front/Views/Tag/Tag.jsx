import css from './Scss/Main.scss';
import classnames from 'classnames';
class Tag extends React.Component {
	constructor(props){
		super(props);
    this.state = {
      'data':[],
      'toggle':false
    }
	}
  parent(){
        return this.context.component
    }
  toggle(){
    this.setState({'toggle':!this.state.toggle})
  }
  componentDidMount(){
    let _this = this
    new Promise((resolve,reject)=>{
        let url = 'http://localhost:8000/getTag'
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
  }
  itemClick(id){
     this.parent().search({'tag':id})
     this.setState({'toggle':false})
  }
  render() {
    return (
        <div className={classnames('tag-wrapper',{'hidden':!this.state.toggle})}>
          <h3>Tag列表</h3>
          <div className="list" ref='list'>
            {this.state.data.map((v)=>{
              return (<span onClick={this.itemClick.bind(this,v.TAG_ID)}>{v.TAG_NAME}</span>)
            })}
          </div>
          <div className="btn" onClick={this.toggle.bind(this)}>{this.state.toggle?'收回':'展开'}</div>
        </div>
    )
  }
}

Tag.contextTypes = {
  component: React.PropTypes.any
};

Tag.propTypes={//属性校验器，表示改属性必须是bool，否则报错
  
}
Tag.defaultProps={
  
};//设置默认属性

//导出组件
export default Tag;