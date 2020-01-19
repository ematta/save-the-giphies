import Vue from 'vue';
import Vuex from 'vuex';

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
  removeTagFromGiphyApi,
} from '@/api';
import { isValidJwt, jwtGetExpireTime, EventBus } from '@/utility';

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
        .then((response) => {
          context.commit('setJwt', response.data);
        })
        .catch((error) => {
          EventBus.$emit('errorMessage', error);
        });
    },
    registerUser(context, user) {
      return registerUserApi(user)
        .then(() => {
          EventBus.$emit('changeView', 'login');
        })
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
        .then(() => {
          context.dispatch('getUserGiphies')
            .then(() => {
              EventBus.$emit('changeView', 'profile');
            });
        })
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
          EventBus.$emit('changeView', 'profile');
        })
        .catch((error) => {
          EventBus.$emit('errorMessage', error);
        });
    },
    addTagToGiphy(context, payload) {
      return addTagToGiphyApi(payload, context.state.jwt)
        .then(() => {
          context.dispatch('getTagsToGiphy', payload.giphyId);
        })
        .catch((error) => {
          EventBus.$emit('errorMessage', error);
        });
    },
    getTagsToGiphy(context, giphyId) {
      return getTagsToGiphyApi(giphyId, context.getters.jwt)
        .then((response) => {
          context.commit('setTags', response.data);
          EventBus.$emit('changeView', 'giphy');
        })
        .catch((error) => {
          EventBus.$emit('errorMessage', error);
        });
    },
    removeTagFromGiphy(context, payload) {
      return removeTagFromGiphyApi(payload, context.getters.jwt)
        .then(() => {
          context.dispatch('getTagsToGiphy', payload.giphyId)
            .then(() => {
              EventBus.$emit('changeView', 'giphy');
            });
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
      return new Promise((resolve) => {
        const token = Vue.$cookies.get('token');
        if (token && isValidJwt(token)) {
          context.commit('setJwtSansCookie', token);
          resolve();
        }
      })
        .then(() => {
          context.dispatch('getUserInfo');
        });
    },
  },
  mutations: {
    setErrorMessage(state, errorMessage) {
      state.errorMessage = errorMessage;
    },
    setTags(state, payload) {
      state.tags = payload;
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
      state.isAuthenticated = isValidJwt(payload.token);
      Vue.$cookies.set('token', payload.token, jwtGetExpireTime(payload.token));
    },
    setJwtSansCookie(state, token) {
      state.jwt = token;
      state.isAuthenticated = isValidJwt(token);
    },
    setUser(state, user) {
      state.user.name = user.data.user.name;
      state.user.email = user.data.user.email;
      state.user.id = user.data.user.id;
    },
    logout(state) {
      state.jwt = '';
      state.user = {};
      state.isAuthenticated = false;
      Vue.$cookies.remove('token');
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
