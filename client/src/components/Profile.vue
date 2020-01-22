<template>
  <div v-if="isAuthenticated">
    <br />
    <p> Here are your gifs </p>
    <div v-for="giphy in giphies" :key="giphy.id">
      <div>

        <router-link
          class="nav-item nav-word"
          :to="{ name: 'Giphy', params: { giphyId: giphy.id } }"
        >
          <img
          v-bind:src="giphy.images.preview_gif.url"
        />
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';

export default {
  name: 'Profile',
  computed: mapState(['isAuthenticated', 'giphies']),
  beforeMount() {
    this.$store.dispatch('getUserGiphies');
  },
};
</script>
