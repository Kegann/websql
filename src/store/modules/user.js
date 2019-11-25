const user = {
    state: {
        token: null,
        userName: null,
        userId: null,
        avatar: null,
    },

    mutations: {
        SET_TOKEN: (state, token) => {
            state.token = token
        },
        SET_NAME: (state, name) => {
            state.userName = name
        },
        SET_ID: (state, id) => {
            state.userId = id
        }
    },

    actions: {
        SetUserInfo( {commit} ) {
            let token = window.localStorage.getItem('websql-token');
            let name = JSON.parse(atob(token.split('.')[1])).user_name;
            let id = JSON.parse(atob(token.split('.')[1])).user_id;
            commit('SET_NAME', name);
            commit('SET_ID', id)
        },
        Logout({commit}) {
            window.localStorage.setItem('websql-token', null);
            commit('SET_NAME', null);
            commit('SET_ID', null);
            // 注销时，删掉webStorage中保存的store信息，防止多用户互串信息
            if (window.localStorage.getItem("store")) {
              window.localStorage.removeItem("store")
            }
        }
    }
}

export default user
