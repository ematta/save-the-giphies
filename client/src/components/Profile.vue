<template>
  <div v-if="isAuthenticated">
    <br />
    <p> Here are your gifs </p>
    <div v-for="giphy in giphies" :key="giphy.id">
      <div>
        <img
          @click.stop="viewGiphy(giphy.id)"
          v-bind:src="giphy.images.preview_gif.url"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';

export default {
  name: 'Profile',
  computed: mapState(['isAuthenticated', 'giphies']),
  methods: {
    async viewGiphy(giphyId) {
      await this.$store.dispatch('setSingleGiphy', giphyId);
      await this.$root.$emit('changeView', 'giphy');
    },
  },
};
</script>
