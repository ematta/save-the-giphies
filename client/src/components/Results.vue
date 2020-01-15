<template>
  <div class="results">
    <div v-if="results.data">
      <div v-for="result in results.data.data" :key="result.id">
        <div>
          <img v-bind:src="result.images.preview_gif.url" />
        </div>
        <div>
          {{ result.title }}
          <br />
          <a class="button is-large is-primary" @click.stop="save">Save gif</a>
        </div>
      </div>
      <div class="column is-offset-one-quarter is-half">
        <nav class="pagination is-centered" role="navigation" aria-label="pagination">
          <a href="#" class="pagination-previous" @click.stop="backwards">
            <i class="fa fa-chevron-left" aria-hidden="true"></i> &nbsp;&nbsp; Back
          </a>
          <a href="#" class="pagination-next" @click.stop="forward">
            Next &nbsp;&nbsp;
            <i class="fa fa-chevron-right" aria-hidden="true"></i>
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
    forward() {
      const newPageNumber = this.page + 1;
      this.$store.commit('setPage', newPageNumber);
      this.$store.commit('setOffset', newPageNumber * 25);
      this.$root.$emit('updatingResults');
    },
    backwards() {
      if (this.page === 1) {
        return;
      }
      const newPageNumber = this.page - 1;
      this.$store.commit('setPage', newPageNumber);
      this.$store.commit('setOffset', newPageNumber * 25);
      this.$root.$emit('updatingResults');
    },
  },
  mounted() {
    this.$root.$on('updatingResults', () => {
      this.$store.dispatch('retrieveGiphies');
    });
  },
};
</script>
