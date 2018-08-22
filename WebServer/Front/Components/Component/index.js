import classnames from 'classnames';

class Component extends React.Component {
    classNames(...args){
        return classnames(...args);
    }
    style(args) {
        return Object.assign({}, args, this.props.style)
    }
    getParams(key){
        let {search} = this.context.router.route.location;
        if(search != ''){
            search = search.substring(1);
            search = search.split('=');
            for (let i = 0; i < search.length; i = i + 2) {
                if (search[i] == key) {
                    return search[i + 1];
                }
            }
        }
        return null;
    }
}

Component.PropTypes = {
    className:React.PropTypes.string,
    style:React.PropTypes.object,
}

Component.contextTypes = {
    router: React.PropTypes.Object
}

export default Component;