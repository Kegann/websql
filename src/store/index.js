import Vue from "vue";
import Vuex from "vuex";
import permission from './modules/permission.js'
import user from './modules/user.js'
import app_config from './modules/app_config.js'
import getters from './getter'

Vue.use(Vuex);

export default new Vuex.Store({
  state: {},
  mutations: {},
  actions: {},
  modules: {
    permission,
    user,
    app_config
  },
  getters
});
