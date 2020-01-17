<template>
  <div class="results">
    <div v-if="results.data">
      <div v-for="result in results.data.data" :key="result.id">
        <div>
          <img v-bind:src="result.images.preview_gif.url" />
        </div>
        <div v-if="$store.getters.isAuthenticated === true">
          <a class="button is-large is-primary" @click.stop="save(result.id)">Save gif</a>
        </div>
      </div>
      <div class="column is-offset-one-quarter is-half">
        <nav class="pagination is-centered" role="navigation" aria-label="pagination">
          <a  class="pagination-previous" @click.stop="backwards">
            Back
          </a>
          <a class="pagination-next" @click.stop="forward">
            Next
          </a>
        </nav>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: 'Results',
  computed: {
    results() {
      return this.$store.getters.response;
    },
    page() {
      return this.$store.getters.page;
    },
    offset() {
      return this.$store.getters.offset;
    },
    limit() {
      return this.$store.getters.limit;
    },
  },
  methods: {
    async save(id) {
      await this.$store.dispatch('saveUserGiphy', id);
    },
    async forward() {
      const newPageNumber = this.page + 1;
      await this.$store.commit('setPage', newPageNumber);
      await this.$store.commit('setOffset', newPageNumber * 25);
      await this.$root.$emit('updatingResults');
    },
    async backwards() {
      if (this.page === 1) {
        return;
      }
      const newPageNumber = this.page - 1;
      await this.$store.commit('setPage', newPageNumber);
      await this.$store.commit('setOffset', newPageNumber * 25);
      await this.$root.$emit('updatingResults');
    },
  },
  async mounted() {
    await this.$root.$on('updatingResults', () => {
      this.$store.dispatch('retrieveGiphies');
    });
  },
};
</script>
