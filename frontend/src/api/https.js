import axios from 'axios'
import {Message} from 'element-ui'
import router from '../router'
import qs from 'qs'
 
// let base = 'http://127.0.0.1:5000/'  //配置接口地址
 
//请求拦截器
axios.interceptors.request.use(config=>{
  //如果存在token，请求携带这个token
  if(window.sessionStorage.getItem('tokenStr')){
    config.headers['Authorization']=window.sessionStorage.getItem('tokenStr');
  }
  return config;
},error=>{
  console.log(error);
})

//响应拦截器
axios.interceptors.response.use( success =>{
  //业务逻辑错误
  if(success.status && success.status==200){
    if(success.data.code==500||success.data.code==401||success.data.code==403){
      Message.error({message:success.data.message});
      return;
    }
    if(success.data.message){
      Message.success({message:success.data.message});
    }
    //返回成功的数据
    return success.data;
  }
  //return response;
},error=> {
  //连接接口失败
  if(error.response.code==504||error.response.code==404){
    Message.error({message:'服务器被吃了'});
  }else if(error.response.code==403){
    Message.error({message:'权限不足'});
  }else if(error.response.code==401){
    Message.error({message:'尚未登录，请登录'});
    router.replace('/login');
  }else{
    if(error.response.data.message){
      Message.error({message:error.response.data.message});
    }else{
      Message.error({message:'未知错误！'});
    }
  }
  return;
});
 
//传输json格式的post请求
export const postRequest=(url,params)=>{
  return axios({
    method:'post',
    url:url,
    data:qs.stringify(params),
    header:{
      'contentType': "application/x-www-form-urlencoded"
    }
  })
}

//传输json格式的编辑请求
export const putRequest=(url,params)=>{
  return axios({
    method:'put',
    url:url,
    data:qs.stringify(params),
    header:{
      'contentType': "application/x-www-form-urlencoded"
    }
  })
}
//传输json格式的get请求
export const getRequest=(url,params)=>{
  return axios({
    method:'get',
    url:url,
    params,
    header:{
      'contentType': "application/x-www-form-urlencoded"
    }
  })
}
//传输json格式的delete请求
export const deleteRequest=(url,params)=>{
  return axios({
    method:'delete',
    url:url,
    params:params,
    header:{
      'contentType': "application/x-www-form-urlencoded"
    }
  })
}