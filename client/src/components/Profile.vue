<template>
  <div v-if="this.authenticated">
    <br />
    <p> Here are your gifs </p>
    <div v-for="giphy in this.giphies" :key="giphy.id">
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

export default {
  name: 'Profile',
  computed: {
    authenticated() {
      return this.$store.getters.isAuthenticated;
    },
    giphies() {
      return this.$store.getters.giphies;
    },
  },
  methods: {
    async viewGiphy(giphyId) {
      await this.$store.dispatch('setSingleGiphy', giphyId);
      await this.$root.$emit('changeView', 'giphy');
    },
  },
};
</script>
