const app_config = {
    state: {
        login_reminder: true
    },

    mutations: {
        SET_LOGIN_REMINDER: (state, flag) => {
            state.login_reminder = flag
        }
    },

    actions: {
        SetLoginReminder( {commit}, flag){
            commit('SET_LOGIN_REMINDER', flag)
        }
    }
}

export default app_config
