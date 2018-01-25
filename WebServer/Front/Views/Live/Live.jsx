import css from './Scss/Main.scss';
import Component from '../../Components/Component';
class Live extends Component {
	constructor(props){
		super(props);
	}
    getChildContext(){
        return {
          component: this
        };
    }
    render() {
        return (
            <div ref="app" className="list-page">
                <div></div>
            </div>
        )
    }
}

Live.childContextTypes = {
    component: React.PropTypes.any
};

Live.PropTypes = {
    
}

Live.defaultProps = {
    
}

//导出组件
export default Live;