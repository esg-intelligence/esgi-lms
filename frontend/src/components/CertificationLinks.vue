<template>
	<Button v-if="certification.data && certification.data.certificate" @click="downloadCertificate" variant="outline"
		class="w-full mt-2" size="md">
		{{ __('View Certificate') }}
	</Button>
	<div v-else-if="
		certification.data &&
		certification.data.membership &&
		certification.data.paid_certificate &&
		user.data?.is_student
	">
		<router-link v-if="!certification.data.membership.purchased_certificate" :to="{
			name: 'Billing',
			params: {
				type: 'certificate',
				name: courseName,
			},
		}">
			<Button class="w-full !border !bg-transparent !py-5 !border-primary-500 !text-primary-500">
				<template #prefix>
					<GraduationCap class="size-4 stroke-1.5" />
				</template>
				{{ __('Get Certified') }}
			</Button>
		</router-link>
		<router-link v-else-if="!certification.data.membership.certificate" :to="{
			name: 'CourseCertification',
			params: {
				courseName: courseName,
			},
		}">
			<Button class="w-full !border !bg-transparent !py-5 !border-primary-500 !text-primary-500"
				variant="outline">
				<template #prefix>
					<GraduationCap class="size-4 stroke-1.5" />
				</template>
				{{ __('Get Certified') }}
			</Button>
		</router-link>
	</div>
</template>
<script setup>
import { createResource } from 'frappe-ui'
import { inject } from 'vue'
import { GraduationCap } from 'lucide-vue-next'
import Button from '@/components/ui/Button.vue'

const user = inject('$user')

const props = defineProps({
	courseName: {
		type: String,
		required: true,
	},
})

const certification = createResource({
	url: 'lms.lms.api.get_certification_details',
	params: {
		course: props.courseName,
	},
	auto: user.data ? true : false,
	cache: ['certificationData', user.data?.name],
})

const downloadCertificate = () => {
	window.open(
		// `/api/method/frappe.utils.print_format.download_pdf?doctype=LMS+Certificate&name=${
		`/api/method/lms.lms.utils.get_pdf?name=${certification.data.certificate.name}`
	)
}
</script>
