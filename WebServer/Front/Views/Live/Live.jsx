import css from './Scss/Main.scss';
import Dialog from '../Dialog';
import Header from '../Header';
import Log from '../Log';
import Tag from '../Tag';
class Live extends React.Component {
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
        }
	}
    getChildContext(){
        return {
          component: this
        };
    }
    render() {
        return (
            <div ref="app" className="list-page">
                
            </div>
        )
    }
}

Live.childContextTypes = {
    component: React.PropTypes.any
};

Live.PropTypes = {
    space:React.PropTypes.number
}

Live.defaultProps = {
    space:10
}

//导出组件
export default Live;