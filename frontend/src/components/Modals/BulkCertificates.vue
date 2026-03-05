<template>
	<Dialog
		v-model="show"
		:options="{
			title: __('Generate Certificates'),
			size: 'lg',
		}"
	>
		<template #body-content>
			<div class="space-y-4">
				<FormWrapper type="combobox">
					<Link
						v-model="details.evaluator"
						:label="__('Evaluator')"
						doctype="Course Evaluator"
					/>
				</FormWrapper>
				<FormWrapper>
					<FormControl
						type="date"
						v-model="details.issue_date"
						:label="__('Issue Date')"
					/>
				</FormWrapper>
				<FormWrapper>
					<FormControl
						type="date"
						v-model="details.expiry_date"
						:label="__('Expiry Date')"
					/>
				</FormWrapper>
				<FormWrapper type="combobox">
					<FormControl
						type="select"
						v-model="details.course"
						:label="__('Course')"
						:options="getCourses()"
					/>
				</FormWrapper>
				<FormWrapper type="combobox">
					<Link
						v-model="details.template"
						:label="__('Template')"
						doctype="Print Format"
						:filters="{
							doc_type: 'LMS Certificate',
						}"
					/>
				</FormWrapper>
				<FormWrapper type="switch">
					<Switch
						size="sm"
						:label="__('Published')"
						:description="
							__(
								'Enabling this will publish the certificate on the certified participants page.',
							)
						"
						v-model="details.published"
					/>
				</FormWrapper>
			</div>
		</template>
		<template #actions="{ close }">
			<Button
				class="w-full"
				variant="solid"
				@click="generateCertificates(close)"
			>
				Create
			</Button>
		</template>
	</Dialog>
</template>
<script setup>
import { inject, reactive } from 'vue'
import { createResource, Dialog, FormControl, Switch, toast } from 'frappe-ui'
import Link from '@/components/Controls/Link.vue'
import FormWrapper from '../ui/FormWrapper.vue'

const show = defineModel()
const dayjs = inject('$dayjs')
const details = reactive({
	issue_date: dayjs().format('YYYY-MM-DD'),
	expiry_date: null,
	template: null,
	evaluator: null,
	published: true,
})

const props = defineProps({
	batch: {
		type: [Object, null],
		required: true,
	},
})

const createCertificate = createResource({
	url: 'frappe.client.insert',
	makeParams(values) {
		return {
			doc: {
				doctype: 'LMS Certificate',
				issue_date: details.issue_date,
				expiry_date: details.expiry_date,
				template: details.template,
				published: details.published,
				course: values.course,
				batch_name: values.batch,
				member: values.member,
				evaluator: details.evaluator,
			},
		}
	},
})

const generateCertificates = (close) => {
	props.batch?.students.forEach((student) => {
		createCertificate.submit(
			{
				course: details.course,
				batch: props.batch.name,
				member: student,
			},
			{
				onError(err) {
					toast.error(err.messages?.[0] || err)
				},
			},
		)
	})
	close()
	toast.success(__('Certificates generated successfully'))
}

const getCourses = () => {
	return props.batch?.courses.map((course) => {
		return {
			label: course.course,
			value: course.course,
		}
	})
}
</script>
