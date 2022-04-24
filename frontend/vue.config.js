
// let proxyObj={}

// proxyObj['/']={
//   //websocker
//   ws:false,
//   //目标地址（后端端口地址）
//   target:"http://127.0.0.1:5000/",
//   // target:"http://localhost:8081/login",
//   // 发送请求头host会被设置target
//   ChangeOrigin:true,
//   //不重写请求地址
//   pathRewrite:{
//     '^':'/'
//   }
// }
// module.exports = {
//   devServer:{
//     host:'localhost',
//     port:8080,
//     proxy:proxyObj
//   }
// }



// module.exports = {

//   assetsDir: process.env.NODE_ENV === 'production'? '../static' : 'static',

//   publicPath: process.env.NODE_ENV === 'production'? './' : '/',

//   outputDir: path.resolve(__dirname, '../templates')

// }

