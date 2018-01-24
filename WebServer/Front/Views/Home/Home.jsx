import css from './Scss/Main.scss';
import Component from '../../Components/Component'
const Link = ReactRouterDOM.Link
class Home extends Component {
	constructor(props){
		super(props);
	}
  componentDidMount(){

  }
  render() {
    return (
        <div className='home'>
          <Link to="/list"><div className="block blue"></div></Link>
          <Link to="/live"><div className="block red"></div></Link>
        </div>
    )
  }
}

Home.propTypes={//属性校验器，表示改属性必须是bool，否则报错
  
}
Home.defaultProps={
  
};//设置默认属性

//导出组件
export default Home;