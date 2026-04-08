<template>
    <div class="flex flex-col items-center gap-2 p-4">
        <div class="relative w-[160px] h-[160px]">
            <Doughnut :data="chartData" :options="chartOptions" />
            <div class="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                <div class="text-2xl font-bold text-gray-900">{{ value }}%</div>
                <div class="text-xs text-gray-500 font-medium">{{ label }}</div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue'
import { Chart as ChartJS, ArcElement, Tooltip } from 'chart.js'
import { Doughnut } from 'vue-chartjs'

ChartJS.register(ArcElement, Tooltip)

const props = defineProps({
    value: {
        type: Number,
        default: 0
    },
    label: {
        type: String,
        default: ''
    },
    color: {
        type: String,
        default: '#125CA2'
    }
})

const chartData = computed(() => ({
    labels: [props.label, ''],
    datasets: [{
        data: [props.value, 100 - props.value],
        backgroundColor: [props.color, '#e5e7eb'],
        borderWidth: 0,
        borderRadius: 4,
        cutout: '70%'
    }]
}))

const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: { display: false },
        tooltip: {
            callbacks: {
                label: function (context) {
                    if (context.dataIndex === 0) {
                        return `${props.label}: ${props.value}%`
                    }
                    return null
                }
            },
            filter: function (item) {
                return item.dataIndex === 0
            }
        }
    },
    animation: {
        animateScale: true,
        animateRotate: true
    }
}
</script>
