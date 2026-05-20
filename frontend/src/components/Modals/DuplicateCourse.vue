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
					<div>
						<FormControl
							:model-value="newId"
							:label="__('Course ID')"
							:required="true"
							@input="onIdInput"
						/>
						<p v-if="newId && !idCheckPending && !idAvailable" class="mt-1 text-sm text-red-500">
							{{ __('This Course ID is already in use. Please choose a different one.') }}
						</p>
						<p v-else-if="newId" class="mt-1 text-sm text-ink-gray-5">
							{{ __('URL-safe identifier for the course. Auto-filled from title.') }}
						</p>
					</div>
				</div>
				<div class="flex justify-end space-x-2 mt-5">
					<Button @click="show = false">{{ __('Cancel') }}</Button>
					<Button
						variant="solid"
						@click="confirm()"
						:loading="duplicateResource.loading || idCheckPending"
						:disabled="!canSubmit"
					>
						{{ __('Duplicate') }}
					</Button>
				</div>
			</div>
		</template>
	</Dialog>
</template>
<script setup>
import { Button, Dialog, FormControl, toast, createResource } from 'frappe-ui'
import { ref, watch, computed } from 'vue'
import { useRouter } from 'vue-router'
import { escapeHTML } from '@/utils'

const show = defineModel()
const router = useRouter()

const props = defineProps({
	course: { type: Object },
})

const newTitle = ref('')
const newId = ref('')
const idManuallyEdited = ref(false)
const idAvailable = ref(true)
const idCheckPending = ref(false)

function toSlug(text) {
	return text
		.toLowerCase()
		.replace(/[^a-z0-9\s-]/g, '')
		.trim()
		.replace(/[\s-]+/g, '-')
		.replace(/^-+|-+$/g, '')
}

watch(show, (val) => {
	if (val) {
		newTitle.value = props.course?.title ? `Copy of ${props.course.title}` : ''
		newId.value = ''
		idManuallyEdited.value = false
		idAvailable.value = true
		idCheckPending.value = false
	}
})

watch(newTitle, (title) => {
	if (!idManuallyEdited.value) {
		newId.value = toSlug(title)
	}
})

const onIdInput = (e) => {
	idManuallyEdited.value = true
	newId.value = e.target.value.toLowerCase().replace(/[^a-z0-9-]/g, '-').replace(/-+/g, '-')
}

const checkNameResource = createResource({
	url: 'lms.lms.api.check_course_name_available',
	onSuccess(available) {
		idAvailable.value = available
		idCheckPending.value = false
	},
	onError() {
		idCheckPending.value = false
	},
})

let debounceTimer = null

watch(newId, (id) => {
	if (!id) {
		idAvailable.value = true
		idCheckPending.value = false
		return
	}
	idCheckPending.value = true
	idAvailable.value = true
	clearTimeout(debounceTimer)
	debounceTimer = setTimeout(() => {
		checkNameResource.submit({ name: id })
	}, 400)
})

const canSubmit = computed(() => {
	return (
		newTitle.value.trim() &&
		newId.value.trim() &&
		idAvailable.value &&
		!idCheckPending.value
	)
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
	const name = newId.value.trim()
	if (!title || !name || !idAvailable.value) return
	duplicateResource.submit({ course: props.course?.name, new_title: title, new_name: name })
}
</script>
