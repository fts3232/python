import css from './Scss/Main.scss';
import Component from '../../Components/Component';
const Link = ReactRouterDOM.Link;
class NotFound extends Component {
	constructor(props){
		super(props);
	}
  render() {
    return (
        <div className="not-found">
          <h2>PAGE NOT FOUND</h2>
          <h3>WE COULDN’T FIND THIS PAGE</h3>
          <Link to="/">Back To Home</Link>
        </div>
    )
  }
}

NotFound.propTypes={//属性校验器，表示改属性必须是bool，否则报错
}
NotFound.defaultProps={
};//设置默认属性

//导出组件
export default NotFound;