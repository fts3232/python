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
          <Link to="/av"><div className="block av">A</div></Link>
          <Link to="/live"><div className="block live">直</div></Link>
          <Link to="/comic"><div className="block comic">漫</div></Link>
          <Link to="/dnf"><div className="block setting">D</div></Link>
          <Link to="/setting"><div className="block setting">设</div></Link>
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