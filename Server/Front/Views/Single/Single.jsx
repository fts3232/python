import css from './Scss/Main.scss';
class Single extends React.Component {
	constructor(props){
		super(props);
        this.state = {
            data:{}
        }
	}
    componentDidMount(){
        
    }
    render() {
        return (
            <div className="home-page">
                123
            </div>
        )
    }
}

Single.PropTypes = {

}

Single.defaultProps = {
    
}

//导出组件
export default Single;