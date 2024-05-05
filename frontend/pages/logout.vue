<script setup lang="ts">
import {useAuthStore} from "~/stores/auth";

const router = useRouter()
const authStore = useAuthStore()

;(async() => {
  await authStore.logout()
  await router.push('/')
})()
</script>