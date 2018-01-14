import css from './Scss/Main.scss';
class Dialog extends React.Component {
	constructor(props){
		super(props);
        this.state = {
            data:{}
        }
	}
    componentDidMount(){
        
    }
    enlargeImage(src){
        $(this.refs.big_image).show()
        $(this.refs.big_image).find('img').attr('src',src)
    }
    show(){
        $(this.refs.dialog).show()
        $('body').css({overflow: 'hidden'})
    }
    onClose(){
        $(this.refs.dialog).hide()
        $('body').css({overflow: 'auto'})
    }
    onCloseDownload(){
        $(this.refs.download).hide()
    }
    downloadShow(){
        $(this.refs.download).show()
    }
    downloadHide(){
        $(this.refs.download).hide()
    }
    bigImageClose(){
        $(this.refs.big_image).hide()
    }
    play(identifier){
        new Promise((resolve,reject)=>{
            request.get('http://localhost:8000/play/?identifier='+identifier)
                   .end(function(err, res){
                        if(res.ok){
                            resolve(JSON.parse(res.text))
                        }else{
                            reject(err)
                        }
                   })
        }).then((data)=>{
            if(!data.status)
                alert(data.msg)
        })
    }
    render() {
        let data = this.state.data
        return (
            <div className="dialog" ref="dialog">
                <div className="wrapper">
                    <div className="close" onClick={this.onClose.bind(this)}>X</div>
                    <h3>{data.TITLE}</h3>
                    <div className="box">
                        <div className="image">
                            <img src={data.IMAGE}  onClick={this.enlargeImage.bind(this,data.IMAGE)}/>
                        </div>
                        <div className="info">
                            <p>番号：{data.IDENTIFIER}</p>
                            <p>类别：</p>
                            <p>{data.TAG}</p>
                            <div className="button-box">
                                <button onClick={this.downloadShow.bind(this)}>下载</button>
                                <button onClick={this.play.bind(this,data.IDENTIFIER)}>播放</button>
                            </div>
                        </div>
                    </div>
                    <div className="thumb">
                        <ul>
                            {typeof data.SAMPLE != 'undefined' && data.SAMPLE.map((v)=>{
                                return (
                                    <li><img src={v} onClick={this.enlargeImage.bind(this,v)}/></li>
                                )
                            })}
                        </ul>
                    </div>
                </div>
                <div className="big-image" ref="big_image" onClick={this.bigImageClose.bind(this)}>
                    <img />
                </div>
                <div className="download" ref="download">
                    <div className="wrapper">
                        <div className="close" onClick={this.downloadHide.bind(this)}>X</div>
                        <h4>下载链接</h4>
                        {typeof data.LINK != 'undefined' && data.LINK.map((v)=>{
                            return (<a href={v.LINK}>{v.LINK}</a>)
                        })}
                    </div>
                   
                </div>
            </div>
        )
    }
}

Dialog.PropTypes = {

}

Dialog.defaultProps = {
    
}

//导出组件
export default Dialog;