<template>
  <div>
    <p class="subtitle error-msg" @click.stop="clearMessage">{{ errorMessage }}</p>
    <div>
      <!-- <h1> {{ $log(HOW TO GET LOGGER) }} </h1> -->
      <section class="hero is-primary">
        <div class="hero-body">
          <div class="container has-text-centered">
            <img src=".././assets/logo.png" width=50 height=50 />
            <h2 class="title">
              Save the Giphies
            </h2>
          </div>
          <div>
            <a class="button is-large is-primary" @click.stop="setSearch">Search </a>
            &nbsp;&nbsp;&nbsp;
            <div v-if="$store.getters.isAuthenticated === false">
              <a class="button is-large is-primary" @click.stop="setLogin">Login</a>
              &nbsp;&nbsp;&nbsp;
              <a class="button is-large is-primary" @click.stop="setRegister">Register</a>
            </div>
            <div v-if="$store.getters.isAuthenticated === true">
              <a class="button is-large is-primary" @click.stop="setProfile">Profile </a>
              &nbsp;&nbsp;&nbsp;
              <a class="button is-large is-primary" @click.stop="logout">Logout </a>
            </div>
          </div>
        </div>
      </section>
    </div>
    <div v-if="giphy()">
      <Giphy />
    </div>
    <div v-else-if="login()">
      <Login />
    </div>
    <div v-else-if="register()">
      <Register />
    </div>
    <div v-else-if="profile()">
      <Profile />
    </div>
    <div v-else>
      <Search />
      <Results />
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';
import Search from '@/components/Search.vue';
import Results from '@/components/Results.vue';
import Login from '@/components/Login.vue';
import Register from '@/components/Register.vue';
import Profile from '@/components/Profile.vue';
import Giphy from '@/components/Giphy.vue';
import { EventBus } from '@/utility';

export default {
  name: 'Home',
  components: {
    Search,
    Results,
    Login,
    Register,
    Profile,
    Giphy,
  },
  computed: mapState(['view', 'errorMessage']),
  data() {
    return {
      search: () => this.view === 'search',
      login: () => this.view === 'login',
      register: () => this.view === 'register',
      profile: () => this.view === 'profile',
      giphy: () => this.view === 'giphy',
    };
  },
  mounted() {
    EventBus.$on('changeView', (view) => {
      this.$store.commit('setView', view);
    });
    EventBus.$on('errorMessage', (msg) => {
      this.$store.commit('setErrorMessage', msg);
    });
  },
  methods: {
    async clearMessage() {
      this.$store.commit('setErrorMessage', '');
    },
    async setSearch() {
      await EventBus.$emit('changeView', 'search');
    },
    async setLogin() {
      await EventBus.$emit('changeView', 'login');
    },
    async setProfile() {
      await this.$store.dispatch('getUserGiphies')
        .then(() => {
          EventBus.$emit('changeView', 'profile');
        });
    },
    async setRegister() {
      await EventBus.$emit('changeView', 'register');
    },
    async logout() {
      await this.$store.commit('logout');
      await EventBus.$emit('changeView', 'search');
    },
  },
  beforeDestroy() {
    EventBus.$off('errorMessage');
  },
};
</script>
