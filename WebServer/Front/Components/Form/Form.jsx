//Component1.jsx
/*import React from 'react';*/
import Component from '../Component';

const Link = ReactRouterDOM.Link

class Loader extends Component {
    constructor(props) {
        super(props);
        this.state = {
            'Component': null,
        }
    }

    loadPage(props) {
        let {controller, action} = props.match.params;
        let location = props.location
        controller = controller.substring(0,1).toUpperCase() + controller.substring(1);
        if (typeof action == 'undefined') {
            action = 'main';
        }
        action = action.substring(0,1).toUpperCase() + action.substring(1);
        import(/* webpackChunkName: "lazy" */`../../Views/${controller}/index.js`).then((component) => {
            let Component = component[action];
            this.setState({'Component': <Component location={location}/>})

        }).catch((err) => {
            console.log(err)
            import(/* webpackChunkName: "lazy" */`../../Views/NotFound/index.js`).then((component) => {
                let Component = component.default;
                this.setState({'Component': <Component location={location}/>})
            }).catch((err) => {
                console.log(err);
            })
        });
    }

    componentWillReceiveProps(props) {
        this.loadPage(props)
    }

    componentDidMount() {
        this.loadPage(this.props)
    }

    render() {
        return (
            <div>
                {this.state.Component}
            </div>
        )
    }
}

Loader.propTypes = {//属性校验器，表示改属性必须是bool，否则报错
    location: React.PropTypes.object
}
Loader.defaultProps = {
    location: {}
};//设置默认属性

//导出组件
export default Loader;