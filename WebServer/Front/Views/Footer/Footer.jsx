import Component from '../../Components/Component'

class Footer extends Component {
    constructor(props) {
        super(props);
    }

    componentDidMount() {

    }

    render() {
        return (
            <div className='footer'></div>
        )
    }
}

Footer.propTypes = {//属性校验器，表示改属性必须是bool，否则报错

}
Footer.defaultProps = {};//设置默认属性

//导出组件
export default Footer;