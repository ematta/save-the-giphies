import Vue from 'vue';
import Vuex from 'vuex';

import { giphySearch, authenticate, register } from '@/api';
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
  },
  actions: {
    login(context, user) {
      context.commit('setUser', { user });
      return authenticate(user)
        .then(response => context.commit('setJwt', { jwt: response.data }))
        .catch((error) => {
          EventBus.$emit('failedAuthentication', error);
        });
    },
    registerUser(context, user) {
      context.commit('setUser', { user });
      return register(user)
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
      return giphySearch(postData)
        .then((response) => {
          context.commit('setResults', { response });
        });
    },
  },
  mutations: {
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
      state.user = jwt.user;
    },
    setUser(state, user) {
      state.user = user;
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
    isAuthenticated: state => isValidJwt(state.jwt.token),
  },
});

export default store;
