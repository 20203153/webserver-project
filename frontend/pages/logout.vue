<script setup lang="ts">
import {useAuthStore} from "~/stores/auth";

const router = useRouter()
const authStore = useAuthStore()

authStore.logout()
router.push('/')
</script>