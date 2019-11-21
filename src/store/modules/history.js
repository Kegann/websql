const history = {
  state: {
    active: 0,
    sql_line: "",
    sql_res: "",
  },

  mutations: {
    SET_ACTIVE: (state, active) => {
      state.active = active
    },
    SET_LINE: (state, line) => {
      state.sql_line = line
    },
    SET_RES: (state, sql_res) => {
      state.sql_res = sql_res
    }
  },

  actions: {
    DeactiveHis( {commit} ) {
      commit('SET_ACTIVE', 0);
      commit('SET_LINE', "");
      commit('SET_RES', "");
    },

    ActiveHis( {commit}, payload) {
      // console.log("ActiveHis...", payload)
      if (payload.line) {
        commit('SET_ACTIVE', 1);
        commit('SET_LINE', payload.line);
        commit('SET_RES', payload.res);
      }
    }
  }
}

export default history
