<template>
  <div class="results">
    <div v-if="results">
      <div v-for="result in results" :key="result.id">
        <img
          v-bind:src="result.images.preview_gif.url"
          @click.stop="viewGiphy(result.id)"
        />
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
import { mapState } from 'vuex';
import { EventBus } from '@/utility';

export default {
  name: 'Results',
  computed: mapState([
    'results',
    'page',
    'offset',
    'limit',
  ]),
  methods: {
    async forward() {
      const newPageNumber = this.page + 1;
      await this.$store.commit('setPage', newPageNumber);
      await this.$store.commit('setOffset', newPageNumber * 25);
      await EventBus.$emit('updatingResults');
    },
    async backwards() {
      if (this.page === 1) {
        return;
      }
      const newPageNumber = this.page - 1;
      await this.$store.commit('setPage', newPageNumber);
      await this.$store.commit('setOffset', newPageNumber * 25);
      await EventBus.$emit('updatingResults');
    },
    async viewGiphy(giphyId) {
      await this.$store.dispatch('setSingleGiphyFromResults', giphyId);
      await EventBus.$emit('changeView', 'giphy');
    },
  },
  created() {
    EventBus.$on('updatingResults', () => {
      this.$store.dispatch('giphySearch');
    });
  },
};
</script>
