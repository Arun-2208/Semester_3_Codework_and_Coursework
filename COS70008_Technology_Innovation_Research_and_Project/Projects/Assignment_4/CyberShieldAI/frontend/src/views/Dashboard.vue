
<template>
  <div class="flex">
    <Sidebar :isAdmin="user.user_type==='admin'" />
    <div class="flex-1">
      <NavBar :username="user.username" @logout="logout" />
      <router-view />
    </div>
  </div>
</template>
<script>
import NavBar from '../components/NavBar.vue';
import Sidebar from '../components/Sidebar.vue';
export default {
  name: 'Dashboard',
  components: { NavBar, Sidebar },
  computed: {
    user() { return JSON.parse(localStorage.getItem('user')); }
  },
  methods: {
    logout() {
      localStorage.clear();
      this.$router.push('/');
    }
  }
};
</script>
