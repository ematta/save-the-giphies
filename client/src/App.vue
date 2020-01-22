<template>
  <div id="app">
    <p class="subtitle error-msg" @click.stop="clearMessage">{{ errorMessage }}</p>
    <div>
      <!-- <h1> {{ $log(HOW TO GET LOGGER) }} </h1> -->
      <section class="hero is-primary">
        <div class="hero-body">
          <div class="container has-text-centered">
            <img src="./assets/logo.png" width=50 height=50 />
            <h2 class="title">
              Save the Giphies
            </h2>
          </div>
          <div>
            <router-link
              class="nav-item nav-word"
              :to="{ name: 'Search' }"
            >
              Search
            </router-link>
            <div v-if="$store.getters.isAuthenticated">
              <router-link
                class="nav-item nav-word"
                :to="{ name: 'Profile' }"
              >
                Profile
              </router-link>
              <router-link
                class="nav-item nav-word"
                :to="{ name: 'Logout' }"
              >
                Logout
              </router-link>
            </div>
            <div v-else>
              <router-link
                class="nav-item nav-word"
                :to="{ name: 'Login' }"
              >
                Login
              </router-link>
              <router-link
                class="nav-item nav-word"
                :to="{ name: 'Register' }"
              >
                Register
              </router-link>
            </div>
          </div>
        </div>
      </section>
    </div>
    <router-view />
  </div>
</template>

<script>
import { mapState } from 'vuex';

export default {
  name: 'App',
  computed: mapState(['view', 'errorMessage']),
  created() {
    this.$store.dispatch('checkIfLoggedInAlready');
  },
  methods: {
    clearMessage() {
      this.$store.commit('setErrorMessage', '');
    },
  },
};
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 30px;
}
</style>
