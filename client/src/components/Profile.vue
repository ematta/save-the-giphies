<template>
  <div>
    <br />
    <p> Here are your gifs </p>
    <div v-for="giphy in $store.getters.giphies" :key="giphy.data.id">
      <div>
        <img :key="giphy.data.id" v-bind:src="giphy.data.images.preview_gif.url" />
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
    async deleteGiphy(giphyId) {
      await this.$store.dispatch('deleteUserGiphy', giphyId)
        .then(() => this.$router.push('/'));
      await this.$root.$emit('changeView', 'profile');
    },
  },
};
</script>
