
<template>
  <div class="w-64 bg-[#4F378A] text-white min-h-screen">
    <router-link to="scan" class="block px-6 py-3 hover:bg-[#3e2e72]" active-class="bg-[#EADDFF] text-[#4F378A]">Scan</router-link>
    <router-link to="history" class="block px-6 py-3 hover:bg-[#3e2e72]">Scan History</router-link>
    <router-link v-if="isAdmin" to="update-model" class="block px-6 py-3 hover:bg-[#3e2e72]">Update Model</router-link>
    <router-link v-if="isAdmin" to="analytics" class="block px-6 py-3 hover:bg-[#3e2e72]">Analytics</router-link>
  </div>
</template>
<script>
export default {
  name: 'Sidebar',
  props: ['isAdmin']
};
</script>
