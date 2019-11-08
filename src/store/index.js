import Vue from "vue";
import Vuex from "vuex";
import permission from './modules/permission.js'
import getters from './getter'

Vue.use(Vuex);

export default new Vuex.Store({
  state: {},
  mutations: {},
  actions: {},
  modules: {
    permission,
  },
  getters
});
