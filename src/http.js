import vue from 'vue'
import axios from 'axios'
import router from './router'
import store from './store'

axios.defaults.baseURL = 'http://10.17.0.65:24802'
//超时时间60s
axios.defaults.timeout = 60000

export default axios
