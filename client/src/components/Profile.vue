<template>
  <div>
    <br />
    <p> Here are your gifs </p>
    <div v-for="giphy in $store.getters.giphies" :key="giphy.data.id">
      <div>
        <img v-bind:src="giphy.data.images.preview_gif.url" />
        <br />
        <a class="button is-large is-primary" @click.stop="deleteGiphy(giphy.data.id)">Delete</a>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'Profile',
  methods: {
    deleteGiphy(giphyId) {
      this.$store.dispatch('deleteUserGiphy', giphyId)
        .then(() => this.$router.push('/'));
      this.$root.$emit('changeView', 'profile');
    },
  },
};
</script>
