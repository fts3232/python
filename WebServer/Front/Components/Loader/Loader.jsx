//Component1.jsx
/*import React from 'react';*/
import Component from '../Component';
import css from './Scss/Main.scss';
const Link = ReactRouterDOM.Link
class Loader extends Component {
	constructor(props){
		super(props);
        this.state = {
            'Component':null,
        }
	}
    loadPage(props){
        let componentName = props.match.params.path;
        let location = props.location
        componentName = componentName.replace(/^[a-z]/,(s)=>{
            return s.toUpperCase();
        })
        import(/* webpackChunkName: "lazy" */`../../Views/${componentName}/index.js`).then((component)=>{
            let Component = component.default;
            this.setState({'Component':<Component location={location} />})

        }).catch((err)=>{
            import(/* webpackChunkName: "lazy" */`../../Views/NotFound/index.js`).then((component)=>{
                let Component = component.default;
                this.setState({'Component':<Component location={location} />})
            }).catch((err)=>{
                console.log(err);
            })
        });
    }
    componentWillReceiveProps (props){
        this.loadPage(props)
    }
    componentDidMount(){
        this.loadPage(this.props)
    }
    render() {
        return (
            <div className="Loader">
                <Link to="/"><button className="back-home">返回</button></Link>
                {this.state.Component}
            </div>
        )
    }
}

Loader.propTypes={//属性校验器，表示改属性必须是bool，否则报错
    location:React.PropTypes.object
}
Loader.defaultProps={
    location:{}
};//设置默认属性

//导出组件
export default Loader;