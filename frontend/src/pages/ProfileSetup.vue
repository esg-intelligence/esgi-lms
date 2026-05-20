<template>
	<div class="min-h-screen flex items-center justify-center bg-surface-gray-1 px-4">
		<div class="bg-white rounded-xl shadow-md p-8 w-full max-w-md space-y-6">
			<div class="text-center space-y-1">
				<h2 class="text-xl font-semibold text-ink-gray-9">
					{{ __('Complete Your Profile') }}
				</h2>
				<p class="text-sm text-ink-gray-6">
					{{ __('Please select your Sector and Industry to personalise your learning experience before continuing.') }}
				</p>
			</div>

			<div class="space-y-4">
				<FormWrapper type="combobox">
					<Link
						:label="__('Sector')"
						v-model="sector"
						doctype="LMS Sector"
					/>
				</FormWrapper>
				<FormWrapper type="combobox">
					<Link
						:key="sector"
						:label="__('Industry')"
						v-model="subSector"
						doctype="LMS Sub Sector"
						:filters="sector ? { sector } : {}"
						:readonly="!sector"
					/>
				</FormWrapper>
			</div>

			<Button
				class="w-full"
				variant="solid"
				:disabled="!sector || !subSector"
				:loading="saving"
				@click="save"
			>
				{{ __('Save & Continue') }}
			</Button>
		</div>
	</div>
</template>
<script setup>
import { ref, watch, inject } from 'vue'
import { call, toast } from 'frappe-ui'
import { useRouter, useRoute } from 'vue-router'
import Link from '@/components/Controls/Link.vue'
import FormWrapper from '@/components/ui/FormWrapper.vue'
import Button from '@/components/ui/Button.vue'

const router = useRouter()
const route = useRoute()
const user = inject('$user')

const sector = ref('')
const subSector = ref('')
const saving = ref(false)

watch(sector, (newVal, oldVal) => {
	if (newVal !== oldVal) subSector.value = ''
})

async function save() {
	if (!sector.value || !subSector.value) return
	saving.value = true
	try {
		await call('frappe.client.set_value', {
			doctype: 'User',
			name: user.data?.name,
			fieldname: { sector: sector.value, sub_sector: subSector.value },
		})
		await user.reload()
		const redirect = route.query.redirect || '/courses'
		router.push(redirect)
	} catch (err) {
		toast.error(err.messages?.[0] || err)
	} finally {
		saving.value = false
	}
}
</script>
