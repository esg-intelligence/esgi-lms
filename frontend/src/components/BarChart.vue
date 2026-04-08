<template>
    <div class="h-[260px] w-full">
        <Bar :data="chartData" :options="chartOptions" />
    </div>
</template>

<script setup>
import { computed } from 'vue'
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
} from 'chart.js'
import { Bar } from 'vue-chartjs'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

const props = defineProps({
    data: {
        type: Array,
        default: () => []
    },
    name: {
        type: String,
        default: ''
    }
})

const truncate = (str, max = 20) =>
    str.length > max ? str.slice(0, max) + '…' : str

const chartData = computed(() => ({
    labels: props.data.map(d => truncate(d.label)),
    datasets: [{
        label: props.name,
        data: props.data.map(d => d.value),
        backgroundColor: 'rgba(18, 92, 162, 0.8)',
        borderRadius: 6,
        borderSkipped: false
    }]
}))

const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: { display: false },
        tooltip: {
            backgroundColor: '#111827',
            titleColor: '#9ca3af',
            bodyColor: '#fff',
            titleFont: { family: 'Inter, sans-serif', size: 12, weight: 'normal' },
            bodyFont: { family: 'Inter, sans-serif', size: 14, weight: 'bold' },
            padding: 12,
            cornerRadius: 8,
            displayColors: false,
            callbacks: {
                label: function (context) {
                    return `${context.parsed.y}%`
                }
            }
        }
    },
    scales: {
        x: {
            grid: { display: false },
            ticks: {
                color: '#6b7280',
                font: { family: 'Inter, sans-serif', size: 12 }
            },
            border: { display: false }
        },
        y: {
            min: 0,
            max: 100,
            grid: {
                color: '#f3f4f6',
                drawBorder: false,
                drawTicks: false
            },
            ticks: {
                color: '#6b7280',
                font: { family: 'Inter, sans-serif', size: 12 },
                padding: 10,
                callback: (val) => `${val}%`
            },
            border: { display: false }
        }
    }
}
</script>
