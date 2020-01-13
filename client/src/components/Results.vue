<template>
  <div class="results">
    <div v-for="result in results.data" :key="result.id">
      <div>{{ result.title }}</div>
      <div>
        <img :src="result.images.preview_gif.url" />
      </div>
      <div>
        <a href="#" v-on:click="saveGif(result.id)">Save gif</a>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios';

export default {
  name: 'Results',
  props: {
    msg: {
      type: String,
    },
  },
  data: () => ({
    results: '',
    query: '',
  }),
  methods: {
    getGifs(query) {
      const path = `${process.env.VUE_APP_BASE_URL}/giphy/?q=${query}`;
      axios
        .get(path)
        .then((res) => {
          this.results = res.data;
        })
        .catch(error => Promise.reject(error));
    },
  },
  watch: {
    msg() {
      this.query = this.msg;
      this.getGifs(this.query);
    },
  },
};
</script>
