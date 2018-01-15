import css from './Scss/Main.scss';
class Header extends React.Component {
	constructor(props){
		super(props);
	}
    search(){
        let val = $(this.refs.input).val()
        this.props.search(val)
    }
    scan(){
        new Promise((resolve,reject)=>{
            request.get('http://localhost:8000/scan/')
                   .end(function(err, res){
                        if(res.ok){
                            resolve(JSON.parse(res.text))
                        }else{
                            reject(err)
                        }
                   })
        }).then((data)=>{
            console.log(data)
        })
    }
    render() {
        return (
            <div className="header">
                <input ref='input'/>
                <button onClick={this.search.bind(this)}>搜索</button>
                <button onClick={this.scan.bind(this)}>扫描</button>
                <button onClick={this.scan.bind(this)}>爬取</button>
            </div>
        )
    }
}

Header.PropTypes = {
    
}

Header.defaultProps = {
    
}

//导出组件
export default Header;