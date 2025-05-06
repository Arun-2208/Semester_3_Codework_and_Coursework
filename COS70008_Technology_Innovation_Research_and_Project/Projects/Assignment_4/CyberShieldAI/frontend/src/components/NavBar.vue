
<template>
  <div class="w-full bg-white shadow-md flex justify-between items-center px-6 py-4">
    <div class="text-lg font-medium">Welcome, {{ username }}</div>
    <button @click="$emit('logout')" class="text-sm underline">Logout</button>
  </div>
</template>
<script>
export default {
  name: 'NavBar',
  props: ['username']
};
</script>
