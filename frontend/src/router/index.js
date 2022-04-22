// import { queue } from 'jquery'
import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'


Vue.use(VueRouter)

const routes = [
  {
    //登录
    path: '/',
    name: 'Login',
    component: () => import('@/views/login'), 
  },
  {
    path: '/home',
    name: 'Home',
    component: Home,
    children: [
      {
        // 主页
        path: '/homepage',
        name: 'Homepage',
        component: () => import('@/views/homepage')
      },
      {
        // 项目管理页面
        path: '/project',
        name: 'Project',
        component: () => import('@/views/project')
      },
      {
        // 项目-届次页面
        path: '/sessions:project_id,project_name',
        name: 'Sessions',
        component: () => import('@/views/sessions')
      },
      {
        // 届次-证书页面
        path: '/session-certificate:session_id,number',
        name: 'Session-certificate',
        component: () => import('@/views/session-certificate')
      },
      {
        // 证书管理详情页
        path: '/certificate',
        name: 'Certificate',
        component: () => import('@/views/certificate'),
      },
      {
        // 自定义证书
        path: '/design',
        name: 'Design',
        component: () => import('@/views/design'),
      },
      {
        // 后台管理
        path: '/backstage',
        name: 'Backstage',
        component: () => import('@/views/backstage')
      },
      {
        // 个人信息
        path: '/information',
        name: 'Information',
        component: () => import('@/views/information'),
      },
    ]
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
