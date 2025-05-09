<template>
  <div class="w-screen min-h-screen bg-white font-['Calibri'] flex flex-col items-center py-8 px-4">
    <div class="w-full max-w-5xl flex flex-col items-center">
      <h1 class="text-2xl font-semibold text-[#4F378A] mb-6">Analytics Dashboard</h1>

      <!-- Summary Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 w-full mb-8">
        <div class="bg-[#F6F2FF] rounded-xl shadow p-6 text-center">
          <h2 class="text-[#4F378A] font-medium text-lg mb-2">Scans This Month</h2>
          <p class="text-2xl font-bold text-gray-700">{{ monthlyCount }}</p>
        </div>
        <div class="bg-[#F6F2FF] rounded-xl shadow p-6 text-center">
          <h2 class="text-[#4F378A] font-medium text-lg mb-2">Scans This Week</h2>
          <p class="text-2xl font-bold text-gray-700">{{ weeklyCount }}</p>
        </div>
        <div class="bg-[#F6F2FF] rounded-xl shadow p-6 text-center">
          <h2 class="text-[#4F378A] font-medium text-lg mb-2">Scans Today</h2>
          <p class="text-2xl font-bold text-gray-700">{{ dailyCount }}</p>
        </div>
      </div>

      <!-- Bar Chart: Avg Detection Rate -->
      <div class="bg-[#F6F2FF] rounded-xl shadow p-6 w-full mb-8">
        <h2 class="text-[#4F378A] font-medium text-lg mb-4 text-center">Avg Detection Rate per Malware Type</h2>
        <canvas id="barChart" class="w-full h-60"></canvas>
      </div>

      <!-- Pie Chart: Malware Distribution -->
      <div class="bg-[#F6F2FF] rounded-xl shadow p-6 w-full mb-8">
        <h2 class="text-[#4F378A] font-medium text-lg mb-4 text-center">Malware Type Distribution</h2>
        <canvas id="pieChart" class="w-full h-60"></canvas>
      </div>
    </div>
  </div>
</template>
<script>
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

export default {
  name: 'Analytics',
  data() {
    return {
      monthlyCount: 0,
      weeklyCount: 0,
      dailyCount: 0,
      detectionRates: {},
      malwareDistribution: {}
    };
  },
  async mounted() {
    try {
      const res = await fetch('http://localhost:5000/admin-analytics');
      const data = await res.json();

      this.monthlyCount = Object.values(data.monthly_counts)[0] || 0;
      this.weeklyCount = Object.values(data.weekly_counts)[0] || 0;
      this.dailyCount = Object.values(data.daily_counts)[0] || 0;

      this.detectionRates = data.average_detection_rate_by_type || {};
      this.malwareDistribution = data.malware_distribution || {};

      this.renderBarChart();
      this.renderPieChart();
    } catch (err) {
      console.error('Error fetching analytics:', err);
    }
  },
  methods: {
    getColor(type) {
      const key = type.toLowerCase();
      if (key.includes('ransom')) return '#ef4444'; // red
      if (key.includes('trojan')) return '#f97316'; // orange
      if (key.includes('spy')) return '#ec4899';    // pink
      return '#7c3aed';                             // fallback purple
    },
    renderBarChart() {
      const ctx = document.getElementById('barChart').getContext('2d');
      const labels = Object.keys(this.detectionRates);
      const dataValues = Object.values(this.detectionRates);
      const colors = labels.map(this.getColor);

      new Chart(ctx, {
        type: 'bar',
        data: {
          labels,
          datasets: [{
            label: 'Detection Rate (%)',
            data: dataValues,
            backgroundColor: colors,
            borderColor: colors,
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              max: 100
            }
          }
        }
      });
    },
    renderPieChart() {
      const ctx = document.getElementById('pieChart').getContext('2d');
      const labels = Object.keys(this.malwareDistribution);
      const dataValues = Object.values(this.malwareDistribution);
      const colors = labels.map(this.getColor);

      new Chart(ctx, {
        type: 'pie',
        data: {
          labels,
          datasets: [{
            data: dataValues,
            backgroundColor: colors
          }]
        },
        options: {
          responsive: true
        }
      });
    }
  }
};
</script>


<style scoped>
canvas {
  max-height: 300px;
}
</style>
