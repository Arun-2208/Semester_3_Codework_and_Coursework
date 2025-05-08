
<template>
 <div class="w-[90%] max-w-[1440px] h-[90%] flex justify-between items-center relative font-['Calibri']">
<div class = "flex">
    <div class="flex-1">
      <NavBar :username="user.username" @logout="logout" />
      <router-view />
    </div>
    </div>
</div>
</template>
<script>
import NavBar from '../components/NavBar.vue';

export default {
  name: 'Dashboard',
  components: { NavBar},
  computed: {
    user() { return JSON.parse(sessionStorage.getItem('user')); }
  },
  methods: {
    logout() {
      localStorage.clear();
      this.$router.push('/');
    }
  }
};
</script>
