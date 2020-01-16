import Vue from 'vue';
import Vuex from 'vuex';

import {
  allGiphySearchApi,
  loginUserApi,
  registerUserApi,
  saveUserGiphyApi,
  getUserGiphiesApi,
  getUserInfoApi,
  deleteUserGiphyApi,
} from '@/api';
import { isValidJwt, EventBus } from '@/utility';

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    query: '',
    response: {},
    offset: 0,
    limit: 25,
    page: 1,
    view: 'search',
    jwt: '',
    user: {},
    flash: {},
    giphies: {},
  },
  actions: {
    login(context, user) {
      return loginUserApi(user)
        .then(response => context.commit('setJwt', { jwt: response.data }))
        .catch((error) => {
          EventBus.$emit('failedAuthentication', error);
        });
    },
    getUserInfo(context) {
      return getUserInfoApi(context.state.jwt.token)
        .then((response) => {
          context.commit('setUser', response);
        })
        .catch((error) => {
          EventBus.$emit('failedAuthentication', error);
        });
    },
    registerUser(context, user) {
      return registerUserApi(user)
        .catch((error) => {
          EventBus.$emit('failedRegistering: ', error);
        });
    },
    retrieveGiphies(context) {
      const postData = {
        q: context.state.query,
        offset: context.state.offset,
        limit: context.state.limit,
      };
      return allGiphySearchApi(postData)
        .then((response) => {
          context.commit('setResults', { response });
        });
    },
    saveUserGiphy(context, giphyId) {
      return saveUserGiphyApi(giphyId, context.state.jwt.token)
        .then(context.commit('setFlash', 'Saved gif'));
    },
    deleteUserGiphy(context, giphyId) {
      return deleteUserGiphyApi(giphyId, context.state.jwt.token)
        .then(context.dispatch('getUserGiphies'));
    },
    getUserGiphies(context) {
      return getUserGiphiesApi(context.state.jwt.token)
        .then(response => context.commit('setUserGiphies', { response }));
    },
  },
  mutations: {
    setUserGiphies(state, payload) {
      state.giphies = payload.response.data;
    },
    setFlash(state, msg) {
      state.flash = msg;
    },
    setQuery(state, query) {
      state.query = query;
    },
    setResults(state, payload) {
      state.response = payload.response;
    },
    setOffset(state, offset) {
      state.offset = offset;
    },
    setLimit(state, limit) {
      state.limit = limit;
    },
    setPage(state, page) {
      state.page = page;
    },
    setView(state, view) {
      state.view = view;
    },
    setJwt(state, jwt) {
      localStorage.token = jwt.jwt.token;
      state.jwt = jwt.jwt;
    },
    setUser(state, user) {
      state.user.name = user.data.user.name;
      state.user.email = user.data.user.email;
      state.user.id = user.data.user.id;
    },
    logout(state) {
      state.jwt = '';
      state.user = {};
      localStorage.token = null;
    },
  },
  getters: {
    response: state => state.response,
    offset: state => state.offset,
    limit: state => state.limit,
    page: state => state.page,
    view: state => state.view,
    jwt: state => state.jwt,
    user: state => state.user,
    giphies: state => state.giphies,
    isAuthenticated: state => isValidJwt(state.jwt.token),
  },
});

export default store;
