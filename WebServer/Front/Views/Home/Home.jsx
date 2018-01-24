import css from './Scss/Main.scss';
import Component from '../../Components/Component'
class Home extends Component {
	constructor(props){
		super(props);
	}
  componentDidMount(){
    /*var f=document.getElementById('fall');  
        f.style.right='0px';  
        f.style.bottom='40px';  
        i&&clearInterval(i);  
    var h=1,v=1,hp=(hp>0&&hp<1)?hp:0.2,vp=(vp>0&&vp<1)?vp:0.5,sp=(sp>20 || sp<1000)?sp:30;  
        i=setInterval(function(){  
            if(f){  
                var r=parseInt(f.style.right)+h,b=parseInt(f.style.bottom)-v;  
                f.style.right=r+'px';  
                f.style.bottom=b+'px';  
                if(r>1000)clearInterval(i);  
                if(b>-210){  
                    v+=2  
                } else {  
                    h=(v>0)?v*hp:0;  
                    v*=(v>0)?-1*vp:0  
                }  
            }  
        },sp);  */
  }

  render() {
    return (
        <div className='home'>
          <div className="blue" ref="blue"></div>
          <div className="red"></div>
        </div>
    )
  }
}

Home.propTypes={//属性校验器，表示改属性必须是bool，否则报错
  
}
Home.defaultProps={
  
};//设置默认属性

//导出组件
export default Home;