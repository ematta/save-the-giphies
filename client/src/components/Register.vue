<template>
  <div>
    <section class="hero is-primary">
      <div class="hero-body">
        <div class="container has-text-centered">
          <h2 class="title">Register</h2>
          <p class="subtitle error-msg">{{ errorMsg }}</p>
        </div>
      </div>
    </section>
    <section class="section">
      <div class="container">
        <div class="field">
          <label class="label is-large" for="name">Name:</label>
          <div class="control">
            <input class="input is-large" id="name" v-model="name">
          </div>
        </div>
        <div class="field">
          <label class="label is-large" for="email">Email:</label>
          <div class="control">
            <input type="email" class="input is-large" id="email" v-model="email">
          </div>
        </div>
        <div class="field">
          <label class="label is-large" for="password">Password:</label>
          <div class="control">
            <input type="password" class="input is-large" id="password" v-model="password">
          </div>
        </div>

        <div class="control">
          <a class="button is-large is-success" @click="register">Register</a>
        </div>

      </div>
    </section>

  </div>
</template>

<script>
import { EventBus } from '@/utility';

export default {
  data() {
    return {
      name: '',
      email: '',
      password: '',
      errorMsg: '',
    };
  },
  methods: {
    async register() {
      await this.$store.dispatch('registerUser', { name: this.name, email: this.email, password: this.password })
        .then(() => this.$router.push('/'));
      await this.$root.$emit('changeView', 'login');
    },
  },
  mounted() {
    EventBus.$on('failedRegistering', (msg) => {
      this.errorMsg = msg;
    });
  },
  beforeDestroy() {
    EventBus.$off('failedRegistering');
  },
};
</script>
