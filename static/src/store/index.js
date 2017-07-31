import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

const state = {
  authUser: null,
  authenticated: false,
  post: ''
}

const mutations = {
  SET_USER (state, payload) {
    state.authUser = payload || null
  },
  SET_TOKEN (state, payload) {
    state.token = payload || null
  },
  SET_POST (state, payload) {
    state.post = payload
  }
}

const actions = {
  setToken ({ commit }, { payload }) {
    commit('SET_TOKEN', payload)
  },
  updateUser ({ commit }, { payload }) {
    commit('UPDATE_USER', payload)
  },
  login ({ commit }, { email, password }) {
    console.log('Logging in...')
    axios.post('http://127.0.0.1:5000/api/v1/auth/login', {
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email,
        password
      })
    })
    .then((res) => {
      if (res.status === 401) {
        throw new Error('Bad credentials')
      } else {
        return res.json()
      }
    })
    .then((authToken) => {
      commit('SET_TOKEN', authToken)
      // commit('SET_USER', authUser)
    })
  },
  logout ({ commit }) {
    return fetch('/api/logout', {
      // Send the client cookies to the server
      credentials: 'same-origin',
      method: 'POST'
    })
    .then(() => {
      commit('SET_USER', null)
    })
  },
  getPost ({ commit }) {
    axios.get('/test')
    .then((res) => {
      console.log(res)
      commit('SET_POST', res)
    })
  }
}

const getters = {
  isAuthenticated (state) {
    return !!state.authUser
  },
  loggedUser (state) {
    return state.authUser
  },
  showPost (state) {
    return state.post
  }
}

export default new Vuex.Store({
  state,
  getters,
  actions,
  mutations
})
