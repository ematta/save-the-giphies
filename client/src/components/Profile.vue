<template>
  <div>
    {{ $store.user.getters.name }}
  </div>
</template>

<script>

export default {
  name: 'Profile',
  beforeMount() {
    this.$store.dispatch('loadUser');
  },
};
</script>
