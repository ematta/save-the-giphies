import Vue from 'vue';
import Vuex from 'vuex';
import Cookies from 'js-cookie';

import {
  giphySearchApi,
  loginUserApi,
  registerUserApi,
  saveUserGiphyApi,
  getUserGiphiesApi,
  getUserInfoApi,
  deleteUserGiphyApi,
  addTagToGiphyApi,
  getTagsToGiphyApi,
} from '@/api';
import { isValidJwt, EventBus } from '@/utility';

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    query: '',
    results: {},
    offset: 0,
    limit: 25,
    page: 1,
    view: 'search',
    jwt: '',
    user: {},
    errorMessage: '',
    giphies: [],
    giphy: {},
    tags: [],
    isAuthenticated: false,
  },
  actions: {
    login(context, user) {
      return loginUserApi(user)
        .then(response => context.commit('setJwt', response.data))
        .catch((error) => {
          EventBus.$emit('errorMessage', error);
        });
    },
    getUserInfo(context) {
      return getUserInfoApi(context.state.jwt)
        .then((response) => {
          context.commit('setUser', response);
        })
        .catch((error) => {
          EventBus.$emit('errorMessage', error);
        });
    },
    registerUser(context, user) {
      return registerUserApi(user)
        .catch((error) => {
          EventBus.$emit('errorMessage', error);
        });
    },
    giphySearch(context) {
      const postData = {
        q: context.state.query,
        offset: context.state.offset,
        limit: context.state.limit,
      };
      return giphySearchApi(postData)
        .then((response) => {
          context.commit('setResults', response.data);
        })
        .catch((error) => {
          EventBus.$emit('errorMessage', error);
        });
    },
    setSingleGiphy(context, giphyId) {
      context.getters.giphies.forEach((giphy) => {
        if (giphyId === giphy.id) {
          context.commit('setGiphy', giphy);
        }
      });
    },
    setSingleGiphyFromResults(context, giphyId) {
      context.getters.results.forEach((giphy) => {
        if (giphyId === giphy.id) {
          context.commit('setGiphy', giphy);
        }
      });
    },
    saveUserGiphy(context, giphyId) {
      return saveUserGiphyApi(giphyId, context.state.jwt)
        .then(context.commit('setFlash', 'Saved gif'))
        .catch((error) => {
          EventBus.$emit('errorMessage', error);
        });
    },
    deleteUserGiphy(context, giphyId) {
      return deleteUserGiphyApi(giphyId, context.state.jwt)
        .then(() => {
          const newGiphies = [];
          context.getters.giphies.forEach((giphy) => {
            if (giphyId !== giphy.id) {
              newGiphies.push(giphy);
            }
          });
          context.commit('setUserGiphies', newGiphies);
          context.commit('setGiphy', {});
        })
        .catch((error) => {
          EventBus.$emit('errorMessage', error);
        });
    },
    addTagToGiphy(context, payload) {
      return addTagToGiphyApi(payload, context.state.jwt)
        .then(context.dispatch('getTagsToGiphy', payload.giphyId), payload)
        .catch((error) => {
          EventBus.$emit('errorMessage', error);
        });
    },
    getTagsToGiphy(context, giphyId) {
      return getTagsToGiphyApi(giphyId, context.getters.jwt)
        .then((response) => {
          context.commit('setTags', response.data);
        })
        .catch((error) => {
          EventBus.$emit('errorMessage', error);
        });
    },
    getUserGiphies(context) {
      return getUserGiphiesApi(context.state.jwt)
        .then((response) => {
          const userGiphies = [];
          response.data.forEach((giphy) => {
            userGiphies.push(giphy.data);
          });
          context.commit('setUserGiphies', userGiphies);
        })
        .catch((error) => {
          EventBus.$emit('errorMessage', error);
        });
    },
    checkIfLoggedInAlready(context) {
      const token = Cookies.get('Token');
      if (token && isValidJwt(token)) {
        context.commit('setJwtSanCookie', token);
      }
    },
  },
  mutations: {
    setErrorMessage(state, errorMessage) {
      state.errorMessage = errorMessage;
    },
    setTags(state, payload) {
      state.tags.push(payload);
    },
    deleteTags(state, payload) {
      const newTags = [];
      state.tags.forEach((tag) => {
        if (tag.tag !== payload.tag && tag.giphyId !== payload.giphyId) {
          newTags.push(tag);
        }
      });
      state.tags = newTags;
    },
    setUserGiphies(state, giphies) {
      state.giphies = giphies;
    },
    setFlash(state, msg) {
      state.flash = msg;
    },
    setQuery(state, query) {
      state.query = query;
    },
    setResults(state, results) {
      state.results = results;
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
    setJwt(state, payload) {
      state.jwt = payload.token;
      state.user = payload.user;
      Cookies.set('Token', payload.token, { expires: 1 / 48, path: '' });
      state.isAuthenticated = isValidJwt(payload.token);
    },
    setJwtSanCookie(state, payload) {
      state.jwt = payload.token;
      state.user = payload.user;
      state.isAuthenticated = isValidJwt(payload.token);
    },
    setUser(state, user) {
      state.user.name = user.data.user.name;
      state.user.email = user.data.user.email;
      state.user.id = user.data.user.id;
    },
    logout(state) {
      state.jwt = '';
      state.user = {};
      Cookies.remove('Token');
      state.isAuthenticated = false;
    },
    setGiphy(state, giphy) {
      state.giphy = giphy;
    },
  },
  getters: {
    results: state => state.results,
    offset: state => state.offset,
    limit: state => state.limit,
    page: state => state.page,
    view: state => state.view,
    jwt: state => state.jwt,
    user: state => state.user,
    giphies: state => state.giphies,
    giphy: state => state.giphy,
    isAuthenticated: state => state.isAuthenticated,
    tags: state => state.tags,
  },
});

export default store;
