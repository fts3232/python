var path = require('path');
var env = process.env.NODE_ENV;
var config = {
	//开发环境(dev)
	'development':{
		'ENV':'development',
		'ROOT_PATH':path.resolve(__dirname),
		'ROOT':'/',
		'APP_PATH':path.resolve(path.resolve(__dirname), 'Front'),
		'BUILD_PATH':path.resolve(path.resolve(__dirname), 'Build'),
		'ASSET_PATH':path.resolve(path.resolve(__dirname),'Assets')
	},
	//测试环境(test)
	'test':{
		'ENV':'test',
		'ROOT_PATH':path.resolve(__dirname),
		'ROOT':'/',
		'APP_PATH':path.resolve(path.resolve(__dirname), 'Front'),
		'BUILD_PATH':path.resolve(path.resolve(__dirname), 'Build'),
		'ASSET_PATH':path.resolve(path.resolve(__dirname),'Assets')
	},
	//正式生产环境(production)
	'production':{
		'ENV':'production',
		'ROOT_PATH':path.resolve(__dirname),
		'ROOT':'/',
		'APP_PATH':path.resolve(path.resolve(__dirname), 'Front'),
		'BUILD_PATH':path.resolve(path.resolve(__dirname), 'Build'),
		'ASSET_PATH':path.resolve(path.resolve(__dirname),'Assets')
	}
};
module.exports = config[env];