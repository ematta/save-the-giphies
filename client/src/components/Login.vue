<template>
  <div>
    <section class="hero is-primary">
      <div class="hero-body">
        <div class="container has-text-centered">
          <h2 class="title">Login</h2>
          <p class="subtitle error-msg">{{ errorMsg }}</p>
        </div>
      </div>
    </section>
    <section class="section">
      <div class="container">
        <div class="field">
          <label class="label is-large" for="email">Email:</label>
          <div class="control">
            <input type="email" class="input is-large" id="email" v-model="email">
          </div>
        </div>
        <div class="field">
          <label class="label is-large" for="password">Password:</label>
          <div class="control">
            <input
              type="password"
              class="input is-large"
              id="password"
              v-model="password"
              @keyup.enter="authenticate"
            >
          </div>
        </div>

        <div class="control">
          <a class="button is-large is-primary" @click="authenticate">Login</a>
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
      email: '',
      password: '',
      errorMsg: '',
    };
  },
  methods: {
    async authenticate() {
      await this.$store.dispatch('login', { email: this.email, password: this.password });
      await this.$store.dispatch('getUserInfo');
      await EventBus.$emit('changeView', 'search');
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
