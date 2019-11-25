import axios from 'axios'
import store from './store'
import router from './router'
import { Message } from 'element-ui'

// test backend 24812
// prod backend 24802
axios.defaults.baseURL = 'http://10.17.0.65:24812'
//超时时间120s
axios.defaults.timeout = 120000

//全局拦截request,带上token
axios.interceptors.request.use( config => {
    let token = window.localStorage.getItem('websql-token');
    if (token) {
        // console.log("take token -----------", token)
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config
}, error => {
    // console.log(error);
    Promise.reject(error);
})

// 全局response拦截
axios.interceptors.response.use( response => {
  console.log("GLOBAL response: ", response)
  let token = response.data.token;
  if (token) {
    console.log("Token changed....")
    window.localStorage.setItem('websql-token', token);
  }
  return response
}, error => {
    if (error.response) {
        // console.log("ERROR: ", error.response)
        switch (error.response.status) {
            case 401:
               if (router.currentRoute.path !== '/auth/login') {
                   Message({
                       type: 'warning',
                       message: error.response.message ? error.response.message : error.response.data.message,
                       duration: 1 * 1000
                   })
                   store.dispatch('Logout');
                   router.replace({
                       path: '/auth/login',
                       query: { redirect: router.currentRoute.path },
                   })
               }
        }
    } else {
        // console.log(error)
    }
    return Promise.reject(error)
})

export default axios
