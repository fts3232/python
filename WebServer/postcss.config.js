var path = require('path');
var envConfig = require('./env.config.js');
var BUILD_PATH = envConfig.BUILD_PATH;
var env = envConfig.ENV;
var config = {
	plugins: [
		require('autoprefixer')({ /* ...options */ }),
		require('postcss-at2x')(),
	]
}
if(env == 'production'){
	var sprites =  require('postcss-sprites')({
    	//retina: true,//支持retina，可以实现合并不同比例图片
	    verbose: true,
	    spritePath: './',//雪碧图合并后存放地址
	    stylesheetPath: BUILD_PATH+'/css/',
	    basePath: './',
	    filterBy: function (image) {
	        //过滤一些不需要合并的图片，返回值是一个promise，默认有一个exist的filter
	        if (image.originalUrl.indexOf('?__sprites') === -1) {
	            return Promise.reject();
	        }
	        return Promise.resolve();
	    },
	    groupBy: function (image) {
	        //将图片分组，可以实现按照文件夹生成雪碧图
	        var groupName = '/sprite';
	        var url = path.dirname(image.url);
	            url = url.replace(/\.\.\//g,'');
	            url = url.replace(/\.\//g,'');
	        if(image.url.indexOf('@2x')!==-1){
	        	groupName = '/sprite@2x';
	        }
	        else if(image.url.indexOf('@3x')!==-1){
	        	groupName = '/sprite@3x';
	        }
	        return Promise.resolve(url+groupName);
	    },
	    hooks:{
	    	onSaveSpritesheet: function(opts, spritesheet) {
	            // We assume that the groups is not an empty array
	            var filenameChunks = spritesheet.groups.concat(spritesheet.extension);
	            return path.join(opts.spritePath, filenameChunks.join('.'));
	        }
	    }
    })
	config.plugins.push(sprites);
}
module.exports = config;