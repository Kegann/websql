import Vue from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import router from "./router";
import store from "./store";
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import axios from './http'
Vue.prototype.$axios = axios;

Vue.config.productionTip = false;
Vue.use(ElementUI)

new Vue({
  router,
  store,
  created() {
    //页面加载时读取localStorage里的状态信息
    if (window.localStorage.getItem("store")) {
      this.$store.replaceState(Object.assign({}, this.$store.state, JSON.parse(window.localStorage.getItem("store"))))
    }
    //页面刷新前将vuex中的信息保存在localStorage里
    window.addEventListener("beforeunload", () => {
      window.localStorage.setItem("store", JSON.stringify(this.$store.state))
    })
  },
  render: h => h(App)
}).$mount("#app");
