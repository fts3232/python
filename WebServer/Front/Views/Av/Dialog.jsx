import css from './Scss/Dialog.scss';
import Component from '../../Components/Component';
class Dialog extends Component {
	constructor(props){
		super(props);
        this.state = {
            data:{},
            thumb_index:0,
        }
	}
    parent(){
        return this.context.component
    }
    enlargeImage(src,i){
        let _this = this
        if(src.indexOf('cover.jpg')==-1){
            this.setState({'thumb_index':i})
        }
        $(this.refs.big_image).find('img').attr('src',src)
        $(_this.refs.big_image).addClass('show')
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
        $(this.refs.big_image).removeClass('show')
    }
    play(identifier){
        this.parent().socketSend('play',identifier)
    }
    setInfo(){
        var identifier=prompt("输入番号","")
        if (identifier!=null && identifier!=""){
            this.parent().socketSend('update-movie',{'identifier':identifier,'movie_id':this.state.data.MOVIE_ID})
            this.parent().refs.log.resetData();
            this.parent().refs.log.setState({'toggle':true});
        }
    }
    searchStar(id){
        this.parent().search({'star':id})
        this.onClose()
    }
    searchTag(id){
        this.parent().search({'tag':id})
        this.onClose()
    }
    openDir(identifier){
        this.parent().socketSend('openDir',identifier)
    }
    thumbPrev(){
        let currentIndex = this.state.thumb_index
        if(currentIndex==0){
            currentIndex = this.state.data.SAMPLE.length - 1
        }else{
            currentIndex -= 1
        }
        let src = this.state.data.SAMPLE[currentIndex].URL
        $(this.refs.big_image).find('img').attr('src',src)
        this.setState({'thumb_index':currentIndex})
    }
    thumbNext(){
        let currentIndex = this.state.thumb_index
        if(currentIndex==this.state.data.SAMPLE.length - 1){
            currentIndex = 0
        }else{
            currentIndex += 1
        }
        let src = this.state.data.SAMPLE[currentIndex].URL
        $(this.refs.big_image).find('img').attr('src',src)
        this.setState({'thumb_index':currentIndex})
    }
    render() {
        let data = this.state.data
        let star = []
        if(typeof data.STAR != 'undefined' && data.STAR != '' && data.STAR !=null){
            data.STAR.map((v)=>{
                star.push(
                    <div className="star-item" onClick={this.searchStar.bind(this,v.STAR_ID)}>
                        <img src={v.IMAGE} />
                        <span className="tag">{v.STAR_NAME}</span>
                    </div>
                )
            })
        }else{
            star = (<span>暂无演员信息</span>)
        }               
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
                            <div className="tag-box">
                                {typeof data.TAG != 'undefined' && data.TAG != '' && data.TAG !=null && data.TAG.map((v)=>{
                                    return (<span className="tag" onClick={this.searchTag.bind(this,v.TAG_ID)}>{v.TAG_NAME}</span>)
                                })}
                            </div>
                            <div className="button-box">
                                <button onClick={this.downloadShow.bind(this)}>下载</button>
                                <button onClick={this.play.bind(this,data.IDENTIFIER)}>播放</button>
                                <div className="row">
                                    <button className="set-info" onClick={this.setInfo.bind(this)}>设置资料来源</button>
                                    <button onClick={this.openDir.bind(this,data.IDENTIFIER)}>打开文件夹</button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="star">
                        {star}
                    </div>
                    <div className="thumb">
                        <ul>
                            {typeof data.SAMPLE != 'undefined' && data.SAMPLE.map((v,k)=>{
                                return (
                                    <li  onClick={this.enlargeImage.bind(this,v.URL,k)}><img src={v.URL}/></li>
                                )
                            })}
                        </ul>
                    </div>
                </div>
                <div className="big-image" ref="big_image">
                    <div className="image-wrapper">
                        <div>
                            <span className="close" onClick={this.bigImageClose.bind(this)}>X</span>
                            <img src="http://dev.www.202.hk/images/company/license1.jpg"/>
                            <span onClick={this.thumbPrev.bind(this)} className="prev-btn">&lt;</span>
                            <span onClick={this.thumbNext.bind(this)} className="next-btn">&gt;</span>
                        </div>
                    </div>
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

Dialog.contextTypes = {
  component: React.PropTypes.any
};

Dialog.PropTypes = {

}

Dialog.defaultProps = {
    
}

//导出组件
export default Dialog;