<template>
  <div>
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
            <div v-if="$store.getters.isAuthenticated === false">
              <a class="button is-large is-primary" @click.stop="setLogin">Login</a>
              &nbsp;&nbsp;&nbsp;
              <a class="button is-large is-primary" @click.stop="setRegister">Register</a>
            </div>
            <div v-if="$store.getters.isAuthenticated === true">
              <a class="button is-large is-primary" @click.stop="setProfile">Profile </a>
              &nbsp;&nbsp;&nbsp;
              <a class="button is-large is-primary" @click.stop="setSearch">Search </a>
              &nbsp;&nbsp;&nbsp;
              <a class="button is-large is-primary" @click.stop="logout">Logout </a>
            </div>
          </div>
        </div>
      </section>
    </div>
    <div v-if="$store.getters.view === 'search'">
      <Search />
      <Results />
    </div>
    <div v-if="$store.getters.view === 'login'">
      <Login />
    </div>
    <div v-if="$store.getters.view === 'register'">
      <Register />
    </div>
    <div v-if="$store.getters.view === 'profile'">
      <Profile />
    </div>
  </div>
</template>

<script>
import Search from '@/components/Search.vue';
import Results from '@/components/Results.vue';
import Login from '@/components/Login.vue';
import Register from '@/components/Register.vue';
import Profile from '@/components/Profile.vue';

export default {
  name: 'Home',
  components: {
    Search,
    Results,
    Login,
    Register,
    Profile,
  },
  mounted() {
    this.$root.$on('changeView', (view) => {
      this.$store.commit('setView', view);
    });
  },
  methods: {
    setSearch() {
      return this.$root.$emit('changeView', 'search');
    },
    setLogin() {
      return this.$root.$emit('changeView', 'login');
    },
    setProfile() {
      this.$store.dispatch('getUserGiphies')
        .then(() => {
          this.$root.$emit('changeView', 'profile');
        });
    },
    setRegister() {
      return this.$root.$emit('changeView', 'register');
    },
    logout() {
      this.$store.commit('logout');
      return this.$root.$emit('changeView', 'search');
    },
  },
};
</script>
