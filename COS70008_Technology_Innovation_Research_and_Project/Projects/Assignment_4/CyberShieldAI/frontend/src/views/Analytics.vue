
<template>
  <div class="p-6">
    <h2 class="text-2xl mb-4">Analytics Dashboard</h2>
    <canvas id="confusionChart" class="mb-6"></canvas>
    <canvas id="distChart"></canvas>
  </div>
</template>
<script>
import { onMounted } from 'vue';
import axios from 'axios';
import { Chart, BarController, CategoryScale, LinearScale, BarElement } from 'chart.js';
Chart.register(BarController, CategoryScale, LinearScale, BarElement);
export default {
  name: 'Analytics',
  async mounted() {
    const res = await axios.get('http://localhost:5000/analytics');
    // Confusion Matrix
    new Chart(document.getElementById('confusionChart'), {
      type: 'bar', data: { labels: res.data.labels, datasets: [{ data: res.data.confusion, label: 'Confusion' }] }
    });
    // Distribution
    new Chart(document.getElementById('distChart'), {
      type: 'bar', data: { labels: res.data.categories, datasets: [{ data: res.data.distribution, label: 'Distribution' }] }
    });
  }
};
</script>