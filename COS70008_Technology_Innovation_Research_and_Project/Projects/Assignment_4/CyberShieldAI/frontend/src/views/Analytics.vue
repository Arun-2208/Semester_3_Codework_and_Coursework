<template>
    <div class="w-screen min-h-screen bg-white flex flex-col items-center py-8 px-4 font-['Calibri']">
      <div class="w-full max-w-5xl flex flex-col items-center flex-grow">
        <!-- Title -->
        <h1 class="text-2xl font-semibold text-[#4F378A] mb-6">Analytics Dashboard</h1>
  
        <!-- Stats Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-6 w-full mb-8">
          <div class="bg-[#F6F2FF] rounded-xl shadow p-6 w-full text-center">
            <h2 class="text-[#4F378A] font-medium text-lg mb-2">Total Scans</h2>
            <p class="text-2xl font-bold text-gray-700">{{ totalScans }}</p>
          </div>
          <div class="bg-[#F6F2FF] rounded-xl shadow p-6 w-full text-center">
            <h2 class="text-[#4F378A] font-medium text-lg mb-2">Malware Detection Rate</h2>
            <p class="text-2xl font-bold text-gray-700">{{ detectionRate }}%</p>
          </div>
        </div>
  
        <!-- Top Malware Section -->
        <div class="bg-[#F6F2FF] rounded-xl shadow p-6 w-full mb-8">
          <h2 class="text-[#4F378A] font-medium text-lg mb-4 text-center">Top Malware Types</h2>
          <ul class="list-disc pl-6 space-y-1 text-gray-700">
            <li v-for="(count, type) in topMalware" :key="type">
              {{ type }} – {{ count }} detections
            </li>
          </ul>
          <p v-if="!Object.keys(topMalware).length" class="text-center text-gray-500 italic">
            No malware data available.
          </p>
        </div>
  
        <!-- Chart Placeholder -->
        <div class="bg-[#F6F2FF] rounded-xl shadow p-6 w-full mb-8">
          <h2 class="text-[#4F378A] font-medium text-lg mb-4 text-center">Scan Trends (Coming Soon)</h2>
          <div class="h-48 flex items-center justify-center text-gray-400 italic">
            Chart placeholder or integrate Chart.js / Recharts
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'Analytics',
    data() {
      return {
        totalScans: 0,
        detectionRate: 0,
        topMalware: {}
      };
    },
    async mounted() {
      try {
        const res = await axios.get('http://localhost:5000/admin-analytics');
        this.totalScans = res.data.total_scans;
        this.detectionRate = res.data.malware_detection_rate;
        this.topMalware = res.data.top_malware_types;
      } catch (err) {
        console.error('Analytics fetch error:', err);
      }
    }
  };
  </script>
  
  <style scoped>
  </style>
  