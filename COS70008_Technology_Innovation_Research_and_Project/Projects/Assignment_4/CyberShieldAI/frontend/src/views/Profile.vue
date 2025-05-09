<template>
  <div class="w-screen min-h-screen bg-white font-['Calibri'] flex flex-col items-center px-4 py-6">
    <div class="w-full max-w-4xl bg-[#F4F0FF] rounded-2xl p-8 shadow-md">
      <h2 class="text-2xl font-semibold text-center text-[#4F378A] mb-8">User Profile</h2>

      <div v-if="user" class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="flex flex-col items-center col-span-full mb-6">
          <img
            src="https://avatars.githubusercontent.com/u/583231?v=4"
            alt="Profile"
            class="w-24 h-24 rounded-full border border-gray-300 shadow-sm"
          />
          <p class="mt-2 text-sm text-gray-500">Session-based identity</p>
        </div>

        <div class="flex text-[#4F378A] flex-col">
          <label class="text-sm text-gray-600 mb-1">Username</label>
          <input type="text" :value="user.username" disabled class="bg-white border border-gray-300 rounded-md px-4 py-2" />
        </div>

        <div class="flex text-[#4F378A] flex-col">
          <label class="text-sm text-gray-600 mb-1">Email</label>
          <input type="text" :value="user.email" disabled class="bg-white border border-gray-300 rounded-md px-4 py-2" />
        </div>

        <div class="flex text-[#4F378A] flex-col">
          <label class="text-sm text-gray-600 mb-1">User Type</label>
          <input type="text" :value="formatUserType(user.user_type)" disabled class="bg-white border border-gray-300 rounded-md px-4 py-2" />
        </div>

        <div class="flex text-[#4F378A] flex-col">
          <label class="text-sm text-gray-600 mb-1">User ID</label>
          <input type="text" :value="user.user_id" disabled class="bg-white border border-gray-300 rounded-md px-4 py-2" />
        </div>
      </div>

      <div v-else class="text-center text-gray-500 mt-8">
        No user session found. Please log in again.
      </div>

      <div class="mt-10 text-center text-sm text-gray-500">
        This information is read-only and synced from your session.
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Profile',
  data() {
    return {
      user: null
    };
  },
  mounted() {
    const storedUser = JSON.parse(sessionStorage.getItem('user'));
    if (storedUser) {
      this.user = storedUser;
    }
  },
  methods: {
    formatUserType(type) {
      if (!type) return '';
      return type.charAt(0).toUpperCase() + type.slice(1).toLowerCase();
    }
  }
};
</script>
