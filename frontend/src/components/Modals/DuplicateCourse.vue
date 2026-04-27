<template>
	<Dialog v-model="show" :options="{ size: 'sm' }">
		<template #body>
			<div class="p-5 text-base">
				<div class="text-lg text-ink-gray-9 font-semibold mb-5">{{ __('Duplicate Course') }}</div>
				<div class="space-y-4">
					<FormControl
						v-model="newTitle"
						:label="__('New Course Title')"
						:required="true"
					/>
				</div>
				<div class="flex justify-end space-x-2 mt-5">
					<Button @click="show = false">{{ __('Cancel') }}</Button>
					<Button variant="solid" @click="confirm()" :loading="duplicateResource.loading">
						{{ __('Duplicate') }}
					</Button>
				</div>
			</div>
		</template>
	</Dialog>
</template>
<script setup>
import { Button, Dialog, FormControl, toast, createResource } from 'frappe-ui'
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { escapeHTML } from '@/utils'

const show = defineModel()
const router = useRouter()

const props = defineProps({
	course: { type: Object },
})

const newTitle = ref('')

watch(show, (val) => {
	if (val) {
		newTitle.value = props.course?.title ? `Copy of ${props.course.title}` : ''
	}
})

const duplicateResource = createResource({
	url: 'lms.lms.api.duplicate_course',
	onSuccess(newCourseName) {
		toast.success(__('Course duplicated successfully'))
		show.value = false
		router.push({ name: 'CourseForm', params: { courseName: newCourseName } })
	},
	onError(err) {
		toast.error(err.messages?.[0] || err)
	},
})

const confirm = () => {
	const title = escapeHTML(newTitle.value.trim())
	if (!title) return
	duplicateResource.submit({ course: props.course?.name, new_title: title })
}
</script>
