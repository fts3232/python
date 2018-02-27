/*import css from './Scss/Main.scss';*/
import Component from '../../Components/Component';
class Main extends Component {
    constructor(props){
        super(props);
        this.state = {
            
        }
    }
    getChildContext(){
        return {
          component: this
        };
    }
    render() {
        return (
            <div ref="app" className="dnf-page">
                <form>
                    <div>
                        <label>账号1</label>
                        <input type="text"/>
                    </div>
                    <div>
                        <label>账号1</label>
                        <input type="text"/>
                    </div>
                    <div>
                        <label>账号1</label>
                        <input type="text"/>
                    </div>
                    <div>
                        <label>账号1</label>
                        <input type="text"/>
                    </div>
                    <div>
                        <label>账号1</label>
                        <input type="text"/>
                    </div>
                    <div>
                        <label>账号1</label>
                        <input type="text"/>
                    </div>
                    <button>提交</button>
                </form>
                
            </div>
        )
    }
}

Main.childContextTypes = {
    component: React.PropTypes.any
};

Main.PropTypes = {
    space:React.PropTypes.number
}

Main.defaultProps = {
    space:10
}

//导出组件
export default Main;