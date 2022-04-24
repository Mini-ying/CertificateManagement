import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import axios from 'axios';
import VueKonva from 'vue-konva'
Vue.prototype.$axios = axios;

import { postRequest } from './api/https'
import { putRequest } from './api/https'
import { getRequest } from './api/https'
import { deleteRequest } from './api/https'
import{postFileRequest}from './api/https'

Vue.use(ElementUI)
Vue.use(VueKonva)

Vue.prototype.postRequest=postRequest;
Vue.prototype.putRequest=putRequest;
Vue.prototype.getRequest=getRequest;
Vue.prototype.deleteRequest=deleteRequest;
Vue.prototype.postFileRequest=postFileRequest;

Vue.config.productionTip = false
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

export default Vue
