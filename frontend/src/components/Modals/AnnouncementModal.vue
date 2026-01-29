<template>
	<Dialog
		v-model="show"
		:options="{
			title: __('Make an Announcement'),
			size: 'xl',
		}"
	>
		<template #body-content>
			<div class="flex flex-col gap-4">
				<div class="">
					<div class="mb-1.5 text-sm text-ink-gray-5">
						{{ __('Subject') }}
						<span class="text-ink-red-3">*</span>
					</div>
					<FormWrapper>
						<Input type="text" v-model="announcement.subject" />
					</FormWrapper>
				</div>
				<div class="">
					<div class="mb-1.5 text-sm text-ink-gray-5">
						{{ __('Reply To') }}
						<span class="text-ink-red-3">*</span>
					</div>
					<FormWrapper>
						<Input type="text" v-model="announcement.replyTo" />
					</FormWrapper>
				</div>
				<div class="">
					<div class="mb-1.5 text-sm text-ink-gray-5">
						{{ __('Announcement') }}
						<span class="text-ink-red-3">*</span>
					</div>
					<FormWrapper type="editor" class="">
						<TextEditor
							:fixedMenu="true"
							@change="(val) => (announcement.announcement = val)"
							editorClass="prose-sm px-2 min-h-[200px] border-outline-gray-2 border hover:border-outline-gray-3 rounded-b-md bg-surface-gray-3"
					/></FormWrapper>
				</div>
			</div>
		</template>
		<template #actions="{ close }">
			<Button class="w-full" variant="solid" @click="makeAnnouncement(close)">
				Submit
			</Button>
		</template>
	</Dialog>
</template>
<script setup>
import { Dialog, Input, TextEditor, createResource, toast } from 'frappe-ui'
import { reactive } from 'vue'
import FormWrapper from '../ui/FormWrapper.vue'

const show = defineModel()

const props = defineProps({
	batch: {
		type: String,
		required: true,
	},
	students: {
		type: Array,
		required: true,
	},
})

const announcement = reactive({
	subject: '',
	replyTo: '',
	announcement: '',
})

const announcementResource = createResource({
	url: 'frappe.core.doctype.communication.email.make',
	makeParams(values) {
		return {
			recipients: announcement.replyTo,
			bcc: props.students.join(', '),
			subject: announcement.subject,
			content: announcement.announcement,
			doctype: 'LMS Batch',
			name: props.batch,
			send_email: 1,
		}
	},
})

const makeAnnouncement = (close) => {
	announcementResource.submit(
		{},
		{
			validate() {
				if (!props.students.length) {
					return __('No students in this batch')
				}
				if (!announcement.subject) {
					return __('Subject is required')
				}
				if (!announcement.announcement) {
					return __('Announcement is required')
				}
				if (!announcement.replyTo) {
					return __('Reply To is required')
				}
			},
			onSuccess() {
				close()
				toast.success(__('Announcement has been sent successfully'))
			},
			onError(err) {
				toast.error(__(err.messages?.[0] || err))
			},
		},
	)
}
</script>
