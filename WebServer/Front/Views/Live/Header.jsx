import css from './Scss/Header.scss';
import Component from '../../Components/Component';
class Header extends Component {
  	constructor(props){
  		super(props);
  	}
    parent(){
        return this.context.component
    }
    update(){
      this.parent().getData()
    }
    render() {
        return (
            <div className="header">
                <button onClick={this.update.bind(this)}>更新数据</button>
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